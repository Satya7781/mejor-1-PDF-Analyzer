"""
pipeline.py
-----------
End-to-end document processing pipeline that:
1. Extracts hierarchical outline via `PDFOutlineParser`
2. Extracts full raw text via `RawTextExtractor`
3. Detects pages with no text and applies OCR fallback via `OCRProcessor`
4. Merges everything into a single rich JSON output structure ready for RAG.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List

from parser import PDFOutlineParser
from raw_text_extractor import RawTextExtractor
from ocr_utils import OCRProcessor
from table_extractor import TableExtractor


class DocumentPipeline:
    """High-level façade for processing a PDF through all extractors."""

    def __init__(self, ocr_enabled: bool = True):
        self.logger = logging.getLogger(__name__)
        self.outline_parser = PDFOutlineParser()
        self.raw_extractor = RawTextExtractor()
        self.ocr_processor = OCRProcessor()
        self.table_extractor = TableExtractor()
        self.ocr_enabled = ocr_enabled

    def process(self, pdf_path: Path) -> Dict[str, Any]:
        """Run the pipeline and return rich JSON output."""
        # 1. Outline extraction (structure & hierarchy)
        outline_data = self.outline_parser.extract_outline(pdf_path)

        # 2. Raw text extraction for completeness
        raw_text_pages = self.raw_extractor.extract(pdf_path)

        tables = self.table_extractor.extract_tables(pdf_path)

        # 4. Identify missing pages text and OCR
        pages_missing_text: List[int] = [p["page"] for p in raw_text_pages if not p["text"].strip()]

        # Step 3: OCR for pages without text (disabled for now due to tesseract issues)
        pages_without_text = [page for page in raw_text_pages if not page['text'].strip()]
        if pages_without_text:
            self.logger.info(f"OCR would be needed for {len(pages_without_text)} pages without text (skipping OCR)")
            # OCR disabled - continue without it
            # try:
            #     from ocr_utils import OCRProcessor
            #     ocr = OCRProcessor()
            #     ocr_results = ocr.process_pdf(pdf_path, [p['page'] for p in pages_without_text])
            #     
            #     # Merge OCR results back into raw_text
            #     ocr_map = {r['page']: r['text'] for r in ocr_results}
            #     for page in raw_text_pages:
            #         if page['page'] in ocr_map and not page['text'].strip():
            #             page['text'] = ocr_map[page['page']]
            #             
            # except Exception as e:
            #     self.logger.warning(f"OCR processing failed: {e}")
            #     # Continue without OCR
        return {
            "title": outline_data.get("title", "Untitled Document"),
            "outline": outline_data.get("outline", []),
            "raw_text": raw_text_pages,
            "tables": tables
        }