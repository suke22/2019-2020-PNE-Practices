import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq

PORT = 8080

SEQ_GET = [
    "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA",
    "AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA",
    "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT",
    "CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA",
    "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"
]

FOLDER = "../Session-04/"
EXT = ".txt"

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        req_line = self.requestline.split(' ')
        path = req_line[1]
        arguments = path.split('?')
        verb = arguments[0]
        contents = Path('Error.html').read_text()
        error_code = 404

        if verb == "/":
            contents = Path('form-4.html').read_text()
            error_code = 200
        elif verb == "/ping":
            contents = """
            <!DOCTYPE html>
            <html lang = "en">
            <head>
            <meta charset = "utf-8" >
              <title> PING </title >
            </head >
            <body>
            <h2> PING OK!</h2>
            <p> The SEQ2 server in running... </p>
            <a href="/">Main page</a>
            </body>
            </html>
            """
            error_code = 200

        elif verb == "/get":
            pair = arguments[1]
            pairs = pair.split('&')
            name, value = pairs[0].split("=")
            n = int(value)
            seq = SEQ_GET[n]
            contents = f"""
                        <!DOCTYPE html>
                        <html lang = "en">
                        <head>
                        <meta charset = "utf-8" >
                          <title> GET </title >
                        </head >
                        <body>
                        <h2> Sequence number {n}</h2>
                        <p> {seq} </p>
                        <a href="/">Main page</a>
                        </body>
                        </html>
                        """
            error_code = 200

        elif verb == "/gene":
            pair = arguments[1]
            pairs = pair.split('&')
            name, value = pairs[0].split("=")
            s = Seq()
            s.read_fasta(FOLDER + value + EXT)
            value_gene = str(s)
            contents = f"""
                            <!DOCTYPE html>
                            <html lang = "en">
                            <head>
                            <meta charset = "utf-8" >
                              <title> GET </title >
                            </head >
                            <body>
                            <h2> Gene: {value}</h2>
                            <p> {value_gene} </p>
                            <a href="/">Main page</a>
                            </body>
                            </html>
                            """
            error_code = 200

        elif verb == "/operation":
            pair = arguments[1]
            pairs = pair.split('&')
            name, seq = pairs[0].split("=")
            name, op = pairs[1].split("=")
            s = Seq(seq)
            if op == "comp":
                result = s.seq_complement()
            elif op == "rev":
                result = s.seq_reverse()
            else:
                slen = s.len()
                ca = s.count_base('A')
                pa = round(100 * ca / slen, 1)
                cc = s.count_base('C')
                pc = round(100 * cc / slen, 1)
                cg = s.count_base('G')
                pg = round(100 * cg / slen, 1)
                ct = s.count_base('T')
                pt = round(100 * ct / slen, 1)

                result =  f"""
                <p>Total length: {slen}</p>
                <p>A: {ca} ({pa}%)</p>
                <p>C: {cc} ({pc}%)</p>
                <p>G: {cg} ({pg}%)</p>
                <p>T: {ct} ({pt}%)</p>"""

            contents = f"""
                            <!DOCTYPE html>
                            <html lang = "en">
                            <head>
                            <meta charset = "utf-8" >
                              <title> OPERATION </title >
                            </head >
                            <body>
                            <h2> Sequence </h2>
                            <p> {seq} </p>
                            <h2> Operation </h2>
                            <p> {op} </p>
                            <h2> Result </h2>
                            <p> {result} </p>
                            <a href="/">Main page</a>
                            </body>
                            </html>
                            """
            error_code = 200
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
