CC=gcc
CFLAGS="-I. -O3"
DEBUG="-I. -gp"
DEPS = include/bst.h
OBJDIR=obj
OBJ= ${OBJDIR}/bst.o ${OBJDIR}/bst_driver.o

OUT=build

${OBJDIR}/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OUT}/bst_driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

${OUT}/bst_driver_debug: $(OBJ)
	$(CC) -o $@ $^ $(DEBUG)