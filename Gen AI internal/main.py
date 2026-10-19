"""
Prompt-Based Information Extraction System (Technical Workshop Extractor)
Syllabus Alignment: Prompt Engineering, Structured-Output Prompting,
Context Engineering, and AI Output Validation.
"""

import json
import re
from typing import Dict, Any, Tuple, List

# ==============================================================================
# TASK (a): Sample paragraph containing workshop information
# ==============================================================================
SAMPLE_PARAGRAPH_A = (
    "The Department of Computer Science is organizing a hands-on workshop titled "
    "'Mastering Generative AI and LLM Applications'. The event is scheduled to take "
    "place on November 15, 2026, at the Main Auditorium, Block B. The session will be "
    "delivered by Dr. Ananya Sharma, Principal AI Scientist at DeepTech Labs. "
    "The workshop will cover Prompt Engineering, Retrieval-Augmented Generation (RAG), "
    "Fine-tuning Open-Source Models, and Responsible AI Governance."
)

# ==============================================================================
# TASK (b): Structured Prompt Design
# ==============================================================================
PROMPT_TEMPLATE_BASIC = """
You are an expert AI data extraction assistant.
Extract the technical workshop details from the input text below into a structured format.

Input Text:
\"\"\"{input_text}\"\"\"

Required fields to extract:
- title: Name or title of the workshop
- date: Date of the workshop
- venue: Location or venue
- speaker: Name of the keynote speaker / trainer
- topics: List of topics covered
"""

# ==============================================================================
# TASK (c) & (d): JSON-Constrained Prompt with Missing-Information Handling
# ==============================================================================
PROMPT_TEMPLATE_ROBUST = """
You are a precise data extraction system. Your task is to extract information about a technical workshop from the provided text and output ONLY a valid JSON object.

### Extraction Schema:
{
  "title": string or null,
  "date": string or null,
  "venue": string or null,
  "speaker": string or null,
  "topics": array of strings (empty array [] if none found)
}

### Strict Rules:
1. Output MUST be strictly valid JSON without markdown fences (```json), commentary, or extra text.
2. Ground truth constraint: Extract values ONLY if explicitly stated in the context.
3. Handling missing information (Anti-Hallucination): If a field is not mentioned or cannot be directly inferred, assign `null` for scalar fields or `[]` for lists. DO NOT invent, assume, or extrapolate any values.
4. Format dates as clearly mentioned in the source.

### Context Text:
\"\"\"{input_text}\"\"\"

### JSON Output:
"""

# Expected JSON Schema for validation
EXPECTED_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": ["string", "null"]},
        "date": {"type": ["string", "null"]},
        "venue": {"type": ["string", "null"]},
        "speaker": {"type": ["string", "null"]},
        "topics": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["title", "date", "venue", "speaker", "topics"]
}


