# 🚀 Complete Setup Guide - Adobe Hackathon PDF Intelligence

## 📋 **Prerequisites**

### **System Requirements**
- **Python 3.8+** (Python 3.11 recommended)
- **4GB RAM** minimum (8GB+ recommended for large PDFs)
- **2GB free disk space** (for dependencies and models)

### **System Dependencies**

#### **Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    ghostscript
```

#### **macOS:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python poppler tesseract ghostscript
```

#### **Windows:**
1. **Install Python 3.8+** from python.org
2. **Install poppler**: Download from https://github.com/oschwartz10612/poppler-windows/releases
3. **Install tesseract**: Download from https://github.com/UB-Mannheim/tesseract/wiki
4. **Add to PATH**: Add poppler and tesseract to your system PATH

---

## 🔧 **Installation Steps**

### **Step 1: Clone Repository**
```bash
git clone https://github.com/Satya7781/mejor-1-PDF-Analyzer.git
cd mejor-1-PDF-Analyzer
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### **Step 3: Install Python Dependencies**
```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### **Step 4: Verify Installation**
```bash
# Test core functionality
python -c "from parser import PDFOutlineParser; print('✅ Core modules loaded successfully')"

# Test AI components
python -c "from app.embedder import embed; print('✅ AI components loaded successfully')"

# Test web framework
python -c "from flask import Flask; print('✅ Web framework loaded successfully')"
```

---

## 🚀 **Running the Application**

### **Option 1: Web Interface (Recommended)**
```bash
# Start the web server
python web_app.py

# Open browser and go to:
# http://localhost:5000
```

### **Option 2: Command Line Interface**

#### **Basic PDF Processing:**
```bash
# Process PDFs in input/ directory
python main2.py
```

#### **Advanced AI Analysis:**
```bash
# Process Challenge 1B with AI ranking
python main.py
```

### **Option 3: Docker (Alternative)**
```bash
# Build and run web interface
docker build -t pdf-intelligence .
docker run -p 5000:5000 pdf-intelligence

# Or run CLI version
docker build -f Dockerfile.main -t pdf-intelligence-cli .
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-intelligence-cli
```

---

## 🧪 **Testing the Setup**

### **Quick Test Commands**
```bash
# Run basic tests
python tests/test_system.py

# Test Challenge 1B functionality
python tests/test_challenge1b.py

# Test web interface (in another terminal)
curl http://localhost:5000/api/health
```

### **Upload Test PDF**
1. **Start web server**: `python web_app.py`
2. **Open browser**: http://localhost:5000
3. **Upload any PDF** and test processing

---

## 🐛 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Import Errors**
```bash
# If you get "ModuleNotFoundError"
pip install --upgrade -r requirements.txt

# Verify virtual environment is activated
which python  # Should show path to venv/bin/python
```

#### **2. OCR Issues**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract

# Test OCR
tesseract --version
```

#### **3. PDF Processing Errors**
```bash
# Install additional system dependencies
# Ubuntu/Debian
sudo apt-get install poppler-utils ghostscript

# macOS
brew install poppler ghostscript
```

#### **4. Memory Issues**
```bash
# For large PDFs, increase available memory
export PYTHONHASHSEED=0
ulimit -v 8388608  # Limit to 8GB
```

#### **5. Port Already in Use**
```bash
# If port 5000 is busy, use different port
python web_app.py --port 8080

# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### **Model Download Issues**
If the AI model doesn't load:
```bash
# The model is included in the repository
# If missing, it will auto-download on first run
# Ensure internet connection for initial setup
```

---

## 📊 **Verification Checklist**

After setup, verify these work:

- [ ] **Web Interface**: http://localhost:5000 loads
- [ ] **PDF Upload**: Can upload and process PDFs
- [ ] **AI Analysis**: Advanced processing with personas works
- [ ] **Challenge 1B**: Button processes collections
- [ ] **API Health**: http://localhost:5000/api/health returns OK
- [ ] **CLI Tools**: `python main2.py` processes PDFs
- [ ] **Tests Pass**: `python tests/test_system.py` succeeds

---

## 🎯 **Expected Performance**

### **Processing Times**
- **Small PDF (1-10 pages)**: 2-5 seconds
- **Medium PDF (10-50 pages)**: 5-15 seconds  
- **Large PDF (50+ pages)**: 15-60 seconds
- **Challenge 1B (31 PDFs)**: 2-5 minutes

### **Memory Usage**
- **Basic processing**: 500MB-1GB RAM
- **AI analysis**: 1-2GB RAM
- **Large documents**: 2-4GB RAM

---

## 🆘 **Getting Help**

### **If Setup Fails**
1. **Check Python version**: `python --version` (should be 3.8+)
2. **Verify virtual environment**: `which python`
3. **Check system dependencies**: Install poppler, tesseract
4. **Review error logs**: Look for specific missing packages
5. **Try Docker**: Use containerized version if local setup fails

### **Common Success Indicators**
- ✅ Web server starts without errors
- ✅ Can access http://localhost:5000
- ✅ PDF upload form appears
- ✅ Test PDF processes successfully
- ✅ Results display with outline and analysis

---

## 🎉 **You're Ready!**

If all steps complete successfully, you now have:
- ✅ **Complete PDF Intelligence toolkit** running locally
- ✅ **Web interface** for interactive processing
- ✅ **AI-powered analysis** with semantic ranking
- ✅ **Command-line tools** for batch processing
- ✅ **Production-ready setup** for deployment

**Enjoy exploring the Adobe Hackathon PDF Intelligence toolkit!** 🚀

---

## 📞 **Support**

For issues or questions:
- **Check documentation**: See `/docs` folder for detailed guides
- **Review logs**: Check console output for error details
- **Test incrementally**: Start with basic features, then advanced
- **Use Docker**: If local setup is problematic, try containerized version
