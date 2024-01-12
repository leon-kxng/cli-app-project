# server.py
import socketserver
import sys
import threading
from models import UserDatabase

USER_DB = UserDatabase()
CLIENTS = {}

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall("Enter your username: ".encode())
        username = self.request.recv(4096).decode().strip()

        while USER_DB.user_exists(username):
            self.request.sendall("Username already taken. Enter your password: ".encode())
            password = self.request.recv(4096).decode().strip()

            # Check if the entered password is correct
            if USER_DB.get_password(username) == password:
                self.request.sendall("Login successful. Welcome back!\n".encode())
                break
            else:
                self.request.sendall("Incorrect password. Enter your username: ".encode())
                username = self.request.recv(4096).decode().strip()

        # If the username does not exist, prompt to create a new password
        if not USER_DB.user_exists(username):
            self.request.sendall("Username available. Create your password: ".encode())
            password = self.request.recv(4096).decode().strip()
            USER_DB.insert_user(username, password)
            self.request.sendall("Account created successfully. Welcome!\n".encode())

        CLIENTS[username] = self.request

        welcome_msg = f"{username} joined.\n"
        sys.stdout.write(welcome_msg)
        sys.stdout.flush()

        for client in CLIENTS.values():
            if client is not self.request:
                client.sendall(welcome_msg.encode())

        while True:
            data = self.request.recv(4096)
            if data:
                data = data.decode()
                send_msg = f"{username}> {data}"
                sys.stdout.write(send_msg)
                sys.stdout.flush()

                USER_DB.insert_message(username, data)  # Store the message

                for client in CLIENTS.values():
                    if client is not self.request:
                        client.sendall(send_msg.encode())
            else:
                send_msg = f"{username} left.\n"
                sys.stdout.write(send_msg)
                sys.stdout.flush()

                del CLIENTS[username]

                for client in CLIENTS.values():
                    client.sendall(send_msg.encode())
                break

if __name__ == "__main__":
    HOST = ("localhost", 10000)

    server = ThreadedTCPServer(HOST, ThreadedTCPRequestHandler)
    server.daemon_threads = True

    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    sys.stdout.write("Server is up.\n")
    sys.stdout.flush()

    # Main execution will push
    while True:
        try:
            msg = sys.stdin.readline()
            msg = "Server> " + msg
            sys.stdout.write(msg)
            sys.stdout.flush()

            for client in CLIENTS.values():
                client.sendall(msg.encode())

        except KeyboardInterrupt:
            break

    USER_DB.close()
    server.shutdown()
    server.server_close()
    sys.stdout.write("Server is closed.\n")
    sys.stdout.flush()
