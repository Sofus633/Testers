import ctypes
import os

gnl = ctypes.CDLL("./gnl.so")

gnl.get_next_line.argtypes = [ctypes.c_int]
gnl.get_next_line.restype = ctypes.c_char_p


def test_gnl(file_path):
    fd1 = os.open(file_path, os.O_RDONLY)
    fd2 = os.open(file_path, os.O_RDONLY)

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

        return res1 == res2
    os.close(fd2)
    return 0

print(test_gnl('test'))

