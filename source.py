#This is the File System: RDFS (Rachit Dhar File System)
#Project Began On 25/01/2020
#Program created and written by Rachit Dhar
#Project completed on 24/10/2020

#This is the main program file (i.e. the file that is to be executed)

#*********************************************************************************

import mysql.connector as sql
import time
import functionality_RDFS as rdfs
from tabulate import tabulate
import art
import getpass
import systemReboot_RDFS as sysReboot

#Name of App (RDFS is just the temporary name given by me while this program was still under development)
AppName = "asdf" #ASDF : Alternate System for Data Filing

#path of the current directory
path = "rdfs:\\"

#connect python to mysql and store database in db
db = object()
cursor = object()

while True:
    #ask user for mysql password
    #to get the password from the user while displaying nothing on the console
    try:
        pword = getpass.getpass()
        db = sql.connect(host='localhost', user='root', passwd=pword)
        cursor = db.cursor()
        break
    except:
        print("Wrong Password. Try Again")

while True:
    try:
        cursor.execute('use rdfs')
        db.commit()
        break
    except:
        print("System compromised. RDFS database does not exist.")
        time.sleep(1)
        print("Initiating systemReboot_RDFS.py")
        print("Executing scenario 1: Self-repair mode\n")
        sysReboot.systemReboot(cursor=cursor, db=db, scenario=1)  

#help command
def help_cmd():
    cursor.execute('select* from help')
    results = cursor.fetchall()
    
    print(tabulate(results, headers=['Commands', 'Description'], tablefmt='psql'))

#execution of commands entered by the user
def execute_cmd(command):
    if command == "":
        return 2
    elif command.lower() == "help":
        help_cmd()
        return 0
    elif command.lower() == "exit":
        print("Thank you for spending your time here! Bye!")
        time.sleep(0.5)
        return 1
    else:
        #code for particular commands
        return rdfs.maincmds(cmd=command, path=path, cursor=cursor, db=db)

#starting the file system.
#creating the "rdfs: Drive", which shall be used just as we use the "D: Drive" in cmd

art.tprint(AppName)
print(" ASDF System (Alternate System for Data Filing)")
print(" Project started on 25th January 2020, and perfectly completed on 24th October 2020")
print(" Created by: Rachit Dhar")
print("\n")

while True:

    #providing space for user to write the commands
    #should display the path to the current directory (as in cmd)
    print(path + ">",end="")
    command = input()

    #execute the command entered by the user. store a return value in output. 
    #If output = 0, then continue the loop, but otherwise (eg: in case of exit command) break the loop
    output = execute_cmd(command)

    if output == 0:
        print('\n',end='')
        continue
    elif output == 2:
        continue
    elif output == 1:
        break
    else:
        #in case when path is changed then output will contain the new path, which is to be copied into the variable path
        path = output

#diconnecting from MySQL server
db.close()
