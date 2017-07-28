#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main ()
{
	// Constants
	const char* vid_fifo = "video.fifo";
	//const char* data_fifo = "data.fifo";
	const int num_vid = 1;
	//const int num_data = 5;
	const int packet_length = 100;

	// Counter
	int i = 0;

	// Store what was read (1 byte at a time)
	unsigned char* inbuffer;

	// Open the fifos
	int vid_file;
	//int data_file;
	vid_file = open(vid_fifo, O_RDONLY);
	//data_file = open(data_fifo , O_RDONLY | O_NONBLOCK);

	//while (1)
	{
		for (i = 0; i < (num_vid * packet_length); i++)
		{
			read(vid_file, inbuffer, 1);
			fprintf(stdout, "%.*s", 6, inbuffer);
		}
	}

	return 1;
}