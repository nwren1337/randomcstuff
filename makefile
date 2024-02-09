CC=gcc
CFLAGS=-I.

OUT=build
IN=src

BST=${IN}/binarysearchtree

FACT=${IN}/factorial

all : ${OUT}/bst ${OUT}/factorial

${OUT}/bst: 
	cd ${BST} && make

${OUT}/factorial: 
	cd ${FACT} && make

.PHONY: clean

clean:
	rm -f build/*