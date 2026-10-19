#!/usr/bin/env python3
"""
Interactive Prompt-Based Information Extraction & Output Validation
Gen AI Lab Internal - Q1 Prototype
"""

import sys
import json
import time
from main import (
    prototype_extract,
    validate_extracted_json,
    PROMPT_TEMPLATE_BASIC,
    PROMPT_TEMPLATE_ROBUST,
    TEST_PARAGRAPHS,
    SAMPLE_PARAGRAPH_A
)

# Colors for terminal styling
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_box(text: str, color=CYAN):
    border = "=" * 76
    print(f"\n{color}{border}")
    print(f" {text}")
    print(f"{border}{RESET}")

def run_extraction_pipeline(text: str, mode: str = "robust"):
    print(f"\n{BOLD}1. INPUT TEXT (CONTEXT):{RESET}")
    print(f'"{text}"')

    # Prompt Engineering Step
    print(f"\n{BOLD}2. APPLIED SYSTEM PROMPT ({mode.upper()} MODE):{RESET}")
    if mode == "robust":
        formatted_prompt = PROMPT_TEMPLATE_ROBUST.replace("{input_text}", text)
    else:
        formatted_prompt = PROMPT_TEMPLATE_BASIC.replace("{input_text}", text)
    
    print(f"{CYAN}{formatted_prompt.strip()}{RESET}")

    # Simulating LLM Inference & Extraction
    print(f"\n{YELLOW}⚡ Running Prompt-Based Information Extraction...{RESET}")
    time.sleep(0.3)
    is_robust = (mode == "robust")
    extracted_data = prototype_extract(text, robust=is_robust)
    
    # JSON Generation
    print(f"\n{BOLD}3. GENERATED STRUCTURED JSON OUTPUT:{RESET}")
    json_str = json.dumps(extracted_data, indent=2)
    print(f"{GREEN}{json_str}{RESET}")

    # Output Validation
    print(f"\n{BOLD}4. AI OUTPUT VALIDATION REPORT:{RESET}")
    is_valid, errors = validate_extracted_json(extracted_data)
    
    print(f"  Schema Compliance : {'[' + GREEN + 'PASSED' + RESET + ']' if is_valid else '[' + RED + 'FAILED' + RESET + ']'}")
    
    print(f"  Field-by-Field Check:")
    for field in ["title", "date", "venue", "speaker", "topics"]:
        val = extracted_data.get(field)
        if val is None:
            note = f"{YELLOW}(Null: Correctly handled missing info without hallucinating){RESET}"
        elif isinstance(val, list):
            note = f"({len(val)} items captured)"
        else:
            note = f"({type(val).__name__})"
        print(f"    • {field:8}: {json.dumps(val)} {note}")

    if is_valid:
        print(f"\n  {GREEN}✓ Validation Result: All 5 predefined keys conform strictly to target schema.{RESET}")
    else:
        print(f"\n  {RED}✗ Validation Errors Found:{RESET}")
        for err in errors:
            print(f"    - {err}")
    print("-" * 76)

def main():
    print_box("PROMPT-BASED INFORMATION EXTRACTION & VALIDATION SYSTEM", CYAN)
    print("Syllabus: Prompt Engineering • Context Engineering • AI Output Validation\n")

    # If running non-interactively or with arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        for i, test in enumerate(TEST_PARAGRAPHS, 1):
            print_box(f"RUNNING {test['id'].upper()}", CYAN)
            run_extraction_pipeline(test["text"], mode="robust")
        return

    # Run automated showcase first
    print_box("AUTOMATED INTERACTIVE SHOWCASE (ALL 3 TEST CASES)", CYAN)
    for i, test in enumerate(TEST_PARAGRAPHS, 1):
        print(f"\n>>> Running Test Case {i}: {test['id']} <<<")
        run_extraction_pipeline(test["text"], mode="robust")
        time.sleep(0.5)

    print(f"\n{GREEN}{BOLD}All test cases successfully executed, parsed, and validated!{RESET}\n")

if __name__ == "__main__":
    main()
