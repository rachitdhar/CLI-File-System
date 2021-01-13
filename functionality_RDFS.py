#The programming of this module began on 04/02/2020
#Creator: Rachit Dhar

#**********************************************************************************************

import memManager_RDFS as mem
import systemReboot_RDFS as sysReboot

fold_count = 0

def maincmds(cmd, path, cursor, db):
    #executing one of the commands defined in the RDFS system
    if cmd.lower() == "use-py":
        py_interpreter()
        return 0
    elif cmd.split("->")[0].lower() == "mkfold":
        make_folder(cmd.split("->")[1], path, db, cursor)
        return 0
    elif cmd.split("->")[0].lower() == "delfold":
        del_folder(cmd.split("->")[1], path, db, cursor)
        return 0
    elif cmd.lower() == "showfolds":
        showfolds(path, cursor)
        return 0
    elif cmd.split("->")[0].lower() == "into":
        result = into_folder(cmd.split("->")[1], path, cursor)
        if result != "":
            return result
        else:
            return 0
    elif cmd.lower() == "back":
        result = back(path)
        if result != "non-existent":
            return result
        else:
            return 0
    elif cmd.lower() == "clearfolds":
        clearfolds(path, cursor, db)
        return 0
    elif cmd.lower() == "back+": #to go back straight to the rdfs drive
        return "rdfs:\\"
    elif cmd.split("->")[0].lower() == "save":
        filepath = cmd.split("->")[1]
        mem.saveFile(path=path, fpath=filepath, cursor=cursor, db=db, action=0)
        return 0
    elif cmd.lower() == "showfiles":
        showfiles(path, cursor)
        return 0
    elif cmd.split("->")[0].lower() == "del":
        name = cmd.split("->")[1]
        mem.delFile(path=path, name=name, cursor=cursor, db=db, action=0)
        return 0
    elif cmd.lower() == "showpaths":
        if not path=="rdfs:\\":
            showpaths(path, cursor)
        else:
            print("This command can only be used within a folder, not a drive.")
        return 0
    elif cmd.lower() == "numpaths":
        if not path=="rdfs:\\":
            numpaths(path, cursor)
        else:
            print("This command can only be used within a folder, not a drive.")
        return 0
    elif cmd.split("->")[0].lower() == "send":
        name = cmd.split("->")[1]
        mem.retrieve_file(name=name, path=path, cursor=cursor, action=0)
        return 0
    elif cmd.split("->")[0].lower() == "extract":
        #save the file and then delete the original one (the one on the computer system)
        filepath = cmd.split("->")[1]
        mem.saveFile(path=path, fpath=filepath, cursor=cursor, db=db, action=0)
        try:
            import os
            os.remove(filepath)
            print("Original file deleted from the computer system")
        except:pass
        return 0
    elif cmd.split("->")[0].lower() == "dump":
        #to perform combined function of 'send' and 'del' commands
        name = cmd.split("->")[1]
        mem.retrieve_file(name=name, path=path, cursor=cursor, action=0)

        #checking if the file exists in the folder
        if path == "rdfs:\\":
            cursor.execute('select* from drivef')
        else:
            cursor.execute('select* from '+path.split("\\")[-2]+'_files')
        
        x = cursor.fetchall()
        check = False
        for i in x:
            if i[0] == name: check = True

        if check == True:
            mem.delFile(path=path, name=name, cursor=cursor, db=db, action=0)
        return 0
    elif cmd.lower() == "cls":
        from os import system
        system('cls')
        return 0
    elif cmd.split("->")[0].lower() == "cmd":
        from os import system
        system(cmd.split('->')[1])
        return 0
    elif cmd.split("->")[0].lower() == "hide":
        fname = cmd.split("->")[1]
        hidefold(fname, path, cursor, db)
        return 0
    elif cmd.split("->")[0].lower() == "unhide":
        fname = cmd.split("->")[1]
        unhidefold(fname, path, cursor, db)
        return 0
    elif cmd.lower() == "updatehex":
        update_hexmem()
        return 0
    elif cmd.split("->")[0].lower() == "writenew":
        name = cmd.split("->")[1]
        writetext(name, path, cursor, db)
        return 0
    elif cmd.split("->")[0].lower() == "read":
        name = cmd.split("->")[1]
        readtext(name, path, cursor)
        return 0
    elif cmd.split("->")[0].lower() == "write":
        name = cmd.split("->")[1]
        appendtext(name, path, cursor, db)
        return 0
    elif cmd.lower() == "reboot":
        sysReboot.systemReboot(cursor=cursor, db=db, scenario=2)
        return 0
    else:
        #in case user enters anything that is not a defined command
        print("'",cmd,"'", " is not recognized as a command.\n"\
            "To see the list of pre-defined commands, use the 'help' command.")
        return 0

