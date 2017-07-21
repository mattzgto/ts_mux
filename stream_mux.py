#!/usr/bin/python

# Matthew Zachary
# Rochester Institute of Technology
# Transport Stream Multiplexer
# Takes 1 video stream and muxes it with 1 data stream
# Data stream only muxed when data is available (non-blocking)
# Video stream muxed continuously (blocking)
# 6/6/17
# Graduate Research

from subprocess import Popen, PIPE
import sys
from Queue import Queue
from threading import Thread
import os
import signal

# Flag to shut things down
exitapp = False

# Number of packets to insert each loop
ts_packet_size = 188
num_data_packets = 3
num_video_packets = 1
#num_null_packets = 0
#insert_null_when_theres_no_data = False

# Commands that generate ts data to be muxed (must output to STDOUT)
data_cmd = "sudo mpe2sec dvb1 | sec2ts 430 -s"
video_cmd = "sudo raspivid -n -t 0 -fps 25 -w 1280 -h 720 -pf high -vf -hf -b 1000000 -o - | ffmpeg -re -an -i - -vcodec copy -b:v 1000000 -f mpegts -mpegts_flags system_b -muxrate 1500000 -"

# Null TS Packet
null_pkt = chr(0x47) + chr(0x1f) + chr(0xff) + chr(0x10) + chr(0x0)*184


# Spawner
def main(args):
	try:
		# Stores data received from the programs
		data_queue = Queue();
		video_queue = Queue();

		# Opens the data TS generation program
		data_process = Popen([data_cmd], shell=True, stdout=PIPE, preexec_fn=os.setsid) 
		data_thread = Thread(target=acquire_data, args=(data_queue, data_process))
		data_thread.daemon = True
		data_thread.start()

		# Opens the video TS generation program
		video_process = Popen([video_cmd], shell=True, stdout=PIPE, preexec_fn=os.setsid)
		video_thread = Thread(target=acquire_data, args=(video_queue, video_process))
		video_thread.daemon = True
		video_thread.start()

		# Loop for data infinitely
		while(1):
			# Look for (num_video_packets), wait until they are received
			for v in range(0, num_video_packets):
				sys.stdout.write(video_queue.get())
				
			# Look for (num_data_packets), don't wait if there are none
			for d in range(0, num_data_packets):
				if data_queue.empty() != True:
					sys.stdout.write(data_queue.get_nowait())
				# elif insert_null_when_theres_no_data == True:
				# 	muxed_pkt += null_pkt

			# Add null packets
			# null_counter = 0
			# while null_counter < num_null_packets:
			# 	muxed_pkt += null_pkt
			# 	null_counter = null_counter + 1

			# # Write to the stdout pipe
			# try:
			# 	sys.stdout.write(muxed_pkt)
			# 	#sys.stdout.flush()
			# # If this doesn't work, shut it down
			# except IOError as e:
			# 	# Ends the threads
			#     exitapp = True
			    
			#     # Ends the processes
			#     os.killpg(os.getpgid(video_process.pid), signal.SIGTERM)
			#     os.killpg(os.getpgid(data_process.pid), signal.SIGTERM)

			#     # Closes stdout
			#     try:
			#         sys.stdout.close()
			#     except IOError:
			#         pass
			#     try:
			#         sys.stderr.close()
			#     except IOError:
			#         pass

			#     return

	# If the user ends it
	except KeyboardInterrupt:
		# Ends the threads
		exitapp = True

		# Ends the processes
		os.killpg(os.getpgid(video_process.pid), signal.SIGTERM)
		os.killpg(os.getpgid(data_process.pid), signal.SIGTERM)

        raise

			
# Stores data received by programs into a Python Queue
def acquire_data(my_queue, my_process):
	# As long as we're not trying to exit
	while(exitapp != True):
		crt_pkt = my_process.stdout.read(ts_packet_size)
		my_queue.put(crt_pkt)

	# Kill the program when we're done
	os.killpg(os.getpgid(my_process.pid), signal.SIGTERM)
	return

# Default operation calls main
if __name__ == "__main__":
	args=[]

	main(args)
