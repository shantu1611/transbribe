from os import listdir
from os.path import isfile, join
from pathlib import Path
import csv
import os
from datetime import timedelta
from whisper.utils import format_timestamp
import torch
import whisper

from .models import videos, transcribes  # relative import, since this file is inside the app


def save_to_db(video_path, segments):
    """Save a transcription's segments to the database, linked to one video row."""
    v = videos.objects.create(video_path=video_path)

    rows_to_create = [
        transcribes(
            v_id=v,
            start=timedelta(seconds=segment["start"]),
            end=timedelta(seconds=segment["end"]),
            text=segment["text"].strip(),
        )
        for segment in segments
    ]

    transcribes.objects.bulk_create(rows_to_create)
    print(f"Saved {len(rows_to_create)} segments to DB for video {v.video_id}")


def model_run_script(PATHS):
    BASE_DIR = Path(__file__).resolve().parent 
    CSV_DIR = BASE_DIR / "csv_file"
    SRT_DIR = BASE_DIR / "srt_files"
    print([BASE_DIR,CSV_DIR,SRT_DIR])
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(torch.cuda.is_available())

    MODEL_NAME = "base"
    print(f"Using device: {device}")

    model = whisper.load_model(MODEL_NAME).to(device)

    for VIDEO_PATH in PATHS:
        print(VIDEO_PATH)
        result = model.transcribe(
            VIDEO_PATH,
            language="en",
            fp16=(device == "cuda"),
            verbose=True
        )

        base_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]

        csv_file = base_name + "_transcript.csv"
        srt_file = base_name + ".srt"
        print("starting to save as csv")

        with open(CSV_DIR/csv_file, "w", newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Start", "End", "Text"])
            for segment in result["segments"]:
                writer.writerow([
                    format_timestamp(segment["start"], always_include_hours=True),
                    format_timestamp(segment["end"], always_include_hours=True),
                    segment["text"].strip()
                ])

        print(f"\nTranscript saved as: {csv_file}")

        with open(SRT_DIR/srt_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = format_timestamp(segment["start"], always_include_hours=True, decimal_marker=",")
                end = format_timestamp(segment["end"], always_include_hours=True, decimal_marker=",")
                text = segment["text"].strip()
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        print(f"Subtitle saved as: {srt_file}")

        # --- Save this video's transcript to the database ---
        save_to_db(VIDEO_PATH, result["segments"])