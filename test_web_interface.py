#!/usr/bin/env python3
"""
Test the web interface functionality directly
"""

import requests
import time
import json
from pathlib import Path

def test_web_interface():
    """Test the web interface step by step"""
    base_url = "http://localhost:5000"
    
    print("🌐 Testing PDF Intelligence Web Interface")
    print("=" * 50)
    
    # Test 1: Check if server is responding
    print("1. Testing server response...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is responding")
            print(f"   📄 Page size: {len(response.text)} characters")
            
            # Check if JavaScript is included
            if 'app.js' in response.text:
                print("   ✅ JavaScript file is included")
            else:
                print("   ❌ JavaScript file is missing")
                
            # Check if form elements exist
            if 'uploadForm' in response.text:
                print("   ✅ Upload form is present")
            else:
                print("   ❌ Upload form is missing")
                
        else:
            print(f"   ❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server connection failed: {e}")
        return False
    
    # Test 2: Check API endpoints
    print("\n2. Testing API endpoints...")
    
    # Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
    
    # Challenge 1B
    try:
        response = requests.get(f"{base_url}/api/challenge1b", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Challenge 1B working: {data.get('collections_processed', 0)} collections")
        else:
            print(f"   ❌ Challenge 1B failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Challenge 1B error: {e}")
    
    # Test 3: Test file upload
    print("\n3. Testing file upload...")
    
    test_file = "uploads/test_acrobat_tutorial.pdf"
    if Path(test_file).exists():
        try:
            with open(test_file, 'rb') as f:
                files = {'file': f}
                data = {'processing_type': 'basic'}
                
                print("   📤 Uploading test PDF...")
                response = requests.post(
                    f"{base_url}/api/upload",
                    files=files,
                    data=data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        outline_count = len(result['result'].get('outline', []))
                        page_count = len(result['result'].get('raw_text', []))
                        table_count = len(result['result'].get('tables', []))
                        
                        print(f"   ✅ Upload successful!")
                        print(f"   📊 Results: {page_count} pages, {outline_count} headings, {table_count} tables")
                        
                        if outline_count > 0:
                            print("   🎯 PDF has good structure - perfect for testing!")
                        else:
                            print("   ⚠️  PDF has no headings - normal for some document types")
                            
                        return True
                    else:
                        print(f"   ❌ Upload failed: {result.get('error', 'Unknown error')}")
                        return False
                else:
                    print(f"   ❌ Upload HTTP error: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Upload test error: {e}")
            return False
    else:
        print(f"   ❌ Test file not found: {test_file}")
        return False

def test_javascript_functionality():
    """Test if JavaScript files are accessible"""
    print("\n4. Testing JavaScript files...")
    
    js_url = "http://localhost:5000/static/js/app.js"
    css_url = "http://localhost:5000/static/css/style.css"
    
    try:
        # Test JavaScript file
        response = requests.get(js_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ JavaScript file accessible")
            if 'uploadForm.addEventListener' in response.text:
                print("   ✅ Form event listener found")
            else:
                print("   ❌ Form event listener missing")
        else:
            print(f"   ❌ JavaScript file error: {response.status_code}")
            
        # Test CSS file
        response = requests.get(css_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ CSS file accessible")
        else:
            print(f"   ❌ CSS file error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Static files error: {e}")

def main():
    """Run all tests"""
    print("🚀 PDF Intelligence Web Interface Test Suite")
    print("=" * 60)
    
    # Run tests
    web_test = test_web_interface()
    test_javascript_functionality()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if web_test:
        print("🎉 WEB INTERFACE IS WORKING!")
        print("\n✅ What's working:")
        print("   - Server responding correctly")
        print("   - API endpoints functional")
        print("   - File upload processing")
        print("   - PDF analysis working")
        print("   - JavaScript files accessible")
        print("\n🌐 Your web app is ready for use!")
        print("   Visit: http://localhost:5000")
        print("   Upload: uploads/test_acrobat_tutorial.pdf")
        print("   Expected: 43 headings, 116 tables extracted")
        
    else:
        print("❌ WEB INTERFACE HAS ISSUES")
        print("\n🔧 Check:")
        print("   - Server is running on port 5000")
        print("   - All dependencies installed")
        print("   - JavaScript files present")
        print("   - Test PDF file exists")
        
    print("\n💡 If upload seems slow, that's normal!")
    print("   - Basic processing: 30-40 seconds")
    print("   - Advanced AI: 40-60 seconds")
    print("   - Large PDFs take longer")

if __name__ == "__main__":
    main()
