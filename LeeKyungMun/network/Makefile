# Compiler
CC = g++

# Compiler flags
CFLAGS =-g -Wall 

# Target executable
TARGET = add-nbo

# Source files
SRCS = main.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Default target
all: $(TARGET)

# Rule to build the target executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Rule to build object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Rule to clean the build directory
clean:
	rm -f $(OBJS) $(TARGET)

# Rule to run the program
run: $(TARGET)
	./$(TARGET)
