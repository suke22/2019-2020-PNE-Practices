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


def document(title, color):
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
        conn.request("GET", endpoint + parameters)
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
        # index
        if verb == "/":
            contents = Path('index.html').read_text()
            self.send_response(200)

        # 1) List of species in the genome database
        elif verb == "/listSpecies":
            limit = req_line.split("=")[1]
            try:
                info = get_info("info/species?")["species"]
                contents = document("LIST OF SPECIES IN THE BROWSER", "lightblue")
                contents += f"""<h>The total number of species in ensembl is: 267</h><p>"""
                contents += f"""<h>The limit you have selected is: {limit}</h><p>"""
                if limit == "":
                    for element in info:
                        contents += f"""<h>The names of the species are:</h>"""
                        contents += f"""<p> • {element["display_name"]}</p>"""
                elif 267 >= int(limit):
                    counter = 0
                    contents += f"""<h>The names of the species are:</h>"""
                    for element in info:
                        if counter < int(limit):
                            contents += f"""<p> • {element["display_name"]}</p>"""
                            counter += 1
                else:
                    contents += f"""You must enter a number between 0 and 267"""
                self.send_response(200)
            except ValueError:
                contents = Path('Error.html').read_text()
                self.send_response(404)

        # 2) Information about the karyotype
        elif verb == "/karyotype":
            specie = req_line.split("=")[1]
            list_species = get_info("info/species?")["species"]
            for dictionary in list_species:
                if specie in dictionary.values():
                    info = get_info("info/assembly/" + specie + "?")["karyotype"]
                    contents = document("KARYOTYPE OF A SPECIFIC SPECIES", "lightblue")
                    contents += f"""<h> The names of the chromosomes are: </h>"""
                    for element in info:
                        contents += f"""<p> • {element}</p>"""
                    self.send_response(200)
                    break
                else:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)

        elif verb == "/chromosomeLength":
            number = req_line.split("=")[2]
            values = req_line.split("=")[1]
            specie = values.split("&")[0]
            list_species = get_info("info/species?")["species"]
            for dictionary in list_species:
                if specie in dictionary.values():
                    info = get_info("info/assembly/" + specie + "?")["top_level_region"]
                    contents = document("KARYOTYPE OF A SPECIFIC SPECIES", "lightblue")
                    contents += f"""<h> The names of the chromosomes are: </h>"""
                    for element in info:  # iteration to get all chromo from list
                        if element["name"] == number:
                            contents =f"""<h> {element["length"]} </h>"""
                            self.send_response(200)
                            break
                else:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)

        else:
            contents = Path('Error.html').read_text()
            self.send_response(404)

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
