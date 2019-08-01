import socket
from os import system


# prompts the user to choose a target either by selecting a domain name or an IP address
def target_in():
    c = int(input('''
please choose:
1.target by domain name
2.target by IP address\n'''))
    if c == 1:
        system('cls') # clear the screen (for good looks)
        target = input("please enter your target's address: ")
        target = socket.gethostbyname(target) # gets the ip address from the domain name
        return target
    elif c == 2:
        system('cls')
        target = input("please enter your target's IP address: ")
        return target
    else:
        print("please choose the correct option (HINT 1 OR 2)") # error handling


# User inserts selected ports here,
def port_in():
    system('cls')
    global flag # a flag that decides if the user selected specific ports or a range of ports,for the scan functions
    ports = input('''
please enter ports to scan
The formats are : <start port>-<end port> or <port>,<port>,<port>.....: \n''')
    if "-" in ports: # check if the string contains '-' for range
        ports = ports.split('-')
        flag = 1
        return ports
    elif ',' in ports: # check if the string contains ',' for specific ports
        flag = 0
        ports = ports.split(',')
        return ports


# check if port open, closed or filtered for the full tcp scan
def check_tcp(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # wait half a second then move on to the next
        s.connect((target, port))
        s.close()
        return True # port open
    except TimeoutError:
        return False # port filtered
    except:
        return None # port closed


# check if port open, closed or filtered for the full udp scan
def check_udp(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect((target, port))
        return True
    except TimeoutError:
        return False
    except:
        return None


# full tcp scan 3 way handshake
def full_scan(target, ports):
    system('cls')
    print('-' * 60)
    print('please wait while the scan is done. scanning: {}'.format(target))
    print('-' * 60)
    ut_flag = int(input("please choose TCP = 1 or UDP = 2\n")) # flag to decide the use of a tcp or udp scan
    system('cls')
    if flag == 1:
        try:
            for port in range(int(ports[0]), int(ports[1]) + 1): # ports[0]= starting port ports[1]+1=ending port
                if ut_flag == 1:
                    answer = check_tcp(target, port)
                    if answer == True:
                        print("port {}: Open".format(port))
                    elif answer == None:
                        print("port {}: Closed".format(port))
                    elif answer == False:
                        print("port {}: Filtered".format(port))
                elif ut_flag == 2:
                    system('cls')
                    answer = check_udp(target, port)
                    if answer == True:
                        print("port {}: Open".format(port))
                    elif answer == None:
                        print("port {}: Closed".format(port))
                    elif answer == False:
                        print("port {}: Filtered".format(port))
        except KeyboardInterrupt: # press ctrl+c to stop the program from running
            print("You stopped !!!!")
            system(exit())
        except socket.error: # error handling
            print("Could not connect to server")
    elif flag == 0:
        try:
            for port in ports:
                port = int(port)
                answer = check_tcp(target, port)
                if answer == True:
                    print("port {}: Open".format(port))
                elif answer == None:
                    print("port {}: Closed".format(port))
                elif answer == False:
                    print("port {}: Filtered".format(port))
        except KeyboardInterrupt:
            print("You stopped !!!!")
            system(exit())
        except socket.error:
            print("Could not connect to server")


def main():
    system('cls')
    full_scan(target_in(), port_in())
    print("scan is done")


main()
