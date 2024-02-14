CC=gcc
CFLAGS="-I. -O3 -march=native"
DEBUG="-I. -gp"
DEPS = include/bst.h
OBJDIR=obj
OBJ= ${OBJDIR}/bst.o ${OBJDIR}/bst_driver.o
DEBUGOBJ= ${OBJDIR}/bst_debug.o ${OBJDIR}/bst_driver_debug.o

OUTDIR=build

${OBJDIR}/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OBJDIR}/%_debug.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(DEBUG)

${OUTDIR}/bst_driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

${OUTDIR}/bst_driver_debug: $(DEBUGOBJ)
	$(CC) -o $@ $^ $(DEBUG)

.PHONY=setup

setup: 
	@rm -rf ${OUTDIR}
	@rm -rf ${OBJDIR}
	mkdir ${OUTDIR}
	mkdir ${OBJDIR}