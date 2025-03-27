import os

def is_cuda_available():
    return os.path.exists("/dev/nvidia0")
