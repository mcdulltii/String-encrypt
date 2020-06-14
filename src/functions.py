#!/usr/bin/env python3
import random
import string
import sys
from contextlib import contextmanager
import threading
import _thread


# Generates random alphachar variable names
def gen_varstr(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


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
@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        print("Time exceeded!")
        sys.exit()
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()


# Store functions within list for function randomization
encode_func = [xor, neg, add, sub, index, inc, dec]


# Random generator with non-consecutive repeats
# n: Indexes of encode_func
# N: Encoding multiplier
class generator:
    def __init__(self, n, N):
        assert n > 1, "n has to be more than 1"
        self.n = n
        self.N = N
        self.combi = [[0],[1],[2,3],[4],[5,6]]

    def __iter__(self):
        prev = [-1]
        cur_len = 0
        while cur_len < self.N:
            is_four = 0
            x = random.randint(0,self.n)
            if x not in prev:
                if x == 4:
                    x = random.choice([i for i in [0,2,3] if i not in prev])
                    is_four = 1
                prev = [i for i in self.combi if x in i][0]
                #print(prev)
                cur_len += 1
                if (is_four):
                    yield [4, x]
                else:
                    yield x


# Encode input characters with encoding multiplier
def encode(input_list, func_len, length, encoding):
    # Randomise encoding functions
    encode_seq = [i for i in generator(func_len, encoding)]
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
        if (temp < 0):
            return encode_seq, rand_seq, [-1, -1, -1]
        output_seq.append(temp)
    return encode_seq, rand_seq, output_seq


# Find all-positive output values
def find_pos(input_list, length, encoding, timing, func_len=len(encode_func)-1):
    encode_seq, rand_seq, output_seq = encode(input_list, func_len, length, encoding)
    # Initiate timeout
    with time_limit(timing):
    # Determine ideal output of all-positive values
        while (sum([False if 0<=i<256 else True for i in output_seq]) > 0):
            encode_seq, rand_seq, output_seq = encode(input_list, func_len, length, encoding)
    return encode_seq, rand_seq, output_seq


# Reverse encoding functions
def decode(encode_seq, rand_seq, decode_fmt, enc_var1, enc_var2):
    body = ""
    for i in range(len(encode_seq)-1, -1, -1):
        if isinstance(encode_seq[i], list):
            body += "\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i][1]], enc_var1)
        elif encode_seq[i] == 1:
            body += "\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]], enc_var2)
        elif encode_seq[i] >= 5:
            body += "\t%s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]])
        else:
            body += "\t%s %s%s;\n" % (enc_var2, decode_fmt[encode_seq[i]], hex(rand_seq[i]))
    return body

