# import socket
# import pickle

# HEADERSIZE=10

# s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(),1234))


# while True:
# 	full_msg=b''
# 	newmsg=True
# 	while True:
# 		msg=s.recv(16)
# 		if newmsg:
# 			print(f'new message length: {msg[:HEADERSIZE]}')
# 			msglen=int(msg[:HEADERSIZE])
# 			newmsg=False

# 		full_msg+=msg

# 		if len(full_msg)-HEADERSIZE==msglen:
# 			print('full msg received')
# 			print(full_msg[HEADERSIZE:])
# 			d=pickle.loads(full_msg[HEADERSIZE:])
# 			print(d)
# 			newmsg=True
# 			full_msg=b''
# 	print(full_msg)


import socket
import sys
import errno

HEADERLEN=10
IP='127.0.0.1'
PORT=1234

my_username=input("Username: ")
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username=my_username.encode("utf-8")
username_header=f"{len(username):<{HEADERLEN}}".encode("utf-8")
client_socket.send(username_header+username)

while True:
	message=input(f"{my_username} > ")

	if message:
		message=message.encode("utf-8")
		message_header=f"{len(message):<{HEADERLEN}}".encode("utf-8")
		client_socket.send(message_header + message)

	try:
		while True:
			#receiving things:
			username_header=client_socket.recv(HEADERLEN)
			if not username_header:
				print("connection closed by server")
				sys.exit()
			username_length=int(username_header.decode("utf-8"))
			username=client_socket.recv(username_length).decode("utf-8")
			message_header=client_socket.recv(HEADERLEN)
			message_len=int(message_header.decode("utf-8"))
			message=client_socket.recv(message_len).decode("utf-8")

			print(f"{username} > {message}")

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error',str(e))
			sys.exit()
		continue

	except Exception as e:
		print('General error',str(e))
		sys.exit()