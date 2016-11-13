#! /opt/anaconda3/bin/python3

import os
import sys
import socket
import pickle
import signal
from utils import StorageSystem, menu, clear, getch

WIDTH = int(os.popen('stty size', 'r').read().split()[1])

HOST = '127.0.0.1'
PORT = 1488

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

fieldnames = (('Model', str), ('System cache', int), ('Max controllers', int), ('Protocols', str),
	('Port types', str), ('Max disks', int), ('Price', int))

attrnames = 'Hint: id, model, system_cache, max_controllers, protocols, port_types, max_disks, price'

def signal_handler(signal, frame):
        print('\nYou pressed Ctrl+C!')
        sys.exit(0)

def head(fn):
	def wrapper(arg):
		clear()
		print(menu[arg] + '\n' + '-' * WIDTH)
		return fn(arg)
	return wrapper

@head
def add_record(num):
	record_attr = []
	for field in fieldnames:
		while True:
			tmp = input('{}: '.format(field[0]))
			if not tmp:	continue
			try:
				field[1](tmp)
				break
			except:
				print('Wrong type.')
		record_attr.append(tmp)
	res = (num, record_attr)
	send(conn, res)

	input('Press Enter to return in main menu...')
	return res

@head
def edit_record(num):
	print(attrnames)

	rec_id = input('Enter object ID: ')
	try:
		int(rec_id)
	except:
		return
	
	field = input('Enter field name: ')
	if not field: 
		print('No data.')
		input()
		return
	if field == 'id':
		print('Cannot edit ID.')
		input()
		return
	val = input('Enter new value: ')
	if not val: 
		print('No data.')
		input()
		return
	
	res = (rec_id, field, val)
	data = (num, res)
	send(conn, data)

	input('Press Enter to return in main menu...')

@head
def delete_record(num):
	rec_id = input('Enter object ID to delete: ')
	data = (num, rec_id)
	send(conn, data)

	input('Press Enter to return in main menu...')

@head
def search(num):
	print(attrnames)
	field = input('Enter field name: ')
	val = input('Enter value: ')
	data = (num, (field, val))
	send(conn, data)
	input('Press Enter to return in main menu...')

@head
def show_all(num):
	data = (num, 0)
	send(conn, data)
	input('Press Enter to return in main menu...')

@head
def sort(num):
	print(attrnames)
	param = input('Sort by: ')
	data = (num, param)
	send(conn, data)

	input('Press Enter to return in main menu...')

def show_menu():	
	print('Лаб. раб. №1, Системы хранения данных Huawei')
	print('-' * WIDTH)

	for key in sorted(menu):
		print(key + ' - ' + menu[key])

def send(conn, data):
	bytes_data = pickle.dumps(data)
	conn.send(bytes_data)

	response = conn.recv(4096)
	str_data = pickle.loads(response)
	print(str_data)

def main():
	clear()

	try:
		conn.connect((HOST, PORT))
	except socket.error as msg:
		print(msg)
		print('Well, it looks like server is shut down.')
		input('Press Enter for quit...')
		clear()
		sys.exit()

	while True:
		clear()
		show_menu()
		answer = getch()
		
		if answer == 'q' : 
			clear()
			sys.exit()
		if answer in menu:
			options = {
				'1': add_record,
				'2': edit_record,
				'3': delete_record,
				'4': search,
				'5': show_all,
				'6': sort
			}
			options[answer](answer)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
