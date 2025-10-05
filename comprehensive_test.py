#!/usr/bin/env python3
"""
Comprehensive test suite for Adobe Hackathon PDF Intelligence
Tests all core functionality without requiring a running web server
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

class PDFIntelligenceTest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name, status, details="", duration=0):
        """Log test results"""
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'duration': duration
        })
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   {details}")
        if duration > 0:
            print(f"   Duration: {duration:.2f}s")
        print()

    def test_imports(self):
        """Test 1: Core module imports"""
        test_start = time.time()
        
        try:
            # Test core PDF processing
            from parser import PDFOutlineParser
            from pipeline import DocumentPipeline
            
            # Test AI components
            from app.embedder import embed
            from app.ranker import rank_sections
            
            # Test web framework
            from flask import Flask
            
            self.log_test(
                "Core Module Imports", 
                "PASS", 
                "All core modules imported successfully",
                time.time() - test_start
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Core Module Imports", 
                "FAIL", 
                f"Import error: {str(e)}",
                time.time() - test_start
            )
            return False

    def test_pdf_processing(self):
        """Test 2: PDF processing functionality"""
        test_start = time.time()
        
        # Find test PDFs
        test_pdfs = [
            "Challenge_1b/Collection 2/PDFs/Learn Acrobat - Create and Convert_1.pdf",
            "Challenge_1b/Collection 1/PDFs/South of France - Cities.pdf"
        ]
        
        working_pdfs = []
        
        try:
            from parser import PDFOutlineParser
            parser = PDFOutlineParser()
            
            for pdf_path in test_pdfs:
                if Path(pdf_path).exists():
                    try:
                        result = parser.extract_outline(Path(pdf_path))
                        
                        pages = len(result.get('raw_text', []))
                        headings = len(result.get('outline', []))
                        tables = len(result.get('tables', []))
                        
                        if pages > 0:
                            working_pdfs.append({
                                'file': pdf_path,
                                'pages': pages,
                                'headings': headings,
                                'tables': tables
                            })
                    except Exception as e:
                        print(f"   Error with {pdf_path}: {e}")
            
            if working_pdfs:
                details = f"Processed {len(working_pdfs)} PDFs successfully"
                for pdf in working_pdfs:
                    details += f"\n   - {Path(pdf['file']).name}: {pdf['pages']} pages, {pdf['headings']} headings, {pdf['tables']} tables"
                
                self.log_test(
                    "PDF Processing", 
                    "PASS", 
                    details,
                    time.time() - test_start
                )
                return True
            else:
                self.log_test(
                    "PDF Processing", 
                    "FAIL", 
                    "No PDFs could be processed",
                    time.time() - test_start
                )
                return False
                
        except Exception as e:
            self.log_test(
                "PDF Processing", 
                "FAIL", 
                f"Processing error: {str(e)}",
                time.time() - test_start
            )
            return False

    def test_ai_components(self):
        """Test 3: AI/ML functionality"""
        test_start = time.time()
        
        try:
            from app.embedder import embed
            from app.ranker import rank_sections
            
            # Test text embedding
            test_text = "This is a test document about travel planning"
            embedding = embed(test_text)
            
            if embedding is not None and len(embedding) > 0:
                embedding_size = len(embedding)
                
                # Test ranking
                test_sections = [
                    {"text": "Travel Tips", "page": 1, "level": "H1"},
                    {"text": "Budget Planning", "page": 2, "level": "H2"},
                    {"text": "Accommodation", "page": 3, "level": "H2"}
                ]
                
                task_vector = embed("Plan a budget trip")
                ranked = rank_sections(test_sections, task_vector, top_k=3)
                
                if ranked and len(ranked) > 0:
                    self.log_test(
                        "AI Components", 
                        "PASS", 
                        f"Embedding size: {embedding_size}, Ranked {len(ranked)} sections",
                        time.time() - test_start
                    )
                    return True
                else:
                    self.log_test(
                        "AI Components", 
                        "FAIL", 
                        "Ranking failed",
                        time.time() - test_start
                    )
                    return False
            else:
                self.log_test(
                    "AI Components", 
                    "FAIL", 
                    "Embedding generation failed",
                    time.time() - test_start
                )
                return False
                
        except Exception as e:
            self.log_test(
                "AI Components", 
                "FAIL", 
                f"AI error: {str(e)}",
                time.time() - test_start
            )
            return False

    def test_challenge1b_data(self):
        """Test 4: Challenge 1B data integrity"""
        test_start = time.time()
        
        try:
            challenge_dir = Path('Challenge_1b')
            if not challenge_dir.exists():
                self.log_test(
                    "Challenge 1B Data", 
                    "FAIL", 
                    "Challenge_1b directory not found",
                    time.time() - test_start
                )
                return False
            
            collections = list(challenge_dir.glob('Collection*'))
            collection_data = []
            
            for collection in collections:
                input_file = collection / 'challenge1b_input.json'
                refined_file = collection / 'challenge1b_refined_output.json'
                pdfs_dir = collection / 'PDFs'
                
                if input_file.exists() and refined_file.exists() and pdfs_dir.exists():
                    with open(input_file, 'r') as f:
                        input_data = json.load(f)
                    
                    with open(refined_file, 'r') as f:
                        refined_data = json.load(f)
                    
                    pdf_count = len(list(pdfs_dir.glob('*.pdf')))
                    extracted_sections = len(refined_data.get('extracted_sections', []))
                    
                    collection_data.append({
                        'name': collection.name,
                        'persona': input_data.get('persona', {}).get('role', 'Unknown'),
                        'pdfs': pdf_count,
                        'sections': extracted_sections
                    })
            
            if collection_data:
                details = f"Found {len(collection_data)} valid collections"
                total_pdfs = sum(c['pdfs'] for c in collection_data)
                total_sections = sum(c['sections'] for c in collection_data)
                
                for collection in collection_data:
                    details += f"\n   - {collection['name']}: {collection['persona']}, {collection['pdfs']} PDFs, {collection['sections']} sections"
                
                details += f"\n   Total: {total_pdfs} PDFs, {total_sections} extracted sections"
                
                self.log_test(
                    "Challenge 1B Data", 
                    "PASS", 
                    details,
                    time.time() - test_start
                )
                return True
            else:
                self.log_test(
                    "Challenge 1B Data", 
                    "FAIL", 
                    "No valid collections found",
                    time.time() - test_start
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Challenge 1B Data", 
                "FAIL", 
                f"Data integrity error: {str(e)}",
                time.time() - test_start
            )
            return False

    def test_web_server_startup(self):
        """Test 5: Web server startup"""
        test_start = time.time()
        
        try:
            # Start web server in background
            process = subprocess.Popen(
                ['python', 'web_app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            # Wait a bit for startup
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                # Server started successfully, now stop it
                process.terminate()
                process.wait(timeout=5)
                
                self.log_test(
                    "Web Server Startup", 
                    "PASS", 
                    "Flask server started and stopped successfully",
                    time.time() - test_start
                )
                return True
            else:
                # Process died, check error
                stdout, stderr = process.communicate()
                error_msg = stderr.decode() if stderr else "Unknown startup error"
                
                self.log_test(
                    "Web Server Startup", 
                    "FAIL", 
                    f"Server failed to start: {error_msg}",
                    time.time() - test_start
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Web Server Startup", 
                "FAIL", 
                f"Startup test error: {str(e)}",
                time.time() - test_start
            )
            return False

    def test_dependencies(self):
        """Test 6: Required dependencies"""
        test_start = time.time()
        
        required_packages = [
            ('flask', 'flask'), ('flask_cors', 'flask_cors'), ('werkzeug', 'werkzeug'),
            ('pdfplumber', 'pdfplumber'), ('PyMuPDF', 'fitz'), ('pdfminer.six', 'pdfminer'),
            ('sentence_transformers', 'sentence_transformers'), ('torch', 'torch'), ('scikit_learn', 'sklearn'),
            ('pandas', 'pandas'), ('numpy', 'numpy'), ('requests', 'requests')
        ]
        
        missing_packages = []
        installed_packages = []
        
        for package_name, import_name in required_packages:
            try:
                __import__(import_name.replace('-', '_'))
                installed_packages.append(package_name)
            except ImportError:
                missing_packages.append(package_name)
        
        if not missing_packages:
            self.log_test(
                "Dependencies Check", 
                "PASS", 
                f"All {len(installed_packages)} required packages installed",
                time.time() - test_start
            )
            return True
        else:
            self.log_test(
                "Dependencies Check", 
                "FAIL", 
                f"Missing packages: {', '.join(missing_packages)}",
                time.time() - test_start
            )
            return False

    def test_file_structure(self):
        """Test 7: Project file structure"""
        test_start = time.time()
        
        required_files = [
            'web_app.py', 'parser.py', 'pipeline.py',
            'requirements.txt', 'README.md', 'LICENSE',
            'app/embedder.py', 'app/ranker.py',
            'templates/index.html', 'static/css/style.css', 'static/js/app.js'
        ]
        
        required_dirs = [
            'app/', 'templates/', 'static/', 'Challenge_1b/', 
            'docs/', 'tests/', 'scripts/'
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                missing_dirs.append(dir_path)
        
        if not missing_files and not missing_dirs:
            self.log_test(
                "File Structure", 
                "PASS", 
                f"All {len(required_files)} files and {len(required_dirs)} directories present",
                time.time() - test_start
            )
            return True
        else:
            issues = []
            if missing_files:
                issues.append(f"Missing files: {', '.join(missing_files)}")
            if missing_dirs:
                issues.append(f"Missing directories: {', '.join(missing_dirs)}")
            
            self.log_test(
                "File Structure", 
                "FAIL", 
                "; ".join(issues),
                time.time() - test_start
            )
            return False

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Adobe Hackathon PDF Intelligence - Comprehensive Test Suite")
        print("=" * 70)
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests
        tests = [
            self.test_file_structure,
            self.test_dependencies,
            self.test_imports,
            self.test_pdf_processing,
            self.test_ai_components,
            self.test_challenge1b_data,
            self.test_web_server_startup
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
        
        # Summary
        total_time = (datetime.now() - self.start_time).total_seconds()
        
        print("=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total: {passed + failed}")
        print(f"⏱️  Duration: {total_time:.2f}s")
        print()
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Your PDF Intelligence system is fully functional!")
            print()
            print("✅ Ready for:")
            print("   - Production deployment")
            print("   - Portfolio showcase")
            print("   - Job applications")
            print("   - Live demonstrations")
        else:
            print("⚠️  Some tests failed. Check the details above for issues to fix.")
        
        print()
        print("🌐 To start the web interface:")
        print("   python web_app.py")
        print()
        print("🔗 GitHub Repository:")
        print("   https://github.com/Satya7781/mejor-1-PDF-Analyzer")
        
        return failed == 0

if __name__ == "__main__":
    tester = PDFIntelligenceTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
