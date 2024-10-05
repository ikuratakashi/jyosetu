#!/home/jyosetu/.pyenv/shims/python

import http.server
import socketserver
import sys
import signal
import platform

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/" \
            and not self.path.startswith("/static") \
            and not self.path.startswith("/doc") \
            and not self.path.startswith("/img_md") \
            :
            self.path = "/"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main():
    PORT = 50100
    print(f"Python version : {platform.python_version()}")

    Handler = MyRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def shutdown():
    print("Shutdown")
    sys.exit(0)

if __name__ == "__main__":
    # プログラム終了時のハンドリング
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown())

    main()
