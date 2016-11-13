import os
import itertools
import tty, sys, termios

last_id = 0
if os.path.isfile('last_id'):
	with open('last_id', 'r') as f:
		global last_id
		last_id = int(f.read()) + 1

class StorageSystem:
	class_counter = itertools.count(last_id)

	def __init__(self, args):
		self.id = int(next(self.class_counter))
		self.model = args[0]
		self.system_cache = int(args[1])
		self.max_controllers = int(args[2])
		self.protocols = args[3]
		self.port_types = args[4]
		self.max_disks = int(args[5])
		self.price = int(args[6])

	#def __lt__(self, other):
	#	return int(self.price) < int(other.price)

	def __str__(self):
		attr = (str(self.id), self.model, str(self.system_cache), 
			str(self.max_controllers), self.protocols, self.port_types, 
			str(self.max_disks), str(self.price))
		return '\t\t'.join(attr)

menu = {
	'1': 'Add new record',
	'2': 'Edit record',
	'3': 'Delete record',
	'4': 'Search model',
	'5': 'Show all',
	'6': 'Sort',
	'q': 'For quit'
}

clear = lambda: os.system('clear')

def getch():
	fd = sys.stdin.fileno()
	oldSettings = termios.tcgetattr(fd)

	try:
		tty.setraw(fd)
		answer = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

	return answer
