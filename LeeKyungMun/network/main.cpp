#include <stddef.h> // for size_t
#include <stdint.h> // for uint8_t
#include <stdio.h>  // for printf
#include <stdlib.h>
#include <netinet/in.h>

uint32_t read_file_value(const char* filename) {
    FILE* fstream;
    uint32_t value, result;

    fstream = fopen(filename, "rb"); // Use "rb" for binary reading

    if(fstream == NULL) {
        printf("FILE OPEN ERROR: %s\n", filename);
        exit(1);
    }

    // Determine file size
    fseek(fstream, 0, SEEK_END);
    long file_size = ftell(fstream);
    fseek(fstream, 0, SEEK_SET);

    // Check if file size is 4 bytes
    // printf("%d", file_size);
    if(file_size != 4) {
        printf("FILE SIZE ERROR: %s is not 4 bytes\n", filename);
        fclose(fstream);
        exit(1);
    }

    // Read the 4-byte integer
    fread(&value, sizeof(uint32_t), 1, fstream);
    fclose(fstream);

    // Add value to the result
    // Convert from network byte order to host byte order
    result = ntohl(value); 
    return result;
}

int main(int argc, char *argv[]) {

    //if argv count is not 2 => error.
    if (argc != 3) {
        printf("Usage: %s <file1> <file2>\n", argv[0]);
        return 1;
    }
    char name[] = "문경태";

    // Read and add values from files
    uint32_t value1 = read_file_value(argv[1]);
    uint32_t value2 = read_file_value(argv[2]);
    uint32_t result = value1 + value2;

    printf("[bob13][개발]add-nbo[%s]\n", name);
    printf("%u(0x%x) + %u(0x%x) = %u(0x%x)\n", value1, value1, value2, value2, result, result);

    return 0;
}
