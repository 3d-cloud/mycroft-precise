#!/usr/bin/env python3

import sys
sys.path += ['.']  # noqa

from subprocess import Popen, PIPE
from pyaudio import PyAudio, paInt16
from precise.common import pr


def main():
    pa = PyAudio()
    stream = pa.open(pr.sample_rate, 1, paInt16, True, frames_per_buffer=1024)

    proc = Popen(['python3', 'precise/stream.py', 'keyword.pb', '1024'], stdin=PIPE, stdout=PIPE)

    print('Listening...')
    try:
        while True:
            proc.stdin.write(stream.read(1024))
            proc.stdin.flush()

            prob = float(proc.stdout.readline())
            print('!' if prob > 0.5 else '.', end='', flush=True)
    except KeyboardInterrupt:
        print()
    finally:
        stream.stop_stream()
        pa.terminate()

if __name__ == '__main__':
    main()
