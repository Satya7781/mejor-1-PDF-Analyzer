#!/usr/bin/env python3
"""
Quick test script to verify PDF upload functionality
"""

import requests
import os
from pathlib import Path

def test_upload():
    """Test the upload endpoint"""
    print("🧪 Testing PDF upload functionality...")
    
    # Check if we have a test PDF
    test_files = [
        "Challenge_1b/Collection 1/PDFs/South of France - Cities.pdf",
        "input/SIH.pdf"
    ]
    
    test_file = None
    for file_path in test_files:
        if os.path.exists(file_path):
            test_file = file_path
            break
    
    if not test_file:
        print("❌ No test PDF found")
        return False
    
    print(f"📄 Using test file: {test_file}")
    
    try:
        # Test basic upload
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {
                'processing_type': 'basic'
            }
            
            response = requests.post(
                'http://localhost:5000/api/upload',
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Basic upload test PASSED")
                print(f"   Title: {result['result'].get('title', 'N/A')}")
                print(f"   Outline items: {len(result['result'].get('outline', []))}")
                return True
            else:
                print(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_advanced_upload():
    """Test advanced AI processing"""
    print("\n🧪 Testing AI-powered analysis...")
    
    test_file = "Challenge_1b/Collection 1/PDFs/South of France - Cities.pdf"
    if not os.path.exists(test_file):
        print("❌ No test PDF found for AI test")
        return False
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {
                'processing_type': 'advanced',
                'persona': 'Travel Planner',
                'task': 'Plan a trip for college friends'
            }
            
            response = requests.post(
                'http://localhost:5000/api/upload',
                files=files,
                data=data,
                timeout=60
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ AI analysis test PASSED")
                ranked = result['result'].get('ranked_sections', [])
                print(f"   AI ranked sections: {len(ranked)}")
                if ranked:
                    print(f"   Top section: {ranked[0]['section']['text']}")
                    print(f"   Relevance score: {ranked[0]['score']:.2%}")
                return True
            else:
                print(f"❌ AI test failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ AI test HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI test failed: {e}")
        return False

def test_challenge1b():
    """Test Challenge 1B endpoint"""
    print("\n🧪 Testing Challenge 1B...")
    
    try:
        response = requests.get('http://localhost:5000/api/challenge1b', timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Challenge 1B test PASSED")
                print(f"   Collections processed: {result.get('collections_processed', 0)}")
                return True
            else:
                print(f"❌ Challenge 1B failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Challenge 1B HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Challenge 1B test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Intelligence - Upload Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_ok = test_upload()
    
    if basic_ok:
        # Test AI functionality
        ai_ok = test_advanced_upload()
        
        # Test Challenge 1B
        challenge_ok = test_challenge1b()
        
        print("\n" + "=" * 50)
        if basic_ok and ai_ok and challenge_ok:
            print("🎉 All tests PASSED! Your application is working correctly.")
        elif basic_ok:
            print("⚠️  Basic functionality works, but some advanced features may have issues.")
        else:
            print("❌ Basic functionality failed. Check server logs for errors.")
    else:
        print("\n❌ Basic upload test failed. Check server configuration.")
    
    print("\n💡 If tests fail, check:")
    print("   - Server is running on http://localhost:5000")
    print("   - All dependencies are installed")
    print("   - PDF files exist in expected locations")
    print("   - Check server logs for detailed error messages")
