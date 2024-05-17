#!/usr/bin/env python3
import socket
import selectors
import types
from datetime import datetime
from config.config import logging, HOST, PORT, SOCKET_VERSION


sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    fecha_hora_actual = datetime.now()
    logging.debug(f'{fecha_hora_actual} [SocketListener] accepted connection from {addr}', )
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            logging.debug('[SocketListener] closing connection to %s', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            logging.debug('[SocketListener] PACKET RECEIVED: %s --> %s', repr(data.outb), data.addr)
            # Format:
            # The Morpho response packet:
            # short answer:
            #   Access DENIED
            #       0x50 0x01 0x00 0xFF
            #   Access GRANTED
            #       0x50 0x01 0x00 0x00
            #   No Acction
            #       0x50 0x01 0x00 0xXX (any other value not 0x00 or 0xFF)
            data.outb = data.outb[0]


if __name__ == '__main__':
   
    #send_rmq.connect()

    """ send_rmq.connect()
 """
    l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    l_sock.bind((HOST, PORT))
    l_sock.listen()
    logging.debug('[SocketListener] listening on %s:%s (v:%s)', HOST, PORT, SOCKET_VERSION)
    l_sock.setblocking(False)
    sel.register(l_sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                try:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
                except:
                    logging.critical('[SocketListener] Filed to socket packet received', exc_info=True)
    except KeyboardInterrupt:
        logging.warning('[SocketListener] keyboard interrupt, exiting')
    finally:
        sel.close()
    logging.critical('[SocketListener] -- Process finished!')
