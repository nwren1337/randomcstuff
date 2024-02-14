CC=gcc
CFLAGS="-I. -O3"
DEBUG="-I. -gp"
DEPS = include/bst.h
OBJ= bst.o bst_driver.o

OUT=build

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OUT}/bst_driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

${OUT}/bst_driver_debug: $(OBJ)
	$(CC) -o $@ $^ $(DEBUG)