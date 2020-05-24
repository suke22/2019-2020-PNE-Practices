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


# we need a function to compute de response html
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


# we need a function to connect with ensembl data
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
                info = info_json("info/species?")["species"]  # here we get the all the species
                contents = document("LIST OF SPECIES IN THE BROWSER", "plum")  # we compute the html response
                contents += f"""<h4>The total number of species in ensembl is: 286</h4><p>"""
                contents += f"""<h4>The limit you have selected is: {limit}</h4><p>"""
                if limit == "":  # if the client does not enter anything
                    contents += f"""<h4>The names of the species are:</h4>"""
                    for element in info:
                        contents += f"""<p> • {element["display_name"]}</p>"""  # get the species name
                    self.send_response(200)
                elif 286 >= int(limit) >= 0:  # if the client enter a valid limit
                    counter = 0
                    contents += f"""<h4>The names of the species are:</h4>"""
                    for element in info:
                        if counter < int(limit):  # get the correct number of species for the limit
                            contents += f"""<p> • {element["display_name"]}</p>"""  # we just ger the specie's name
                            counter += 1
                    self.send_response(200)
                else:  # if the client enter a value out of range
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            except ValueError:  # if the client enter a word
                contents = Path('Error.html').read_text()
                self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 2) Information about the karyotype
        elif verb == "/karyotype":
            specie = req_line.split("=")[1]
            list_species = info_json("info/species?")["species"]  # we get all the species
            contents = ""
            for dictionary in list_species:
                if specie in dictionary.values():  # check if the specie entered by the client is valid
                    info = info_json("info/assembly/" + specie + "?")["karyotype"]  # get the karyotype of the species
                    contents = document("KARYOTYPE OF A SPECIFIC SPECIES", "plum")  # we compute the html response
                    contents += f"""<h4> The names of the {specie}'s chromosomes are: </h4>"""
                    for element in info:
                        contents += f"""<p> • {element}</p>"""
                    self.send_response(200)
                    break
                else:  # if the species does not exist
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 3) Chromosome Length
        elif verb == "/chromosomeLength":
            number = req_line.split("=")[2]
            values = req_line.split("=")[1]
            specie = values.split("&")[0]
            list_species = info_json("info/species?")["species"]  # we get all the species
            contents = ""
            for dictionary in list_species:
                if specie in dictionary.values():  # check if the specie entered by the client is valid
                    info = info_json("info/assembly/" + specie + "?")["top_level_region"]  # get all the lengths
                    for element in info:
                        if element["name"] == number:  # check if the chromosome is valid
                            # we compute the html response
                            contents = document("LENGTH OF A SPECIFIC CHROMOSOME", "plum")
                            contents += f"""<h4> The length of the chromosomes {number} is: </h4>"""
                            contents += f"""<p> {element["length"]} </p>"""
                            self.send_response(200)
                            break
                        else:  # if the chromosome does not exist
                            contents = Path('Error.html').read_text()
                            self.send_response(404)
                    break
                else:  # if the chromosome does not exist
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 4) Sequence of a human gene
        elif verb == "/geneSeq":
            value = req_line.split("=")[1]
            if value == "":  # if the client does not enter anything
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:  # if the value is a number it prints an error
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:  # if the value is not a number
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]  # get the id
                        seq = info_json(f"/sequence/id/{gene_id}?")   # get all the information about the gene
                        contents = document("GENE SEQUENCE", "plum")  # we compute the html response
                        contents += f'<p> The sequence of gene {value} is: </p>'
                        # get the sequence of the id
                        contents += f'<textarea rows = "30" cols = "150"> {seq["seq"]} </textarea>'
                        self.send_response(200)
                    except IndexError:  # if the gene does not exist
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 5) Information about a human gene
        elif verb == "/geneInfo":
            value = req_line.split("=")[1]
            if value == "":  # if the client does not enter anything
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:  # if the value is not a number
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]  # get the id
                        seq_info = info_json(f"/lookup/id/{gene_id}?")  # get all the information about the gene
                        contents = document("SEQUENCE INFORMATION", "plum")  # we compute the html response
                        contents += f'<h4> The sequence of gene {value} is: </h4>'
                        contents += f'<p> The start point is: {seq_info["start"]} </p>'
                        contents += f'<p> The end point is: {seq_info["end"]} </p>'
                        contents += f'<p> The length is: {seq_info["end"] - seq_info["start"]} </p>'
                        contents += f'<p> The id is: {seq_info["id"]} </p>'
                        contents += f'<p> The chromose is: {seq_info["seq_region_name"]} </p>'
                        self.send_response(200)
                    except IndexError:  # if the gene does not exist
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 6) Total length and % of bases os a human gene
        elif verb == "/geneCalc":
            value = req_line.split("=")[1]
            if value == "":   # if the client does not enter anything
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:  # if the value is not a number
                    value = int(value)
                    contents = Path('Error.html').read_text()
                    self.send_response(404)
                except ValueError:
                    try:
                        gene_id = info_json(f"/xrefs/symbol/homo_sapiens/{value}?")[0]["id"]  # get the id
                        sequence = info_json(f"/sequence/id/{gene_id}?")["seq"]  # get the sequence of the gene
                        seq = Seq(sequence)
                        contents = document("SEQUENCE CALCULATIONS", "plum")  # we compute the html response
                        contents += f'<h4> Calculations over the introduced gene {value}: </h4>'
                        contents += f'<p> Total length of this gene is: {seq.len()}</p>'  # calculate the length
                        contents += f'<p> Percentage of the bases is: </p>'
                        for base in bases:  # calculate the count and the percentage od the sequence
                            count = seq.count_base(base)
                            percentage = round(seq.count_base(base) * (100 / seq.len()), 2)
                            contents += f'<p> {base}: {count} ({percentage}%) </p>'
                        self.send_response(200)
                    except IndexError:  # if the gene does not exist
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
            contents += f"""<a href="/">Main page</a></body></html>"""

        # 7) List of genes located in a chromosome
        elif verb == "/geneList":
            value = req_line.split("?")[1]
            chromo_number, start_number, end_number = value.split("&")
            chromo = chromo_number.split("=")[1]
            start = start_number.split("=")[1]
            end = end_number.split("=")[1]
            if chromo == "" or start == "" or end == "":  # if the client does not enter anything
                contents = Path('Error.html').read_text()
                self.send_response(404)
            else:
                try:
                    start = int(start)  # check if the start point is a number
                    end = int(end)  # check if the start point is a number
                    # check if the chromosome is human
                    if chromo in ["x", "X", "y", "Y", "MT"] or 1 <= int(chromo) <= 22:
                        # get the genes inside that positions
                        genes = info_json(f"/overlap/region/human/{chromo}:{start}-{end}?feature=gene;")
                        try:
                            contents = document("GENE LIST", "plum")  # we compute the html response
                            contents += f"<h4>Genes located in the chromosome {chromo} from {start} to {end} positions </h4>"
                            for list in genes:
                                contents += f'<p> - {list["external_name"]}</p>'
                            self.send_response(200)
                        except TypeError:  # if the start or end points are no valid
                            contents = Path('Error.html').read_text()
                            self.send_response(404)
                    else:  # if the chromosome is not one of the human
                        contents = Path('Error.html').read_text()
                        self.send_response(404)
                except ValueError:  # if something entered by the client is not a number
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
