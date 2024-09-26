# 12-School-Project

A school project pairing a futures-themed chat client/server with a bundled tkinter game suite.

## Features
- TCP chat server with full user management (list, remove, ban, unban, clear chat)
- Threaded multi-client handling with heartbeats, inactivity cleanup, and auto-reconnect
- Client GUI with chat log, online-user list, and per-user / all-user messaging
- End-to-end file sharing: file requests, accept/reject, base64 transfer, auto-save to `received_files/`
- Length-prefixed JSON message protocol over sockets; async file forwarding (aiofiles/asyncio)
- "Play Game" launcher opens a bundled tkinter game collection (Hangman, TicTacToe, Drawing Game)

## Tech Stack
- Python 3, `tkinter`/`ttk`, `socket`, `threading`, `asyncio`/`aiofiles`, `requests`, `Pillow`
- JSON message protocol

## Project Structure
```
chat-server .py         # FuturisticChatServer — socket + GUI, ban/remove, file routing
chat-client.py          # FuturisticChatClient — GUI, messaging, file sharing, reconnect
Project OG.py           # tkinter mini-games (Hangman, TicTacToe, Drawing) launched from client
```

## Installation
```
pip install requests aiofiles pillow
```
(The `install_required_modules()` helper auto-installs missing modules.)

## Usage
1. Start the server: `python "chat-server .py"` (binds 0.0.0.0:5000).
2. Launch clients: `python chat-client.py`, enter the server's public IP and port, then a username.

Both endpoints are run on machines on the same network; the server prompts for a login dialog as clients connect.