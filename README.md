# ts_mux
Basic Transport Stream Multiplexer

Reads data in from two named pipes (FIFOs), and multiplexes them together according to ratios defined in the code. Multiplexed data is written to STDOUT.

Usage:
	gcc stream_mux.c -o stream_mux
	./stream_mux > multiplexed.ts

	An example command that writes h264 video Transport Stream packets to the named pipe 'video.fifo':
	raspivid -n -t 0 -fps 25 -w 1280 -h 720 -pf high -b 1000000 -o - | ffmpeg -re -an -i - -vcodec copy -f mpegts -mpegts_flags system_b - > video.fifo

	An exmaple command that writes MPE data Transport Stream packets to the named pipe 'data.fifo'
	sudo mpe2sec dvb1 | sec2ts 430 -s > data.fifo