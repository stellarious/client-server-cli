import os
import sys
import socket
import pickle
import operator
from utils import StorageSystem, menu, clear

clear()

fieldnames = ('ID', 'Model', 'Sys. Cache', 'Max control.', 
	'Protocols.', 'Ports', 'Max disks', 'Price')

dbfilename = 'db.dat'

db = []

def check_db():
	if os.path.isfile(dbfilename):
		with open(dbfilename, 'rb') as f:
			data = f.read()
			db = pickle.loads(data)
		print('File was loaded.')

def save_db():
	with open(dbfilename, 'wb') as f:
		data = pickle.dumps(db)
		f.write(data)
	print('Data saved.')

#-------------------------------------------------------------
def header(func):
	def wrapped(arg):
		h = '\t'.join(fieldnames)
		return h + '\n' + func(arg)
	return wrapped
 
def add_record(args):
	new_record = StorageSystem(args)
	db.append(new_record)
	return '<<< OK'

def edit_record(args):
	if not db: return '<<< DB is empty'

	obj_id = args[0]
	field = args[1]
	new_value = args[2]

	for item in db:
		if item.id == obj_id:
			setattr(item, field, new_value)
		else:
			return '<<< No such record'


def delete_record(obj_id):
	if not db: return '<<< DB is empty' 

	for item in db:
		if item.id == obj_id:
			db.remove(item)
			return '<<< Record with id {} was deleted'.format(obj_id)
		else:
			return '<<< No such record'

@header
def search(args):
	if not db: return '<<< DB is empty'

	field = args[0]
	value = args[1]

	field_vals = list(map(operator.attrgetter(field), db))
	items_vals = list(zip(db, field_vals))
	items = [str(x[0]) for x in items_vals if x[1] == value]

	res = '\n'.join(items)
	return res

@header
def show_all(args):
	if not db: return '<<< DB is empty' 
	items = [str(x) for x in db]
	res = '\n'.join(items)
	return res

@header
def sort(args):
	if not db: return '<<< DB is empty' 

	sorted_items = list(sorted(db, key=operator.attrgetter(args)))
	items = [str(x) for x in sorted_items]
	res = '\n'.join(items)

	return res

#-------------------------------------------------------------

def get_info_from_client(data):
	cmd_num = data[0]
	cmd_args = data[1]

	print(menu[cmd_num], end=': ')
	print(cmd_args)
	
	options = {
		'1': add_record,
		'2': edit_record,
		'3': delete_record,
		'4': search,
		'5': show_all,
		'6': sort
	}
	return options[cmd_num](cmd_args)

def send(conn, data):
	bytes_data = pickle.dumps(data)
	conn.send(bytes_data)

def main():
	HOST = ''
	PORT = 1488

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # what

	try:
		sock.bind((HOST, PORT))
	except socket.error as msg:
		print(msg)
		sys.exit()

	print('Socket bind complete.')

	sock.listen(5)
	print ('Socket now listening on %s ...' % PORT)

	while True:
		conn, addr = sock.accept()
		
		print('Connected with {}:{}'.format(addr[0], addr[1]))

		check_db()

		while True:
			data = conn.recv(4096)
			if not data: break
			str_data = pickle.loads(data)
			result = get_info_from_client(str_data)
			send(conn, result)

		conn.close()
		print('{}:{} disonnected '.format(addr[0], addr[1]))
		save_db()

if __name__ == '__main__':
	main()
	