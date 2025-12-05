#cc  -fPIC -shared  file.c -o file.so
import sys
import random, string
from ctypes import *
import os, io
import tempfile
from contextlib import contextmanager
import ctypes
import signal
from text_gen import gen_text_lines
pos = 0
libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

TEST_NUMBER = int(sys.argv[1])
all_good = True
lib_gnl = CDLL("./gnl.so")
libc = CDLL(None)
f = io.StringIO()
lib_gnl.get_next_line.restype = ctypes.c_char_p  
lib_gnl.get_next_line.argtypes = [ctypes.c_int] 
def test_gnl(text):
    with open("nf", "w") as f:
        f.write(text)
    

    fd1 = os.open("nf", os.O_RDONLY)
    fd2 = os.open("nf", os.O_RDONLY)
    res2 = []
    with os.fdopen(fd2, "r") as file_obj:
        res1 = []

        for lines in file_obj:
            res1.append(lines)
    while True:
        line = lib_gnl.get_next_line(fd1)
        if not line:
            break
        res2.append(line.decode('utf-8'))
    os.close(fd1)

    return res1, res2


def handle_sigint(signum, frame):
    global i
    global TEST_NUMBER
    try:
        print(f"\nTesting Interrupted (Ctrl-C) Only {i}/{TEST_NUMBER}", file=sys.stderr)
    except ValueError:
        pass  
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

test_len = 0
line_max_len = 0
line_min_len = 0
errors = []
error_count = 0
for i in range(TEST_NUMBER):
    print(f"\ntest number {i} ;")
    res =  test_gnl(gen_text_lines(line_min_len, line_max_len, test_len))
    test_len += 1
    line_max_len += 1
    out1 =  res[0]
    out2 = res[1]
    print("real :",out1)
    print("mine :",out2) 
    #print("real :",len(out1.replace('\x00', '')))
    #print("mine :",len(out2.replace('\x00', ''))) 

    if out1 == out2:
        print(f"\nTest {i}: Test PASS ✅.\n")
    else:
        all_good = False
        print(f"\nTest {i}: Test FAIL ❌❗‼️⁉️.\n")
        print(f"  libc 1: {out1}")
        print(f"  libft 2: {out2}")
        error_count += 1
        errors.append((i, out1, out2))
if all_good:
    print(f"\n{ 1+ i} random test ✨Perfect✨")
else:
    print(f" ‼️{error_count}‼️ test faild ❌❗‼️⁉️")
    for error in errors:
        print(f"\n\nTest {error[0]} Failed ❌❗‼️n\n Real Function : {error[1]}\n Your Function : {error[2]}")

def test_gnl_sup(text):
    global lib_gnl
    out1 =  test_gnl(text);
    out2 =  test_gnl(text)
    print("real :",out1)
    print("mine :",out2) 
    #print("real :",len(out1.replace('\x00', '')))
    #print("mine :",len(out2.replace('\x00', ''))) 

    if out1 == out2:
        print(f"\nTest : Test PASS ✅.\n")
    else:
        all_good = False
        print(f"\n Test : Test FAIL ❌❗‼️⁉️.\n")
        print(f"  libc 1: {out1}")
        print(f"  libft 2: {out2}")
        return 0
    return 1


print("\n\n✨Suplementary tests ✨:\n")
supp_tests = [
    "",
    "WOPIE GOPIE",
    "\n\n\n\n\n\n\n",
    "\n\n\0\n\n",
    "\0\0\0\0\0\0\0",
    "dasd qFaer y 34rw er",
    "a" * 10000,
    "",
    "",
    "",
]
for i in range(len(supp_tests)):
    print(f"\nSupplementary Test {i}:")
    test_gnl_sup(supp_tests[i])