#--------------------------------------------------------------------------------------------#
#                           CODES FOR FUNCTIONALITY OF COMMANDS                              #
#--------------------------------------------------------------------------------------------#

#To be able to use a python 'interpreter' within the file system
def py_interpreter():
    pyinput = str()
    while True:
        pyinput = input(">>>") # interpreter taking in a line of python code
        pylines = ""
        if pyinput[-1] == ":":
            line = ""
            while line != "\n":
                print(">>>",end='')
                line = ("\n" + input())
                pylines += line.rstrip()
        if pyinput.lower() == "exit-py": # exit-py will be used in order to leave the python interpreter
            break
        try:
            exec(pyinput + pylines) #executing the python code
        except:
            print("----------------EXECUTION STOPPED!!----------------")
            print("--------Your Python code produced an Error!!-------") #in case of any error

#to create a folder within the existing folder (or within rdfs drive in case path is "rdfs:\")
def make_folder(name, path, db, cursor):
    if path == "rdfs:\\":
        #getting a list of all folders in the allfolds to make sure the new folder is unique
        folds = list()
        cursor.execute('select* from allfolds')
        for i in cursor.fetchall():
            folds += i
        
        if name not in folds:
            try:                             
                cursor.execute('insert into drive values("'+name+'")')
                db.commit()
                cursor.execute('insert into allfolds values("'+name+'")')
                db.commit()
                print("New Folder '",name,"' Created Successfully.")
                
                #creating a new table with its name being the name of the newly created folder (for storing sub-folders)
                cursor.execute('create table '+name+'('+name+'Folders varchar(200))')
                db.commit()

                #creating a new table with its name being the name of the newly created folder (for storing files)
                cursor.execute('create table '+name+'_files'+'('+name+'Files varchar(200))')
                db.commit()
            except:
                print("Name Length must be less than 30 bits") 
        else:
            print("Sorry. This name already exists. Try again using a new name.")
    else:
        #getting a list of all folders in the allfolds to make sure the new folder is unique
        folds = list()
        crntFold = path.split("\\")[-2]
        cursor.execute('select* from allfolds')
        for i in cursor.fetchall():
            folds += i
        
        if name not in folds:
            try:                             
                cursor.execute('insert into '+crntFold+' values("'+name+'")')
                db.commit()
                cursor.execute('insert into allfolds values("'+name+'")')
                db.commit()
                print("New Folder '",name,"' Created Successfully.")
                
                #creating a new table with its name being the name of the newly created folder (for storing sub-folders)
                cursor.execute('create table '+name+'('+name+'Folders varchar(200))')
                db.commit()

                #creating a new table with its name being the name of the newly created folder (for storing files)
                cursor.execute('create table '+name+'_files'+'('+name+'Files varchar(200))')
                db.commit()
            except:
                print("Name Length must be less than 30 bits") 
        else:
            print("Sorry. This name already exists. Try again using a new name.")

#code to delete all files existing within a folder that is to be deleted
def destroyFiles(fold, db, cursor):
    #copying a list of all file names in the deleted folder, and then deleting those files from memory
    cursor.execute('select* from '+fold+'_files')
    x = cursor.fetchall()
    files = list()
    for i in x:
        files.append(i[0])
    
    lines = list()
    with open("D:\\memory_RDFS.txt", 'r') as f:
        lines = f.readlines()

    cursor.execute('select* from memAddr')
    mem_list = cursor.fetchall()

    for i in range(len(lines)):
        if lines[i].split(":")[0] == "#>>----------MemoryAddress":
            address = lines[i].split(":")[1].split("-")[0]
            for j in mem_list:
                if j[0]==address:
                    if j[1] in files:
                        lines[i+1] = ""

                        #clear the file name from memAddr
                        cursor.execute('update memAddr set FileName="" where Memory_Location="'+j[0]+'"')
                        db.commit()              
    
    for i in range(len(lines)):
                if i < len(lines) - 1:
                    if "\n" not in lines[i]:
                        lines[i] += "\n"

    with open("D:\\memory_RDFS.txt", 'w') as f:
        f.writelines(lines)

