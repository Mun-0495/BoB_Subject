#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define SECTOR_SIZE 512

typedef struct {
    uint8_t boot_indicator;
    uint8_t start_chs[3];
    uint8_t partition_type;
    uint8_t end_chs[3];
    uint32_t start_lba;
    uint32_t size_in_sectors;
} PartitionEntry;

uint64_t offset(uint32_t start_lba) {
    return (uint64_t)start_lba * SECTOR_SIZE;
}

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
    if(bytes_read != sizeof(mbr)) {
        perror("Error Reading MBR");
        fclose(file);
        return;
    }

    else if(mbr[510] != 0x55 || mbr[511] != 0xAA) {
        perror("There is not Signature");
        fclose(file);
        return ;
    }

    fseek(file, 446, SEEK_SET);  // MBR의 파티션 테이블 시작 위치
    PartitionEntry partitions[4];
    fread(partitions, sizeof(PartitionEntry), 4, file);

    for(int i = 0; i < 4; i++) {
        if(partitions[i].partition_type == 0x05) {
            //TODO : extended MBR
            //go EBR address
            //file seek
            fseek(file, offset(partitions[i].start_lba), SEEK_SET);
            fread(ebr, 1, sizeof(ebr), file);
            
        }

        if(partitions[i].partition_type == 0x07) {
            //TODO : just go and idenify the type of Partition.
            //go EBR address, just print type

        }
    }
    // 파티션 테이블


    fclose(file);
}

int main() {
    // MBR 파일 경로
    const char *file_path = "./mbr_128/mbr_128.dd";
    read_mbr(file_path);
    return 0;
}
