#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

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

void find_file_system_and_partition(uint32_t partition_type, uint32_t start_lba, uint32_t size_in_sectors) {
     /*
     * 0x00	EMPTY	    0x0E	FAT16
     * 0x01	FAT12	    0x0F	MS Extended
     * 0x04	FAT16	    0x83	Linux
     * 0x05	MS Extended	0x85	Linux Extended
     * 0x06	FAT16	    0xA5	FreeBDS
     * 0x07	NTFS	    0xA8	MACOSX
     * 0x0B	FAT32	    0xAB	MAC OSX BOOT
     * 0x0C	FAT32	    0XEE	EFI GTP DIST 
     * Reference : https://twoicefish-secu.tistory.com/153
     */

    if(partition_type == 0x00) {
        return;  // Unused partition entry
    }
        
    if(partition_type == 0x07) {
        printf("%s %u %u\n", "NTFS", start_lba, size_in_sectors);
    }

    if(partition_type == 0x0B || partition_type == 0x0C) {
        printf("%s %u %u\n", "FAT32", start_lba, size_in_sectors);
    }

    /*
     * FAT12, FAT16 Does not necessary.
     */
    // if(partition_type == 0x01) {
    //     printf("%s %u %u\n", "FAT12", start_lba, size_in_sectors);
    // }

    // if(partition_type == 0x04 || partition_type == 0x06) {
    //     printf("%s %u %u\n", "FAT16", start_lba, size_in_sectors);
    // }
    
}

void read_extended_partition(FILE *file, uint32_t ebr_lba, uint32_t base_lba) {
    PartitionEntry ebr_partitions[4]; // Primary and next EBR pointers
    unsigned char signature[2];

    // If not Signature, Don't Do.
    fseek(file, offset(ebr_lba) + 510, SEEK_SET);
    fread(signature, sizeof(char), 2, file);
    if(signature[0] != 0x55 || signature[1] != 0xAA) {
        fprintf(stderr, "Invalid MBR signature\n");
        fclose(file);
        return;
    }
    
    /*
     * File Offset
     * Suppose Sector size -> 512
     * File Seek -> offset + 446 (Find end of 4 line)
     */ 
    fseek(file, offset(ebr_lba) + 446, SEEK_SET);
    fread(ebr_partitions, sizeof(PartitionEntry), 4, file);

    for(int i = 0; i < 4; i++) {
        if(ebr_partitions[i].partition_type == 0x05) {
            //printf("start lba -> 0x%x\n", ebr_partitions[i].start_lba);
            /*
             * Go and Find new partition
             * base addr + start_lba -> new address, offset calculate wiil do before loop
             * new base addr -> ebr_lba
             */
            read_extended_partition(file, base_lba + ebr_partitions[i].start_lba, ebr_lba);
        }
        else {
            //printf("partition type is 0x%x\n", ebr_partitions[i].partition_type);
            find_file_system_and_partition(ebr_partitions[i].partition_type, 
                                           base_lba + ebr_partitions[i].start_lba, ebr_partitions[i].size_in_sectors);
        }
    }
}

void read_mbr(const char *file_path) {
    FILE *file = fopen(file_path, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    unsigned char mbr[512];
    PartitionEntry partitions[4];
    size_t bytes_read = fread(mbr, 1, sizeof(mbr), file);
    if (bytes_read != sizeof(mbr)) {
        perror("Error reading MBR");
        fclose(file);
        return;
    }

    // If not Signature, Don't Do.
    if (mbr[510] != 0x55 || mbr[511] != 0xAA) {
        fprintf(stderr, "Invalid MBR signature\n");
        fclose(file);
        return;
    }

    // MBR의 파티션 테이블 시작 위치
    fseek(file, 446, SEEK_SET);  
    fread(partitions, sizeof(PartitionEntry), 4, file);

   
    for(int i = 0; i < 4; i++) {
        if(partitions[i].partition_type == 0x05) {
            //printf("start lba -> 0x%x\n", partitions[i].start_lba);
            read_extended_partition(file, partitions[i].start_lba, partitions[i].start_lba);
        }
        else {
            //printf("partition type is 0x%x ", partitions[i].partition_type);
            find_file_system_and_partition(partitions[i].partition_type, partitions[i].start_lba, partitions[i].size_in_sectors);
        }
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <disk image file>\n", argv[0]);
        return 1;
    }

    const char *file_path = argv[1];
    read_mbr(file_path);
    return 0;
}
