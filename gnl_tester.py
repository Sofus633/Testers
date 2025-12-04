#cc  -fPIC -shared  file.c -o file.so
import sys
import random, string
from ctypes import *
import os, io
import tempfile
from contextlib import contextmanager
import ctypes
import signal

pos = 0
libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

@contextmanager
def stdout_redirector(stream):
    original_stdout_fd = sys.stdout.fileno()
    
    def _redirect_stdout(to_fd):
        """Redirect stdout to the given file descriptor."""

        libc.fflush(c_stdout)

        sys.stdout.close()

        os.dup2(to_fd, original_stdout_fd)

        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))


    saved_stdout_fd = os.dup(original_stdout_fd)
    try:

        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stdout(tfile.fileno())

        yield
        _redirect_stdout(saved_stdout_fd)

        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read().decode("utf-8"))
    finally:
        tfile.close()
        os.close(saved_stdout_fd)

TEST_NUMBER = int(sys.argv[1])
all_good = True
lib_gnl = CDLL("./gnl.so")
libc = CDLL(None)
f = io.StringIO()

def test_gnl():
    with open("nf", "a") as f:
        f.write(gen_text_lines(10, 1000, 50))
    

    fd1 = os.open("nf", os.O_RDONLY)
    fd2 = os.open("nf", os.O_RDONLY)

    with os.fdopen(fd2, "r") as file_obj:
        res1 = []
        res2 = []
        while True:
            line = gnl.get_next_line(fd1)
            if not line:
                break
            res2.append(line.decode('utf-8'))
        os.close(fd1)
        for lines in file_obj:
            res1.append(lines)
        os.close(fd2)
        return res1, res2
    os.close(fd2)
    return 0, 0


def handle_sigint(signum, frame):
    global i
    global TEST_NUMBER
    try:
        print(f"\nTesting Interrupted (Ctrl-C) Only {i}/{TEST_NUMBER}", file=sys.stderr)
    except ValueError:
        pass  
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)
 
rrors = []
for i in range(TEST_NUMBER):

    arg = gnl_arg()
    print(f"\ntest number {i} ;")
    print(arg)
    res =  get_output(lib_printf.ft_printf, arg)
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
        errors.append((i, arg, out1, out2))
if all_good:
    print(f"\n{ 1+ i} random test ✨Perfect✨")
else:
    print("test faild ❌❗‼️⁉️")
    for error in errors:
        print(f"\n\nTest {error[0]} Failed ❌❗‼️\ntest arguments {error[1]}\n\n Real Function : {error[2]}\n Your Function : {error[3]}")

def test_gnl(fd):
    global lib_gnl
    out1 =  tests_gnl();
    out2 =  tests_gnl()
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
    [b""],
    [b"Number: %d, Hex: %x, Char: %c", 42, 255, ord('A')],
    [b"Pointer: %p", ctypes.c_void_p(12345678)],
    [b"Empty arg string: %s", b""],
    [b"Null string: %s", ctypes.c_char_p(None)],
    [b"Null pointer: %p", ctypes.c_void_p(0)],
    [b"Int min/max: %d %d", -2147483648, 2147483647],
    [b"Unsigned max: %u", 4294967295],
    [b"Hex extremes: %x %X", 3735928559, 3735928559],
    [b"Mixed: %s %c %p %d %u %x %X %%", b"test", ord('Z'), ctypes.c_void_p(0x1234), -1, 4294967295, 305419896, 305419896],
]
for i in range(len(supp_tests)):
    print(f"\nSupplementary Test {i}:")
    test_gnl(supp_tests[i])

