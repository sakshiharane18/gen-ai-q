# Gen AI Lab Internal: Question 1
## Prompt Engineering and Structured Output Generation (25 Marks)

**Course Alignment:** Prompt Engineering, Structured-Output Prompting, Context Engineering, and AI Output Validation.

---

### Task (a): Sample Paragraph
> "The Department of Computer Science is organizing a hands-on workshop titled 'Mastering Generative AI and LLM Applications'. The event is scheduled to take place on November 15, 2026, at the Main Auditorium, Block B. The session will be delivered by Dr. Ananya Sharma, Principal AI Scientist at DeepTech Labs. The workshop will cover Prompt Engineering, Retrieval-Augmented Generation (RAG), Fine-tuning Open-Source Models, and Responsible AI Governance."

**Key Entities Present:**
- **Title:** Mastering Generative AI and LLM Applications
- **Date:** November 15, 2026
- **Venue:** Main Auditorium, Block B
- **Speaker:** Dr. Ananya Sharma
- **Topics:** Prompt Engineering, Retrieval-Augmented Generation (RAG), Fine-tuning Open-Source Models, Responsible AI Governance

---

### Task (b): Structured Prompt Design
```text
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
```
**Techniques Applied:**
- **Role Specification:** Assigning the model a domain persona ("expert AI data extraction assistant").
- **Delimiter Isolation:** Using triple quotes `\"\"\"` to clearly isolate user context and prevent prompt injection.
- **Explicit Field Definitions:** Naming the expected attributes clearly.

---

### Task (c): Structured Output in Predefined JSON Format
```json
{
  "title": "Mastering Generative AI and LLM Applications",
  "date": "November 15, 2026",
  "venue": "Main Auditorium, Block B",
  "speaker": "Dr. Ananya Sharma",
  "topics": [
    "Prompt Engineering",
    "Retrieval-Augmented Generation (RAG)",
    "Fine-tuning Open-Source Models",
    "Responsible AI Governance"
  ]
}
```

---

### Task (d): Modified Prompt for Handling Missing Information (Anti-Hallucination)
To avoid hallucinations, defaults, or invented values when certain fields are missing from the paragraph:

```text
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
```

---

### Task (e): Testing & AI Output Validation Across 3 Different Paragraphs

#### Test Case 1: Complete Information
- **Input Text:**
  > "The Department of Computer Science is organizing a hands-on workshop titled 'Mastering Generative AI and LLM Applications'. The event is scheduled to take place on November 15, 2026, at the Main Auditorium, Block B. The session will be delivered by Dr. Ananya Sharma, Principal AI Scientist at DeepTech Labs. The workshop will cover Prompt Engineering, Retrieval-Augmented Generation (RAG), Fine-tuning Open-Source Models, and Responsible AI Governance."
- **Generated JSON:**
  ```json
  {
    "title": "Mastering Generative AI and LLM Applications",
    "date": "November 15, 2026",
    "venue": "Main Auditorium, Block B",
    "speaker": "Dr. Ananya Sharma",
    "topics": [
      "Prompt Engineering",
      "Retrieval-Augmented Generation (RAG)",
      "Fine-tuning Open-Source Models",
      "Responsible AI Governance"
    ]
  }
  ```
- **Validation:** **[PASSED]** All 5 fields present and non-null with correct data types.

#### Test Case 2: Missing Date and Venue
- **Input Text:**
  > "We are thrilled to announce a specialized crash course on 'NextGen Cloud Architecture & Microservices' led by Mr. Rajesh Verma. The session agenda includes Containerization with Docker, Kubernetes Orchestration, and Service Mesh Deployment. Registration link is active on the college portal."
- **Generated JSON:**
  ```json
  {
    "title": "NextGen Cloud Architecture & Microservices",
    "date": null,
    "venue": null,
    "speaker": "Mr. Rajesh Verma",
    "topics": [
      "Containerization with Docker",
      "Kubernetes Orchestration",
      "Service Mesh Deployment"
    ]
  }
  ```
- **Validation:** **[PASSED]** Missing `date` and `venue` mapped to `null` instead of invented dates or generic venues.

#### Test Case 3: Missing Speaker & Virtual Venue
- **Input Text:**
  > "Mark your calendars for December 5, 2026! A hands-on student boot camp on 'Cybersecurity & Ethical Hacking' will be hosted live on Google Meet. The workshop will cover Penetration Testing, Network Sniffing, and Web Vulnerability Assessment."
- **Generated JSON:**
  ```json
  {
    "title": "Cybersecurity & Ethical Hacking",
    "date": "December 5, 2026",
    "venue": "Google Meet",
    "speaker": null,
    "topics": [
      "Penetration Testing",
      "Network Sniffing",
      "Web Vulnerability Assessment"
    ]
  }
  ```
- **Validation:** **[PASSED]** Unspecified speaker mapped to `null`; online venue cleanly captured; schema validated.

---

### How to Run the Prototype

1. **CLI Version:**
   ```bash
   cd "Gen AI internal"
   python3 main.py
   ```

2. **Interactive Web Prototype:**
   Open `index.html` directly in your browser:
   ```bash
   open "Gen AI internal/index.html"
   ```
   Or serve locally:
   ```bash
   python3 -m http.server 8000
   ```
   and visit `http://localhost:8000`.
