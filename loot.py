#!/usr/bin/env python3

import sys, os, argparse
from multiprocessing import Pool
import socket


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE =range(8)

def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)


def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)

def findstuff(domain):
    
    
    try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            host = str.strip(domain)
            s.connect ((host, 6556))
            data = ''
            res = ''
            while True:
                data = s.recv(1024).decode('utf-8')
                res += data
                if not data:
                    
                    break
            print("==========================")
            print("XX    "+ host + "  XX")
            print("==========================")
            print(res)
            s.close

    except socket.timeout:
                print (".", sep=' ', end='', flush=True)
    except socket.error:
                print (".", sep=' ', end='', flush=True)
        
   
   

if __name__ == '__main__':
    

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='ip.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='results.txt', help='output file')
    parser.add_argument('-t', '--threads', default=5, help='threads')
    args = parser.parse_args()

    DOMAINFILE=args.inputfile
    OUTPUTFILE=args.outputfile
    MAXPROCESSES=int(args.threads)
    print(" ##                                      .__                                    ##")
    print(" ##    ____  _____    ___  _______    |  |   ____  __ _________              ##")
    print(" ##  _/ ___\ \__  \   \  \/ /\__  \   |  | _/ __ \|  |  \_  __ \             ##")
    print(" ##  \  \___  / __ \_  \   /  / __ \_ |  |_\  ___/|  |  /|  | \/             ##")
    print(" ##   \___  > ____  /   \_/  (____  / |____/\___  >____/ |__|                ##")
    print(" ##       \/      \/              \/            \/                           ##")
    print(" ##    _____       .__                 .__           ___.   .__  __          ##")
    print(" ##  _/ ____\____  |__|______   ____   |  | _____    \_ |__ |__|/  |_  ____  ##")
    print(" ##  \   __\ \__  \|  \_  __ \_/ __ \  |  | \__  \    | __ \|  \   __\/ __ \ ##")
    print(" ##   |  |   / __ \|  ||  | \/\  ___/  |  |__/ __ \_  | \_\ \  ||  | \  ___/ ##")
    print(" ##   |__|  (____  /__||__|    \___  > |____(____  /  |___  /__||__|  \___  >##")
    print(" ##              \/                \/            \/       \/              \/ ##")

    print("Scanning...")
    pool = Pool(processes=MAXPROCESSES)
    domains = open(DOMAINFILE, "r").readlines()
    pool.map(findstuff, domains)
    print("Finished")
