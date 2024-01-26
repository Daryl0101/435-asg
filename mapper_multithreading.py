#!/usr/bin/env python
"""mapper_multithreading.py"""

import sys
import concurrent.futures

def process_line(line):
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    result = []
    for word in words:
        # tab-delimited; the trivial word count is 1
        result.append("%s\t%s" % (word, 1))
    return result

def main():
    # set the number of threads to 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_line, line) for line in sys.stdin]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()