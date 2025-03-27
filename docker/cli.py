import argparse
import json
import os
import sys
import time
from datetime import timedelta
from faster_whisper import WhisperModel

# Fix OpenMP errors
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def validate_device(device: str):
    if device == "cuda":
        try:
            import torch
            if not torch.cuda.is_available():
                sys.exit("ERROR: CUDA requested but no GPU is available.")
        except ImportError:
            sys.exit("ERROR: CUDA requested but PyTorch is not installed.")

def format_timestamp(seconds: float):
    delta = timedelta(seconds=seconds)
    return str(delta)[:-3]

def build_output_path(input_path: str, output_dir: str, output_format: str):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_dir, f"{filename}.{output_format}")

def write_output(segments, output_path, fmt, include_timestamps, metadata=None):
    if fmt == "txt":
        with open(output_path, "w") as f:
            for segment in segments:
                if include_timestamps:
                    f.write(f"[{format_timestamp(segment.start)} - {format_timestamp(segment.end)}] ")
                f.write(segment.text.strip() + "\n")
    elif fmt == "json":
        data = {
            "segments": [s._asdict() for s in segments],
            "metadata": metadata or {}
        }
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
    elif fmt == "srt":
        with open(output_path, "w") as f:
            for i, segment in enumerate(segments, start=1):
                f.write(f"{i}\n")
                f.write(f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n")
                f.write(segment.text.strip() + "\n\n")
    else:
        sys.exit("Unsupported output format.")

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using faster-whisper")
    parser.add_argument("--input", required=True, help="Path to audio file")
    parser.add_argument("--output", help="Full path to output file")
    parser.add_argument("--output_dir", help="Directory to write output to (auto-names the file)")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"], help="Device to use")
    parser.add_argument("--model", default="base", help="Whisper model size to use. Options: tiny, base, small, medium, large-v1, large-v2, large-v3 (default: base)")
    parser.add_argument("--language", default="en", help="Language code (e.g. en, es). Defaults to 'en'")
    parser.add_argument("--output_format", default="txt", choices=["txt", "json", "srt"], help="Output format")
    parser.add_argument("--timestamps", action="store_true", help="Include timestamps in TXT output")
    parser.add_argument("--threads", type=int, default=1, help="Number of CPU threads to use")
    parser.add_argument("--verbose", action="store_true", help="Print extra information like elapsed time")

    args = parser.parse_args()

    # Auto-select device if 'auto'
    if args.device == "auto":
        try:
            import torch
            args.device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            args.device = "cpu"

    validate_device(args.device)

    compute_type = "float16" if args.device == "cuda" else "int8"
    cache_dir = os.getenv("WHISPER_CACHE", None)

    if args.verbose:
        print(f"> Using device: {args.device}")
        print(f"> Model: {args.model}")
        print(f"> Threads: {args.threads}")
        print(f"> Caching to: {cache_dir or '[default]'}")

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=compute_type,
        cpu_threads=args.threads,
        download_root=cache_dir
    )

    start = time.time()
    segments, info = model.transcribe(
        args.input,
        language=args.language,
        beam_size=5,
        vad_filter=False,
        word_timestamps=args.output_format == "json",  # only export word-level data for JSON
        condition_on_previous_text=False
    )
    elapsed = time.time() - start

    # Decide output path
    output_path = None
    if args.output:
        output_path = args.output
    elif args.output_dir:
        output_path = build_output_path(args.input, args.output_dir, args.output_format)

    if output_path:
        write_output(
            segments,
            output_path,
            args.output_format,
            include_timestamps=args.timestamps,
            metadata={
                "input": args.input,
                "model": args.model,
                "device": args.device,
                "language": args.language,
                "elapsed_seconds": round(elapsed, 2)
            } if args.output_format == "json" else None
        )
        if args.verbose:
            print(f"> Transcription written to {output_path}")
    else:
        for segment in segments:
            if args.timestamps:
                print(f"[{format_timestamp(segment.start)} - {format_timestamp(segment.end)}]", end=" ")
            print(segment.text.strip())

    if args.verbose:
        print(f"> Elapsed: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
