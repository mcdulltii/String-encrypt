#!/usr/bin/env python3
import sys
from src.functions import *


# Prints debug statements
def debug(title, strings, debugging):
    if (debugging): print("[*] %s:\t%s" % (title, strings))
    return


# String encryption for C
def C(input_list, debugging, length, encoding, timing, output_file):
    # Encryption method: UNICODE/ANSI -> wchar/stdio
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
    debug("Input list", input_list, debugging)

    # Find all-positive output values
    encode_seq, rand_seq, output_seq = find_pos(input_list, length, encoding, timing)
    debug("Encode sequence", encode_seq, debugging)
    debug("Output list", output_seq, debugging)
    # Store char array
    header += ", ".join([hex(i) for i in output_seq]) + " };\n\n"

    enc_var1, enc_var2 = gen_varstr(), gen_varstr()
    # Decryption loop
    body = "int main() {\n\tfor (unsigned int %s = 0, %s = 0; %s < %s; %s++) {\n" % (enc_var1, enc_var2, enc_var1, length, enc_var1)
    body += "\t\t%s = str[%s];\n" % (enc_var2, enc_var1)
    # Reverse encoding functions
    body += decode(encode_seq, rand_seq, decode_fmt, enc_var1, enc_var2)
    body += "\t\tstr[%s] = %s;\n" % (enc_var1, enc_var2)
    # Print decoded string
    if (enc_fmt == 1):
        body += "\t}\n\twprintf(str);\n}\n"
    else:
        body += "\t}\n\tprintf(\"%s\", str);\n}\n"

    # Output
    output(header, body, output_file)
    return


# String encryption for Python
def py(input_list, debugging, length, encoding, timing, output_file):
    # Strings for decoding
    decode_fmt = ['^= ', '= ~', '-= ', '+= ']

    # Encoded string
    header = "enc_str = [ "
    debug("Input list", input_list, debugging)

    # Find all-positive output values
    encode_seq, rand_seq, output_seq = find_pos(input_list, length, encoding, timing, len(encode_func)-3)
    debug("Encode sequence", encode_seq, debugging)
    debug("Output list", output_seq, debugging)
    # Store char array
    header += ", ".join([hex(i) for i in output_seq]) + " ]\n\n"

    enc_var1, enc_var2 = gen_varstr(), gen_varstr()
    # Decryption loop
    body = "for %s in range(%s):\n" % (enc_var1, length)
    body += "\t%s = enc_str[%s];\n" % (enc_var2, enc_var1)
    # Reverse encoding functions
    body += decode(encode_seq, rand_seq, decode_fmt, enc_var1, enc_var2)
    body += "\tenc_str[%s] = %s;\n" % (enc_var1, enc_var2)
    # Print decoded string
    body += "\nenc_str = ''.join([chr(i) for i in enc_str])\n"
    body += "del %s, %s\n" % (enc_var1, enc_var2)
    body += "print(enc_str)\n"

    # Output
    output(header, body, output_file)
    return


# String encryption for Javascript
def js(input_list, debugging, length, encoding, timing, output_file):
    # Strings for decoding
    decode_fmt = ['^= ', '= ~', '-= ', '+= ', None, '--', '++']

    # Imports
    header = "<script type=\"text/javascript\">\n\nvar str = \""
    debug("Input list", input_list, debugging)

    # Find all-positive output values
    encode_seq, rand_seq, output_seq = find_pos(input_list, length, encoding, timing)
    debug("Encode sequence", encode_seq, debugging)
    debug("Output list", output_seq, debugging)
    # Store char array
    header += "".join([hex(i) for i in output_seq]).replace('0x','\\x') + "\";\n\n"

    enc_var1, enc_var2 = gen_varstr(), gen_varstr()
    # Decryption loop
    body = "for (var %s = 0, %s = 0; %s < %s; %s++) {\n" % (enc_var1, enc_var2, enc_var1, length, enc_var1)
    body += "\t%s = str.charCodeAt(%s);\n" % (enc_var2, enc_var1)
    # Reverse encoding functions
    body += decode(encode_seq, rand_seq, decode_fmt, enc_var1, enc_var2)
    body += "\tstr = str.substr(0, %s) + String.fromCharCode(%s) + str.substr(%s + 1);\n" % (enc_var1, enc_var2, enc_var1)
    # Print decoded string
    body += "}\nalert(str);\n</script>\n"

    # Output
    output(header, body, output_file)
    return


# String encryption for Java
def java(input_list, debugging, length, encoding, timing, output_file):
    # Strings for decoding
    decode_fmt = ['^= ', '= ~', '-= ', '+= ', None, '--', '++']

    # Strip outfile name
    try:
        class_name = output_file.split('.')[-2].split('/')[-1].split('\\')[-1]
    except:
        class_name = input("Input Java class name: ")
    if (not class_name):
        print("Invalid class name")
        sys.exit()

    # Imports
    header = "import java.io.*;\n\npublic class %s {\n\tpublic static void main(String myargs[]) {\n\tString str = \"" % (class_name)
    debug("Input list", input_list, debugging)

    # Find all-positive output values
    encode_seq, rand_seq, output_seq = find_pos(input_list, length, encoding, timing)
    debug("Encode sequence", encode_seq, debugging)
    debug("Output list", output_seq, debugging)
    # Store char array
    header += "\\u00"+"\\u00".join([hex(i) for i in output_seq]).replace('0x','').zfill(2) + "\";\n\n"

    enc_var1, enc_var2 = gen_varstr(), gen_varstr()
    # Decryption loop
    body = "\tfor (int %s = 0, %s = 0; %s < %s; %s++) {\n" % (enc_var1, enc_var2, enc_var1, length, enc_var1)
    body += "\t%s = str.charAt(%s);\n" % (enc_var2, enc_var1)
    # Reverse encoding functions
    body += decode(encode_seq, rand_seq, decode_fmt, enc_var1, enc_var2)
    body += "\tstr = str.substring(0, %s) + (char)(%s) + str.substring(%s + 1);\n" % (enc_var1, enc_var2, enc_var1)
    # Print decoded string
    body += "\t}\n\tSystem.out.println(str);\n\t}\n}\n"

    # Output
    output(header, body, output_file)
    return


# Write to file/stdout
def output(header, body, output_file):
    if (output_file):
        open(output_file, 'w').write(header+body)
        print("Done!")
    else:
        print(header+body)
    return

