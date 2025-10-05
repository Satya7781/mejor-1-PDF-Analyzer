#!/usr/bin/env python3
"""
Quick Challenge 1B demo - shows pre-processed results without re-processing
"""

import json
from pathlib import Path
from flask import Flask, jsonify

def get_challenge1b_results():
    """Get existing Challenge 1B results without reprocessing"""
    results = {}
    challenge_dir = Path('Challenge_1b')
    
    for collection_dir in sorted(challenge_dir.glob('Collection*')):
        if collection_dir.is_dir():
            refined_file = collection_dir / 'challenge1b_refined_output.json'
            if refined_file.exists():
                with open(refined_file, 'r', encoding='utf-8') as f:
                    results[collection_dir.name] = json.load(f)
    
    return {
        'success': True,
        'collections_processed': len(results),
        'results': results,
        'note': 'Using pre-processed results for instant demo'
    }

if __name__ == "__main__":
    # Test the function
    data = get_challenge1b_results()
    print("🏆 Challenge 1B Quick Demo Results:")
    print(f"📊 Collections: {data['collections_processed']}")
    
    for name, result in data['results'].items():
        metadata = result.get('metadata', {})
        print(f"\n📁 {name}:")
        print(f"   👤 {metadata.get('persona', 'N/A')}")
        print(f"   🎯 {metadata.get('job_to_be_done', 'N/A')}")
        print(f"   🔍 {len(result.get('extracted_sections', []))} sections")
