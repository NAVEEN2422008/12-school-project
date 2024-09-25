import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import socket
import threading
import json
import time
import sys
import logging
from typing import Dict, List, Any, Optional
import requests
import subprocess
import asyncio
def install_required_modules():
    required_modules = ['tkinter', 'requests', 'asyncio']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

class FuturisticChatServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 5000):
        self.host: str = host
        self.port: int = port
        self.clients: Dict[str, socket.socket] = {}
        self.file_requests: List[Dict[str, Any]] = []
        self.server_socket: Optional[socket.socket] = None
        self.is_running: bool = False
        self.banned_users: List[str] = []

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger: logging.Logger = logging.getLogger(__name__)

        self.root: tk.Tk = tk.Tk()
        self.root.title("Futuristic Chat Server")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_gui()
        self.start_server()
        self.root.after(60000, self.clean_inactive_connections)

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TButton", background="#3a3a3a", foreground="#ffffff", padding=10, font=('Arial', 10, 'bold'))
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=('Arial', 12))
        style.configure("TLabelframe", background="#1e1e1e", foreground="#ffffff", font=('Arial', 12))
        style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#ffffff", font=('Arial', 12, 'bold'))

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.users_frame = ttk.LabelFrame(self.left_frame, text="Connected Users")
        self.users_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.users_listbox = tk.Listbox(self.users_frame, bg="#2a2a2a", fg="#ffffff", font=('Arial', 12))
        self.users_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.buttons_frame = ttk.Frame(self.left_frame)
        self.buttons_frame.pack(padx=5, pady=5, fill=tk.X)

        self.remove_button = ttk.Button(self.buttons_frame, text="Remove User", command=self.remove_selected_user)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.ban_button = ttk.Button(self.buttons_frame, text="Ban User", command=self.ban_selected_user)
        self.ban_button.pack(side=tk.LEFT, padx=5)

        self.unban_button = ttk.Button(self.buttons_frame, text="Unban User", command=self.unban_user)
        self.unban_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.buttons_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.request_button = ttk.Button(self.buttons_frame, text="File Requests", command=self.show_requests)
        self.request_button.pack(side=tk.LEFT, padx=5)

        self.chat_log_frame = ttk.LabelFrame(self.right_frame, text="Server Log")
        self.chat_log_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.chat_log = scrolledtext.ScrolledText(self.chat_log_frame, wrap=tk.WORD, bg="#2a2a2a", fg="#ffffff", font=('Arial', 12))
        self.chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.status_frame = ttk.LabelFrame(self.right_frame, text="Server Status")
        self.status_frame.pack(padx=5, pady=5, fill=tk.X)

        self.status_label = ttk.Label(self.status_frame, text="Server is starting...")
        self.status_label.pack(padx=5, pady=5)

    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except:
            return socket.gethostbyname(socket.gethostname())

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            public_ip = self.get_public_ip()
            local_ip = socket.gethostbyname(socket.gethostname())
            self.update_status(f"Server is running on Public IP: {public_ip}, Local IP: {local_ip}, Port: {self.port}")
            self.log_message(f"Server started on Public IP: {public_ip}, Local IP: {local_ip}, Port: {self.port}")
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            self.log_message(f"Error starting server: {str(e)}")
            self.update_status("Server failed to start")

    def accept_connections(self):
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True).start()
            except Exception as e:
                if self.is_running:
                    self.log_message(f"Error accepting connection: {str(e)}")

    def handle_client(self, client_socket: socket.socket, address: tuple):
        username = None
        last_activity = time.time()
        try:
            login_data = self.receive_message(client_socket)
            if login_data and login_data['type'] == 'login':
                username = login_data['username']
                if username in self.banned_users:
                    self.send_message(client_socket, json.dumps({
                        "type": "login_response",
                        "status": "error",
                        "message": "You are banned from this server."
                    }))
                    client_socket.close()
                    return
                if username in self.clients:
                    self.send_message(client_socket, json.dumps({
                        "type": "login_response",
                        "status": "error",
                        "message": "Username already taken."
                    }))
                    client_socket.close()
                    return
                self.clients[username] = client_socket
                self.send_message(client_socket, json.dumps({
                    "type": "login_response",
                    "status": "success",
                    "message": "Login successful."
                }))
                self.update_users_list()
                self.broadcast_user_list()
                self.broadcast(json.dumps({
                    'type': 'message',
                    'content': f"SERVER: {username} has joined the chat."
                }))
                self.log_message(f"{username} connected from {address}")

            last_activity = time.time()
            while True:
                data = self.receive_message(client_socket)
                if not data:
                    break
                last_activity = time.time()
                if username is not None and isinstance(username, str):
                    self.process_message(username, data)

        except Exception as e:
            self.log_message(f"Error handling client {username}: {str(e)}")
        finally:
            if username:
                self.handle_client_disconnect(username)

    def process_message(self, username: str, message: Dict[str, Any]):
        message_type = message.get('type')
        if message_type == 'message':
            self.broadcast(json.dumps({
                'type': 'message',
                'content': f"{username}: {message['content']}"
            }))
        elif message_type == 'delete':
            self.delete_message(username, message['content'])
        elif message_type == 'file_request':
            self.handle_file_request(username, message)
        elif message_type in ['file_accepted', 'file_rejected']:
            self.handle_file_response(username, message)
        elif message_type == 'file_data':
            asyncio.run(self.handle_file_data(username, message))
        elif message_type == 'heartbeat':
            pass
        else:
            self.log_message(f"Unknown message type from {username}: {message_type}")

    def broadcast(self, message: str):
        disconnected_clients = []
        for username, client in self.clients.items():
            try:
                self.send_message(client, message)
            except:
                disconnected_clients.append(username)
        
        for username in disconnected_clients:
            self.handle_client_disconnect(username)

    def broadcast_user_list(self):
        user_list = list(self.clients.keys())
        self.broadcast(json.dumps({'type': 'user_list', 'users': user_list}))

    def remove_selected_user(self):
        selected = self.users_listbox.curselection()
        if selected:
            username = self.users_listbox.get(selected[0])
            self.remove_user(username)

    def remove_user(self, username: str):
        if username in self.clients:
            client = self.clients[username]
            try:
                self.send_message(client, json.dumps({
                    'type': 'removed',
                    'content': 'You have been removed by the server.'
                }))
            except:
                pass
            self.handle_client_disconnect(username)
            self.log_message(f"User {username} has been removed by the server.")
            self.broadcast(json.dumps({
                'type': 'message',
                'content': f"SERVER: {username} has been removed from the chat."
            }))

    def ban_selected_user(self):
        selected = self.users_listbox.curselection()
        if selected:
            username = self.users_listbox.get(selected[0])
            self.ban_user(username)

    def ban_user(self, username: str):
        if username in self.clients:
            self.remove_user(username)
        if username not in self.banned_users:
            self.banned_users.append(username)
            self.log_message(f"User {username} has been banned.")
            self.broadcast(json.dumps({
                'type': 'message',
                'content': f"SERVER: {username} has been banned from the chat."
            }))

    def unban_user(self):
        username = simpledialog.askstring("Unban User", "Enter the username to unban:", parent=self.root)
        if username and username in self.banned_users:
            self.banned_users.remove(username)
            self.log_message(f"User {username} has been unbanned.")
            self.broadcast(json.dumps({
                'type': 'message',
                'content': f"SERVER: {username} has been unbanned."
            }))
        elif username:
            messagebox.showinfo("Unban User", f"User {username} is not banned.", parent=self.root)

    def handle_client_disconnect(self, username: str):
        if username in self.clients:
            self.clients[username].close()
            del self.clients[username]
            self.update_users_list()
            self.broadcast_user_list()
            self.broadcast(json.dumps({
                'type': 'message',
                'content': f"SERVER: {username} has disconnected."
            }))
            self.log_message(f"{username} disconnected")

    def clear_chat(self):
        self.broadcast(json.dumps({
            'type': 'clear_chat',
            'content': 'Chat has been cleared by the server.'
        }))
        self.log_message("Chat cleared by server")

    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for username in self.clients.keys():
            self.users_listbox.insert(tk.END, username)

    def delete_message(self, username: str, message: str):
        delete_command = json.dumps({
            'type': 'delete_message',
            'username': username,
            'content': message
        })
        self.broadcast(delete_command)
        self.log_message(f"Message deleted by {username}: {message}")

    def handle_file_request(self, sender: str, data: Dict[str, Any]):
        request = {
            'sender': sender,
            'receiver': data['receiver'],
            'filename': data['filename'],
            'filesize': data['filesize'],
            'filetype': data['filetype']
        }
        self.file_requests.append(request)
        self.log_message(f"File request from {sender} to {data['receiver']}: {data['filename']}")
        self.handle_approved_file_request(request)

    def handle_approved_file_request(self, request: Dict[str, Any]):
        sender = request['sender']
        receiver = request['receiver']
        filename = request['filename']

        if receiver == 'all':
            for username, client in self.clients.items():
                if username != sender:
                    self.send_message(client, json.dumps({
                        'type': 'file_request',
                        'sender': sender,
                        'filename': filename,
                        'filesize': request['filesize'],
                        'filetype': request['filetype']
                    }))
        elif receiver in self.clients:
            self.send_message(self.clients[receiver], json.dumps({
                'type': 'file_request',
                'sender': sender,
                'filename': filename,
                'filesize': request['filesize'],
                'filetype': request['filetype']
            }))
        self.log_message(f"File request approved: {filename} (from {sender} to {receiver})")

    def handle_file_response(self, responder: str, data: Dict[str, Any]):
        for request in self.file_requests:
            if request['sender'] == data['sender'] and request['filename'] == data['filename']:
                if data['type'] == 'file_accepted':
                    self.send_message(self.clients[data['sender']], json.dumps({
                        'type': 'file_accepted',
                        'receiver': responder,
                        'filename': request['filename']
                    }))
                    self.log_message(f"File request accepted: {data['filename']} (from {data['sender']} to {responder})")
                else:
                    self.send_message(self.clients[data['sender']], json.dumps({
                        'type': 'file_rejected',
                        'receiver': responder,
                        'filename': request['filename']
                    }))
                    self.log_message(f"File request rejected: {data['filename']} (from {data['sender']} to {responder})")
                self.file_requests.remove(request)
                break

    async def handle_file_data(self, sender: str, data: Dict[str, Any]):
        try:
            filename = data['filename']
            file_data = data['data']
            receiver = data.get('receiver', 'all')

            if receiver == 'all':
                tasks = []
                for username, client in self.clients.items():
                    if username != sender:
                        tasks.append(self.send_file_to_client(client, sender, filename, file_data))
                await asyncio.gather(*tasks)
            elif receiver in self.clients:
                await self.send_file_to_client(self.clients[receiver], sender, filename, file_data)
            else:
                self.log_message(f"File transfer failed: Receiver {receiver} not found")
                await self.send_message_async(self.clients[sender], json.dumps({
                    'type': 'file_transfer_failed',
                    'filename': filename,
                    'receiver': receiver,
                    'reason': 'Receiver not found'
                }))
        except Exception as e:
            self.log_message(f"Error handling file data: {str(e)}")
            await self.send_message_async(self.clients[sender], json.dumps({
                'type': 'file_transfer_failed',
                'filename': filename,
                'reason': str(e)
            }))

    async def send_file_to_client(self, client, sender, filename, file_data):
        try:
            await self.send_message_async(client, json.dumps({
                'type': 'file_data',
                'sender': sender,
                'filename': filename,
                'data': file_data
            }))
        except Exception as e:
            self.log_message(f"Failed to send file to {client}. Error: {str(e)}")

    def show_requests(self):
        if not self.file_requests:
            messagebox.showinfo("File Requests", "No pending file requests.")
            return

        request_window = tk.Toplevel(self.root)
        request_window.title("File Requests")
        request_window.geometry("400x300")
        request_window.configure(bg="#1e1e1e")

        request_listbox = tk.Listbox(request_window, width=50, bg="#2a2a2a", fg="#ffffff", font=('Arial', 12))
        request_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for request in self.file_requests:
            request_listbox.insert(tk.END, f"{request['sender']} -> {request['receiver']}: {request['filename']}")

        def on_double_click(event):
            selection = request_listbox.curselection()
            if selection:
                index = selection[0]
                request = self.file_requests[index]
                details = f"Sender: {request['sender']}\n"
                details += f"Receiver: {request['receiver']}\n"
                details += f"Filename: {request['filename']}\n"
                details += f"File size: {request['filesize']} bytes\n"
                details += f"File type: {request['filetype']}"
                messagebox.showinfo("File Request Details", details)

        request_listbox.bind('<Double-1>', on_double_click)

    def log_message(self, message: str):
        self.logger.info(message)
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def update_status(self, message: str):
        self.status_label.config(text=message)

    def send_message(self, client_socket: socket.socket, message: str):
        try:
            message_bytes = message.encode('utf-8')
            message_header = f"{len(message_bytes):<{10}}".encode('utf-8')
            client_socket.send(message_header + message_bytes)
        except Exception as e:
            self.log_message(f"Error sending message: {str(e)}")
            raise

    async def send_message_async(self, client_socket: socket.socket, message: str):
        try:
            message_bytes = message.encode('utf-8')
            message_header = f"{len(message_bytes):<{10}}".encode('utf-8')
            await asyncio.get_event_loop().sock_sendall(client_socket, message_header + message_bytes)
        except Exception as e:
            self.log_message(f"Error sending message asynchronously: {str(e)}")
            raise

    def receive_message(self, client_socket: socket.socket) -> Optional[Dict[str, Any]]:
        try:
            message_header = client_socket.recv(10)
            if not message_header:
                return None
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            return json.loads(message)
        except Exception as e:
            self.log_message(f"Error receiving message: {str(e)}")
            return None

    def clean_inactive_connections(self):
        inactive_users = []
        current_time = time.time()
        for username, client in self.clients.items():
            if current_time - client.last_activity > 300:  # 5 minutes
                inactive_users.append(username)
        
        for username in inactive_users:
            self.handle_client_disconnect(username)
            self.log_message(f"Removed inactive user: {username}")

        self.root.after(60000, self.clean_inactive_connections)  # Run every minute

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.is_running = False
            for client in self.clients.values():
                try:
                    client.close()
                except:
                    pass
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            self.root.destroy()
            sys.exit(0)

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {str(e)}")
        finally:
            self.on_closing()

if __name__ == "__main__":
    install_required_modules()
    server = FuturisticChatServer()
    server.run()
