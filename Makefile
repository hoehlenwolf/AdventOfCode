ifdef OS
	dll202015 = cl.exe /LD aoc_2020\\code\\day15.c /o aoc_2020\\code\\day15_win /Fo:aoc_2020\\code\\day15_win
else
	ifeq ($(shell uname), Linux)
		dll202015 = gcc -shared aoc_2020/code/day15.c -o aoc_2020/code/day15_linux.so
	endif
endif
all: c-2020-15
c-2020-15:
	$(dll202015)

		