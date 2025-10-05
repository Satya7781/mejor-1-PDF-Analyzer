// JavaScript for PDF Intelligence Web App

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const processingTypeSelect = document.getElementById('processingType');
    const advancedOptions = document.getElementById('advancedOptions');
    const progressSection = document.getElementById('progressSection');
    const resultsSection = document.getElementById('resultsSection');
    const processBtn = document.getElementById('processBtn');
    const challenge1BBtn = document.getElementById('processChallenge1B');
    const challenge1bCustomForm = document.getElementById('challenge1bCustomForm');

    // Show/hide advanced options based on processing type
    processingTypeSelect.addEventListener('change', function() {
        if (this.value === 'advanced') {
            advancedOptions.style.display = 'block';
        } else {
            advancedOptions.style.display = 'none';
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const fileInput = document.getElementById('pdfFile');
        
        if (!fileInput.files[0]) {
            showAlert('Please select a PDF file.', 'warning');
            return;
        }

        // Show progress
        showProgress();
        
        // Submit form
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideProgress();
            if (data.success) {
                showResults(data.result, data.result_file);
                showAlert('PDF processed successfully!', 'success');
            } else {
                showAlert(data.error || 'Processing failed', 'danger');
            }
        })
        .catch(error => {
            hideProgress();
            console.error('Error:', error);
            showAlert('An error occurred during processing.', 'danger');
        });
    });

    // Handle Challenge 1B processing
    challenge1BBtn.addEventListener('click', function() {
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        fetch('/api/challenge1b')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showChallenge1BResults(data);
                showAlert(`Challenge 1B completed! Processed ${data.collections_processed} collections.`, 'success');
            } else {
                showAlert(data.error || 'Challenge 1B processing failed', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred during Challenge 1B processing.', 'danger');
        })
        .finally(() => {
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-play me-2"></i>Process Challenge 1B Collections';
        });
    });

    // Handle Custom Challenge 1B form submission
    challenge1bCustomForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const fileInput = document.getElementById('challenge1bPdf');
        const persona = document.getElementById('challenge1bPersona').value;
        const task = document.getElementById('challenge1bTask').value;
        
        if (!fileInput.files[0]) {
            showAlert('Please select a PDF file.', 'warning');
            return;
        }

        if (!task.trim()) {
            showAlert('Please describe your task.', 'warning');
            return;
        }

        // Add processing type and persona info
        formData.append('processing_type', 'advanced');
        formData.append('challenge1b_mode', 'true');
        
        // Show progress
        showCustomChallenge1BProgress();
        
        // Submit form
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideCustomChallenge1BProgress();
            if (data.success) {
                showCustomChallenge1BResults(data.result, persona, task);
                showAlert('Custom Challenge 1B analysis completed!', 'success');
            } else {
                showAlert(data.error || 'Processing failed', 'danger');
            }
        })
        .catch(error => {
            hideCustomChallenge1BProgress();
            console.error('Error:', error);
            showAlert('An error occurred during processing.', 'danger');
        });
    });

    function showProgress() {
        progressSection.style.display = 'block';
        resultsSection.style.display = 'none';
        processBtn.disabled = true;
        processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }

    function hideProgress() {
        progressSection.style.display = 'none';
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-cogs me-2"></i>Process PDF';
    }

    function showResults(result, resultFile) {
        const resultsContent = document.getElementById('resultsContent');
        
        const headingCount = result.outline ? result.outline.length : 0;
        const pageCount = result.raw_text ? result.raw_text.length : 0;
        const tableCount = result.tables ? result.tables.length : 0;
        
        let html = `
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-info-circle me-2"></i>Document Information</h5>
                    <div class="result-item">
                        <strong>Title:</strong> ${result.title || 'Untitled Document'}<br>
                        <strong>Pages:</strong> ${pageCount}<br>
                        <strong>Headings:</strong> ${headingCount}<br>
                        <strong>Tables:</strong> ${tableCount}
                    </div>
                    ${headingCount === 0 ? `
                    <div class="alert alert-info mt-2">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>No headings detected.</strong> This is normal for PDFs without structured headings 
                        (like brochures, forms, or scanned documents). Text extraction still works!
                    </div>
                    ` : ''}
                </div>
                <div class="col-md-6">
                    <h5><i class="fas fa-download me-2"></i>Download Results</h5>
                    <div class="result-item">
                        <a href="/api/download/${resultFile}" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-file-download me-1"></i>Download JSON
                        </a>
                    </div>
                    ${pageCount > 0 ? `
                    <div class="alert alert-success mt-2">
                        <i class="fas fa-check-circle me-2"></i>
                        <strong>Processing successful!</strong> Extracted text from ${pageCount} pages.
                    </div>
                    ` : ''}
                </div>
            </div>
        `;

        // Show outline/headings
        if (result.outline && result.outline.length > 0) {
            html += `
                <div class="mt-4">
                    <h5><i class="fas fa-list me-2"></i>Document Outline</h5>
                    <div class="result-item">
            `;
            
            result.outline.forEach(heading => {
                const levelClass = `heading-${heading.level.toLowerCase()}`;
                html += `
                    <div class="mb-2">
                        <span class="badge bg-secondary me-2">${heading.level}</span>
                        <span class="${levelClass}">${heading.text}</span>
                        <small class="text-muted ms-2">(Page ${heading.page})</small>
                    </div>
                `;
            });
            
            html += `</div></div>`;
        }

        // Show AI rankings if available
        if (result.ranked_sections && result.ranked_sections.length > 0) {
            html += `
                <div class="mt-4">
                    <h5><i class="fas fa-brain me-2"></i>AI-Ranked Sections</h5>
                    <div class="alert alert-info">
                        <strong>Persona:</strong> ${result.persona}<br>
                        <strong>Task:</strong> ${result.task}
                    </div>
            `;
            
            result.ranked_sections.forEach((item, index) => {
                const score = (item.score * 100).toFixed(1);
                html += `
                    <div class="result-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <span class="badge bg-primary me-2">#${index + 1}</span>
                                <strong>${item.section.text}</strong>
                                <small class="text-muted ms-2">(Page ${item.section.page})</small>
                            </div>
                            <span class="score-badge">${score}%</span>
                        </div>
                    </div>
                `;
            });
            
            html += `</div>`;
        }

        // Show tables if available
        if (result.tables && result.tables.length > 0) {
            html += `
                <div class="mt-4">
                    <h5><i class="fas fa-table me-2"></i>Extracted Tables</h5>
            `;
            
            result.tables.forEach((table, index) => {
                html += `
                    <div class="result-item">
                        <h6>Table ${index + 1} (Page ${table.page})</h6>
                        <div class="table-container">
                            <table class="table table-sm table-striped">
                `;
                
                if (table.data && table.data.length > 0) {
                    table.data.forEach((row, rowIndex) => {
                        html += '<tr>';
                        if (Array.isArray(row)) {
                            row.forEach(cell => {
                                const tag = rowIndex === 0 ? 'th' : 'td';
                                html += `<${tag}>${cell || ''}</${tag}>`;
                            });
                        }
                        html += '</tr>';
                    });
                }
                
                html += `
                            </table>
                        </div>
                    </div>
                `;
            });
            
            html += `</div>`;
        }

        resultsContent.innerHTML = html;
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function showChallenge1BResults(data) {
        const resultsDiv = document.getElementById('challenge1BResults');
        
        let html = `
            <div class="alert alert-success">
                <h6><i class="fas fa-check-circle me-2"></i>Processing Complete</h6>
                <p>Successfully processed ${data.collections_processed} collections.</p>
            </div>
        `;

        Object.entries(data.results).forEach(([collectionName, result]) => {
            html += `
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0">${collectionName}</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>Persona:</strong> ${result.metadata.persona}</p>
                        <p><strong>Task:</strong> ${result.metadata.job_to_be_done}</p>
                        <p><strong>Extracted Sections:</strong> ${result.extracted_sections.length}</p>
                        <p><strong>Subsection Analyses:</strong> ${result.subsection_analysis.length}</p>
                    </div>
                </div>
            `;
        });

        resultsDiv.innerHTML = html;
    }

    function showCustomChallenge1BProgress() {
        const resultsDiv = document.getElementById('customChallenge1BResults');
        resultsDiv.innerHTML = `
            <div class="card">
                <div class="card-body text-center">
                    <div class="spinner-border text-success mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5>Analyzing PDF with AI...</h5>
                    <p class="text-muted">Applying persona-specific intelligence to your document.</p>
                </div>
            </div>
        `;
        
        const processBtn = document.getElementById('processCustomBtn');
        processBtn.disabled = true;
        processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }

    function hideCustomChallenge1BProgress() {
        const processBtn = document.getElementById('processCustomBtn');
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Analyze with AI';
    }

    function showCustomChallenge1BResults(result, persona, task) {
        const resultsDiv = document.getElementById('customChallenge1BResults');
        
        let html = `
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-brain me-2"></i>AI Analysis Results</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="alert alert-info">
                                <strong><i class="fas fa-user me-1"></i>Persona:</strong> ${persona}<br>
                                <strong><i class="fas fa-target me-1"></i>Task:</strong> ${task}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="alert alert-light">
                                <strong><i class="fas fa-file-pdf me-1"></i>Document:</strong> ${result.title}<br>
                                <strong><i class="fas fa-list me-1"></i>Sections Found:</strong> ${result.outline ? result.outline.length : 0}
                            </div>
                        </div>
                    </div>
        `;

        // Show AI rankings if available
        if (result.ranked_sections && result.ranked_sections.length > 0) {
            html += `
                <h6><i class="fas fa-trophy me-2"></i>Top Relevant Sections for ${persona}</h6>
                <div class="row">
            `;
            
            result.ranked_sections.forEach((item, index) => {
                const score = (item.score * 100).toFixed(1);
                const badgeClass = index === 0 ? 'bg-warning' : index === 1 ? 'bg-info' : 'bg-secondary';
                
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <span class="badge ${badgeClass} fs-6">#${index + 1}</span>
                                    <span class="score-badge">${score}%</span>
                                </div>
                                <h6 class="card-title">${item.section.text}</h6>
                                <p class="card-text">
                                    <small class="text-muted">
                                        <i class="fas fa-file-alt me-1"></i>Page ${item.section.page} | 
                                        <i class="fas fa-layer-group me-1"></i>${item.section.level}
                                    </small>
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += `</div>`;
        } else {
            html += `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    No specific sections were ranked. The document may not have clear headings, 
                    or the content may not be strongly related to the specified task.
                </div>
            `;
        }

        // Show document outline
        if (result.outline && result.outline.length > 0) {
            html += `
                <div class="mt-4">
                    <h6><i class="fas fa-sitemap me-2"></i>Document Structure</h6>
                    <div class="row">
            `;
            
            result.outline.forEach((heading, index) => {
                const levelClass = `heading-${heading.level.toLowerCase()}`;
                const levelIcon = heading.level === 'H1' ? 'fas fa-heading' : 
                                 heading.level === 'H2' ? 'fas fa-minus' : 'fas fa-circle';
                
                if (index % 2 === 0) html += '<div class="col-md-6">';
                
                html += `
                    <div class="mb-2">
                        <i class="${levelIcon} me-2 ${levelClass}"></i>
                        <span class="${levelClass}">${heading.text}</span>
                        <small class="text-muted ms-2">(Page ${heading.page})</small>
                    </div>
                `;
                
                if (index % 2 === 1 || index === result.outline.length - 1) html += '</div>';
            });
            
            html += `</div></div>`;
        }

        html += `
                </div>
            </div>
        `;

        resultsDiv.innerHTML = html;
        
        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
});