#to delete a folder within the existing folder (or within rdfs drive in case path is "rdfs:\")
def del_folder(name, path, db, cursor):
    #getting a list of all folders in the allfolds to make sure the new folder is unique
    folds = list()
    cursor.execute('select* from allfolds')
    for i in cursor.fetchall():
        folds += i
    
    if name in folds:
        if path == "rdfs:\\":
            #delete the subfolders if they exist
            cursor.execute('select* from '+name)
            c = cursor.fetchall()

            if len(c) > 0:
                for i in c:
                    del_folder(i[0], path+name+"\\", db, cursor)

            cursor.execute('delete from drive where Drive_Folders="'+name+'"')
            db.commit()

            destroyFiles(name, db, cursor)

            #destroy the table of the files in the deleted folder
            cursor.execute('drop table '+name+'_files')
            db.commit()
        else:
            #delete the subfolders if they exist
            cursor.execute('select* from '+name)
            c = cursor.fetchall()

            if len(c) > 0:
                for i in c:
                    del_folder(i[0], path+name+"\\", db, cursor)
            
            #remove folder name from table of the main folder
            cursor.execute('delete from '+path.split("\\")[-2]+' where '+path.split("\\")[-2]+'Folders="'+name+'"')
            db.commit()

            destroyFiles(name, db, cursor)

            #destroy the table of the files in the deleted folder
            cursor.execute('drop table '+name+'_files')
            db.commit()
        
        cursor.execute('delete from allfolds where Folders="'+name+'"')
        db.commit()
        print("The Folder '",name,"' has been Deleted Successfully.")

        #destroy the table for that folder

        cursor.execute('drop table '+name)
        db.commit()          
    else:
        print("Sorry. This folder does not exist")

#to show the list of folders in the current folder (or drive, in case of path being "rdfs:\")
def showfolds(path, cursor):
    crntFold = path.split("\\")[-2]
    #getting a list of all folders in the current folder
    if path == "rdfs:\\":
        cursor.execute('select* from drive')
    else:
        cursor.execute('select* from '+crntFold)
    
    c = cursor.fetchall()
    if len(c) > 0:
        folds = list()
        cursor.execute('select* from hide')
        x = cursor.fetchall()
        for i in c:
            #to consider only those folders that are not hidden
            if not x == []:
                if i[0] not in x[0]:
                    folds.append(i[0])
            else:
                folds.append(i[0])  
        
        #printing the names of folders, 4 folder names per row
        for j in range(len(folds)):
            if j%4==0 and j>0:
                print('\n', end='')
            print(folds[j]+'\t',end='')
        print('\n',end='')    
    else:
        print("No Folders added yet.")

#to show the list of files in the current folder (or drive, in case of path being "rdfs:\")
def showfiles(path, cursor):
    crntFold = path.split("\\")[-2]
    #getting a list of all files in the current folder
    if path == "rdfs:\\":
        cursor.execute('select* from drivef')
    else:
        cursor.execute('select* from '+crntFold+'_files')
    
    c = cursor.fetchall()
    if len(c) > 0:
        files = list()
        for i in c:
            files.append(i[0])
        
        #printing the names of files, 4 file names per row
        for j in range(len(files)):
            if j%4==0 and j>0:
                print('\n', end='')
            print(files[j]+'\t',end='')
        print('\n',end='')    
    else:
        print("No Files added yet.")

#to select a folder and go into it
def into_folder(name, path, cursor):
    newpath = str()
    folder_exists = False
    crntFold = path.split("\\")[-2]
    if path == "rdfs:\\":
        cursor.execute('select* from drive')
    else:
        cursor.execute('select* from '+crntFold)
    
    for i in cursor.fetchall():
        if i[0] == name:
            folder_exists = True
            break
    if folder_exists == False:
        print("Sorry, this folder is non-existent.")
        newpath = ""
    else:
        newpath = path + name + "\\"
    return newpath

#to come out of the current folder
def back(path):
    if path == "rdfs:\\":
        print("This is the Main Drive.\nCannot go back further since no previous folder/drive exists.")
        return "non-existent"
    else:
        s = path.split("\\")[:-2]
        newpath = str()
        for i in s:
            newpath += i
            newpath += "\\"
        return newpath

