#!/usr/bin/env python3

import os
import socket
import ssl
import requests
import time

# Constants

HOST = 'chat.ndlug.org'
PORT = 6697
NICK = f'ircle-{os.environ["USER"]}'

# Functions

def dad_joke():
    # Make the API Request: 
    url = "https://icanhazdadjoke.com/"
    response = requests.get(url, headers={'Accept':'application/json', 'User-Agent': "hello"})

    if response.status_code == 200:
        jokeinfo = response.json()
        joke = jokeinfo["joke"]
        return joke
    else:
        return "failed"

def ircle():
    
    # Connect to IRC server
    ssl_context = ssl.create_default_context()
    tcp_socket  = socket.create_connection((HOST, PORT))
    ssl_socket  = ssl_context.wrap_socket(tcp_socket, server_hostname=HOST)
    ssl_stream  = ssl_socket.makefile('rw')

    # Identify ourselves
    ssl_stream.write(f'USER {NICK} 0 * :{NICK}\r\n')
    ssl_stream.write(f'NICK {NICK}\r\n')
    ssl_stream.flush()

    # Join #bots channel
    ssl_stream.write(f'JOIN #bots\r\n')
    ssl_stream.flush()

    # Read and display
    while True:
        message = ssl_stream.readline().strip()
        if "ping" in message.lower():
            ssl_stream.write(f'PONG {NICK}\r\n')
            ssl_stream.flush()
        if "!dj" in message.lower():
            joke = dad_joke()
            ssl_stream.write(f"PRIVMSG #bots :{joke}\r\n")
            ssl_stream.flush()
        time.sleep(1)


# Main Execution

def main():
    ircle()

if __name__ == '__main__':
    main()