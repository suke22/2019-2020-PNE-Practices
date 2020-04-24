import socket
import termcolor
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

FOLDER = "../Session-04/"
EXT = ".txt"

sequence = [
    "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA",
    "AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA",
    "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT",
    "CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA",
    "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT",
]

def get_seq(n):
    return sequence[n]

def info_cmd(strseq):
    s = Seq(strseq)
    slen = s.len()
    ca = s.count_base('A')
    pa = round(100 * ca / slen, 1)
    cc = s.count_base('C')
    pc = round(100 * cc / slen, 1)
    cg = s.count_base('G')
    pg = round(100 * cg / slen, 1)
    ct = s.count_base('T')
    pt = round(100 * ct / slen, 1)

    response = f"""Sequence: {s}
Total length: {slen}
A: {ca} ({pa}%)
C: {cc} ({pc}%)
G: {cg} ({pg}%)
T: {ct} ({pt}%)"""
    return response

def comp_cmd(strseq):
    s = Seq(strseq)
    return s.seq_complement()

def rev_cmd(strseq):
    s = Seq(strseq)
    return s.seq_reverse()

def gene_cmd(strseq):
    s = Seq()
    s.read_fasta(FOLDER + strseq + EXT)
    return str(s)

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.listen()
print("Server is configured")

while True:
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped by the user")
        ls.close()
        exit()

    else:
        print("A client has connected to the server!")
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode()
        argum = msg.split("\n")
        lcmsg = argum[0].strip().split(' ')
        cmd = lcmsg[0]
        try:
            num = lcmsg[1]
        except IndexError:
            num = ""
        response = ""
        print(f"Received Message:", end="")
        if cmd == "PING":
            termcolor.cprint("PING command!", 'green')
            response = "OK!"
        elif cmd == "GET":
            termcolor.cprint("GET", 'green')
            response = get_seq(int(num))
        elif cmd == "INFO":
            termcolor.cprint("INFO", 'green')
            response = info_cmd(num)
        elif cmd == "COMP":
            termcolor.cprint("COMP", 'green')
            response = comp_cmd(num)
        elif cmd == "REV":
            termcolor.cprint("REV", 'green')
            response = rev_cmd(num)
        elif cmd == "GENE":
            termcolor.cprint("GENE", 'green')
            response = gene_cmd(num)

        print(f"{response}\n")
        cs.send(response.encode())
        cs.close()
