import http.server
import socketserver
import termcolor
import pathlib

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


def open_html(filename):
    file_contents = pathlib.Path(filename).read_text().split("\n")[1:]
    body = "".join(file_contents)
    return body


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        req_line = self.requestline.split(' ')
        path = req_line[1]
        path = path[1:]
        content_type = 'text/html'
        print(path)
        Folder = "../P5/"
        if path == "" or path == "/index.html" or path == "/":
            path = "index.html"
        else:
            path = path[1:]
        try:
            contents = open_html(Folder + path)
            status = 200
        except FileNotFoundError:
            contents = pathlib.Path("Error.html").read_text()
            status = 404

        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(contents.encode()))
        self.end_headers()
        self.wfile.write(contents.encode())
        return


Handler = TestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
