CC=gcc
CFLAGS=-I.
DEPS = bst.h
OBJ= bst.o main.o

OUT=../../build

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OUT}/bst: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)