import dns.resolver
import socket
import threading

# Configuration
host = "0.0.0.0" # Generally just keep this on 0.0.0.0. I had some issues with 127.0.0.1 myself.
port = 2626 # If you change this, we (Ember Maintainer(s)), will not provide support about connectivity problems.

# The server socket gets created. We use TCP, because it's reliable.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen()

# Blacklists
blacklist_server = ["example.com"]
blacklist_user = ["example:example.com"]

# We grab the MX of the server and get the A that the MX is pointing to.
def resolve_dns(client):
	mx_records = dns.resolver.resolve(client, 'MX')

	mx = sorted(mx_records, key=lambda r: r.preference)[0]
	mx_host = mx.exchange.to_text().rstrip(".")

	a_record = dns.resolver.resolve(mx_host, 'A')

	for ip in a_record:
		return ip.to_text()

# Here we handle the client.
def listen_to_client(connection, address):
	message_accepted = "202 Accepted\n".encode()
	message_bad_sequence = "503 Bad Sequence\n".encode()
	message_request_denied = "550 Access Denied\n".encode()
	connection.sendall(message_accepted)

	# User specific varaibles.
	domain = ""
	from_user = ""
	to_user = ""

	while True:
		data = connection.recv(4096)
		if not data:
			break

		decoded_data = data.decode()

		if decoded_data.startswith("DOMAIN "):
			domain = decoded_data.removeprefix("DOMAIN ").strip()

			if domain in blacklist_server:
				connection.sendall(message_request_denied)
				break
			if address[0] != resolve_dns(domain):
				connection.sendall(message_request_denied)
				break

			connection.sendall(message_accepted)

		elif decoded_data.startswith("FROM "):
			user = decoded_data.removeprefix("FROM ")

			if not domain:
				connection.sendall(message_bad_sequence)
				break
			if user + ":" + domain in blacklist_user:
				connection.sendall(message_request_denied)
				break

			connection.sendall(message_accepted)

		elif decoded_data.startswith("TO "):
			to_user = decoded_data.removeprefix("TO ")

			connection.sendall(message_accepted)

		elif decoded_data.startswith("SUBJECT "):
			subject = decoded_data.removeprefix("SUBJECT ")

			connection.sendall(message_accepted)

		elif decoded_data.startswith("BODY "):
			body = decoded_data.removeprefix("BODY ")

			connection.sendall(message_accepted)

		elif decoded_data.strip().equals("BYE"):
			print("Email recieved!\n Subject: " + subject + "\nBody: " + body)

# Opens the socket so we can recieve mail/messages.
def open_socket():
	while True:
		connection, address = serverSocket.accept()
		thread = threading.Thread(target=listen_to_client, args=(connection, address))
		thread.start()

open_socket()
