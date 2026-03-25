CC=gcc
CFLAGS="-I. -O3 -march=native"
DEBUG="-I. -gp"
OBJDIR=obj
DEPS = include/sorting.h
DATA=data

SRT_OBJ= ${OBJDIR}/sorting.o ${OBJDIR}/sortingdriver.o
SRT_DEBUGOBJ= ${OBJDIR}/sorting_debug.o ${OBJDIR}/sortingdriver_debug.o


OUTDIR=build

${OBJDIR}/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

${OBJDIR}/%_debug.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(DEBUG)

${OUTDIR}/srt_driver: $(SRT_OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

${OUTDIR}/srt_driver_debug: $(SRT_DEBUGOBJ)
	$(CC) -o $@ $^ $(DEBUG)

.PHONY=setup

setup: 
	@rm -rf ${OUTDIR}
	@rm -rf ${OBJDIR}
	@rm -rf ${DATA}
	mkdir ${OUTDIR}
	mkdir ${OBJDIR}
	mkdir ${DATA}
	poetry run python3 ./data_gen.py 10
	poetry run python3 ./data_gen.py 100
	poetry run python3 ./data_gen.py 1000
	poetry run python3 ./data_gen.py 10000
	poetry run python3 ./data_gen.py 100000
	poetry run python3 ./data_gen.py 1000000
	poetry run python3 ./data_gen.py 10000000
	poetry run python3 ./data_gen.py 100000000
	poetry run python3 ./data_gen.py 1000000000
	