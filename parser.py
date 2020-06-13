#!/usr/bin/env python3
import argparse
import random
import string
import sys
import signal


# Argument parser
parser = argparse.ArgumentParser(description='Multi-lang String Encryption')
parser.add_argument('--str', '-s', help='String input', default="")
parser.add_argument('--output', '-o', help='File output')
parser.add_argument('--encode', '-e', help='Encoding multiplier', default=2)
parser.add_argument('--timeout', '-t', help='Timeout', default=5)
parser.add_argument('--lang', '-l', help='Language output', default='C')
parser.add_argument('--debug', '-d', help='Enable debug mode', default=False, action='store_true')


# Global variables
args = parser.parse_args()
input_str = args.str
length = len(input_str)
encoding = int(args.encode)
timing = int(args.timeout)
lang = args.lang
debugging = args.debug
output_file = args.output


# Generates random alphachar variable names
def gen_varstr(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


# Prints debug statements
def debug(title, strings):
    if (debugging): print("[*] %s:\t%s" % (title, strings))
    return


# XOR values
def xor(input_string, rand_int):
    return input_string ^ rand_int


# Negate values
def neg(input_string, unused):
    return ~input_string


# Add values
def add(input_string, rand_int):
    return input_string + rand_int


# Subtract values
def sub(input_string, rand_int):
    return input_string - rand_int


# Run random encoding function with for loop index as the variable
def index(input_string, index, rand_int):
    return encode_func[rand_int](input_string, index)


# Increment values
def inc(input_string, unused):
    return input_string + 1


# Decrement values
def dec(input_string, unused):
    return input_string - 1


# Implement timeout for long runs
def timeout(signum, frame):
    print("Time Exceeded!")
    sys.exit()


# Store functions within list for function randomization
encode_func = [xor, neg, add, sub, index, inc, dec]


# Encode input characters with encoding multiplier
def encode(input_list):
    # Randomise encoding functions
    temp_seq = [random.randint(0,len(encode_func)-1) for i in range(encoding)]
    # Replace '4's with a new encoding function
    encode_seq = [[i,random.choice([0,2,3])] if i==4 else i for i in temp_seq]
    # Random variables for encoding functions
    rand_seq = [random.randint(1,255) for i in range(len(encode_seq))]

    output_seq = []
    for i in range(length):
        temp = input_list[i]
        # Run encoding functions on input string
        for j in range(encoding):
            if isinstance(encode_seq[j], list):
                # Using index as variable
                temp = encode_func[encode_seq[j][0]](temp, i, encode_seq[j][1])
            else:
                temp = encode_func[encode_seq[j]](temp, rand_seq[j])
        output_seq.append(temp)
    return encode_seq, rand_seq, output_seq


def C():
    try:
        enc_fmt = int(input("Enter encryption method, [1]:UNICODE or [2]:ANSI : "))
        if (enc_fmt not in [1, 2]):
            sys.exit()
    except:
        print("Cannot parse input")
        sys.exit()

    # Strings for decoding
    decode_fmt = ['^= ', '= ~', '-= ', '+= ', None, '--', '++']

    # Imports
    if (enc_fmt == 1):
        header = "#include <wchar.h>\n\nwchar_t str[%s] = { " % (length)
    else:
        header = "#include <stdlib.h>\n#include <stdio.h>\n\nunsigned char str[%s] = { " % (length)
    input_list = [ord(i) for i in input_str]
    debug("Input list", input_list)

    encode_seq, rand_seq, output_seq = encode(input_list)
    # Initiate timeout
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(timing)
    # Determine ideal output of all-positive values
    while (sum([False if 0<=i<256 else True for i in output_seq]) > 0):
        encode_seq, rand_seq, output_seq = encode(input_list)
    debug("Encoding index", encode_seq)
    debug("Encoded inputs", output_seq)
    # Store char array
    header += ", ".join([hex(i) for i in output_seq]) + " };\n\n"

    enc_var1, enc_var2 = gen_varstr(), gen_varstr()
    # Decryption loop
    body = "int main() {\n\tfor (unsigned int %s = 0, %s = 0; %s < %s; %s++) {\n" % (enc_var1, enc_var2, enc_var1, length, enc_var1)
    body += "\t\t%s = str[%s];\n" % (enc_var2, enc_var1)
    # Reverse encoding functions
    for i in range(len(encode_seq)-1, -1, -1):
        if isinstance(encode_seq[i], list):
            body += "\t\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i][1]], enc_var1)
        elif encode_seq[i] == 1:
            body += "\t\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]], enc_var2)
        elif encode_seq[i] >= 5:
            body += "\t\t%s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]])
        else:
            body += "\t\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]], hex(rand_seq[i]))
    body += "\t\tstr[%s] = %s;\n" % (enc_var1, enc_var2)
    # Print decoded string
    if (enc_fmt == 1):
        body += "\t}\n\twprintf(str);\n}"
    else:
        body += "\t}\n\tprintf(\"%s\", str);\n}"

    # Output
    if (output_file):
        open(output_file, 'w').write(header+body)
        print("Done!")
    else:
        print(header+body)
    return


def main():
    if (lang == 'C' or lang == 'c'):
        C()
    else:
        print("Language not supported yet!")
        sys.exit()


if __name__ == '__main__':
    if (length==0):
        print("No input given!")
        parser.print_help()
        sys.exit()
    main()

