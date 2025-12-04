NAME = test.so

CC = gcc
CFLAGS = -Wall -Wextra -Werror -fPIC -shared

SRC =	$(wildcard file/*.c)



all: comp

comp: 
	$(CC) $(CFLAGS) $(SRC) -o $(NAME)
	 