#to delete all folders in the current folder (or drive)
def clearfolds(path, cursor, db):
    if path == "rdfs:\\":
        cursor.execute("select* from drive")
        c = cursor.fetchall()
        if len(c) != 0:
            for m in c:
                #delete the subfolders if they exist
                cursor.execute('select* from '+m[0])
                k = cursor.fetchall()

                if len(k) > 0:
                    for i in k:
                        del_folder(i[0], path+m[0]+"\\", db, cursor)

                cursor.execute('delete from allfolds where Folders="'+m[0]+'"')
                db.commit()

                destroyFiles(m[0], db, cursor)

                #destroy the table of the files in the deleted folder
                cursor.execute('drop table '+m[0]+'_files')
                db.commit()

                #destroy the table for that folder

                cursor.execute('drop table '+m[0])
                db.commit()   
            cursor.execute('delete from drive')
            db.commit()
            print("The Folders have been Deleted Successfully.")
        else:
            print("The Drive is Empty. No folders available for deletion")
    else:
        crntFold = path.split("\\")[-2]
        cursor.execute("select* from "+crntFold)
        c = cursor.fetchall()
        if len(c) != 0:
            for m in c:
                #delete the subfolders if they exist
                cursor.execute('select* from '+m[0])
                k = cursor.fetchall()

                if len(k) > 0:
                    for i in k:
                        del_folder(i[0], path+m[0]+"\\", db, cursor)

                cursor.execute('delete from allfolds where Folders="'+m[0]+'"')
                db.commit()

                destroyFiles(m[0], db, cursor)

                #destroy the table of the files in the deleted folder
                cursor.execute('drop table '+m[0]+'_files')
                db.commit()

                #destroy the table for that folder

                cursor.execute('drop table '+m[0])
                db.commit()
            
            cursor.execute('delete from '+crntFold)
            db.commit()
            print("The Folders have been Deleted Successfully.")
        else:
            print("The Drive is Empty. No folders available for deletion")

#recursive function for going through all possible subfolders (this function is made for the showpaths() function to work)
def subfolds(foldpath, cursor):
    cursor.execute('select* from '+foldpath.split("---")[-1])
    c = cursor.fetchall()

    #going to the next folders within current folder
    if len(c) > 0:
        for i in c:
            subfolds(foldpath+"---"+i[0], cursor)
    else:
        #if no further subfolders exist, then print the path obtained
        print(foldpath)

#to show a list of all possible paths that could be taken from the current folder
def showpaths(path, cursor):
    crntFold = path.split("\\")[-2]
    import getpass
    p = getpass.getpass(prompt="Enter Password: ", stream=None)
    cursor.execute('select* from pathspass')
    c = cursor.fetchall()
    if p == c[0][0]:
        subfolds(crntFold, cursor)
    else:
        print("Incorrect password.")

#to count number of paths starting from current folder
def numsubfolds(foldpath, cursor):
    global fold_count
    cursor.execute('select* from '+foldpath.split("---")[-1])
    c = cursor.fetchall()

    #going to the next folders within current folder
    if len(c) > 0:
        for i in c:
            numsubfolds(foldpath+"---"+i[0], cursor)
    else:
        #if no further subfolders exist, then add 1 to the count
        fold_count += 1

def numpaths(path, cursor):
    global fold_count
    fold_count = 0
    crntFold = path.split("\\")[-2]
    numsubfolds(crntFold, cursor)
    print("There are "+str(fold_count)+" possible paths")

def hidef(fname, path, cursor, db):
    #checking if the subfolder exists in the current folder
    if path == "rdfs:\\":
        cursor.execute('select* from drive')
    else:
        cursor.execute('select* from '+path.split("\\")[-2])
    
    x = cursor.fetchall()
    check = False
    for i in x:
        if i[0] == fname: check = True

    if check == True:
        #hide the folder and secure with a passcode
        import getpass
        pcode = getpass.getpass(prompt='Enter Passcode to secure the folder: ', stream=None)
        cursor.execute('insert into hide values("'+fname+'","'+pcode+'")')
        db.commit()
        print("Folder hidden securely.")
    else:
        print("This folder does not exist on the current path.")

def hidefold(fname, path, cursor, db):
    #to check if folder is not already hidden
    cursor.execute('select* from hide')
    c = cursor.fetchall()
    if not c == []:
        if fname not in c[0]:
            hidef(fname, path, cursor, db)
        else:
            print("This folder is already hidden.")
    else:
        hidef(fname, path, cursor, db) 

def unhidef(fname, path, cursor, db):
    #checking if the subfolder exists in the current folder
    if path == "rdfs:\\":
        cursor.execute('select* from drive')
    else:
        cursor.execute('select* from '+path.split("\\")[-2])
    
    x = cursor.fetchall()
    check = False
    for i in x:
        if i[0] == fname: check = True

    if check == True:
        #Check if passcode entered is correct and unhide the folder
        import getpass
        pcode = getpass.getpass(prompt='Enter Passcode: ', stream=None)

        cursor.execute('select Passcode from hide where Folders="'+fname+'"')
        p = cursor.fetchall()
        
        if pcode == p[0][0]:
            cursor.execute('delete from hide where Folders="'+fname+'"')
            db.commit()
            print("Folder unhidden successfully.")
        else:
            print("Incorrect password.")
    else:
        print("This folder does not exist on the current path.")

