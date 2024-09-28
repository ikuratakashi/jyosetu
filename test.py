import sys
import time

def spinning_dots():
    while True:
        for char in "|/-\\":
            sys.stdout.write(f"\r{char}")
            sys.stdout.flush()
            time.sleep(0.1)

try:
    spinning_dots()
except KeyboardInterrupt:
    sys.stdout.write("\rDone!\n")
    sys.stdout.flush()
