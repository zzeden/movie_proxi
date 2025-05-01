import socket

SERVER_PORT = 92
SERVER_ADDRESS = "54.71.128.194"
CLIENT_PORT = 9090

def error_fix(data):
    error = '#'
    error_index = data.index(error)
    new_data = 'ERROR' + data[error_index:]
    return new_data

#no results - 'ERROR#"No movie found"'
#crash -fff

def picture_fix(data: str):
    jpg = 'jpg'
    jpg_index = data.index(jpg)
    new_data = data[:jpg_index] + "." + data[jpg_index:]
    return new_data

def main():
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.connect((SERVER_ADDRESS, SERVER_PORT))

    sock_client = socket.socket()
    sock_client.bind(('', CLIENT_PORT))
    sock_client.listen(1)
    conn_client, addr_client = sock_client.accept()

    while True:
        data_from_client = conn_client.recv(1024)
        if not data_from_client:
            break
        sock_server.send(data_from_client)
        response_from_server = sock_server.recv(1024)
        response_from_server = response_from_server.decode()
        if response_from_server.index('ERROR') == 0 or response_from_server.index('ERROR') == 6:
            response_from_server = error_fix(response_from_server)
        else:
            response_from_server = picture_fix(response_from_server)
        response_from_server = response_from_server.encode()
        conn_client.send(response_from_server)

    conn_client.close()
    sock_server.close()

if __name__ == '__main__':
    main()