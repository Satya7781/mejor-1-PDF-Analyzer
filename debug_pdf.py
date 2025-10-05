#!/usr/bin/env python3
"""
Debug PDF processing to see what's happening
"""

from parser import PDFOutlineParser
from pathlib import Path
import json

def debug_pdf(pdf_path):
    """Debug PDF processing step by step"""
    print(f"🔍 Debugging PDF: {pdf_path}")
    print("=" * 50)
    
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    try:
        parser = PDFOutlineParser()
        result = parser.extract_outline(Path(pdf_path))
        
        print(f"📄 Title: {result.get('title', 'N/A')}")
        print(f"📝 Raw text pages: {len(result.get('raw_text', []))}")
        print(f"📋 Outline items: {len(result.get('outline', []))}")
        print(f"📊 Tables: {len(result.get('tables', []))}")
        
        # Show first few pages of raw text
        raw_text = result.get('raw_text', [])
        if raw_text:
            print(f"\n📖 First page text preview:")
            first_page = raw_text[0].get('text', '')[:500]
            print(f"   {first_page}...")
        
        # Show outline if available
        outline = result.get('outline', [])
        if outline:
            print(f"\n📋 Outline structure:")
            for i, item in enumerate(outline[:10]):  # Show first 10
                print(f"   {i+1}. {item['level']}: {item['text']} (Page {item['page']})")
        else:
            print("\n⚠️  No outline structure detected")
            print("   This could mean:")
            print("   - PDF has no headings")
            print("   - Headings are not properly formatted")
            print("   - Font detection needs adjustment")
        
        # Show tables if available
        tables = result.get('tables', [])
        if tables:
            print(f"\n📊 Tables found:")
            for i, table in enumerate(tables[:3]):  # Show first 3
                print(f"   Table {i+1} on page {table['page']}: {len(table.get('data', []))} rows")
        
        return result
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_multiple_pdfs():
    """Test multiple PDFs to see which ones work"""
    test_files = [
        "Challenge_1b/Collection 1/PDFs/South of France - Cities.pdf",
        "Challenge_1b/Collection 1/PDFs/South of France - Cuisine.pdf",
        "Challenge_1b/Collection 2/PDFs/Learn Acrobat - Create and Convert_1.pdf",
        "input/SIH.pdf"
    ]
    
    print("🧪 Testing multiple PDFs to find working examples...")
    print("=" * 60)
    
    working_pdfs = []
    
    for pdf_path in test_files:
        if Path(pdf_path).exists():
            print(f"\n📄 Testing: {pdf_path}")
            result = debug_pdf(pdf_path)
            if result and result.get('outline'):
                working_pdfs.append(pdf_path)
                print("✅ This PDF has good outline structure!")
            else:
                print("⚠️  This PDF has no outline structure")
        else:
            print(f"❌ File not found: {pdf_path}")
    
    print("\n" + "=" * 60)
    if working_pdfs:
        print(f"✅ Found {len(working_pdfs)} PDFs with good structure:")
        for pdf in working_pdfs:
            print(f"   - {pdf}")
        print("\n💡 Try uploading one of these PDFs in the web interface!")
    else:
        print("⚠️  No PDFs with outline structure found.")
        print("💡 This is normal for PDFs without proper headings.")
        print("   The system still extracts text and can do AI analysis!")

if __name__ == "__main__":
    test_multiple_pdfs()
