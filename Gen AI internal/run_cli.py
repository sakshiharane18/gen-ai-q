#!/usr/bin/env python3
"""
Custom Interactive CLI for Prompt-Based Information Extraction and Validation.
Usage:
  python3 run_cli.py "Your custom technical workshop text here..."
  python3 run_cli.py --case 1
  python3 run_cli.py --case 2
  python3 run_cli.py --case 3
"""

import sys
import json
from main import prototype_extract, validate_extracted_json, PROMPT_TEMPLATE_ROBUST, TEST_PARAGRAPHS

def run_extraction_on_text(text: str):
    print("=" * 76)
    print(" 1. INPUT TEXT (CONTEXT):")
    print("=" * 76)
    print(text.strip())

    print("\n" + "=" * 76)
    print(" 2. STRUCTURED PROMPT WITH ANTI-HALLUCINATION GUARD:")
    print("=" * 76)
    prompt = PROMPT_TEMPLATE_ROBUST.replace("{input_text}", text)
    print(prompt.strip())

    print("\n" + "=" * 76)
    print(" 3. EXTRACTED STRUCTURED JSON OUTPUT:")
    print("=" * 76)
    extracted = prototype_extract(text, robust=True)
    print(json.dumps(extracted, indent=2))

    print("\n" + "=" * 76)
    print(" 4. AI OUTPUT VALIDATION REPORT:")
    print("=" * 76)
    is_valid, errors = validate_extracted_json(extracted)
    
    if is_valid:
        print("  Status: [PASSED] Valid JSON conforming 100% to target schema.")
        print("  Key Verification:")
        for k in ["title", "date", "venue", "speaker", "topics"]:
            v = extracted.get(k)
            state = "Present" if v is not None and v != [] else "Handled as null / [] (No Hallucination)"
            print(f"   - {k:8}: {state} => {json.dumps(v)}")
    else:
        print("  Status: [FAILED]")
        for err in errors:
            print(f"   - {err}")
    print("=" * 76 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--case" and len(sys.argv) > 2:
            case_idx = int(sys.argv[2]) - 1
            run_extraction_on_text(TEST_PARAGRAPHS[case_idx]["text"])
        else:
            run_extraction_on_text(" ".join(sys.argv[1:]))
    else:
        # Default: run on Test Case 1
        run_extraction_on_text(TEST_PARAGRAPHS[0]["text"])
