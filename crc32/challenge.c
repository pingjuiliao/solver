#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <zlib.h>

#define SIZE 4

/*
 * 1) create table with a separate function, e.g., crc32_table_gen();
 *
 */

uint32_t table[256];
uint32_t have_table = 0;
uint32_t rem;

void
crc32_table_gen(void) {
    uint32_t i, j;

	/* This check is not thread safe; there is no mutex. */
	if (have_table == 0) {
		/* Calculate CRC table. */
		for (i = 0; i < 256; i++) {
			rem = i;  /* remainder from polynomial division */
			for (j = 0; j < 8; j++) {
				if (rem & 1) {
					rem >>= 1;
					rem ^= 0xedb88320;
				} else
					rem >>= 1;
			}
			table[i] = rem;
		}
		have_table = 1;
	}
}

uint32_t
f_crc32(uint32_t crc, const char* buf, size_t len) {
	const char *p, *q;
	// uint8_t* b = (uint8_t * ) buf ;
    
    crc = ~crc;
	q = buf + len;
	for (p = buf; p < q; p++) {
        uint8_t new_input = *p;
        uint32_t table_input = table[(crc & 0xff) ^ new_input];
        crc = (crc >> 8) ^ table_input;
	}
	return ~crc;
}
 
void 
bugs(void) {
    puts("bug FOUND");
    // __builtin_trap() ;
}
int
main(void) {
    int r = 0 ;
    char in_buf[5] ;
    uint32_t out ; 
    char out_buf[5];
    bzero(in_buf, sizeof(in_buf)) ;
    crc32_table_gen();
    

    if ( (r = read(0, in_buf, SIZE) ) == 0 ) {
        fprintf(stderr, "Read() error: zero bytes received\n") ;
        exit(-1) ;
    }
    
    out = f_crc32(0, in_buf, SIZE) ;
    printf("0x%08x\n", out);
    if ( out == 0xed82cd11 ) { // ' crc32("abcd") == 0xed82cd11 '
        bugs() ;
    } else {
        fprintf(stderr, "Incorrect !\n") ;
    }

    return 0 ;
}
