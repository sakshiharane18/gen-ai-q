"""Test script to verify all 3 sample images and custom heuristics run cleanly."""
import os
from pathlib import Path
from PIL import Image
import analyzer
import evaluator
from sample_data import SAMPLE_IMAGES

samples = ["education", "technology", "everyday"]
samples_dir = Path(__file__).parent / "samples"

print("=== STARTING MULTIMODAL PIPELINE VERIFICATION ===")
for s in samples:
    img_name = SAMPLE_IMAGES[s]["filename"]
    path = samples_dir / img_name
    assert path.exists(), f"File {path} does not exist!"
    img = Image.open(path)
    res = analyzer.analyze_image(img, sample_id=s, api_key=None)
    eval_res = res["evaluation_report"]
    
    print()
    print(f"[OK] Tested: {s}")
    print(f"  Caption: {res.get('caption')}")
    print(f"  Description snippet: {res.get('description')[:75]}...")
    print(f"  Objects/Elements count: {len(res.get('important_elements', []))}")
    print(f"  Verified count: {len(eval_res.get('verified_observations', []))}")
    print(f"  Omissions count: {len(eval_res.get('possible_omissions', []))}")
    print(f"  Unsupported count: {len(eval_res.get('unsupported_observations', []))}")
    print(f"  Grounding Score: {eval_res.get('grounding_score')}%")

print()
print("=== TESTING CUSTOM IMAGE HEURISTIC ===")
dummy_img = Image.new("RGB", (400, 300), color=(120, 150, 180))
dummy_res = analyzer.analyze_image(dummy_img, sample_id=None, api_key=None)
dummy_eval = dummy_res["evaluation_report"]
print(f"[OK] Custom Image Caption: {dummy_res.get('caption')}")
print(f"  Custom Verified: {len(dummy_eval.get('verified_observations', []))}")
print(f"  Custom Omissions: {len(dummy_eval.get('possible_omissions', []))}")

print()
print("=== ALL MULTIMODAL PIPELINE TESTS PASSED 100%! ===")
