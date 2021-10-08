# To completely wipe the memory and the rdfs database, and create new, fresh versions of them
#-----------------------------------------------------------------------------------------------------
# To ONLY be used in two circumstances:

#       1. In case the source code (python program) is run on a new computer, or a computer
#          that has no memory_RDFS.txt file and no rdfs database written on it already.
#          (My own computer had these two things created independently by me during the development
#           of the RDFS system, and hence I didn't originally need to write any code that will create
#           these two for me.)
#          [ONLY the PROGRAM can decide to act on this scenario]

#       2. In case the memory or the database table(s) have been corrupted to an extent where the
#          the damage is irreversible, and hence the system must restart afresh. For this scenario,
#          the admin himself only can choose to reboot the system, since the reboot command shall be
#          password protected.
#          [ONLY the ADMIN can decide to act on this scenario]

#-----------------------------------------------------------------------------------------------------
# Written on 31/10/2020 by Rachit Dhar
#*****************************************************************************************************

import os
import time
import getpass

#Manual Reboot Authorization Code
CODE = "1234" #Keep a STRONG security code here!

#security protocol
def securityCheck():
    usercode = getpass.getpass()
    if usercode == CODE:
        time.sleep(2)
        print("\nHello Admin!")
        time.sleep(1)
        print("Let's clean up the mess.\n")
        time.sleep(1)
        return True
    else:
        return False

# Reboot the system
def systemReboot(cursor, db, scenario):
    check = True
    if scenario == 2:
        check = securityCheck()
    
    if check == True:
        i = 1
        while i<=60:
            print("=", end="")
            time.sleep(0.01)
            i += 1

        print("\n\nRunning system reboot...")
        print("Fresh Memory and RDFS Database will be created.")
        time.sleep(1)
        print("Reboot program systemReboot_RDFS.py has been initiated...")
        time.sleep(1)

        # to delete the memory file (if it exists) and create a new blank memory in its place
        mem_existed = bool()

        try:
            os.remove("D:\\memory_RDFS.txt")
            print("System memory wiped.")
            mem_existed = True
        except:mem_existed = False
        try:
            os.remove("D:\\hexmemory_RDFS.txt")
        except:pass

        # create the memory files
        mem = open("D:\\memory_RDFS.txt", 'w')
        hmem = open("D:\\hexmemory_RDFS.txt", 'w')
        mem.close()
        hmem.close()

        if mem_existed == False:
            print("New memory installed successfully.")
        else:
            print("Memory reinstalled successfully.")

        # to delete the rdfs database (if it exists)
        db_existed = bool()
        try:
            cursor.execute('drop database rdfs')
            db.commit()
            print("Database destroyed successfully.")
            db_existed = True
        except:
            db_existed = False
        
        #obtain password for the renewed file system
        new_pword = getpass.getpass()
        
        # create a new fresh rdfs database with the default tables
        queries = ['create database rdfs',\
                    'use rdfs',\
                    'create table allfolds(Folders varchar(200))',\
                    'create table drive(Drive_Folders varchar(200))',\
                    'create table drivef(Drive_Files varchar(200))',\
                    'create table hide(Folders varchar(200), Passcode varchar(100))',\
                    'create table memaddr(Memory_Location varchar(200), FileName varchar(200))',\
                    'create table pathspass(Password varchar(30))',\
                    'create table help(Commands varchar(30), Description varchar(200))',\
                    'insert into memaddr values("0x0", "")',\
                    'insert into pathspass values("'+new_pword+'")'
                    ]

        for query in queries:
            cursor.execute(query)
            db.commit()

        # to insert all rows of the help table
        help_table = [("help","To view all the available commands and their description"),                                           
                        ("exit","To leave the RDFS File System"),                                                                                                                 
                        ("use-py","To use the python interpreter within the file system"),                                                                                        
                        ("mkfold","To create a new folder within the current folder/drive using the syntax mkfold->NAME_OF_FOLDER"),                                              
                        ("delfold","To delete a folder within the current folder/drive using the syntax delfold->NAME_OF_FOLDER"),                                                
                        ("showfolds","To show a list of all folders within the current folder/drive"),                                                                            
                        ("into","To open one of the folders present inside your current folder/drive and enter it using the syntax into->NAME_OF_FOLDER"),                       
                        ("back","To come out of your current folder and go back to the previous folder in your path"),                                                            
                        ("clearfolds","To delete all folders within the current folder/drive"),                                                                                   
                        ("back+","To go back to the RDFS drive folder"),                                                                                                          
                        ("save","To save a file to the RDFS Memory using the syntax save->PATH_TO_THE_FILE (with file extension)"),                                               
                        ("exit-py","To exit the python interpreter"),                                                                                                             
                        ("showfiles","To show the files associated with the current folder/drive"),                                                                               
                        ("del","To delete a file in current path using the syntax del->NAME_OF_FILE (with extension)"),                                                           
                        ("showpaths","To show a list of all possible paths that can be taken from the current folder."),                                                                   
                        ("numpaths","To count the number of possible paths that exist starting from the current folder"),                                                            
                        ("send","To retrieve a saved file from RDFS Memory and reproduce it onto the actual computer system, using syntax send->NAME_OF_FILE (with extension)"),     
                        ("extract","To save a file to the RDFS Memory while also deleting the one on the Computer system. Syntax: extract->PATH_TO_THE_FILE (with extension)"),         
                        ("dump","To perform the combined function of 'send' and 'del' commmands. Syntax: dump->NAME_OF_FILE (with extension)"),                                   
                        ("cls","To clear the whole screen"),                                                                                                                     
                        ("cmd","To execute a statement in command prompt, with syntax cmd->COMMAND_STATEMENT"),                                                                    
                        ("hide","To prevent a folder from being visible through showfolds command. Syntax: hide->NAME_OF_FOLDER"),                                     
                        ("unhide","To unhide a previously hidden folder. Syntax: unhide->NAME_OF_FOLDER"),                                                                        
                        ("updatehex","To update the hexmemory_RDFS.txt file (which displays the RDFS Memory in hexadecimal format)"),                                                      
                        ("writenew","To write a new text file, to be saved in RDFS system at the current path. Syntax: writenew->FILE_NAME (without extension)"),                         
                        ("read","To read a text file saved at the current path. Syntax: read->FILE_NAME (with extension)"),                                                           
                        ("write","To append new data into an already existent text file (present at the current path in the RDFS system). Syntax: write->FILE_NAME (with extension)"),
                        ("reboot","To destroy the existing memory and database, and rebuild a fresh RDFS System with a blank memory and database. [ADMIN ACCESS ONLY]")
                        ]

        for row in help_table:
            cursor.execute('insert into help values("'+row[0]+'","'+row[1]+'")')
            db.commit()
        
        if db_existed == False:
            print("New RDFS Database has been installed successfully.")
        else:
            print("Fresh RDFS Database reinstalled successfully.")

        # display closing comments
        print("\n")
        print("Database architecture constructed successfully.")
        print("Fresh memory file constructed.")
        print("All Processes completed")
        print("System reboot successful.")
        time.sleep(1)
        print("\nWelcome to the System!...\n")
        time.sleep(2)
        print("="*60)

    else:
        print("Wrong Authorization code. Permission NOT granted!")
