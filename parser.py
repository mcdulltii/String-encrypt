#!/usr/bin/env python3
import argparse
import random
import string
import sys
from contextlib import contextmanager
import threading
import _thread
from src.functions import *
from src.encrypt import *


# Argument parser
parser = argparse.ArgumentParser(description='Multi-lang String Encryption')
parser.add_argument('--str', '-s', help='String input', default="")
parser.add_argument('--output', '-o', help='File output')
parser.add_argument('--encode', '-e', help='Encoding multiplier', default=2)
parser.add_argument('--timeout', '-t', help='Timeout', default=5)
parser.add_argument('--lang', '-l', help='Language output (C, Python, Javascript, Java)', default='py')
parser.add_argument('--debug', '-d', help='Enable debug mode', default=False, action='store_true')


# Global variables
args = parser.parse_args()
input_str = args.str
input_list = [ord(i) for i in input_str]
length = len(input_str)
encoding = int(args.encode)
timing = int(args.timeout)
lang = args.lang
debugging = args.debug
output_file = args.output


# Check for supported languages
def main():
    if (lang in ['C', 'c', 'cpp', 'c++']):
        C(input_list, debugging, length, encoding, timing, output_file)
    elif (lang in ['py', 'py3', 'python', 'python2', 'python3', 'Python', 'Python2', 'Python3']):
        py(input_list, debugging, length, encoding, timing, output_file)
    elif (lang in ['js', 'javascript', 'Javascript']):
        js(input_list, debugging, length, encoding, timing, output_file)
    elif (lang in ['java', 'Java']):
        java(input_list, debugging, length, encoding, timing, output_file)
    else:
        print("Language not supported yet!")
        sys.exit()


# Check for arguments
if __name__ == '__main__':
    if (length==0):
        print("No input given!")
        parser.print_help()
        sys.exit()
    main()

