import os
import sys
import argparse
import json
import time
from faster_whisper import WhisperModel

def build_output_path(input_path, output_dir, fmt):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_dir, f"{filename}.{fmt}")

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using faster-whisper")
    parser.add_argument("--input", required=True, help="Path to audio file to transcribe")
    parser.add_argument("--output", help="Output file path (overrides --output_dir)")
    parser.add_argument("--output_dir", help="Directory to save output file")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny, base, small, medium, large-v1/v2/v3)")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"], help="Device to use")
    parser.add_argument("--output_format", default="txt", choices=["txt", "json", "srt"], help="Output format")
    parser.add_argument("--timestamps", action="store_true", help="Include word-level timestamps (JSON only)")
    parser.add_argument("--threads", type=int, default=1, help="Number of CPU threads")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        sys.exit(f"ERROR: Input file not found: {args.input}")
    if not os.path.isfile(args.input):
        sys.exit(f"ERROR: Input path is not a file: {args.input}")
    if not os.access(args.input, os.R_OK):
        sys.exit(f"ERROR: Input file is not readable: {args.input}")

    # Device detection without torch
    if args.device == "auto":
        args.device = "cuda" if os.path.exists("/dev/nvidia0") else "cpu"
    elif args.device == "cuda" and not os.path.exists("/dev/nvidia0"):
        sys.exit("ERROR: CUDA requested but /dev/nvidia0 not found (is NVIDIA runtime available?).")

    # Determine compute type
    compute_type = "float16" if args.device == "cuda" else "int8"

    # Setup output path
    if args.output:
        output_path = args.output
    elif args.output_dir:
        if not os.path.exists(args.output_dir):
            try:
                os.makedirs(args.output_dir)
                if args.verbose:
                    print(f"> Created output directory: {args.output_dir}")
            except OSError as e:
                sys.exit(f"Error creating output directory {args.output_dir}: {e}")
        output_path = build_output_path(args.input, args.output_dir, args.output_format)
    else:
        output_path = None

    # Load model
    if args.verbose:
        print(f"> Loading model '{args.model}' on {args.device}...")
    model = WhisperModel(args.model, device=args.device, compute_type=compute_type, cpu_threads=args.threads)

    # Transcribe
    try:
        if args.verbose:
            print(f"> Starting transcription...")
        start = time.time()
        segments, info = model.transcribe(
            args.input,
            language=args.language,
            beam_size=5,
            vad_filter=False,
            word_timestamps=args.timestamps,
            condition_on_previous_text=False
        )
        elapsed = time.time() - start
    except Exception as e:
        sys.exit(f"Transcription error: {e}")

    # Output handling
    if args.output_format == "json":
        result = {
            "segments": [
                {
                    "start": s.start,
                    "end": s.end,
                    "text": s.text,
                    "words": [
                        {
                            "word": w.word,
                            "start": w.start,
                            "end": w.end,
                            "probability": w.probability
                        } for w in s.words
                    ] if args.timestamps and hasattr(s, "words") and s.words else []
                } for s in segments
            ],
            "language": args.language,
            "model": args.model,
            "device": args.device,
            "duration": round(elapsed, 2)
        }
        output_content = json.dumps(result, indent=2)
    elif args.output_format == "srt":
        output_lines = []
        for i, s in enumerate(segments):
            output_lines.append(f"{i+1}")
            output_lines.append(f"{format_timestamp(s.start)} --> {format_timestamp(s.end)}")
            output_lines.append(s.text.strip())
            output_lines.append("")  # Empty line between subtitles
        output_content = "\n".join(output_lines)
    else:
        output_content = "\n".join([s.text for s in segments])

    # Write output to file or stdout
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_content)
            if args.verbose:
                print(f"> Output written to {output_path}")
        except IOError as e:
            sys.exit(f"Error writing to output file {output_path}: {e}")
    else:
        print(output_content)

if __name__ == "__main__":
    main()
