import os
import zipfile
from datetime import datetime

def zip_project():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"OmniPDR_Backup_{timestamp}.zip"
    zip_path = os.path.join(os.path.abspath(os.path.join(project_root, "..")), zip_name)

    # Excluded items (don't include sensitive or huge files)
    excluded = {
        '.env', 
        '.venv', 
        '__pycache__', 
        '.git', 
        '.streamlit', 
        '.gemini',
        'OmniPDR_Transfer.zip',
        'OmniPDR_Guncel_Yedek.zip'
    }

    print(f"📦 Zipping project to: {zip_path}")
    print(f"🚫 Excluding: {', '.join(excluded)}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in excluded]
            
            for file in files:
                if file in excluded:
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_root)
                zipf.write(file_path, arcname)

    print(f"✅ Successfully created: {zip_path}")

if __name__ == "__main__":
    zip_project()
