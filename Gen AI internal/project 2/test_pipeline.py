"""Test script to verify all 3 sample images and custom heuristics run cleanly."""
import os
from PIL import Image
import analyzer
import evaluator

samples = ["education", "technology", "everyday_objects"]
sample_files = {
    "education": "samples/education.jpg",
    "technology": "samples/technology.jpg",
    "everyday_objects": "samples/everyday_objects.jpg"
}

print("=== STARTING MULTIMODAL PIPELINE VERIFICATION ===")
for s in samples:
    path = sample_files[s]
    assert os.path.exists(path), f"File {path} does not exist!"
    img = Image.open(path)
    res = analyzer.analyze_image(img, s, user_api_key=None)
    eval_res = evaluator.evaluate_vision_output(s, res)
    print(f"\n[OK] Tested: {s}")
    print(f"  Caption: {res.get('caption')}")
    print(f"  Description snippet: {res.get('description')[:75]}...")
    print(f"  Objects count: {len(res.get('important_elements', {}).get('objects', []))}")
    print(f"  Activities count: {len(res.get('important_elements', {}).get('activities', []))}")
    print(f"  Observed Errors: {len(eval_res.get('observed_errors', []))}")
    print(f"  Omissions: {len(eval_res.get('notable_omissions', []))}")

print("\n=== TESTING CUSTOM IMAGE HEURISTIC ===")
dummy_img = Image.new("RGB", (400, 300), color=(120, 150, 180))
dummy_res = analyzer.analyze_image(dummy_img, "custom_test.png", user_api_key=None)
dummy_eval = evaluator.evaluate_vision_output("custom_test.png", dummy_res, is_custom=True)
print(f"[OK] Custom Image Analysis: {dummy_res.get('caption')}")
print(f"  Evaluation Verdict: {dummy_eval.get('evaluation_verdict')[:75]}...")

print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
