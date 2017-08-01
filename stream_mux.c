// Matthew Zachary
// Rochester Institute of Technology
// Transport Stream Multiplexer
// Takes 1 video stream and muxes it with 1 data stream
// Data stream only muxed when data is available (non-blocking)
// Video stream muxed continuously (blocking)
// 7/28/17
// Graduate Research

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main ()
{
	// Constants
	const char* vid_fifo = "video.fifo";
	const char* data_fifo = "data.fifo";
	const int num_vid = 2;
	const int num_data = 5;
	const int ts_frame_pkt_length = 188;

	// Counters
	volatile int i = 0;
	volatile int j = 0;
	volatile int num_read  = 0;
	volatile int num_to_read = ts_frame_pkt_length;

	// Store what was read (1 byte at a time)
	unsigned char videobuffer[ts_frame_pkt_length];
	unsigned char databuffer[ts_frame_pkt_length];
	
	// Open the fifos
	int vid_file;
	int data_file;
	vid_file = open(vid_fifo, O_RDONLY);
	data_file = open(data_fifo, O_RDONLY | O_NONBLOCK);

	while (1)
	{
		// Read and output video packets (blocking)
		for (i = 0; i < num_vid; i++)
		{
			// Read in 188 bytes
			num_read = 0;
			while (num_read != ts_frame_pkt_length)
			{
				num_read = read(vid_file, videobuffer, ts_frame_pkt_length);
			}

			// Print these out
			for (j = 0; j < ts_frame_pkt_length; j++)
			{
				printf("%c", videobuffer[j]);
			}
		}

		// Flush STDOUT
		fflush(stdout);

		// Read and output data packets (non-blocking)
		for (i = 0; i < num_data; i++)
		{
			// Read in 188 bytes (ideally)
			num_read = read(data_file, &databuffer[ts_frame_pkt_length - num_to_read], num_to_read);

			// Received a full packet
			if (num_read == num_to_read)
			{
				// Print these out
				for (j = 0; j < ts_frame_pkt_length; j++)
				{
					printf("%c", databuffer[j]);
				}

				// Reset
				num_to_read = ts_frame_pkt_length;
			}
			// Received a partial packet
			else if (num_read > 0) // not -1 or 0
			{
				// Only read in some next time
				num_to_read -= num_read;
			}
		}

		// Flush STDOUT
		fflush(stdout);
	}

	return 1;
}