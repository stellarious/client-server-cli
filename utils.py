import os
import itertools

class StorageSystem:
	class_counter = itertools.count()

	def __init__(self, args):
		self.id = str(next(self.class_counter))
		self.model = args[0]
		self.system_cache = args[1]
		self.max_controllers = args[2]
		self.protocols = args[3]
		self.port_types = args[4]
		self.max_disks = args[5]
		self.price = args[6]

	#def __lt__(self, other):
	#	return int(self.price) < int(other.price)

	def __str__(self):
		attr = (self.id, self.model, self.system_cache, 
			self.max_controllers, self.protocols, self.port_types, 
			self.max_disks, self.price)
		return '\t'.join(attr)

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
