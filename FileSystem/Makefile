# 컴파일러 및 플래그 설정
CC = gcc
CFLAGS = -Wall -Wextra -O2

# 실행 파일 이름
MBR_TARGET = MBRParser
GPT_TARGET = GPTParser
FAT32_TARGET = FAT32Parser

# 소스 파일
MBR_SRC = MBRParser.c
GPT_SRC = GPTParser.c
FAT32_SRC = FAT32Parser.c

# 목표 정의
all: $(MBR_TARGET) $(GPT_TARGET) $(FAT32_TARGET)

$(MBR_TARGET): $(MBR_SRC)
	$(CC) $(CFLAGS) -o $@ $^

$(GPT_TARGET): $(GPT_SRC)
	$(CC) $(CFLAGS) -o $@ $^

$(FAT32_TARGET): $(FAT32_SRC)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(MBR_TARGET) $(GPT_TARGET) $(FAT32_TARGET)

.PHONY: all clean
