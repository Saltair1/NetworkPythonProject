import json
from socket import *

rr_table = []

# 'data' is a list of dictionaries, with each dictionary being an entry on the table
with open("localserver_rr.json") as table:
    data = json.load(table)

for record in data["rr_table"]:
    rr_table.append(record)

# Constants
LOCAL_DNS_PORT = 15000

# create a socket for communication with the client
# create sockets to communicate with the Qualcomm and ViaSat DNS servers
# listen for incoming requests from client
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", LOCAL_DNS_PORT))
print("Local Server is ready...")

while True:
    # receive a DNS query from client
    # process the query and check if you have the information in RR table
    # if you have the information, construct a DNS response and send to client
    # if not, forward the query to the DNS server (Qualcomm or ViaSat)
    # receive the response from the external DNS server
    # store the information in RR table
    # construct a DNS response and send to the client
    message, client_address = server_socket.recvfrom(2048)
    name_length = int.from_bytes(message[4:8], byteorder="big") & 0x00FF0000 >> 16
    query_name = message[12 : 12 + name_length].decode()
    qr = 1
    type_flags = (int.from_bytes(message[4:8], byteorder="big") & 0x0F000000) >> 24
    query_type = ["A", "AAAA", "CNAME", "NS"]
    value = ""

    for record in rr_table:
        if record["name"] == query_name and record["type"] == query_type[type_flags]:
            query_name = record["name"]
            value = record["value"]

    value_length = len(value)

    transaction_id = int.from_bytes(message[:4], byteorder="big")
    dns_response = (
        transaction_id.to_bytes(4, byteorder="big")
        + (qr << 28 | type_flags << 24 | name_length).to_bytes(4, byteorder="big")
        + value_length.to_bytes(4, byteorder="big")
        + query_name.encode()
        + value.encode()
    )
    server_socket.sendto(dns_response, client_address)
