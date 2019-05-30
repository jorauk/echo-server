import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # Set an address for our server.
    address = ('127.0.0.1', 10000)
    
    # Instantiate a TCP socket with IPv4 Addressing.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
        socket.IPPROTO_TCP)
    
    # Socket setting to avoid 'port in use' error.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Log that we are building a server.
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind 'sock' to address above and begin to listen
    #   for incoming connections
    sock.bind(address)
    sock.listen(1)
    
    try:
        # The outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # Make a new socket when a client connects.
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # The inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # Receive 16 bytes of data from the client.
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    # Send the data you received back to the client.
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))
                    
                    # Check here to see whether you have received the end
                    # of the message. If you have, then break from the loop.
                    if len(data) < 16:
                        break
                    
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                #       Close the socket created above.
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        #       Close the server socket and exit from the server function.
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
