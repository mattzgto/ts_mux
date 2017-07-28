#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main ()
{
	// Constants
	const char* vid_fifo = "video.fifo";
	const char* data_fifo = "data.fifo";
	const int num_vid = 1;
	const int num_data = 5;
	const int packet_length = 188;

	// Counter
	int i = 0;
	int num_read = 0;

	// Store what was read (1 byte at a time)
	unsigned char* inbuffer[188];

	// Open the fifos
	int vid_file;
	int data_file;
	vid_file = open(vid_fifo, O_RDONLY);
	data_file = open(data_fifo , O_RDONLY | O_NONBLOCK);

	while (1)
	{
		// Read and output video packets (blocking)
		for (i = 0; i < num_vid; i++)
		{
			num_read = 0;
			while (num_read != packet_length)
			{
				num_read = read(vid_file, inbuffer, packet_length);
			}
			
			fprintf(stdout, "%.*s", packet_length, inbuffer);
			fflush(stdout);
		}

		// Read and output data packets (non-blocking)
		for (i = 0; i < num_data; i++)
		{
			num_read = read(data_file, inbuffer, packet_length);
			
			if (num_read == packet_length)
			{
				fprintf(stdout, "%.*s", packet_length, inbuffer);
				fflush(stdout);
			}
		}
	}

	return 1;
}