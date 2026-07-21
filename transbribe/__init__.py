from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent 
UPLOAD_DIR = BASE_DIR / "upload"
DONE_DIR = BASE_DIR / "done"
CSV_DIR = BASE_DIR / "csv_file"
SRT_DIR = BASE_DIR / "srt_files"
LOG_DIR = BASE_DIR / "logs"


for d in (UPLOAD_DIR, DONE_DIR, CSV_DIR, SRT_DIR):
    os.makedirs(d,exist_ok=True)