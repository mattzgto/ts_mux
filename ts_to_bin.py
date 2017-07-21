#!/usr/bin/python

# Matthew Zachary
# Rochester Institute of Technology
# Converts a TS to Binary for transmission in BladeRF
# Reads from STDIN, outputs to STDOUT
# 6/28/17
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
packet_size = 4

def main(args):
	try:
		csv_string = ""
		read_pkt = ""

		# Loop for data infinitely
		while(1):
			# Read 4 bytes as a string
			read_pkt = sys.stdin.read(2)

			# Assemble and output string
			sys.stdout.write(read_pkt[0])
			sys.stdout.write(chr(0))
			sys.stdout.write(read_pkt[1])
			sys.stdout.write(chr(0))

	# If the user ends it
	except KeyboardInterrupt:
		# Ends the threads
		exitapp = True

        raise

# Default operation calls main
if __name__ == "__main__":
	args=[]

	main(args)
