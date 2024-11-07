CC=gcc
CFLAGS="-I. -O3 -march=native"
DEBUG="-I. -gp"
OBJDIR=obj
DEPS = include/bst.h include/avl.h

BST_OBJ= ${OBJDIR}/bst.o ${OBJDIR}/bst_driver.o
BST_DEBUGOBJ= ${OBJDIR}/bst_debug.o ${OBJDIR}/bst_driver_debug.o

AVL_OBJ= ${OBJDIR}/avl.o ${OBJDIR}/avl_driver.o

OUTDIR=build

${OBJDIR}/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OBJDIR}/%_debug.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(DEBUG)

${OUTDIR}/bst_driver: $(BST_OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

${OUTDIR}/bst_driver_debug: $(BST_DEBUGOBJ)
	$(CC) -o $@ $^ $(DEBUG)

${OUTDIR}/avl_driver: $(AVL_OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY=setup

setup: 
	@rm -rf ${OUTDIR}
	@rm -rf ${OBJDIR}
	mkdir ${OUTDIR}
	mkdir ${OBJDIR}