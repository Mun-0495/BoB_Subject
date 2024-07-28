#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    uint8_t boot_indicator;
    uint8_t start_chs[3];
    uint8_t partition_type;
    uint8_t end_chs[3];
    uint32_t start_lba;
    uint32_t size_in_sectors;
} PartitionEntry;

void read_mbr(const char *file_path) {
    FILE *file = fopen(file_path, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    unsigned char mbr[512];
    unsigned char ebr[512];
    PartitionEntry partitions[4];

    size_t bytes_read = fread(mbr, 1, sizeof(mbr), file);
    if (bytes_read != sizeof(mbr)) {
        perror("Error reading MBR");
        fclose(file);
        return;
    }

    fseek(file, 446, SEEK_SET);  // MBR의 파티션 테이블 시작 위치
    PartitionEntry partitions[4];
    fread(partitions, sizeof(PartitionEntry), 4, file);

    // 파티션 테이블
    printf("Partition Table (next 64 bytes): ");
    for (int i = 446; i < 510; i++) {
        printf("%02X ", mbr[i]);
    }
    printf("\n");

    // 시그니처
    printf("Signature (last 2 bytes): %02X %02X\n", mbr[510], mbr[511]);

    fclose(file);
}

int main() {
    // MBR 파일 경로
    const char *file_path = "./mbr_128/mbr_128.dd";
    read_mbr(file_path);
    return 0;
}
