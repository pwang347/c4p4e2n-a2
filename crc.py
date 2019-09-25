# crc.py
# Finds collisions in crc32
#
# See results of run at collision1.txt and collision2.txt
#

from collections import defaultdict
from subprocess import run, PIPE
import argparse
import base64
import struct
import time
import binascii
import math

parser = argparse.ArgumentParser(description='CRC collision finder')
parser.add_argument('--x')
parser.add_argument('--question_id', type=int, default=1)
args = parser.parse_args()

x_file = "crc_%d_x.txt" % args.question_id
y_file = "crc_%d_y.txt" % args.question_id

def int_to_bytes(n):
    """
    Credits: https://stackoverflow.com/a/51446863
    """
    num_bytes = int(math.ceil(n.bit_length() / 8))
    n_bytes = n.to_bytes(num_bytes, byteorder='big')
    return n_bytes

def find_crc32_match(target=None):
    """
    It's way too costly to use pycrc as a binary through shell calls, and also writing to files.
    We reduce the costs by using binascii.crc32 instead.
    """
    start = time.time()
    iterations = 0

    if target is not None:
        i = int.from_bytes(target.encode("utf-8"), "big")
        x_value = binascii.crc32(target.encode())
        print(x_value)
        targets = [i]
    else:
        targets = range(1, 2**32) # binascii and PyCRC seem to disagree on the value of 0x0

    for i in targets:
        xb = int_to_bytes(i)
        x_value = binascii.crc32(xb)
        print(x_value)

        # try all 2^32 bit arrangements
        for j in range(2**32):
            yb = int_to_bytes(j)
            y_value = binascii.crc32(yb)

            if y_value == x_value and j != i:
                end = time.time()
                elapsed = end - start
                iterations = i * 2**32 + j if target is None else j
                print("Found match in %d iterations after %.2f seconds: %d and %d have value %s" % (
                    iterations,
                    elapsed,
                    i,
                    j,
                    y_value))
                x_bytes = int_to_bytes(i)
                y_bytes = int_to_bytes(j)
                print("X")
                try:
                    print("String: %s" % x_bytes.decode())
                except UnicodeDecodeError:
                    pass
                print("Base64: %s" % str(base64.b64encode(x_bytes), "utf-8"))
                print("Hex: %s" % hex(i))
                with open(x_file, "wb") as xfile:
                    xfile.write(x_bytes)

                print ("Y")
                try:
                    print("String: %s" % int_to_bytes(j).decode())
                except UnicodeDecodeError:
                    pass
                print("Base64: %s" % str(base64.b64encode(y_bytes), "utf-8"))
                print("Hex: %s" % hex(j))
                with open(y_file, "wb") as yfile:
                    yfile.write(y_bytes)

                return
    
    raise Exception("Should not have reached here")

find_crc32_match(args.x)
