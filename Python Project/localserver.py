import socket

# Constants
LOCAL_DNS_PORT = 15000

# create a socket for communication with the client
# create sockets to communicate with the Qualcomm and ViaSat DNS servers
# listen for incoming requests from client

while True:
    # receive a DNS query from client
    # process the query and check if you have the information in RR table
    # if you have the information, construct a DNS response and send to client
    # if not, forward the query to the DNS server (Qualcomm or ViaSat)
    # receive the response from the external DNS server
    # store the information in RR table
    # construct a DNS response and send to the client
