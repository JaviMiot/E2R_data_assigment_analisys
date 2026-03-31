import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_docx_text(docx_path):
    """Extract text from a .docx file without external dependencies."""
    try:
        with zipfile.ZipFile(docx_path) as z:
            content = z.read('word/document.xml')
            root = ET.fromstring(content)
            
            # Namespaces
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Find all text elements
            texts = []
            for para in root.findall('.//w:p', ns):
                para_text = []
                for t in para.findall('.//w:t', ns):
                    if t.text:
                        para_text.append(t.text)
                if para_text:
                    texts.append("".join(para_text))
            
            return "\n".join(texts)
    except Exception as e:
        return f"Error extracting text from {docx_path}: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_docx_text.py <path_to_docx>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    print(extract_docx_text(docx_path))
