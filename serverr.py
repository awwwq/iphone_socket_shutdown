# -*- coding: UTF-8 -*-

import socket,os
import base64,hashlib


HOST = '192.168.1.100'
PORT = 5000
MAGIC_STRING = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: {1}\r\n" \
                   "WebSocket-Location: ws://{2}/chat\r\n" \
                   "WebSocket-Protocol:chat\r\n\r\n"


def handshake(con):
    # con为用socket，accept()得到的socket
    # 这里省略监听，accept的代码,具体可见blog：http://blog.csdn.net/ice110956/article/details/29830627
    headers = {}
    shake = con.recv(1024)

    if not len(shake):
        return False

    header, data = shake.split(bytes('\r\n\r\n'.encode('utf-8')), 1)
    for line in header.split(bytes('\r\n'.encode('utf-8')))[1:]:
        #print(line.decode('utf-8'))
        key, val = line.decode('utf-8').split(': ', 1)
        headers[key] = val

    if 'Sec-WebSocket-Key' not in headers:
        print('This socket is not websocket, client close.')
        con.close()
        return False

    sec_key = headers['Sec-WebSocket-Key'].encode('utf-8')
    #print(sec_key)
    res_key = base64.b64encode(hashlib.sha1(sec_key + MAGIC_STRING).digest())
    res_key = res_key.decode('utf-8')

    str_handshake = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}', HOST + ':' + str(PORT))
    str_handshake = str_handshake.encode('utf-8')
    #print(str_handshake)
    con.send(str_handshake)
    return True

def recv_data(con, num):
    try:
        all_data = con.recv(num)
        #print(all_data)
        if not len(all_data):
            return False
    except:
        return False
    else:
        code_len = all_data[1] & 127
        if code_len == 126:
            masks = all_data[4:8]
            data = all_data[8:]
        elif code_len == 127:
            masks = all_data[10:14]
            data = all_data[14:]
        else:
            masks = all_data[2:6]
            data = all_data[6:]
    raw_str = ""
    raw = b''
    i = 0
    for d in data:
         #raw_str += chr(d ^ masks[i % 4])
         raw += bytes([d ^ masks[i % 4]])
         i += 1
    #print(raw)
    if raw == b'\x03\xe8':
        return "disconnect"
    #print(raw.decode('utf-8'))
    return raw.decode('utf-8')

sk = socket.socket()
sk.bind(("192.168.1.100",5000))
sk.listen(20)
while(1):
    conn,address = sk.accept()
    handshake(conn)
    print(address)
    while(conn):
        msg = recv_data(conn,1024)
        if msg:
            print(msg)
            if msg=="disconnect":
                conn.close()
                break
            if msg[:8] == "shutdown":
                #print("shutdown"+msg[8:])
                time = int(msg[8:])
                os.system("shutdown -s -t %d" %time)
            if msg == "cancle":
                #print("cancle")
                os.system("shutdown -a")