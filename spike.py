# -*- coding:utf-8 -*-

import xml.dom.minidom as md
import re
import fileinput
import statistics
import numpy as np
import sys
import os
from os import path
import datetime
import shutil
import time

# $ Arg recebido na exec do script ex: 'python spike.py (exemple.rrd(arg))'
arg = sys.argv[1:]
pid1 = os.getpid()  # tmp file
pid = ('{}.xml' .format(pid1))  # tmp file

def main():
    # Loop da função principal, remove todos os valores spikes
    while True:

        # Parse do xml para abrir o xmo, "v" seleciona os valores dessa row
        filexml = md.parse('/xxx/cacti/{}' .format(pid))
        num = filexml.getElementsByTagName("v")

        # Variaveis principais da func
        main.lista1 = []   # Com valores duplicados
        main.norep = []    # Sem vlores duplicados
        main.outliers = []
        main.nan = 'NaN'
        main.spike = []

        # For para recolha individual dos valores
        for name in num:
            a = (name.firstChild.nodeValue)
            if a == main.nan:
                continue
            main.lista1.append(float(a))

        # Remove duplicados da lista1
        for i in main.lista1:
            if i not in main.norep:
                main.norep.append(float(i))

        main.meand = ((statistics.mean(main.norep)))    # Mean, média dos valores da lista norep
        main.stand = ((statistics.stdev(main.norep)))   # Desvio padrão da lista norep

        # Calculo para definir quais valores são spikes, i = valor, meand = média, stand = desvio padrão
        for i in main.norep:
            z = ((i - main.meand) / main.stand)
            #print(i,z)
            if z >= 10:
                main.outliers.append(i)
                #print(i,z)
            else:
                continue

        # For para selecionar os valores spikes, converter para str para o replace a seguir
        for i in main.outliers:
            a = ('{:.10e}'.format(i))
            main.spike.append((a))

        # For para substituir os valores spikes por NaN
        for i in main.spike:
            f = open('/xxx/cacti/{}'.format(pid), 'r')
            filedata = f.read()
            f.close()
            newdata = filedata.replace(i, main.nan)
            f = open('/xxx/cacti/{}'.format(pid), 'w')
            f.write(newdata)
            f.close()
            #print(i, main.nan)
        if not main.spike:
            break
def dump():
    #for arg in sys.argv:
    argdump = arg
    rrd = argdump[0][-4:]
    if rrd != '.rrd':
        sys.exit()
    if len(sys.argv) == 1:
            print('O script, precisa de um argumento $1')
    else:
        os.system('rrdtool dump {} > {}' .format(argdump[0],pid))
    file_exist = (path.exists(argdump[0]))
    if file_exist == False:
        sys.exit()

def backup():
        backup.timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        #print(backup.timestamp)
        if len(sys.argv) == 1:
                print('O script, precisa de um argumento $1' % (arg[0]))
                return 1

        save_file = arg[0]
        backup_dir = '/xxx/cacti/backup_spike'

        save_file_basename = os.path.basename(save_file)
        last_modified = None

        modified = None
        try:
                modified = str(os.path.getmtime(save_file))
        except Exception as ex:
                print('Reading file modified failed: %s' % (str(ex)))

        if last_modified != modified:
                backup_file_name = '%s_%s' % (backup.timestamp, save_file_basename)
                backup_file_path = os.path.join(backup_dir, backup_file_name)
                try:
                        shutil.copyfile(save_file, backup_file_path)
                        last_modified = modified
                        #print('Backup created: %s' % (backup_file_name))
                except Exception as ex:
                        print('Backup failed: %s' % (str(ex)))

def restore():
        restore_name = arg[0]
       #save_file_basename = os.path.basename(restore_name)
        os.system('rm {}'.format(restore_name))
        os.system('rrdtool restore {} {}'.format(pid,restore_name))
        os.system('sudo chown -R cacti:apache {}'.format(restore_name))
        os.system('sudo chmod 777 {}'.format(restore_name))
        os.system('rm /xxx/cacti/{}'.format(pid))

def semaforo_e_validacoes():
    # Parse do xml para abrir o xmo, "v" seleciona os valores dessa row
    filexml = md.parse('/xxx/cacti/{}' .format(pid))
    num = filexml.getElementsByTagName("v")
    # Variaveis principais da func
    teste1 = []   # Com valores duplicados
    norep = []    # Sem vlores duplicados
    outliers = []
    nan = 'NaN'
    for name in num:
        a = (name.firstChild.nodeValue)
        if a == nan:
            continue
        teste1.append(float(a))
    if sum(teste1) == 0:
        sys.exit()
    #Remove duplicados da lista1
    for i in teste1:
        if i not in norep:
            norep.append(float(i))
    meand = ((statistics.mean(norep)))    # Mean, média dos valores da lista norep
    stand = ((statistics.stdev(norep)))   # Desvio padrão da lista norep
    # Calculo para definir quais valores são spikes, i = valor, meand = média, stand = desvio padrão
    for i in norep:
        z = ((i - meand) / stand)
        #print(i,z)
        if z >= 10:
            outliers.append(i)
           # print(i,z)
        else:
            continue
    if not outliers:
        #print('No spike')
        os.system('rm /xxx/cacti/{}' .format(pid))
        sys.exit()

    if len(sys.argv) == 1:
        print('No arg')
        sys.exit()

dump()
semaforo_e_validacoes()
main()
backup()
restore()