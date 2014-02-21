#!/usr/bin/env python2.7

__author__ = "bsloan"

from urllib import urlopen
from re import match
from re import compile
from re import IGNORECASE
from collections import deque
from urlparse import urlparse
from sys import argv
from bs4 import BeautifulSoup

def extract_links(soup, domains, uri, match_pattern, block_pattern = ""):
    # extracts and returns a list of URIs linked from {soup}

    links = []
    base_domain = urlparse(uri)
    base_domain = base_domain.scheme + "://" + base_domain.netloc

    # iterate only links that match regular expression {match_pattern}
    for tag in soup.findAll('a', href = compile(match_pattern)):
        href = str(tag.get("href"))

        # handle relative links, assume they're on the base domain of {uri}
        if href.startswith("/"):
            link = base_domain + href
            if block_pattern == "" or not match(block_pattern, link, IGNORECASE):
                links.append(link)

        # handle full URIs - must be located on a domain in {domains}
        else:
            for domain in domains:
                if href.startswith(domain):
                    if block_pattern == "" or not match(block_pattern, href, IGNORECASE):
                        links.append(href)
    return links

def archive_url(soup, name):
    # writes {soup} to disk

    with open(name, "wb") as file:
        file.write(soup.prettify("utf-8"))
        print name, "saved to disk"

def read_config(fname, domains, seeds):
    # initializes required configuration for {domains} and {seeds} from file {fname}

    with open(fname, "r") as cfg:
        n_domains = int(cfg.readline())
        for i in range(n_domains):
            domains.append(cfg.readline().strip())
        n_seeds = int(cfg.readline())

        for i in range(n_seeds):
            seeds.append(cfg.readline().strip())

        # return two strings containing the match and block regular expressions
        match_pattern = cfg.readline().strip()
        block_pattern = cfg.readline().strip()
        return match_pattern, block_pattern

def main():
    domains = []
    url_seeds = []
    match_pattern = ""
    block_pattern = ""

    if len(argv) != 2:
        print "usage: bcrawler <config_file>"
        exit(0)
    try:
        match_pattern, block_pattern = read_config(argv[1], domains, url_seeds)
    except:
        print "failed to read configuration file", argv[1]
        exit(-1)

    url_queue = deque(url_seeds)
    url_handler = None
    archiving = True # hard-coded for now
    counter = 0
    crawled = set()

    while len(url_queue) > 0:
        try:
            url = url_queue.popleft()
            print "crawling", url
            url_handler = urlopen(url)
            soup = BeautifulSoup(url_handler.read())

            if archiving:
                fname = str(counter).rjust(5, "0") + ".sav"
                archive_url(soup, fname)
                counter += 1

            links = extract_links(soup, domains, url, match_pattern, block_pattern)
            for link in links:
                if link not in crawled:
                    url_queue.append(link)
                    crawled.add(link)

            print len(url_queue), "URLs in queue"
            print len(crawled), "unique URLs crawled"

            # better crawler would have built-in throttle, for now prompt user for each request
            inp = raw_input("press any key to continue crawling, or X to exit:")
            if inp.lower() == "x": break

        except Exception, err:
            print "error occurred, exiting:\n", err
            url_handler.close()
            exit(-1)

        finally:
            url_handler.close()
            print "bcrawler exiting with", counter, "files archived"

if __name__ == "__main__":
    main()
