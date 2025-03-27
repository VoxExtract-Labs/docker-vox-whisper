import os
import subprocess
import sys
from utils import is_cuda_available

AUDIO_PATH = "/app/audio/sample.mp3"
OUTPUT_PATH = "/app/output/transcript.txt"

def run_transcription(device):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    cmd = [
        "python3", "/app/cli.py",
        "--input", AUDIO_PATH,
        "--output", OUTPUT_PATH,
        "--output_format", "txt",
        "--device", device,
        "--language", "en",
        "--verbose"
    ]

    print(f">> Running transcription CLI [device={device}]...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ CLI failed on device {device}:")
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
    # Always test CPU mode first
    run_transcription("cpu")
    validate_output()

    # Then optionally test CUDA if available
    if is_cuda_available():
        print("⚡ Detected CUDA. Running test with GPU...")
        run_transcription("cuda")
        validate_output()
    else:
        print("⚠️ CUDA device not found. Skipping GPU test.")
