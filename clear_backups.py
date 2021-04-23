#!/usr/bin/env python

import sys, os
import time, datetime
import getopt

def helper():
    print ('Usage:  clear_backups.py [-p path] [-P project] [-n number_of_files]\
\nOptions:\
\n-p, --path=<string>                   Path to backup. Default - local folder\
\n-P, --project=<string>                Project name\
\n-n, --surviving_files=<number>        Number of files not deleted\
\n-e, --ext=<string>                    Files extension\
\n-h, --help\
')

def wrLog(msg):
    if not os.path.exists('log'):
        os.makedirs('log')
    log_file='log/out.log'
    logfile = open(log_file, "a")
    t = time.strftime("%Y-%m-%d %H:%M:%S ")
    logfile.write(t + msg + '\n')
    logfile.close()

def fileClear(path,project,surviving_files,ext):
    full_path = path+"/"+project
    full_list = []
    try:
        for i in os.listdir(full_path):
            if i.endswith(ext):
                full_list.append(os.path.join(full_path, i))
    except OSError as e:
        print (e)
        sys.exit()
    time_sorted_list = sorted(full_list, key = os.path.getmtime,reverse=True)[surviving_files:]
    if len(time_sorted_list) > 0:
        wrLog('INFO :: Files will be deleted: ' + ', '.join(time_sorted_list))
        print('INFO :: Delete file: ')
        for i in time_sorted_list:
            try:
                os.remove(i)
            except OSError as e:
                print ("ERROR:")
                sys.exit()
            print('\t %s' % (i))
    else:
        wrLog('INFO :: Nothing delete')
        print('INFO :: Nothing delete')

def main(argv):
    surviving_files = 5
    path = '.'
    project = ''
    ext = 'tar.gz'

    wrLog('INFO :: Start script...' + '#'*10)

    try:
        opts, args = getopt.getopt(argv,"hu:P:p:n:e:",["help","project=","path=","surviving_files=","ext="])
    except getopt.GetoptError:
        helper()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helper()
            sys.exit()
        elif opt in ("-P", "--project"):
            project = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-e", "--ext"):
            ext = arg
        elif opt in ("-n", "--surviving_files"):
            try:
                surviving_files = int(arg)
            except:
                wrLog('ERROR :: Invalid days value - ' + arg)
                helper()
                sys.exit()
    if project and surviving_files>=0:
        fileClear(path,project,surviving_files,ext)
    else:
        helper()
        sys.exit()

main(sys.argv[1:])
