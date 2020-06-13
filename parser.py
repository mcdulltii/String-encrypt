#!/usr/bin/env python3
import argparse
import random
import string
import sys


parser = argparse.ArgumentParser(description='Multi-lang String Encryption')
parser.add_argument('--str', '-s', help='String input', default="")
parser.add_argument('--output', '-o', help='File output')
parser.add_argument('--encode', '-e', help='Encoding multiplier', default=2)
parser.add_argument('--debug', '-d', help='Enable debug mode', default=False, action='store_true')
args = parser.parse_args()
input_str = args.str
length = len(input_str)
encoding = args.encode
debugging = args.debug
output_file = args.output


def gen_varstr(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def debug(title, strings):
    if (debugging): print("[*] %s:\t%s" % (title, strings))
    return


def xor(input_string, rand_int):
    return input_string ^ rand_int


def neg(input_string, unused):
    return ~input_string


def add(input_string, rand_int):
    return input_string + rand_int


def sub(input_string, rand_int):
    return input_string - rand_int


def encode(input_list, encode_func):
    encode_seq = [random.randint(0,3) for i in range(encoding)]
    rand_seq = [random.randint(1,255) for i in range(encoding)]

    output_seq = []
    for i in range(length):
        temp = input_list[i]
        for j in range(encoding):
            temp = encode_func[encode_seq[j]](temp, rand_seq[j])
        output_seq.append(temp)
    return encode_seq, rand_seq, output_seq


def main():
    encode_fmt = ['^=', '= ~', '+=', '-=']
    encode_names = ["XOR", "NEG", "ADD", "SUB"]
    encode_func = [xor, neg, add, sub]
    header = "#include <stdlib.h>\n#include <stdio.h>\n\nunsigned char str[%s] = {" % (length)
    input_list = [ord(i) for i in input_str]
    debug("Input list", input_list)

    encode_seq, rand_seq, output_seq = encode(input_list, encode_func)
    debug("Encoding index", encode_seq)
    debug("Encoding sequence", [encode_names[i] for i in encode_seq])
    debug("Random integers", rand_seq)
    debug("Encoded inputs", output_seq)

    return


if __name__ == '__main__':
    if (length==0):
        print("No input given!")
        parser.print_help()
        sys.exit()
    main()
