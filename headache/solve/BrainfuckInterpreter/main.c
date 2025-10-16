#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main(int argc, char **argv) {
	if (argc < 2) { printf("Program must take a brainfuck script as an argument\n"); return 1; }
	unsigned char			tab[30000];
	unsigned char			*ptr;
	unsigned char			instr[1];
	unsigned char			input[1];
	long long int			pos;
	long long int			ws[30000];
	int						no_w;
	int						fd;
	int						i;

	for (int p = 1; argv[p]; p++) {
		if ((fd = open(argv[p], O_RDONLY)) < 2) { printf("Error trying to open file %s\n", argv[p]); continue ; }
		printf("Executing file %s :\n", argv[p]);
		memset(tab, 0, 30000);
		for (int t = 0; t < 30000; t++) ws[t] = -1;
		ptr = tab;
		pos = 0;
		no_w = 0;
		while (pos++, read(fd, &instr, 1) > 0) {
			if (!no_w) {
				if (*instr == '>') ptr++;
				else if (*instr == '<') ptr--;
				else if (*instr == '+') (*ptr)++;
				else if (*instr == '-') (*ptr)--;
				else if (*instr == '.') write(1, ptr, 1);
				else if (*instr == ',') {
					write(1, ">", 1);
					read(1, input, 1);
					*ptr = *input;
				}
				else if (*instr == '[') {
					if ((*ptr) != 0) {
						i = 29999;
						while (i > 0 && ws[i] == -1) i--;
						if (i == 29999) {
							printf("1:An error occured while executing %s\n", argv[p]);
							break;
						}
						ws[i] = pos - 1;
					}
					else
						no_w = 1;
				}
				if (*instr == ']') {
					i = 29999;
					while (i >= 0 && ws[i] == -1) i--;
					if (i < 0) {
						printf("2:An error occured while executing %s\n", argv[p]);
						break;
					}
					if (lseek(fd, ws[i], SEEK_SET) == -1) {
						printf("3:An error occured while executing %s\n", argv[p]);
						perror(strerror(errno));
						break;
					}
					pos = ws[i];
					ws[i] = -1;
				}
			}
			else if (*instr == ']') no_w = 0;
		}
		close(fd);
		printf("\n-------\n");
	}
	return 0;
}
