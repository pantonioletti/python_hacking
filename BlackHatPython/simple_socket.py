import socket
import os
import sys
from struct import *

PROTOCOL_TCP = 6        #TCP protocol for IP layer

def PacketExtractor(packet):
    #Strip off the first 20 caharacters for the ip header
    stripPacket=packet[0:20]

    #Now unpack them
    ipHeaderTuple = unpack('!BBHHHBBH4s4s', stripPacket)

    # unpack returns a tuple, for illustration I will extract
    # each individual values

    verLen       = ipHeaderTuple[0]        # Field 0: Version and length
    TOS          = ipHeaderTuple[1]        # Field 1: Type of service
    packetLength = ipHeaderTuple[2]        # Field 2: Packet length
    packetID     = ipHeaderTuple[3]        # Field 3: Identification
    flagFrag     = ipHeaderTuple[4]        # Field 4: Flags/Fragment Offset
    RES          = (flagFrag >> 15) & 0x01 # Reserved
    DF           = (flagFrag >> 14) & 0x01 # Don't fragment
    MF           = (flagFrag >> 13) & 0x01 # More fragments
    timeToLive   = ipHeaderTuple[5]        # Field 5: Time to live (TTL)
    protocol     = ipHeaderTuple[6]        # Field 6: Protocol number
    checkSum     = ipHeaderTuple[7]        # Field 7: Header checksum
    sourceIP     = ipHeaderTuple[8]        # Field 8: Source IP
    destIP       = ipHeaderTuple[9]        # Field 9: Destination IP

    # Calculate / Conver  extracted values
    version      = verLen >> 4             # Upper nibble is the version number
    length       = verLen & 0x0F           # Lower nibble represents the size
    ipHdrLength  = length * 4              # Calculate the header length in bytes

    # Conver the source and destination address to dotted notation strings
    sourceAddress = socket.inet_ntoa(sourceIP)
    destinationAddress = socket.inet_ntoa(destIP)

    if protocol == PROTOCOL_TCP:
        stripTCPHeader = packet[ipHdrLength:ipHdrLength+20]
        # unpack returns a tuple, for illustration I will extract
        # each individual values using the unpack() function
        tcpHeaderBuffer = unpack('!HHLLBBHHH', stripTCPHeader)

        sourcePort           = tcpHeaderBuffer[0]
        destinationPort      = tcpHeaderBuffer[1]
        sequenceNumber       = tcpHeaderBuffer[2]
        acknowledgement      = tcpHeaderBuffer[3]
        dataOffsetandReserve = tcpHeaderBuffer[4]
        tcpHeaderLength      = (dataOffsetandReserve >> 4) * 4
        flags                = tcpHeaderBuffer[5]
        FIN                  = flags & 0x01
        SYN                  = (flags >> 1) & 0x01
        RST                  = (flags >> 2) & 0x01
        PSH                  = (flags >> 3) & 0x01
        ACK                  = (flags >> 4) & 0x01
        URG                  = (flags >> 5) & 0x01
        ECE                  = (flags >> 6) & 0x01
        CWR                  = (flags >> 7) & 0x01
        windowSize           = tcpHeaderBuffer[6]
        tcpCheckSum          = tcpHeaderBuffer[7]
        urgentPointer        = tcpHeaderBuffer[8]

        if sourcePort < 1024:
            serverIP = sourceAddress
            clientIP = destinationAddress
            serverPort = sourcePort
        elif destinationPort < 1024:
            serverIP = destinationAddress
            clientIP = sourceAddress
            serverPort = destinationPort
        else:
            serverIP = "Filter"
            clientIP = "Filter"
            serverPort = "Filter"
        return ([serverIP,clientIP,serverPort],[SYN,serverIP,TOS,timeToLive,DF,windowSize])
    else:
        return (["Filter", "Filter", "Filter"], [None, None, None, None, None, None])

def send_tcp():
    target_host = "localhost"
    target_port = 81

    #Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect tjhe client
    client.connect((target_host, target_port))
    #Send some data
    client.send(b"GET /jmeter HTTP/1.1\r\nHost: localhost:81\r\n\r\n")

    #Receive some data
    response = client.recv(4096)
    print(response)

def send_udp():
    target_host = "127.0.0.1"
    target_port = 81

    #Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Send some data
    client.sendto(b"AAAABBBCCCC",(target_host, target_port))

    #Receive some data
    data, addr = client.recvfrom(4096)

    print(data)

if __name__ == '__main__':
    # Note script must be run in superuser mode
    # i.e sudo python ...

    # Enable promiscious mode on the NIC
    # make a system call
    # Note: Linux based

    ret = os.system("ifconfig eth0 promisc")

    # if successful, the continue
    if ret == 0:
        print("eth0 configured in promiscious mode")

        # create a new socket using python socket module
        # AF_INET     : Address family internet
        # SOCK_RAW    : A raw protocol at the network layer
        # IPPROTO_TCP : Specifies the socket transport layer is TCP

        # Attempt to open the socket
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            # if if successful pot the result
            print("Raw socket open")
        except:
            # if socket fails
            print("Raw socket open failed")
            sys.exit()
        # create a list to hold the results from the packet capture
        # we will only save Server IP, Client IP, Server Port
        # for this example. Note we will be makin an educated guess as to
        # differentiale Server vs. Client

        ipObservations = []
        osObservations = []

        # Capture a maximum of 500 observations
        maxObservations = 500

        # Port filter set to port 443
        # TCP port 443 is defined as the http protocol over TLS/SSL
        portValue = 443

        try:
            while maxObservations > 0:
                # attepmt receive (this call is asynchronous, and will wait)
                recvBuffer, addr = mySocket.recvfrom(255)

                # decode the received packet
                # call the local packet extract function above
                content, fingerPrint = PacketExtractor(recvBuffer)

                if content[0] != "Filter":
                    # append the results to our list
                    # if it matches our port
                    if content[2] == portValue:
                        ipObservations.append(content)
                        maxObservations = maxObservations - 1
                        # if the SYN flag is set then
                        # record the fingerprint data in observatios
                        if fingerPrint[0] == 1:
                            osObservations.append([fingerPrint[1], \
                                                  fingerPrint[2], \
                                                  fingerPrint[3], \
                                                  fingerPrint[4], \
                                                  fingerPrint[5]])
                        else:
                            # Not our port
                            continue
                    else:
                        # Not a valid packet
                        continue
        except:
            print("Socket failure")
            sys.exit()
        # Capture complete
        # Disable promiscious mode
        # using linux system call
        ret = os.system("ifconfig eth0 -promisc")

        # Close the raw socket
        mySocket.close()

        # Create unique sorted list
        # Next we convert the list into a set to eliminate
        # any duplicate entries
        # then we convert the set back into a list for sorting

        uniqueSrc = set(map(tuple, ipObservations))
        finalList = list(uniqueSrc)
        finalList.sort()

        uniqueFingerprints = set(map(tuple,osObservations))
        finalFingerPrintList = list(uniqueFingerprints)
        finalFingerPrintList.sort()

        # Print out the unique combinations
        print("Unique packets")
        for packet in finalList:
            print(packet)
        print("Unique fingerprints")
        for osFinger in finalFingerPrintList:
            print(osFinger)
    else:
        print("Promiscious mode not set")

#send_udp()
