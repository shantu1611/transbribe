import whisper
from whisper.utils import format_timestamp
import os
import csv
import time
import torch
from os import listdir
from os.path import isfile, join
import shutil

start_time = time.perf_counter()
         


def get_files():

    dir=r"C:\Users\shantu\Desktop\my_works\transbribe\upload"
    onlyfiles = [os.path.join(dir, f) for f in os.listdir(dir) if 
    os.path.isfile(os.path.join(dir, f))]
    return onlyfiles





# Load Whisper model

print("Loading Whisper model...")


print("Transcribing video...")

def model_run():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(torch.cuda.is_available())

    MODEL_NAME = "medium"
    print(f"Using device: {device}")

    model = whisper.load_model(MODEL_NAME).to(device)

    PATHS= get_files()

    for VIDEO_PATH in PATHS:
        result = model.transcribe(
    VIDEO_PATH,
    language="en",
    fp16=(device == "cuda"),
    verbose=True
)


        # Output filenames

        base_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]

        csv_file = base_name + "_transcript.csv"
        srt_file = base_name + ".srt"
        print("starting to save as csv")

        # Save csv transcript
        csv_file="C:\\Users\\shantu\\Desktop\\my_works\\transbribe\\csv_file\\"+csv_file
        with open(csv_file, "w", newline="",encoding="utf-8") as f:
            writer = csv.writer(f)

            # Header
            writer.writerow(["Start", "End", "Text"])

            # Data
            for segment in result["segments"]:
                writer.writerow([
                    format_timestamp(segment["start"], always_include_hours=True),
                    format_timestamp(segment["end"], always_include_hours=True),
                    segment["text"].strip()
                ])
                
        shutil.move(VIDEO_PATH,"C:\\Users\\shantu\\Desktop\\my_works\\transbribe\\done\\"+base_name+".mp4")
        print(f"\nTranscript saved as: {csv_file}")


# Save SRT subtitles

        with open("C:\\Users\\shantu\\Desktop\\my_works\\transbribe\\srt_files\\"+srt_file, "w", encoding="utf-8") as f:


            for i, segment in enumerate(result["segments"], start=1):

                start = format_timestamp(
                    segment["start"],
                    always_include_hours=True,
                    decimal_marker=","
                )

                end = format_timestamp(
                    segment["end"],
                    always_include_hours=True,
                    decimal_marker=","
                )

                text = segment["text"].strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        print(f"Subtitle saved as: {srt_file}")
model_run()
print("\nDone!")
end_time=time.perf_counter()

print(f"Execution time: {end_time-start_time:.6f} seconds")