import os

class StorageSystem:
	class_counter = 0

	def __init__(self, args):
		self.obj_id = StorageSystem.class_counter
		self.model = args[0]
		self.system_cache = args[1]
		self.max_controllers = args[2]
		self.protocols = args[3]
		self.port_types = args[4]
		self.max_disks = args[5]
		StorageSystem.class_counter =+ 1

	def __str__(self):
		attr = (self.model, self.system_cache, self.max_controllers, self.protocols, self.port_types, self.max_disks)
		return '\t\t'.join(attr)

menu = {
	'1': 'Add new record',
	'2': 'Edit record',
	'3': 'Delete record',
	'4': 'Search model',
	'5': 'Show all',
	'6': 'Sort by price',
	'q': 'For quit'
}

clear = lambda: os.system('clear')
