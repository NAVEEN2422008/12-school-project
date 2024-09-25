import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, scrolledtext
import socket
import threading
import json
import os
import base64
from pathlib import Path
import time
import sys
import subprocess
from queue import Queue
import random

def install_required_modules():
    required_modules = ['tkinter', 'pillow']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_required_modules()

from PIL import Image, ImageTk

class FuturisticChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None
        self.file_to_send = None
        self.send_queue = Queue()
        
        self.received_files_folder = self.create_received_files_folder()
        
        self.root = tk.Tk()
        self.root.title("Futuristic Chat Client")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_gui()
        self.connect()
        threading.Thread(target=self.send_worker, daemon=True).start()

    def create_received_files_folder(self):
        home_dir = Path.home()
        received_files_folder = home_dir / 'received_files'
        received_files_folder.mkdir(parents=True, exist_ok=True)
        return received_files_folder


    def setup_gui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TButton", background="#3a3a3a", foreground="#ffffff", padding=10, font=('Arial', 10, 'bold'))
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=('Arial', 12))
        style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#ffffff", font=('Arial', 12))

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))

        self.chat_log = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, bg="#2a2a2a", fg="#ffffff", font=('Arial', 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_log.config(state=tk.DISABLED)

        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.users_frame = ttk.LabelFrame(right_frame, text="Online Users")
        self.users_frame.pack(fill=tk.BOTH, expand=True)

        self.users_listbox = tk.Listbox(self.users_frame, bg="#2a2a2a", fg="#ffffff", font=('Arial', 12))
        self.users_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        delete_button = ttk.Button(buttons_frame, text="Delete Message", command=self.delete_message)
        delete_button.pack(fill=tk.X, pady=5)

        self.send_file_button = ttk.Button(buttons_frame, text="Send File", command=self.initiate_file_send)
        self.send_file_button.pack(fill=tk.X, pady=5)

        self.share_file_button = ttk.Button(buttons_frame, text="Share with Selected", command=self.share_file_with_selected)
        self.share_file_button.pack(fill=tk.X, pady=5)
        self.share_file_button.config(state=tk.DISABLED)

        self.game_button = ttk.Button(buttons_frame, text="Play Game", command=self.open_game)
        self.game_button.pack(fill=tk.X, pady=5)

        self.refresh_button = ttk.Button(buttons_frame, text="Refresh", command=self.refresh_client)
        self.refresh_button.pack(fill=tk.X, pady=5)

    def connect(self):
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            self.username = simpledialog.askstring("Username", "Enter your username:", parent=self.root)
            if not self.username:
                self.root.quit()
                return

            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(30)
                print(f"Attempting to connect to {self.host}:{self.port}")
                
                self.client_socket.connect((self.host, self.port))
                
                login_data = {"type": "login", "username": self.username}
                self.send_data(login_data)
                response = self.receive_data()
                if response and response.get("type") == "login_response" and response.get("status") == "success":
                    print("Successfully connected to the server")
                    break
                else:
                    messagebox.showerror("Login Error", response.get("message", "Unknown error"), parent=self.root)
                    self.client_socket.close()
                    attempts += 1
            except Exception as e:
                messagebox.showerror("Connection Error", f"Could not connect to the server: {str(e)}", parent=self.root)
                attempts += 1

        if attempts == max_attempts:
            messagebox.showerror("Connection Failed", "Failed to connect after multiple attempts. Please try again later.", parent=self.root)
            self.root.quit()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()
        threading.Thread(target=self.send_heartbeat, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.receive_data()
                if data:
                    self.handle_incoming_message(data)
                else:
                    raise Exception("Connection lost")
            except Exception as e:
                print(f"Error receiving message: {str(e)}")
                self.update_chat_log("Lost connection to the server. Attempting to reconnect...")
                if not self.reconnect():
                    break

    def send_data(self, data):
        try:
            message = json.dumps(data).encode('utf-8')
            message_header = f"{len(message):<{10}}".encode('utf-8')
            self.client_socket.sendall(message_header + message)
        except socket.error as e:
            print(f"Socket error while sending data: {str(e)}")
            self.reconnect()

    def receive_data(self):
        try:
            message_header = self.client_socket.recv(10)
            if not message_header:
                return None
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')
            return json.loads(message)
        except socket.timeout:
            print("Connection timed out. Attempting to reconnect...")
            self.reconnect()
            return None
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error while receiving data: {str(e)}")
            self.reconnect()
            return None

    def handle_incoming_message(self, data):
        message_handlers = {
            'message': self.update_chat_log,
            'clear_chat': self.clear_chat,
            'delete_message': self.remove_message,
            'file_request': self.handle_file_request,
            'file_accepted': self.send_file_data,
            'file_rejected': self.handle_file_rejected,
            'file_data': self.receive_file_data,
            'user_list': self.update_user_list,
            'removed': self.handle_removed,
            'refresh_response': self.handle_refresh_response,
        }
        
        handler = message_handlers.get(data['type'])
        if handler:
            handler(data)
        else:
            print(f"Unknown message type: {data['type']}")

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message['content'] + '\n')
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)
        self.animate_message()

    def animate_message(self):
        colors = ['#3a3a3a', '#4a4a4a', '#5a5a5a', '#6a6a6a', '#7a7a7a']
        for color in colors + list(reversed(colors)):
            self.chat_log.config(bg=color)
            self.chat_log.update()
            time.sleep(0.05)
        self.chat_log.config(bg='#2a2a2a')

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            data = {'type': 'message', 'content': message}
            self.send_queue.put(data)
            self.message_entry.delete(0, tk.END)

    def send_worker(self):
        while True:
            data = self.send_queue.get()
            try:
                self.send_data(data)
            except Exception as e:
                print(f"Error sending data: {str(e)}")
                self.reconnect()
            self.send_queue.task_done()

    def delete_message(self):
        message_to_delete = simpledialog.askstring("Delete Message", "Enter the exact text of your message to delete:", parent=self.root)
        if message_to_delete:
            try:
                data = {'type': 'delete', 'content': message_to_delete}
                self.send_queue.put(data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete message: {str(e)}", parent=self.root)

    def remove_message(self, data):
        username, message = data['username'], data['content']
        self.chat_log.config(state=tk.NORMAL)
        start_index = "1.0"
        while True:
            start_index = self.chat_log.search(f"{username}: {message}", start_index, tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(username) + len(message) + 3}c"
            self.chat_log.delete(start_index, end_index)
        self.chat_log.config(state=tk.DISABLED)

    def clear_chat(self, data):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete(1.0, tk.END)
        self.chat_log.config(state=tk.DISABLED)

    def initiate_file_send(self):
        self.file_to_send = filedialog.askopenfilename(parent=self.root)
        if self.file_to_send:
            self.share_file_button.config(state=tk.NORMAL)
            messagebox.showinfo("File Selected", "File selected. Please choose recipients and click 'Share with Selected'.", parent=self.root)
        else:
            self.share_file_button.config(state=tk.DISABLED)

    def share_file_with_selected(self):
        if not self.file_to_send:
            messagebox.showerror("Error", "Please select a file first.", parent=self.root)
            return

        selected_indices = self.users_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one recipient.", parent=self.root)
            return

        recipients = [self.users_listbox.get(idx) for idx in selected_indices]
        if "All Users" in recipients:
            recipients = ["all"]

        file_name = os.path.basename(self.file_to_send)
        file_size = os.path.getsize(self.file_to_send)
        file_type = os.path.splitext(file_name)[1]

        for recipient in recipients:
            try:
                data = {
                    'type': 'file_request',
                    'filename': file_name,
                    'filesize': file_size,
                    'filetype': file_type,
                    'receiver': recipient,
                    'sender': self.username
                }
                self.send_queue.put(data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send file request to {recipient}: {str(e)}", parent=self.root)

        self.share_file_button.config(state=tk.DISABLED)
        messagebox.showinfo("File Sharing", f"File '{file_name}' is being shared with the selected recipient(s).", parent=self.root)

    def send_file_data(self, data):
        max_retries = 3
        retry_delay = 5
        for attempt in range(max_retries):
            try:
                with open(self.file_to_send, 'rb') as file:
                    file_data = file.read()
                    encoded_data = base64.b64encode(file_data).decode('utf-8')
                    data = {'type': 'file_data', 'filename': os.path.basename(self.file_to_send), 'data': encoded_data, 'receiver': data['receiver']}
                    self.send_queue.put(data)
                messagebox.showinfo("File Sent", f"File '{data['filename']}' has been sent successfully.", parent=self.root)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    self.update_chat_log({"content": f"File transfer failed. Retrying in {retry_delay} seconds..."})
                    time.sleep(retry_delay)
                else:
                    messagebox.showerror("Error", f"Failed to send file after {max_retries} attempts: {str(e)}", parent=self.root)

    def handle_file_request(self, data):
        print(f"Received file request for '{data['filename']}' from {data['sender']}")
        response = messagebox.askyesno("File Request", f"Accept file '{data['filename']}' from {data['sender']}?", parent=self.root)
        try:
            if response:
                print("User accepted the file.")
                self.send_queue.put({'type': 'file_accepted', 'sender': data['sender'], 'filename': data['filename']})
            else:
                print("User rejected the file.")
                self.send_queue.put({'type': 'file_rejected', 'sender': data['sender'], 'filename': data['filename']})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to respond to file request: {str(e)}", parent=self.root)

    def handle_file_rejected(self, data):
        messagebox.showinfo("File Rejected", f"Your file '{data['filename']}' was rejected by {data['receiver']}.", parent=self.root)

    def receive_file_data(self, data):
        print(f"Receiving file data for '{data['filename']}'")
        filename = data['filename']
        file_data = base64.b64decode(data['data'])
        
        save_path = self.received_files_folder / filename
        
        counter = 1
        while save_path.exists():
            name, ext = os.path.splitext(filename)
            save_path = self.received_files_folder / f"{name}_{counter}{ext}"
            counter += 1
        
        try:
            with open(save_path, 'wb') as file:
                file.write(file_data)
            self.update_chat_log({"content": f"File '{filename}' has been received and saved in the 'received_files' folder."})
            messagebox.showinfo("File Received", f"File '{filename}' has been saved in the 'received_files' folder.")
            
            # Open the file automatically
            if sys.platform == "win32":
                os.startfile(save_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", save_path])
            else:
                subprocess.call(["xdg-open", save_path])
        except Exception as e:
            self.update_chat_log({"content": f"Failed to save or open file: {str(e)}"})
            messagebox.showerror("File Error", f"Failed to save or open file: {str(e)}")

    def update_user_list(self, data):
        self.users_listbox.delete(0, tk.END)
        for user in data['users']:
            if user != self.username:
                self.users_listbox.insert(tk.END, user)
        self.users_listbox.insert(tk.END, "All Users")

    def handle_removed(self, data):
        messagebox.showinfo("Removed", data['content'], parent=self.root)
        self.root.quit()

    def reconnect(self):
        reconnect_delay = 5
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            try:
                self.client_socket.close()
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(30)
                self.client_socket.connect((self.host, self.port))
                login_data = {"type": "login", "username": self.username}
                self.send_data(login_data)
                response = self.receive_data()
                if response and response.get("type") == "login_response" and response.get("status") == "success":
                    self.update_chat_log({"content": "Reconnected to the server."})
                    return True
            except Exception as e:
                attempts += 1
                self.update_chat_log({"content": f"Reconnection attempt {attempts} failed. Retrying in {reconnect_delay} seconds..."})
                time.sleep(reconnect_delay)
                reconnect_delay *= 2  # Exponential backoff

        self.update_chat_log({"content": "Failed to reconnect after multiple attempts. Please restart the application."})
        return False

    def send_heartbeat(self):
        while True:
            time.sleep(15)  # Send heartbeat every 15 seconds
            try:
                self.send_queue.put({'type': 'heartbeat'})
            except:
                print("Failed to send heartbeat. Attempting to reconnect...")
                self.reconnect()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", parent=self.root):
            try:
                if self.client_socket:
                    self.send_queue.put({'type': 'logout'})
                    self.client_socket.close()
            except:
                pass
            self.root.destroy()

    def open_game(self):
        subprocess.Popen([sys.executable, "Project OG (3).py"])

    def refresh_client(self):
        try:
            # Disconnect from the server
            self.send_queue.put({'type': 'logout'})
            self.client_socket.close()
            
            # Reconnect to the server with the same username
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(30)
            self.client_socket.connect((self.host, self.port))
            
            login_data = {"type": "login", "username": self.username}
            self.send_data(login_data)
            response = self.receive_data()
            
            if response and response.get("type") == "login_response" and response.get("status") == "success":
                self.update_chat_log({"content": "Client refreshed and reconnected to the server."})
                threading.Thread(target=self.receive_messages, daemon=True).start()
            else:
                raise Exception("Failed to reconnect with the same username")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh and reconnect: {str(e)}", parent=self.root)

    def handle_refresh_response(self, data):
        self.update_chat_log({"content": "Client refreshed successfully."})
        if 'user_list' in data:
            self.update_user_list(data['user_list'])
        if 'chat_history' in data:
            self.update_chat_history(data['chat_history'])

    def update_chat_history(self, chat_history):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete(1.0, tk.END)
        for message in chat_history:
            self.chat_log.insert(tk.END, message + '\n')
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    install_required_modules()
    try:
        server_host = input("Enter server's public IP address: ")
        server_port = int(input("Enter server port: "))
        client = FuturisticChatClient(server_host, server_port)
        client.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to exit...")
