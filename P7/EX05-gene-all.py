from Seq1 import Seq
import http.client
import json
import termcolor


GENES = {'FRAT1': "ENSG00000165879",
         'ADA': "ENSG00000196839",
         'FXN': "ENSG00000165060",
         'RNU6_269P': "ENSG00000212379",
         'MIR633': "ENSG00000207552",
         'TTTY4C': "ENSG00000228296",
         'RBMY2YP': "ENSG00000227633",
         'FGFR3': "ENSG00000068078",
         'KDR': "ENSG00000128052",
         'ANK2': "ENSG00000145362"}

bases = ["A", "T", "C", "G"]

SERVER = 'rest.ensembl.org'
endpoint = "/sequence/id/"
parameters = "?content-type=application/json"
for id in GENES:
    URL = SERVER + endpoint + GENES[id] + parameters

    print()
    print(f"Server: rest.ensembl.org")
    print(f"URL: {URL}")

    # Connect with the server
    conn = http.client.HTTPConnection(SERVER)

    # -- Send the request message, using the GET method. We are
    # -- requesting the main page (/)
    try:
        conn.request("GET", "/"+endpoint+GENES[id]+parameters)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    data1 = r1.read().decode("utf-8")

    # -- Create a variable with the data,
    # -- form the JSON received
    response = json.loads(data1)

    termcolor.cprint(f"Gene: ", "green", end="")
    print(id)

    termcolor.cprint(f"Description: ", "green", end="")
    print(response['desc'])

    seq_bases = response['seq']
    sequence = Seq(seq_bases)
    termcolor.cprint(f"Total length: ", "green", end="")
    print(sequence.len())

    for base in bases:
        count = sequence.count_base(base)
        percentage = round(sequence.count_base(base) * (100 / sequence.len()), 2)
        termcolor.cprint(f"{base}", 'blue', end="")
        print(f": {count} ({percentage}%)")

    d = sequence.seq_count()
    ll = list(d.values())
    m = max(ll)
    termcolor.cprint("Most frequent Base:", 'green', end="")
    print(f"{bases[ll.index(m)]}")
