import http.server
import http.client
import socketserver
import termcolor
from pathlib import Path
import json
from Seq1 import Seq

PORT = 8080

bases = ["A", "T", "C", "G"]

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


def info_json(endpoint):
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
                info = info_json("info/species?")["species"]
                contents = document("LIST OF SPECIES IN THE BROWSER", "lightblue")
                contents += f"""<h4>The total number of species in ensembl is: 286</h4><p>"""
                contents += f"""<h4>The limit you have selected is: {limit}</h4><p>"""
                if limit == "":
                    contents += f"""<h4>The names of the species are:</h4>"""
                    for element in info:
                        contents += f"""<p> • {element["display_name"]}</p>"""
                    self.send_response(200)
                elif 286 >= int(limit) >= 0:
                    counter = 0
                    contents += f"""<h4>The names of the species are:</h4>"""
                    for element in info:
                        if counter < int(limit):
                            contents += f"""<p> • {element["display_name"]}</p>"""
                            counter += 1
                    self.send_response(200)
                else:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            except ValueError:
                contents = Path('Error.html').read_text()
                self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 2) Information about the karyotype
        elif verb == "/karyotype":
            specie = req_line.split("=")[1]
            list_species = info_json("info/species?")["species"]
            for dictionary in list_species:
                if specie in dictionary.values():
                    info = info_json("info/assembly/" + specie + "?")["karyotype"]
                    contents = document("KARYOTYPE OF A SPECIFIC SPECIES", "lightblue")
                    contents += f"""<h4> The names of the {specie}'s chromosomes are: </h4>"""
                    for element in info:
                        contents += f"""<p> • {element}</p>"""
                    self.send_response(200)
                    break
                else:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 3) Chromosome Length
        elif verb == "/chromosomeLength":
            number = req_line.split("=")[2]
            values = req_line.split("=")[1]
            specie = values.split("&")[0]
            list_species = info_json("info/species?")["species"]
            for dictionary in list_species:
                if specie in dictionary.values():
                    info = info_json("info/assembly/" + specie + "?")["top_level_region"]
                    for element in info:
                        if element["name"] == number:
                            contents = document("LENGTH OF A SPECIFIC CHROMOSOME", "lightblue")
                            contents += f"""<h4> The length of the chromosomes {number} is: </h4>"""
                            contents += f"""<p> {element["length"]} </p>"""
                            self.send_response(200)
                            break
                        else:
                            contents = Path('Error.html').read_text()
                            self.send_response(404)
                    break
                else:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        #4) Sequence of a human gene
        elif verb == "/geneSeq":
            value = req_line.split("=")[1]
            if value == "":
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]
                        seq = info_json(f"/sequence/id/{gene_id}?")
                        contents = document("GENE SEQUENCE", "lightblue")
                        contents += f'<p> The sequence of gene {value} is: </p>'
                        contents += f'<textarea rows = "30" cols = "150"> {seq["seq"]} </textarea>'
                        self.send_response(200)
                    except IndexError:
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        #5) Information about a human gene
        elif verb == "/geneInfo":
            value = req_line.split("=")[1]
            if value == "":
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]
                        seq_info = info_json(f"/lookup/id/{gene_id}?")
                        contents = document("SEQUENCE INFORMATION", "lightblue")
                        contents += f'<h4> The sequence of gene {value} is: </h4>'
                        contents += f'<p> The start point is: {seq_info["start"]} </p>'
                        contents += f'<p> The end point is: {seq_info["end"]} </p>'
                        contents += f'<p> The length is: {seq_info["end"] - seq_info["start"]} </p>'
                        contents += f'<p> The id is: {seq_info["id"]} </p>'
                        contents += f'<p> The chromose is: {seq_info["seq_region_name"]} </p>'
                        self.send_response(200)
                    except IndexError:
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        #6) Total length and % of bases os a human gene
        elif verb == "/geneCalc":
            value = req_line.split("=")[1]
            if value == "":
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]
                        sequence = info_json(f"/sequence/id/{gene_id}?")["seq"]
                        seq = Seq(sequence)
                        contents = document("SEQUENCE INFORMATION", "lightblue")
                        contents += f'<h4> Calculations over the introduced gene {value}: </h4>'
                        contents += f'<p> Total length of this gene is: {seq.len()}</p>'
                        contents += f'<p> Percentage of the bases is: </p>'
                        for base in bases:
                            count = seq.count_base(base)
                            percentage = round(seq.count_base(base) * (100 / seq.len()), 2)
                            contents += f'<p> {base}: {count} ({percentage}%) </p>'
                        self.send_response(200)
                    except IndexError:
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        #7) List of genes located in a chromosome
        elif verb == "/geneList":
            value = req_line.split("?")[1]
            chromo_number, start_number, end_number = value.split("&")
            chromo = chromo_number.split("=")[1]
            start = start_number.split("=")[1]
            end = end_number.split("=")[1]
            if chromo == "" or start == "" or end == "":
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:
                    start = int(start)
                    end = int(end)
                    if chromo in ["x", "X", "y", "Y" , "MT"] or 1 <= int(chromo) <= 22 :
                        genes = info_json(f"/overlap/region/human/{chromo}:{start}-{end}?feature=gene;")
                        try:
                            contents = document("GENE LIST", "lightblue")
                            contents += f"<h4>Genes located in the chromosome {chromo} from {start} to {end} positions </h4>"
                            for list in genes:
                                contents += f'<p> - {list["external_name"]}</p>'
                            self.send_response(200)
                        except TypeError:
                            contents = Path('Error.html').read_text()
                            self.send_response(404)
                    else:
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
                except ValueError:
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""


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
