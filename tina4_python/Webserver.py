#
# Tina4 - This is not a 4ramework.
# Copy-right 2007 - current Tina4
# License: MIT https://opensource.org/licenses/MIT
#
from tina4_python.Constant import LOOKUP_HTTP_CODE
from tina4_python.Debug import Debug
from http.server import BaseHTTPRequestHandler
from tina4_python.Constant import *
from urllib.parse import urlparse, parse_qsl
import socket
import asyncio
import json
import time
import random


class Webserver:
    async def get_content_length(self):
        content_length = 0
        # get the content length
        for header in self.headers:
            if header.find("Content-Length:") != -1:
                value = header.split(":")
                content_length = int(value[1].strip())
        return content_length

    async def get_content_body(self, content_length):
        # get lines of content where at the end of the request
        content = self.request_raw[-content_length:]

        try:
            content = json.loads(content)
        except Exception as e:
            content = ""

        return content

    async def get_response(self, method):
        headers = []
        if method == "OPTIONS":
            self.send_header("Access-Control-Allow-Origin", "*", headers)
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization", headers)
            self.send_header("Access-Control-Allow-Credentials", "True", headers)

            headers = await self.get_headers(headers, self.response_protocol, HTTP_OK)
            return headers

        params = dict(parse_qsl(urlparse(self.path).query, keep_blank_values=True))

        content_length = await self.get_content_length()
        body = await self.get_content_body(content_length)
        request = {"params": params, "body": body, "raw": self.request}


        response = await self.router_handler.resolve(method, self.path, request, self.headers)

        self.send_header("Access-Control-Allow-Origin", "*", headers)
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization", headers)
        self.send_header("Access-Control-Allow-Credentials", "True", headers)
        self.send_header("Content-Type", response["content_type"], headers)
        self.send_header("Content-Length", str(len(response["content"])), headers)
        self.send_header("Connection", "Keep-Alive", headers)
        self.send_header("Keep-Alive", "timeout=5, max=30", headers)

        headers = await self.get_headers(headers, self.response_protocol, response["http_code"])

        if type(response["content"]) == str:
            return headers + response["content"].encode()
        else:
            return headers + response["content"]

    @staticmethod
    def send_header(header, value, headers):
        headers.append(header + ": " + value)

    @staticmethod
    async def get_headers(response_headers, response_protocol, response_code):
        headers = response_protocol + " " + str(response_code) + " " + LOOKUP_HTTP_CODE[
            response_code] + "\n"
        for header in response_headers:
            headers += header + "\n"
        headers += "\n"
        return headers.encode()

    async def run_server(self):
        server = await asyncio.start_server(self.handle_client, self.host_name, self.port)
        async with server:
            await server.serve_forever()

    async def get_data(self, reader):
        loop = asyncio.get_event_loop()
        # https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
        chunks = []
        data = None
        i = random.randrange(1000, 9999)
        found_length = False
        content_length = 0
        count = 0
        header_offset = 0
        while True:
            data = (await reader.read(2048)).decode("utf-8")
            chunks.append(data)

            if not found_length:
                i = "".join(chunks).find('Content-Length:')
                e = "".join(chunks).find('\n', i)
                if not i == -1 and not e == -1:
                    value = "".join(chunks)[i:e].replace("\r", "").split(":")
                    if len(value) > 1:
                        content_length = int(value[1].strip())
                        found_length = True

            if header_offset == 0:
                i = "".join(chunks).replace("\r", "").find("\n\n")
                if not i == -1:
                    header_offset = i

            if not found_length and (data.find('GET') != -1 or data.find('OPTIONS') != -1) and len(data) < header_offset:
                content_length = len("".join(chunks))

            if len("".join(chunks)) >= content_length+header_offset or len("".join(chunks)) == header_offset or len("".join(chunks)) == 0:
                break
        return "".join(chunks)


    async def handle_client(self, reader, writer):
        loop = asyncio.get_event_loop()
        # Get the client request
        request = await self.get_data(reader)

        # Decode the request
        self.request_raw = request

        self.request = request.replace("\r", "")

        self.path = request.split(" ")

        if len(self.path) > 1:
            self.path = self.request.split(" ")[1]

        self.method = self.request.split(" ")[0]

        initial = self.request.split("\n\n")[0]

        self.headers = initial.split("\n")

        method_list = [TINA4_GET, TINA4_ANY, TINA4_POST, TINA4_PATCH, TINA4_OPTIONS]

        contains_method = [ele for ele in method_list if (ele in self.method)]

        if self.method != "" and contains_method:
            response = await (self.get_response(self.method))
            writer.write(response)
            await writer.drain()

        writer.close()

    def __init__(self, host_name, port):
        self.method = None
        self.response_protocol = "HTTP/1.1"
        self.headers = None
        self.response_headers = []
        self.request = None
        self.request_raw = None
        self.path = None
        self.server_socket = None
        self.host_name = host_name
        self.port = port
        self.router_handler = None
        self.running = False

    def serve_forever(self):
        asyncio.run(self.run_server())

    def server_close(self):
        self.running = False
        self.server_socket.close()
