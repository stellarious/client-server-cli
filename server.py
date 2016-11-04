import os
import sys
import socket
import pickle
from storage import StorageSystem, menu, clear
from io import StringIO

clear()

fieldnames = ('Model', 'Sys. Cache', 'Max control.', 'Protocols.', 'Ports', 'Max disks')

db = []

#-------------------------------------------------------------
def header(func):
	def wrapped(arg):
		h = '\t'.join(fieldnames)
		return h + '\n' + func(arg)
	return wrapped
 
def add_record(args):
	# проверить есть ли файл бд, открыть его и добавить в конец
	new_record = StorageSystem(args)
	db.append(new_record)
	return 'OK'

def edit_record(args):
	pass

def delete_record(args):
	return 'delete!@!!!!!!!!!'

def search(args):
	pass

@header
def show_all(args):
	if db:
		items = [str(x) for x in db]
		res = '\n'.join(items)
	else:
		res = 'Nothing to show.'
	return res

@header
def sort(args):
	pass

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

		while True:
			data = conn.recv(4096)
			if not data: break
			str_data = pickle.loads(data)
			result = get_info_from_client(str_data)
			send(conn, result)

		conn.close()
		print('{}:{} disonnected '.format(addr[0], addr[1]))

if __name__ == '__main__':
	main()