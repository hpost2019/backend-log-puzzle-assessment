#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
# Your name here, and any other people/sources who helped.
# Give credit where credit is due.
__author__ = "hpost2019"

import os
import re
import sys
import urllib.request
import argparse
from collections import defaultdict


def html_tag(tag):
    def wrap_text(file, msg):
        file1 = open(file, "a")
        file1.write('<{0} src="{1}" />'.format(tag, msg))
        file1.close
    return wrap_text


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    url_templist = defaultdict(list)
    url_list = []
    url_pattern = r'(\S*\Spuzzle\S*)'
    temp = filename.split("_")
    domain = 'http://' + temp[1]
    with open(filename) as f:
        for line in f:
            url_found = re.search(url_pattern, line)
            if url_found:
                url_templist[line[url_found.start():url_found.end()]]
    for key in url_templist.keys():
        url_list.append(domain + key)
    if temp[0] == 'animal':
        return sorted(url_list)
    else:
        return sorted(url_list, key=lambda x: x.split('-')[4])


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    img_count = 0
    try:
        os.mkdir(dest_dir)
    except OSError as err:
        print(err)
        exit(1)
    img_tag = html_tag('img')
    for url in img_urls:
        img_filename = os.path.join(dest_dir, 'img' + str(img_count) + '.jpg')
        urllib.request.urlretrieve(url, img_filename)
        img_tag('index.html', img_filename)
        img_count += 1
    pass


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
