#! /opt/anaconda3/bin/python3

import os
import sys
import socket
import pickle
import operator
import signal
from utils import StorageSystem, menu, clear

clear()

fieldnames = ('ID', '\tModel', '\tSys. Cache', 'Max control.', 
	'Protocols.', 'Ports', '\tMax disks', 'Price')

dbfilename = 'db.dat'

def signal_handler(signal, frame):
	save_db()
	print('Bye!')
	sys.exit(0)

def open_db():
	if os.path.isfile(dbfilename):
		with open(dbfilename, 'rb') as f:
			data = f.read()
			db = pickle.loads(data)
			print('File was loaded.')
			return db
	else:
		return []

def save_db():
	with open(dbfilename, 'wb') as f:
		data = pickle.dumps(db)
		f.write(data)
		print('Data saved.')

	if db:
		with open('last_id', 'w') as tf:
			tf.write(str(db[-1].id))

#-------------------------------------------------------------
def check_data(args):
	try:
		str(args[0]) # model
		int(args[1]) # cache
		int(args[2]) # contollers
		str(args[3]) # protocols
		str(args[4]) # ports
		int(args[5]) # disks
		int(args[6]) # price
	except:
		return False
	return True

def header(func):
	def wrapped(arg):
		h = '\t'.join(fieldnames)
		return h + '\n' + func(arg)
	return wrapped
 
def add_record(args):
	if check_data(args):
		new_record = StorageSystem(args)
		db.append(new_record)
		return '<<< OK'
	else:
		return '<<< Bad data'

def edit_record(args):
	if not db: return '<<< DB is empty'

	try:
		obj_id = int(args[0])
	except:
		return '<<< Wrong param'

	field = args[1]
	new_value = args[2]

	for item in db:
		if item.id == obj_id:
			try:
				setattr(item, field, new_value)
				return '<<< OK'
			except:
				return '<<< Bad data'
	return '<<< No such record'


def delete_record(obj_id):
	if not db: return '<<< DB is empty' 

	try:
		obj_id = int(obj_id)
	except:
		return '<<< Wrong param'

	for item in db:
		if item.id == obj_id:
			db.remove(item)
			return '<<< Record with id {} was deleted'.format(obj_id)
	return '<<< No such record'

@header
def search(args):
	if not db: return '<<< DB is empty'

	field, value = args

	try:
		value = int(value)
	except:
		pass

	try:
		field_vals = list(map(operator.attrgetter(field), db))
		items_vals = list(zip(db, field_vals))
		items = [str(x[0]) for x in items_vals if x[1] == value]

		res = '\n'.join(items)
		return res
	except:
		return '<<< Bad params'

@header
def show_all(args):
	if not db: return '<<< DB is empty' 
	items = [str(x) for x in db]
	res = '\n'.join(items)
	return res

@header
def sort(arg):
	if not db: return '<<< DB is empty' 
	try:
		sorted_items = list(sorted(db, key=operator.attrgetter(arg)))
		items = [str(x) for x in sorted_items]
		res = '\n'.join(items)
		return res
	except:
		return '<<< Wrong key'

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

	global db
	db = open_db()

	while True:
		conn, addr = sock.accept()
		
		print('Connected with {}:{}'.format(addr[0], addr[1]))		

		while True:
			data = conn.recv(4096)
			if not data: break
			str_data = pickle.loads(data)
			result = get_info_from_client(str_data)
			send(conn, result)

		conn.close()
		print('{}:{} disonnected '.format(addr[0], addr[1]))

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
	