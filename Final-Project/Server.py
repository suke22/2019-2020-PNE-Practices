import http.server
import http.client
import socketserver
import termcolor
from pathlib import Path
import json
from Seq1 import Seq

PORT = 8080

list_bases = ["A", "C", "G", "T"]

socketserver.TCPServer.allow_reuse_address = True

def html(title, color):
    return f"""
                <!DOCTYPE html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>{title}</title>
                  </head>
                  <body style="background-color: {color}">
                    <p><p>
                    </form>
                  </body>
                </html>
                """


def get_info(endpoint):

    port = 8080
    server = 'rest.ensembl.org'
    parameters = "content-type=application/json"
    print(f"\nConnecting to server: {server}:{port}\n")

    conn = http.client.HTTPConnection(server)

    try:
        conn.request("GET", endpoint+parameters)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()
    print(f"Response received!: {r1.status} {r1.reason}\n")
    data1 = r1.read().decode("utf-8")
    response = json.loads(data1)
    return response


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        req_line = self.requestline.split()[1]
        verb = req_line.split("?")[0]

        if verb == "/":
            contents = Path('index.html').read_text()
            error_code = 200
        elif verb == "/listSpecies":
            limit = req_line.split("=")[1]
            info = get_info("info/species?")["species"]
            contents = html("LIST OF SPECIES IN THE BROWSER", "lightblue")
            contents += f"""<h>The total number of species in ensembl is: 267</h><br>"""
            contents += f"""<h>The limit you have selected is: {limit}</h><br>"""
            contents += f"""<h>The names of the species are:</h>"""
            if limit == "":
                for element in info:
                    contents += f"""<p> • {element["display_name"]}</p>"""
            elif 267 >= int(limit):
                counter = 0
                for element in info:
                    if counter < int(limit):
                        contents += f"""<p> • {element["display_name"]}</p>"""
                        counter += 1
            else:
                for element in info:
                    contents += f"""<p> • {element["display_name"]}</p>"""
            error_code = 200
        else:
            contents = Path('Error.html').read_text()
            self.send_response(404)

        self.send_response(error_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()
        self.wfile.write(str.encode(contents))
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
