#!/usr/bin/env python3
"""
Flask Web Application for Adobe Hackathon PDF Intelligence
Provides a web interface for PDF processing and analysis
"""

import os
import json
import logging
import tempfile
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import our existing PDF processing modules
from parser import PDFOutlineParser
from pipeline import DocumentPipeline
from app.embedder import embed
from app.ranker import rank_sections
from app.outline_to_refined_processor import OutlineToRefinedProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf_basic(pdf_path):
    """Process PDF using basic pipeline (Round-1A)."""
    try:
        pipeline = DocumentPipeline()
        result = pipeline.process(Path(pdf_path))
        return result, None
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return None, str(e)

def process_pdf_advanced(pdf_path, persona="General User", task="Extract key information"):
    """Process PDF with AI-powered analysis (Round-1B style)."""
    try:
        # First get basic outline
        parser = PDFOutlineParser()
        outline_data = parser.extract_outline(Path(pdf_path))
        
        # Create task vector for ranking
        task_vector = embed(f"{persona} {task}")
        
        # Rank sections if outline exists
        ranked_sections = []
        if outline_data.get('outline'):
            sections = [{'text': h['text'], 'page': h['page'], 'level': h['level']} 
                       for h in outline_data['outline']]
            ranked = rank_sections(sections, task_vector, top_k=5)
            ranked_sections = [{'section': s, 'score': float(score)} for s, score in ranked]
        
        # Combine results
        result = {
            'title': outline_data.get('title', 'Untitled Document'),
            'outline': outline_data.get('outline', []),
            'raw_text': outline_data.get('raw_text', []),
            'tables': outline_data.get('tables', []),
            'ranked_sections': ranked_sections,
            'persona': persona,
            'task': task,
            'processing_timestamp': datetime.now().isoformat()
        }
        
        return result, None
    except Exception as e:
        logger.error(f"Error in advanced processing: {str(e)}")
        return None, str(e)

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Get processing parameters
        processing_type = request.form.get('processing_type', 'basic')
        persona = request.form.get('persona', 'General User')
        task = request.form.get('task', 'Extract key information')
        
        # Process the PDF
        if processing_type == 'advanced':
            result, error = process_pdf_advanced(file_path, persona, task)
        else:
            result, error = process_pdf_basic(file_path)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Save result
        result_filename = f"result_{timestamp}_{filename.replace('.pdf', '.json')}"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)
        
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'result': result,
            'result_file': result_filename
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_result(filename):
    """Download result file."""
    try:
        file_path = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/challenge1b')
def process_challenge1b():
    """Process Challenge 1B collections (using pre-processed results for speed)."""
    try:
        # Use existing results for instant demo
        challenge_dir = Path('Challenge_1b')
        results = {}
        
        for collection_dir in sorted(challenge_dir.glob('Collection*')):
            if collection_dir.is_dir():
                refined_file = collection_dir / 'challenge1b_refined_output.json'
                if refined_file.exists():
                    with open(refined_file, 'r', encoding='utf-8') as f:
                        results[collection_dir.name] = json.load(f)
        
        return jsonify({
            'success': True,
            'collections_processed': len(results),
            'results': results,
            'note': 'Using pre-processed results for instant demo. All 31 PDFs already analyzed!'
        })
        
    except Exception as e:
        logger.error(f"Challenge 1B processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/challenge1b/reprocess')
def reprocess_challenge1b():
    """Reprocess Challenge 1B collections (full processing - takes time)."""
    try:
        from main import process_challenge_1b, generate_refined_output
        
        # Process Challenge 1B
        process_challenge_1b()
        generate_refined_output()
        
        # Get results
        challenge_dir = Path('Challenge_1b')
        results = {}
        
        for collection_dir in challenge_dir.glob('Collection*'):
            if collection_dir.is_dir():
                refined_file = collection_dir / 'challenge1b_refined_output.json'
                if refined_file.exists():
                    with open(refined_file, 'r', encoding='utf-8') as f:
                        results[collection_dir.name] = json.load(f)
        
        return jsonify({
            'success': True,
            'collections_processed': len(results),
            'results': results,
            'note': 'Full reprocessing completed'
        })
        
    except Exception as e:
        logger.error(f"Challenge 1B reprocessing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Adobe Hackathon PDF Intelligence Web Server...")
    print("📊 Access the application at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
