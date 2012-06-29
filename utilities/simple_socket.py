import socket

class SimpleSocket:

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(
				socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.sock.connect((host, port))

	def send(self, msg):
		totalsent = 0
		while totalsent < len(msg) - 1:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def receive(self, msg_length):
		msg = ''
		while len(msg) < msg_length:
			chunk = self.sock.recv(msg_length - len(msg))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			msg = msg + chunk
		return msg

