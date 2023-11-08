import json
from socket import *

from query import make_response

rr_table = []

with open("qualcommserver_rr.json") as table:
    data = json.load(table)

for record in data["rr_table"]:
    rr_table.append(record)

# Constants
QUALCOMM_DNS_PORT = 21000

# create a socket for communication with the client
# create a socket to communicate with the local DNS server
# listen for incoming requests from the local DNS server

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", QUALCOMM_DNS_PORT))
t_id = 0
print("QualComm Server is ready...")

while True:
    # receive a DNS query from the local DNS server
    # process the query and check if you have the information in RR table
    # if you have the information, construct a DNS response and send to the local DNS server
    # if not, send a query to the Qualcomm DNS server to fetch the information
    # receive the response from the Qualcomm DNS server
    # store the information in RR table
    # construct a DNS response and send to the local DNS server
    message, client_address = server_socket.recvfrom(2048)
    query_name = message[12:].decode()
    type_flags = (int.from_bytes(message[4:8], byteorder="big") & 0x0F000000) >> 24
    query_id = int.from_bytes(message[:4], byteorder="big")
    query_type = ["A", "AAAA", "CNAME", "NS"]
    value = ""

    print(f"IN QUALCOMM. QUERY NAME: {query_name}")

    for record in rr_table:
        if record["name"] == query_name and record["type"] == query_type[type_flags]:
            value = record["value"]

    if value == "":
        server_socket.sendto("NOT VALID REQUEST".encode(), client_address)
    else:
        dns_response = make_response(query_id, query_name, type_flags, value)
        server_socket.sendto(dns_response, client_address)
