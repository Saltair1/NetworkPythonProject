import datetime
import json
from socket import *

import pandas as pd

from query import make_query, make_response

rr_table = []

# 'data' is a list of dictionaries, with each dictionary being an entry on the table
with open("localserver_rr.json") as table:
    data = json.load(table)

for record in data["rr_table"]:
    rr_table.append(record)

# Constants
LOCAL_DNS_PORT = 15000
QUALCOMM_DNS_PORT = 21000
VIASAT_DNS_PORT = 22000
IP = "localhost"


# create a socket for communication with the client
# create sockets to communicate with the Qualcomm and ViaSat DNS servers
# listen for incoming requests from client
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", LOCAL_DNS_PORT))
print("Local Server is ready...\n")
df = pd.DataFrame(rr_table)
df = df.to_string(index=False)
print(df)

# receive a DNS query from client
# process the query and check if you have the information in RR table
# if you have the information, construct a DNS response and send to client
# if not, forward the query to the DNS server (Qualcomm or ViaSat)
# receive the response from the external DNS server
# store the information in RR table
# construct a DNS response and send to the client
while True:
    message, client_address = server_socket.recvfrom(2048)
    query_name = message[12:].decode()
    type_flags = (int.from_bytes(message[4:8], byteorder="big") & 0x0F000000) >> 24
    query_type = ["A", "AAAA", "CNAME", "NS"]
    value = ""
    transaction_id = int.from_bytes(message[:4], byteorder="big")

    for record in rr_table:
        # if query exists in rr table, then get value from rr table
        if record["name"] == query_name and record["type"] == query_type[type_flags]:
            value = record["value"]
            transaction_id = record["record_number"]
            print("Found existing transaction!")
            continue

    # if query does not exist in table, get it from server
    if value == "":
        if ("viasat" in query_name or "qualcomm" in query_name) and query_type[
            type_flags
        ] == "A":
            query = make_query(transaction_id, query_name, query_type[type_flags])
            if "viasat" in query_name:
                server_socket.sendto(query, (IP, VIASAT_DNS_PORT))
            else:
                server_socket.sendto(query, (IP, QUALCOMM_DNS_PORT))
            message, serverAddress = server_socket.recvfrom(2048)
            value_length = int.from_bytes(message[8:12], byteorder="big")
            value = message[-value_length:].decode()

            # calculating TTL
            now = datetime.datetime.now()
            midnight = datetime.datetime.combine(now.date(), datetime.time())
            ttl = (now - midnight).seconds
            print("Creating new transaction")

            rr_table.append(
                {
                    "record_number": len(rr_table) + 1,
                    "name": query_name,
                    "type": query_type[type_flags],
                    "value": value,
                    "ttl": ttl + 60,
                    "static": 0,
                }
            )
            df = pd.DataFrame(rr_table)
            df = df.to_string(index=False)
            print(df)

    # if value still does not exist, something went wrong
    if value == "":
        server_socket.sendto("NOT VALID REQUEST".encode(), client_address)
    else:
        dns_response = make_response(transaction_id, query_name, type_flags, value)
        server_socket.sendto(dns_response, client_address)
