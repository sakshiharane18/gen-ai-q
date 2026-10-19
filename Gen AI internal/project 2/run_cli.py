#!/usr/bin/env python3
"""
Command-Line Interface for Multimodal AI Image Understanding System.
Allows running analysis on sample images or custom files directly from terminal.

Usage:
  python3 run_cli.py --sample education
  python3 run_cli.py --sample technology
  python3 run_cli.py --sample everyday
  python3 run_cli.py --all
  python3 run_cli.py --file path/to/image.jpg
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image

from analyzer import analyze_image
from sample_data import SAMPLE_IMAGES

def print_separator(char='=', length=75):
    print(char * length)

def display_analysis_report(title: str, result: dict):
    print_separator('=')
    print(' MULTIMODAL AI IMAGE UNDERSTANDING REPORT: ' + title.upper())
    print_separator('=')
    print(' Engine Used : ' + str(result.get('engine')))
    meta = result.get('metadata', {})
    print(f" Image Specs : {meta.get('width')}x{meta.get('height')} px | Aspect: {meta.get('aspect_ratio')} | Mode: {meta.get('mode')}")
    
    if result.get('warning'):
        print(' [Note]      : ' + str(result['warning']))

    print()
    print_separator('-')
    print(' 1. CONCISE CAPTION:')
    print_separator('-')
    print(' "' + str(result.get('caption')) + '"')

    print()
    print_separator('-')
    print(' 2. CONTEXTUAL SUMMARY (2-3 Sentences):')
    print_separator('-')
    print(result.get('summary'))

    print()
    print_separator('-')
    print(' 3. DETAILED IMAGE DESCRIPTION:')
    print_separator('-')
    print(result.get('description'))

    print()
    print_separator('-')
    print(' 4. IMPORTANT OBJECTS, ACTIVITIES & VISUAL ELEMENTS:')
    print_separator('-')
    for idx, elem in enumerate(result.get('important_elements', []), 1):
        print(f'  [{idx:02d}] {elem}')

    eval_rep = result.get('evaluation_report', {})
    print()
    print_separator('=')
    print(f" 5. EVALUATION REPORT (Grounding Index: {eval_rep.get('grounding_score', 'N/A')}%)")
    print_separator('=')
    print(' [A] VERIFIED VISUAL OBSERVATIONS (Pixel-Grounded):')
    for obs in eval_rep.get('verified_observations', []):
        print(f'   ✓ {obs}')

    print()
    print(' [B] POSSIBLE OMISSIONS / MISSED DETAILS (Identified across samples):')
    for om in eval_rep.get('possible_omissions', []):
        print(f'   ⚠ {om}')

    print()
    print(' [C] POTENTIAL UNSUPPORTED OBSERVATIONS (Hallucination Risks / Distinctions):')
    for un in eval_rep.get('unsupported_observations', []):
        print(f'   ✗ {un}')

    print()
    print(' [D] LIMITATIONS ANALYSIS:')
    print('   • ' + str(eval_rep.get('limitations_analysis', 'Standard vision-language constraints apply.')))
    print_separator('=')
    print()

def main():
    parser = argparse.ArgumentParser(description='Multimodal AI Image Understanding CLI')
    parser.add_argument('--sample', choices=['education', 'technology', 'everyday'], help='Select sample domain to analyze')
    parser.add_argument('--all', action='store_true', help='Analyze and evaluate all 3 sample domains')
    parser.add_argument('--file', type=str, help='Path to custom image file to analyze')
    parser.add_argument('--key', type=str, default=None, help='Optional Google Gemini API key')

    args = parser.parse_args()
    base_dir = Path(__file__).parent.resolve()
    samples_dir = base_dir / 'samples'

    if args.all:
        for s_id in ['education', 'technology', 'everyday']:
            sample = SAMPLE_IMAGES[s_id]
            img_path = samples_dir / sample['filename']
            img = Image.open(img_path)
            res = analyze_image(img, sample_id=s_id, api_key=args.key)
            display_analysis_report(sample['title'], res)
        return

    if args.sample:
        sample = SAMPLE_IMAGES[args.sample]
        img_path = samples_dir / sample['filename']
        img = Image.open(img_path)
        res = analyze_image(img, sample_id=args.sample, api_key=args.key)
        display_analysis_report(sample['title'], res)
        return

    if args.file:
        img_path = Path(args.file)
        if not img_path.exists():
            print(f'Error: File not found at {img_path}')
            sys.exit(1)
        img = Image.open(img_path)
        res = analyze_image(img, sample_id=None, api_key=args.key)
        display_analysis_report(f'Custom File: {img_path.name}', res)
        return

    # Default action: run on Education sample
    sample = SAMPLE_IMAGES['education']
    img_path = samples_dir / sample['filename']
    img = Image.open(img_path)
    res = analyze_image(img, sample_id='education', api_key=args.key)
    display_analysis_report(sample['title'], res)

if __name__ == '__main__':
    main()
