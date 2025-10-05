#!/usr/bin/env python3
"""
Simple Challenge 1B test without web server dependency
"""

import json
from pathlib import Path

def test_challenge1b_results():
    """Display Challenge 1B results"""
    print("🏆 Challenge 1B Results Summary")
    print("=" * 60)
    
    challenge_dir = Path('Challenge_1b')
    collections = sorted(challenge_dir.glob('Collection*'))
    
    for collection_dir in collections:
        print(f"\n📁 {collection_dir.name}")
        print("-" * 40)
        
        # Read input configuration
        input_file = collection_dir / 'challenge1b_input.json'
        if input_file.exists():
            with open(input_file, 'r') as f:
                input_data = json.load(f)
            
            persona = input_data.get('persona', {}).get('role', 'Unknown')
            task = input_data.get('job_to_be_done', {}).get('task', 'Unknown')
            docs = input_data.get('documents', [])
            
            print(f"👤 Persona: {persona}")
            print(f"🎯 Task: {task}")
            print(f"📄 Documents: {len(docs)}")
        
        # Read refined output
        refined_file = collection_dir / 'challenge1b_refined_output.json'
        if refined_file.exists():
            with open(refined_file, 'r') as f:
                refined_data = json.load(f)
            
            extracted = refined_data.get('extracted_sections', [])
            analyses = refined_data.get('subsection_analysis', [])
            
            print(f"🔍 Extracted Sections: {len(extracted)}")
            print(f"📝 Subsection Analyses: {len(analyses)}")
            
            # Show top 3 sections
            if extracted:
                print("\n🏅 Top Ranked Sections:")
                for i, section in enumerate(extracted[:3], 1):
                    doc = section.get('document', 'Unknown')
                    title = section.get('section_title', 'Unknown')
                    rank = section.get('importance_rank', i)
                    page = section.get('page_number', 'N/A')
                    print(f"   {rank}. {title} ({doc}, Page {page})")
        else:
            print("❌ No refined output found")
    
    print("\n" + "=" * 60)
    print("✅ Challenge 1B data is ready for testing!")
    print("\n🌐 To test via web interface:")
    print("   1. Open http://localhost:5000")
    print("   2. Click 'Process Challenge 1B' button")
    print("   3. View interactive results")

if __name__ == "__main__":
    test_challenge1b_results()
