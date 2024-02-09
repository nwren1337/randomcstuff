CC=gcc
CFLAGS=-I.
OBJ= factorial.o

OUT=../../build

%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS)

${OUT}/factorial: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)