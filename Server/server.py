import socket
import threading
import queue
from collections import defaultdict

# Server Configuration
HOST = '0.0.0.0'
PORT = 5555

# Dictionary to store rooms, players, and game state
rooms = defaultdict(lambda: {'Game': None, 'Players': [], 'size': 0, 'full': False})
clients = {}
lock = threading.Lock()
roomID = 0
message_queue = queue.Queue()


def get_room_size(game_name):
    return 2 if game_name == 'TICTACTOE' else 0


def handle_menu_messages(client_socket, messages):
    global roomID
    if not messages:
        client_socket.send("ERROR Invalid menu command.".encode())
        return
    OPCODE = messages[0]

    if OPCODE == 'CREATE':
        if len(messages) < 2:
            client_socket.send("ERROR Invalid CREATE format.".encode())
            return
        with lock:
            roomID += 1
            rooms[roomID] = {'Game': messages[1], 'Players': [client_socket], 'size': get_room_size(messages[1]),
                             'full': False}
            clients[client_socket] = roomID
        client_socket.send(f"CREATE {messages[1]} {roomID}".encode())

    elif OPCODE == 'JOIN':
        if len(messages) < 2 or not messages[1].isdigit():
            client_socket.send("ERROR Invalid room ID.".encode())
            return
        room_id = int(messages[1])
        with lock:
            if room_id not in rooms or rooms[room_id]['full']:
                client_socket.send("ERROR Room is full or does not exist.".encode())
                return
            rooms[room_id]['Players'].append(client_socket)
            clients[client_socket] = room_id
            if len(rooms[room_id]['Players']) == rooms[room_id]['size']:
                rooms[room_id]['full'] = True
        client_socket.send(f"JOIN {rooms[room_id]['Game']} {room_id}".encode())


def handle_tictactoe_messages(client_socket, messages):
    if not messages:
        client_socket.send("ERROR Invalid TICTACTOE command.".encode())
        return
    OPCODE = messages[0]

    if OPCODE == 'PLAY':
        if len(messages) < 3:
            client_socket.send("ERROR Invalid move format.".encode())
            return
        if client_socket not in clients:
            client_socket.send("ERROR You must login first.".encode())
            return
        room_id = clients[client_socket]
        if room_id not in rooms or not rooms[room_id]['full']:
            client_socket.send("ERROR Wait for another player to join.".encode())
            return
        try:
            row, col = int(messages[1]), int(messages[2])
            broadcast(room_id, f'PLAY {row} {col}')
        except ValueError:
            client_socket.send("ERROR Invalid input.".encode())
    elif OPCODE == 'LEAVE':
        if client_socket not in clients:
            client_socket.send("ERROR You must login first.".encode())
            return
        room_id = clients.pop(client_socket, None)
        if room_id and room_id in rooms:
            with lock:
                rooms[room_id]['Players'].remove(client_socket)
            broadcast(room_id, "LEAVE")
        if len(rooms[room_id]['Players']) == 0:
            del rooms[room_id]


def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                continue
            words = message.split()
            if not words:
                continue
            if words[0] == 'MENU':
                handle_menu_messages(client_socket, words[1:])
            elif words[0] == 'TICTACTOE':
                handle_tictactoe_messages(client_socket, words[1:])
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        client_socket.close()


def broadcast(room_id, message):
    if room_id in rooms:
        for sock in rooms[room_id]['Players']:
            message_queue.put((sock, message))


def message_worker():
    while True:
        sock, message = message_queue.get()
        try:
            sock.send(message.encode())
        except:
            pass
        message_queue.task_done()


threading.Thread(target=message_worker, daemon=True).start()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'Server listening on {HOST}:{PORT}')
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


if __name__ == '__main__':
    start_server()
