import random
import string

frequency = 10

def gen_text_lines(min, max, nb_lines):
    strr = ""
    if nb_lines == 0:
        return strr
    for y in range(0, nb_lines):
        linelen = random.randint(min, max)
        #strr += str(y) + ' '
        for i in range(0, linelen):
            char =  random.choice(string.printable)
            if char != '\n' and char != '\r':
                strr += char
        strr += '\n'

    return strr

if __name__ == "__main__":
    print(gen_text_lines(0, 1000, 10))
