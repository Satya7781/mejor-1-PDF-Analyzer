#!/usr/bin/env python3
"""
Test script for Challenge 1B functionality
"""

import json
import requests
import time
from pathlib import Path

def test_challenge1b_api():
    """Test Challenge 1B via API endpoint"""
    print("🧪 Testing Challenge 1B via API...")
    
    try:
        # Test the API endpoint
        response = requests.get('http://localhost:5000/api/challenge1b', timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Challenge 1B API test successful!")
            print(f"📊 Collections processed: {data.get('collections_processed', 0)}")
            
            # Show results summary
            results = data.get('results', {})
            for collection_name, result in results.items():
                print(f"\n📁 {collection_name}:")
                metadata = result.get('metadata', {})
                print(f"   👤 Persona: {metadata.get('persona', 'N/A')}")
                print(f"   🎯 Task: {metadata.get('job_to_be_done', 'N/A')}")
                print(f"   📄 Documents: {len(metadata.get('input_documents', []))}")
                print(f"   🔍 Extracted sections: {len(result.get('extracted_sections', []))}")
                print(f"   📝 Subsection analyses: {len(result.get('subsection_analysis', []))}")
            
            return True
        else:
            print(f"❌ API test failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False

def test_challenge1b_files():
    """Test Challenge 1B by checking existing files"""
    print("\n🗂️  Testing Challenge 1B file structure...")
    
    challenge_dir = Path('Challenge_1b')
    if not challenge_dir.exists():
        print("❌ Challenge_1b directory not found!")
        return False
    
    collections = list(challenge_dir.glob('Collection*'))
    print(f"📁 Found {len(collections)} collections")
    
    for collection_dir in collections:
        print(f"\n📂 Testing {collection_dir.name}:")
        
        # Check input file
        input_file = collection_dir / 'challenge1b_input.json'
        if input_file.exists():
            print("   ✅ Input file exists")
            with open(input_file, 'r') as f:
                input_data = json.load(f)
                print(f"   👤 Persona: {input_data.get('persona', {}).get('role', 'N/A')}")
                print(f"   📄 Documents: {len(input_data.get('documents', []))}")
        else:
            print("   ❌ Input file missing")
        
        # Check PDF directory
        pdf_dir = collection_dir / 'PDFs'
        if pdf_dir.exists():
            pdfs = list(pdf_dir.glob('*.pdf'))
            print(f"   📄 PDF files: {len(pdfs)}")
        else:
            print("   ❌ PDFs directory missing")
        
        # Check output files
        refined_file = collection_dir / 'challenge1b_refined_output.json'
        if refined_file.exists():
            print("   ✅ Refined output exists")
            with open(refined_file, 'r') as f:
                output_data = json.load(f)
                print(f"   🔍 Extracted sections: {len(output_data.get('extracted_sections', []))}")
        else:
            print("   ⚠️  Refined output missing (will be generated)")
    
    return True

def main():
    print("🚀 Challenge 1B Test Suite")
    print("=" * 50)
    
    # Test file structure
    files_ok = test_challenge1b_files()
    
    if files_ok:
        print("\n" + "=" * 50)
        # Test API (this will also regenerate results)
        api_ok = test_challenge1b_api()
        
        if api_ok:
            print("\n🎉 All Challenge 1B tests passed!")
            print("\n📋 How to test manually:")
            print("1. Open http://localhost:5000 in your browser")
            print("2. Scroll to 'Challenge 1B - Multi-Collection Analysis'")
            print("3. Click 'Process Challenge 1B' button")
            print("4. View the results for all 3 collections")
        else:
            print("\n⚠️  API test failed, but files are ready")
            print("You can still test via the web interface")
    else:
        print("\n❌ Challenge 1B setup issues detected")

if __name__ == "__main__":
    main()
