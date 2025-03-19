def send_message(client_socket, message):
    try:
        # pos = message.split(' ')
        # if pos[0].lower() == "exit":
        #     pass
        # elif pos[0] == 'PLAY':
        #     row, col = pos[1], pos[2]
        client_socket.send(f"TICTACTOE {message}".encode())
        # else:
        #     print('ERROR Invalid input. Try again.')
    except:
        print('GOT ERROR WHEN SENDING A MESSAGE TO THE SERVER')
