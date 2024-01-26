#!/usr/bin/env python
"""reducer_multithreading.py"""

import sys
import concurrent.futures

def process_line(line):
    # parse the input from mapper_multithreading.py
    word, count = line.split("\t", 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        return None

    return (word, count)

def reducer(lines):
    current_word = None
    current_count = 0

    for line in lines:
        # remove leading and trailing whitespace
        line = line.strip()

        # Process line
        result = process_line(line)
        if result is None:
            continue

        word, count = result

        # this IF-switch only works because Hadoop sorts map output
        # by key (here: word) before it is passed to the reducer
        if current_word == word:
            current_count += count
        else:
            if current_word:
                # write result to STDOUT
                print("%s\t%s" % (current_word, current_count))
            current_count = count
            current_word = word

    # do not forget to output the last word if needed!
    if current_word == word:
        print("%s\t%s" % (current_word, current_count))

def main():

    num_threads = 4  # You can adjust this based on your system and requirements

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # input comes from STDIN (standard input)
        # Read lines and split them into chunks for parallel processing
        lines = sys.stdin.readlines()
        chunk_size = len(lines) // num_threads
        line_chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]

        # Submit each chunk for processing concurrently
        futures = [executor.submit(reducer, chunk) for chunk in line_chunks]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()