#!/usr/bin/env python
#coding=utf8

__author__ = "bsloan"

from sys import stdin, argv


def model1(input, iterations):
    # step 1: collect the candidates
    en_words = set()
    fr_words = set()
    lc = 0

    pairs = []           # store the sentence pairs
    eng_line = ""

    for line in input:
        if lc % 2 == 0:  # even numbered line (english)
            eng_line = line
            words = line.split()
            for word in words:
                en_words.add(word)

        else:            # odd numbered line (foreign)
            pair = (eng_line, line)  # add to our list of sentence pairs
            pairs.append(pair)

            words = line.split()
            for word in words:
                fr_words.add(word)
        lc += 1

    # step 2: initialize all probabilities to uniform
    probs = {}
    for fr_word in fr_words:
        if fr_word in probs:
            pass
        else:
            probs[fr_word] = {}

    for fr_word in probs.keys():
        for en_word in en_words:
            if en_word in probs[fr_word]:
                pass
            else:
                probs[fr_word][en_word] = 1.0 / len(en_words)

    # step 3: iterative step. refine the translation probabilities
    for it in range(iterations):
        tc = {}

        for pair in pairs:
            en_sent = pair[0].split()
            fr_sent = pair[1].split()

            l = len(en_sent)
            m = len(fr_sent)

            for j in range(m):
                total = 0

                for i in range(l):
                    total += probs[fr_sent[j]][en_sent[i]]

                for i in range(l):
                    if fr_sent[j] in tc:
                        if en_sent[i] in tc[fr_sent[j]]:
                            tc[fr_sent[j]][en_sent[i]] += (probs[fr_sent[j]][en_sent[i]] / total)
                        else:
                            tc[fr_sent[j]][en_sent[i]] = (probs[fr_sent[j]][en_sent[i]] / total)

                    else:
                        tc[fr_sent[j]] = {}
                        tc[fr_sent[j]][en_sent[i]] = (probs[fr_sent[j]][en_sent[i]] / total)

        for eng_word in en_words:
            total = 0

            for frn_word in tc:
                if eng_word in tc[frn_word]:
                    total += tc[frn_word][eng_word]

            for frn_word in tc:
                if eng_word in tc[frn_word]:
                    probs[frn_word][eng_word] = (tc[frn_word][eng_word] / total)

    # results to stdout
    print "probabilities after", iterations, "iterations:"
    for frn_word in probs:
        print frn_word, "->",

        sorted_probs = sorted(probs[frn_word].items(), key=lambda x: x[1], reverse=True)
        for trans_word in sorted_probs:
            if trans_word[1] > 0.01:
                print trans_word[0], ":", "{0:.2f}".format(trans_word[1]),
        print

def main():

    if len(argv) != 2:
        print "usage: model1.py <# of iterations>"
        print "input is read from stdin."
        print "example:"
        print "paste -d \"\\n\" spanish.txt english.txt | python model1.py 10"
        exit()
    model1(stdin, int(argv[1]))


if __name__ == "__main__":
    main()
