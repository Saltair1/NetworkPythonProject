import time
import datetime

from socket import *

from query import make_query

localDNSIP = "localhost"
localDNSPort = 15000

rr_table = []  # initially empty
do_query = True  # flag for query
transaction_id = 0  # replace with a unique transaction ID for each query

clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    query_name = input("Enter the desired website or domain: ")
    query_type = input("Enter the query type (A/AAAA/CNAME/NS): ").upper()

    # Checks to see if record is in client's table
    for record in rr_table:
        if record["name"] == query_name and record["type"] == query_type:
            do_query = False

    if do_query:
        # make a DNS query
        dns_query = make_query(transaction_id, query_name, query_type)

        # Send the query to the local DNS server
        clientSocket.sendto(dns_query, (localDNSIP, localDNSPort))

        # Receive the DNS response
        message, serverAddress = clientSocket.recvfrom(2048)

        # Process the response and store the information in your RR table
        # Use the obtained information for your application
        value_length = int.from_bytes(message[8:12], byteorder="big")
        value = message[-value_length:].decode()

        #calculating TTL
        now = datetime.datetime.now()
        midnight = datetime.datetime.combine(now.date(), datetime.time())
        ttl = (now - midnight).seconds

        if value == "NOT VALID REQUEST":
            print(value)
        else:
            rr_table.append(
                {
                    "record_number": len(rr_table) + 1,
                    "name": query_name,
                    "type": query_type,
                    "value": value,
                    "ttl": ttl + 60,
                    "static": 0,
                }
            )

        transaction_id += 1
    do_query = True
    for record in rr_table:
        print(record)

clientSocket.close()