#!/usr/bin/env python2.7

__author__ = "bsloan"

from sys import argv
import re

def main():
    # dump usage and exit if command line is incorrect
    if len(argv) != 3:
        print "usage: distributions.py <input_file> <character>"
        exit(0)

    # variables from user input. permits any UTF8 characters
    input_file = argv[1]
    match_char = argv[2].decode("utf-8")

    # length of match sequence is significant for strings such as "tt" that are longer than 1 char
    match_len = len(match_char)

    # compile the match pattern - use lookahead to capture all matches in a string
    pattern = re.compile(ur"(?=" + match_char + ")")

    # open file and iterate each line, decoding as utf-8 and removing brackets and line breaks
    with open(input_file, "r") as inp:
        for line in inp:
            line = re.sub("\[|\]|\n|\r", "", line).decode("utf-8")

            # for each match in the line...
            for env in re.finditer(pattern, line):
                # stay within boundaries of this string
                start_idx = env.start() - 1 if env.start() > 0 else 0
                end_idx = env.start() + match_len if env.start() < (len(line) - match_len) else len(line) - 1

                # print results in common format used in phonology research
                if env.start() == 0:
                    print line, " -->", "#_" + line[end_idx]
                elif env.start() == len(line) - match_len:
                    print line, " -->", line[start_idx] + "_#"
                else:
                    print line, " -->", line[start_idx] + "_" + line[end_idx]

if __name__ == "__main__":
    main()