def unhidefold(fname, path, cursor, db):
    #to check if folder is hidden
    cursor.execute('select* from hide')
    c = cursor.fetchall()
    if not c == []:
        if fname in c[0]:
            unhidef(fname, path, cursor, db)
        else:
            print("This folder is not hidden.")
    else:
        unhidef(fname, path, cursor, db)

# to update the hexmemory_RDFS.txt file as per the latest memory_RDFS.txt file
# function created on 29/10/2020
def update_hexmem():
    data = str()
    with open("D:\\memory_RDFS.txt", 'r') as f:
        data = f.read()

    with open("D:\\hexmemory_RDFS.txt", 'w') as f:
        lines = data.split('\n')
        for l in lines:
            newl = ""
            if l.split(":")[0] == "#>>----------MemoryAddress":
                newl = l
            elif l == "":
                newl = l
            else:
                bin_list = l.split(' ')
                hex_list = [hex(int(i, 2)) for i in bin_list]
                newl = (' ').join(hex_list)
            f.write(newl+'\n')

    print("Updated hexmemory_RDFS.txt file successfully.")

#to write text files from our file system itself
def writetext(name, path, cursor, db):
    #Instructions
    print("Write your text below.")
    print("Once you go to the next line, you cannot edit the previous lines.")
    print("Type '~exit-txt' when you are done writing the text file.")
    print("Type '~abort' if you want to close the file without saving it.")
    print("___________________________________________________________________")
    print("\n")

    abort = False

    #create a dummy text file to store all the text while it's entered
    filepath = "D:\\"+name.rstrip('.txt')+".txt"
    with open(filepath, 'w') as f:
        line = str()
        while True:
            line = input()
            if (line == "~exit-txt") or (line == "~abort"):
                if line == "~abort":
                    abort = True
                print("___________________________________________________________________")
                break
            else: 
                f.write(line+'\n')
                    
    #'extract' the dummy file (to save it's data onto our memory while deleting the original dummy file)
    if abort == False:
        mem.saveFile(path=path, fpath=filepath, cursor=cursor, db=db, action=0)
    else:
        print("File closed without saving. File not created.")
    import os
    os.remove(filepath)

#to read a text file (as long as it actually exists on the current path)
def readtext(name, path, cursor):
    #retrieve file (if it exists) to make a dummy file
    mem.retrieve_file(name, path, cursor, 1)

    #read the textfile (if it exists)
    filepath = "D:\\"+name
    data = str()
    check = True
    try:
        with open(filepath, 'r') as f:
            data = f.read()
    except:check = False

    if check == True:
        #print the data obtained line by line
        print("___________________________________________________________________")
        print('\n')
        lines = data.split('\n')
        for l in lines:
            print(l)
        print("___________________________________________________________________")

        #remove the dummy file on the computer system
        import os
        os.remove(filepath)

#To append text to an already existing text file saved in the memory
def appendtext(name, path, cursor, db):
    #firstly read the contents of the file upto the last written line
    #retrieve file (if it exists) to make a dummy file
    mem.retrieve_file(name, path, cursor, 1)

    #read the textfile (if it exists)
    filepath = "D:\\"+name
    data = str()
    check = True
    try:
        with open(filepath, 'r') as f:
            data = f.read()
    except:check = False

    if check == True:
        #Instructions
        print("Write your text below.")
        print("Once you go to the next line, you cannot edit the previous lines.")
        print("Type '~exit-txt' when you are done writing the text file.")
        print("Type '~abort' if you want to close the file without saving the changes.")
        print("___________________________________________________________________")
        print('\n')

        abort = False

        #print the data obtained line by line
        lines = data.split('\n')
        for l in lines:
            print(l)
        
        #appending the data entered into the dummy file
        with open(filepath, 'a') as f:
            while True:
                line = input()
                if (line == "~exit-txt") or (line == "~abort"):
                    if line == "~abort":
                        abort = True
                    print("___________________________________________________________________")
                    break
                else: 
                    f.write(line+'\n')
                    
        if abort == False:
            #to delete the existing file from rdfs memory, and instead saving the newly updated version
            mem.delFile(path=path, name=name, cursor=cursor, db=db, action=1)
            mem.saveFile(path=path, fpath=filepath, cursor=cursor, db=db, action=1)
            print("File updated successfully.")
        else:
            print("File closed without saving any new changes.")

        #remove the dummy file on the computer system
        import os
        os.remove(filepath)
