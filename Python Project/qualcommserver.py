import json
import socket

with open("qualcommserver_rr.json") as table:
    data = json.load(table)

for record in data["rr_table"]:
    print(record["name"])

# Constants
QUALCOMM_DNS_PORT = 21000

# create a socket for communication with the client
# create a socket to communicate with the local DNS server
# listen for incoming requests from the local DNS server

while True:
    # receive a DNS query from the local DNS server
    # process the query and check if you have the information in RR table
    # if you have the information, construct a DNS response and send to the local DNS server
    # if not, send a query to the Qualcomm DNS server to fetch the information
    # receive the response from the Qualcomm DNS server
    # store the information in RR table
    # construct a DNS response and send to the local DNS server

    break  # Added this so that the program can run
