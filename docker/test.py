import os
import subprocess
import sys

AUDIO_PATH = "/app/audio/sample.mp3"
OUTPUT_PATH = "/app/output/transcript.txt"

def run_transcription():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    cmd = [
        "python3", "/app/cli.py",
        "--input", AUDIO_PATH,
        "--output", OUTPUT_PATH,
        "--output_format", "txt",
        "--device", "cpu",
        "--language", "en",
        "--verbose"
    ]

    print(">> Running transcription CLI...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print("❌ CLI failed:")
        print(result.stderr)
        sys.exit(1)

def validate_output():
    if not os.path.exists(OUTPUT_PATH):
        print("❌ Output file was not created.")
        sys.exit(1)

    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()
        if not content:
            print("❌ Output file is empty.")
            sys.exit(1)

    print("✅ Transcription output looks good.")

if __name__ == "__main__":
    run_transcription()
    validate_output()
