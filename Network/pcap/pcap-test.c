#include <pcap.h>
#include <stdbool.h>
#include <stdio.h>
#include <libnet.h>

//typedef struct libnet_ethernet_hdr 

void usage() {
	printf("syntax: pcap-test <interface>\n");
	printf("sample: pcap-test wlan0\n");
}

void print_ethernet_header_info(struct libnet_ethernet_hdr* ethernet_header, u_char* packet) {

	printf("Destination MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
		ethernet_header->ether_dhost[0],
		ethernet_header->ether_dhost[1],
		ethernet_header->ether_dhost[2],
		ethernet_header->ether_dhost[3],
		ethernet_header->ether_dhost[4],
		ethernet_header->ether_dhost[5]);
	printf("Source MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
		ethernet_header->ether_shost[0],
		ethernet_header->ether_shost[1],
		ethernet_header->ether_shost[2],
		ethernet_header->ether_shost[3],
		ethernet_header->ether_shost[4],
		ethernet_header->ether_shost[5]);
	printf("Ethernet type: %x\n", ntohs(ethernet_header->ether_type));
	printf("\n");
}

void print_ipv4_header_info(struct libnet_ipv4_hdr* ip_header, u_char* packet) {
	uint32_t source_ip = ntohl(ip_header->ip_src.s_addr);
	uint32_t destination_ip = ntohl(ip_header->ip_dst.s_addr);

	//xxx.xxx.xxx.xxx => 8byte, 8byte, 8byte, 8byte.
	u_int8_t source_ip1 = (source_ip & 0xff000000) >> 24;
	u_int8_t source_ip2 = (source_ip & 0x00ff0000) >> 16;
	u_int8_t source_ip3 = (source_ip & 0x0000ff00) >> 8;
	u_int8_t source_ip4 = (source_ip & 0x000000ff);
	printf("%d.%d.%d.%d\n",source_ip1, source_ip2, source_ip3, source_ip4);

	//xxx.xxx.xxx.xxx => 8byte, 8byte, 8byte, 8byte.
	u_int8_t destionation_ip1 = (destination_ip & 0xff000000) >> 24;
	u_int8_t destionation_ip2 = (destination_ip & 0x00ff0000) >> 16;
	u_int8_t destionation_ip3 = (destination_ip & 0x0000ff00) >> 8;
	u_int8_t destionation_ip4 = (destination_ip & 0x000000ff);
	printf("%d.%d.%d.%d\n",destionation_ip1, destionation_ip2, destionation_ip3, destionation_ip4);

    printf("IP Header Length: %d\n", ip_header->ip_hl * 4);
    printf("Protocol: %d\n", ip_header->ip_p);

	printf("\n");
}

void print_tcp_header_info(struct libnet_tcp_hdr* tcp_header, u_char* packet) {
	
	printf("<TCP>\n");
	printf("Source PORT : ");
	printf("%d\n",ntohs(tcp_header->th_sport));
	printf("Destination PORT : ");
	printf("%d\n",ntohs(tcp_header->th_dport));

	printf("\n");
}

typedef struct {
	char* dev_;
} Param;

Param param = {
	.dev_ = NULL
};

bool parse(Param* param, int argc, char* argv[]) {
	if (argc != 2) {
		usage();
		return false;
	}
	param->dev_ = argv[1];
	return true;
}

int main(int argc, char* argv[]) {
	if (!parse(&param, argc, argv))
		return -1;

	char errbuf[PCAP_ERRBUF_SIZE];

	//PCAP => PACKET Capture
	struct libnet_ethernet_hdr* ethernet_header;
	struct libnet_ipv4_hdr* ip_header;
	struct libnet_tcp_hdr* tcp_header;
	
	pcap_t* pcap = pcap_open_live(param.dev_, BUFSIZ, 1, 1000, errbuf);
	if (pcap == NULL) {
		fprintf(stderr, "pcap_open_live(%s) return null - %s\n", param.dev_, errbuf);
		return -1;
	}

	while (true) {
		struct pcap_pkthdr* header;
		const u_char* packet;
		int res = pcap_next_ex(pcap, &header, &packet);
		
		printf("packet lenth : %d\n", header->len, packet);
		
		if (res == 0) continue;
		if (res == PCAP_ERROR || res == PCAP_ERROR_BREAK) {
			printf("pcap_next_ex return %d(%s)\n", res, pcap_geterr(pcap));
			break;
		}
		ethernet_header = (struct libnet_ethernet_hdr*)packet;
		ip_header = (struct libnet_ipv4_hdr*)(packet + sizeof(struct libnet_ethernet_hdr));
		tcp_header = (struct libnet_tcp_hdr*)(packet + sizeof(struct libnet_ethernet_hdr) + ip_header->ip_hl * 4);

		//6 -> TCP HEADER 
		if(ip_header->ip_p != 0x06) continue;

		print_ethernet_header_info(ethernet_header, packet);
		print_ipv4_header_info(ip_header, packet);
		print_tcp_header_info(tcp_header, packet);
		
		uint32_t hsize = 14 + (ip_header->ip_hl) * 4 + (tcp_header->th_off) * 4;
		printf("header size : %u, capture length : %u\n", hsize, header->caplen);
		printf("Payload(Data) : ");
		for(int i=hsize; i<hsize+8 && i<header->caplen; i++) {
			printf("0x%02X ", packet[i]);
		}
		printf("\n\n");
	
		printf("%u bytes captured\n", header->caplen);
		printf("----------END OF PACKET CAPTURE----------\n\n");

	}

	pcap_close(pcap);
}