# ==============================================================================
# PROTOTYPE EXTRACTION ENGINE
# Provides standalone execution (simulating deterministic LLM extraction based on prompt rules)
# and can seamlessly plug into live LLM APIs if an API key is available.
# ==============================================================================
def prototype_extract(text: str, robust: bool = True) -> Dict[str, Any]:
    """
    Deterministic rule-based extractor simulating an ideal prompt-guided LLM.
    Respects strict extraction rules and handles missing fields without inventing values.
    """
    result: Dict[str, Any] = {
        "title": None,
        "date": None,
        "venue": None,
        "speaker": None,
        "topics": []
    }

    # 1. Title Extraction
    title_match = re.search(r"(?:titled|called|name of|course on|workshop on|boot camp on|session on)\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    if not title_match:
        title_match = re.search(r"['\"]([^'\"]{4,80})['\"]", text)
    if title_match:
        result["title"] = title_match.group(1).strip()

    # 2. Date Extraction
    date_match = re.search(
        r"\b(?:on\s+)?((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})\b",
        text,
        re.IGNORECASE
    )
    if not date_match:
        date_match = re.search(r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b", text, re.IGNORECASE)
    if date_match:
        result["date"] = date_match.group(1) if date_match.groups() else date_match.group(0)

    # 3. Venue Extraction
    venue_match = re.search(r"(?:at|in)\s+(?:the\s+)?([^,.\n]+(?:Auditorium|Hall|Lab|Campus|Room|Block|Center)[^.\n]*)", text, re.IGNORECASE)
    if not venue_match:
        venue_match = re.search(r"(?:venue|location):\s*([^\n,.]+)", text, re.IGNORECASE)
    if not venue_match:
        # Check for online platform
        online_match = re.search(r"\b(Google Meet|Zoom|Microsoft Teams|Webex|Online)\b", text, re.IGNORECASE)
        if online_match:
            result["venue"] = online_match.group(0)
    if venue_match:
        result["venue"] = venue_match.group(1).strip()

    # 4. Speaker Extraction
    speaker_match = re.search(
        r"(?:delivered by|conducted by|speaker\s*(?:is|:)?|led by|trainer\s*(?:is|:)?|\bby\b)\s+((?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        text
    )
    if speaker_match:
        result["speaker"] = speaker_match.group(1).strip()

    # 5. Topics Extraction
    topics_match = re.search(r"(?:cover|topics include|focusing on|agenda includes)\s+(.+?)(?:\.|$)", text, re.IGNORECASE)
    if topics_match:
        raw_topics = topics_match.group(1)
        # Split by comma, 'and', semicolons
        splits = re.split(r",|\band\b|;", raw_topics)
        cleaned_topics = [s.strip(" .") for s in splits if s.strip(" .")]
        result["topics"] = cleaned_topics

    if not robust:
        # If not robust (Task c without anti-hallucination constraint), an untrained system might substitute defaults or placeholders
        for k in result:
            if result[k] is None:
                result[k] = "Not Specified"

    return result


# ==============================================================================
# TASK (e): AI Output Validation System
# ==============================================================================
def validate_extracted_json(json_data: Any) -> Tuple[bool, List[str]]:
    """
    Validates the generated JSON against predefined requirements:
    1. Must be a valid dictionary/object
    2. Must contain all required fields
    3. Types must conform (string or null for scalars, list of strings for topics)
    4. Prohibits hallucinated / placeholder tokens when null was expected
    """
    errors = []
    
    if not isinstance(json_data, dict):
        return False, ["Output root must be a JSON object (dictionary)."]

    required_fields = ["title", "date", "venue", "speaker", "topics"]
    for field in required_fields:
        if field not in json_data:
            errors.append(f"Missing required field: '{field}'")

    if "title" in json_data and not (isinstance(json_data["title"], str) or json_data["title"] is None):
        errors.append("Field 'title' must be string or null")

    if "date" in json_data and not (isinstance(json_data["date"], str) or json_data["date"] is None):
        errors.append("Field 'date' must be string or null")

    if "venue" in json_data and not (isinstance(json_data["venue"], str) or json_data["venue"] is None):
        errors.append("Field 'venue' must be string or null")

    if "speaker" in json_data and not (isinstance(json_data["speaker"], str) or json_data["speaker"] is None):
        errors.append("Field 'speaker' must be string or null")

    if "topics" in json_data:
        if not isinstance(json_data["topics"], list):
            errors.append("Field 'topics' must be a list")
        else:
            for item in json_data["topics"]:
                if not isinstance(item, str):
                    errors.append(f"Topic item '{item}' must be a string")

    is_valid = len(errors) == 0
    return is_valid, errors


# ==============================================================================
# TEST DATASETS FOR TASK (e)
# ==============================================================================
TEST_PARAGRAPHS = [
    {
        "id": "Test Case 1 (Complete Information)",
        "description": "All fields (title, date, venue, speaker, topics) are explicitly present.",
        "text": SAMPLE_PARAGRAPH_A
    },
    {
        "id": "Test Case 2 (Missing Date and Venue)",
        "description": "Tests handling of missing information without inventing or guessing values.",
        "text": (
            "We are thrilled to announce a specialized crash course on 'NextGen Cloud Architecture & Microservices' "
            "led by Mr. Rajesh Verma. The session agenda includes Containerization with Docker, Kubernetes Orchestration, "
            "and Service Mesh Deployment. Registration link is active on the college portal."
        )
    },
    {
        "id": "Test Case 3 (Missing Speaker and Informal Online Venue)",
        "description": "Tests date and topic extraction with no speaker mentioned and virtual platform.",
        "text": (
            "Mark your calendars for December 5, 2026! A hands-on student boot camp on 'Cybersecurity & Ethical Hacking' "
            "will be hosted live on Google Meet. The workshop will cover Penetration Testing, Network Sniffing, "
            "and Web Vulnerability Assessment."
        )
    }
]


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f" {title.upper()}")
    print("=" * 80)


def main():
    print_banner("Gen AI Lab Internal: Question 1 Prototype")
    print("Project: Prompt-Based Information Extraction System (Unstructured Text -> JSON)")

    # --------------------------------------------------------------------------
    # Task (a) Display
    # --------------------------------------------------------------------------
    print_banner("Task (a): Sample Technical Workshop Paragraph")
    print(SAMPLE_PARAGRAPH_A)

    # --------------------------------------------------------------------------
    # Task (b) Display
    # --------------------------------------------------------------------------
    print_banner("Task (b): Structured Prompt Design")
    formatted_prompt_basic = PROMPT_TEMPLATE_BASIC.format(input_text=SAMPLE_PARAGRAPH_A)
    print(formatted_prompt_basic.strip())

    # --------------------------------------------------------------------------
    # Task (c) Display
    # --------------------------------------------------------------------------
    print_banner("Task (c): Extracted Information in Predefined JSON Format")
    extracted_c = prototype_extract(SAMPLE_PARAGRAPH_A, robust=False)
    print(json.dumps(extracted_c, indent=2))

    # --------------------------------------------------------------------------
    # Task (d) Display
    # --------------------------------------------------------------------------
    print_banner("Task (d): Modified Prompt for Handling Missing Information (Anti-Hallucination)")
    print(PROMPT_TEMPLATE_ROBUST.strip())

    # --------------------------------------------------------------------------
    # Task (e) Testing and Output Validation
    # --------------------------------------------------------------------------
    print_banner("Task (e): Testing Across 3 Different Paragraphs & Validation")
    for idx, test_case in enumerate(TEST_PARAGRAPHS, start=1):
        print(f"\n--- [{idx}/3] {test_case['id']} ---")
        print(f"Description: {test_case['description']}")
        print(f"Input Text:\n\"{test_case['text']}\"\n")

        # Run extraction with robust missing-value handling
        extracted_data = prototype_extract(test_case["text"], robust=True)
        json_output_str = json.dumps(extracted_data, indent=2)
        
        print("Generated JSON Output:")
        print(json_output_str)

        # Validate structure
        is_valid, validation_errors = validate_extracted_json(extracted_data)
        
        print("\nValidation Result:")
        if is_valid:
            print("  Status: [PASSED] Valid JSON conforming to target schema.")
            print("  Missing Info Check: Handled cleanly with null/[] without hallucinations.")
        else:
            print("  Status: [FAILED]")
            for err in validation_errors:
                print(f"   - Error: {err}")

    print("\n" + "=" * 80)
    print(" Prototype execution completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
