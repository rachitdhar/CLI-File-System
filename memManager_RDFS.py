#The programming of this module began on 07/02/2020
#Creator: Rachit Dhar

#*****************************************************************************************************

#convert all data stored in a file from binary (or text) to hexadecimal form
def file_to_hex(fpath):
    try:
        data = str()
        with open(fpath, 'rb') as f:
            s = f.read()

            #code to be used to convert data to hexadecimal
            """
            hex_list = [hex(i) for i in s]
            data = (' '.join(hex_list))
            """

            #but I changed my mind as of 28/10/2020, so now I'll convert to Binary instead
            bin_list = [bin(i) for i in s]
            data = (' '.join(bin_list))

        return data
    except:
        return "non-existent"

#use hexadecimal data to make a binary file
def hex_to_file(data, name):
    bin_data = b''

    #old code, to get original data back from hexadecimal form
    """
    hex_list = data.split()  
    for i in hex_list:
        bin_data += bytes(chr(int(i, 16)).encode('utf-8'))
    """

    #new code as of 28/10/2020, to get original data back from binary form
    bin_list = data.split()
    for i in bin_list:
        bin_data += bytes(chr(int(i, 2)).encode('utf-8'))
    
    with open('D:\\'+name, "wb") as f:
        f.write(bin_data)

#saving the file to memory
def saveFile(path, fpath, cursor, db, action):
    #if the memory file is completely empty, then add the initial "0x0" address automatically
    isempty = False
    with open("D:\\memory_RDFS.txt", 'r') as f:
        if f.read() == "":
            isempty = True

    if isempty == True:
        isempty = False
        with open("D:\\memory_RDFS.txt", 'a') as f:
            f.writelines(['#>>----------MemoryAddress:0x0----------<<#\n', "\n"])
    
    data = file_to_hex(fpath)
    name = fpath.split("\\")[-1]

    if data == "non-existent":
        print("This file name does not exist at the specified path")
    else:
        #finding if any memory_location in memAddr table which is empty
        empty_mem_loc = False
        address = str()

        cursor.execute('select* from memAddr')
        mem_list = cursor.fetchall()

        #if finds, then add FileName there and return address
        for i in mem_list:
            if i[1] == "": #empty location
                address = i[0]
                empty_mem_loc = True
                cursor.execute('update memAddr set FileName="'+name+'" where Memory_Location="'+address+'"')
                db.commit()
                break
        
        #else creating a new address (1 greater than the last address created) and add FileName to it, and return that address
        if empty_mem_loc == False:
            #finding new address
            newadd = hex(int(mem_list[-1][0], 0)+1)
            #add to list of memory addresses
            cursor.execute('insert into memAddr values("'+newadd+'", "'+name+'")')
            db.commit()
            #add data to new memory space
            with open("D:\\memory_RDFS.txt", 'a') as f:
                f.writelines(["#>>----------MemoryAddress:"+newadd+"----------<<#\n", data+"\n"])
        else:
            #add data to existing memory space
            lines = list()
            with open("D:\\memory_RDFS.txt", 'r') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].split(":")[0] == "#>>----------MemoryAddress" and lines[i].split(":")[1] == address+"----------<<#\n":
                    lines[i+1] = data+"\n"
                    
            with open("D:\\memory_RDFS.txt", 'w') as f:
                f.writelines(lines)
        
        #add the name of this file to the table of filenames of the folder in which it was saved
        if path=="rdfs:\\":
            cursor.execute('insert into drivef values("'+name+'")')
        else:
            cursor.execute('insert into '+path.split("\\")[-2]+'_files'+' values("'+name+'")')
        db.commit()

        if action == 0:
            print("File has been saved successfully.")

#to delete a file from a folder as specified by the user, and then also delete it from memory
def delFile(path, name, cursor, db, action):
    #checking if the file exists in the folder, and then deleting it from memory
    if path == "rdfs:\\":
        cursor.execute('select* from drivef')
    else:
        cursor.execute('select* from '+path.split("\\")[-2]+'_files')
    
    x = cursor.fetchall()
    check = False
    for i in x:
        if i[0] == name: check = True

    if check == False:
        print("This file name does not exist at the specified path")
    else:
        lines = list()
        with open("D:\\memory_RDFS.txt", 'r') as f:
            lines = f.readlines()

        cursor.execute('select* from memAddr')
        mem_list = cursor.fetchall()

        jobdone = False
        for i in range(len(lines)):
            if lines[i].split(":")[0] == "#>>----------MemoryAddress":
                address = lines[i].split(":")[1].split("-")[0]
                for j in mem_list:
                    if j[0]==address:
                        if j[1] == name:
                            lines[i+1] = "\n"

                            #clear the file name from memAddr
                            cursor.execute('update memAddr set FileName="" where Memory_Location="'+j[0]+'"')
                            db.commit()
                            jobdone = True              
            if jobdone == True:
                break

        with open("D:\\memory_RDFS.txt", 'w') as f:
            f.writelines(lines)

        if path == "rdfs:\\":
            cursor.execute('delete from drivef where Drive_Files="'+name+'"')
        else:
            cursor.execute('delete from '+path.split("\\")[-2]+'_files where '+path.split("\\")[-2]+'Files ="'+name+'"')
        db.commit()
        
        if action == 0:
            print("File has been deleted successfully.")

#to send the file from memory to the computer's actual file system
def retrieve_file(name, path, cursor, action):
    #checking if the file exists in the folder
    if path == "rdfs:\\":
        cursor.execute('select* from drivef')
    else:
        cursor.execute('select* from '+path.split("\\")[-2]+'_files')
    
    x = cursor.fetchall()
    check = False
    for i in x:
        if i[0] == name: check = True

    if check == False:
        print("This file name does not exist at the specified path")
    else:
        lines = list()
        with open("D:\\memory_RDFS.txt", 'r') as f:
            lines = f.readlines()

        cursor.execute('select* from memAddr')
        mem_list = cursor.fetchall()

        jobdone = False
        for i in range(len(lines)):
            if lines[i].split(":")[0] == "#>>----------MemoryAddress":
                address = lines[i].split(":")[1].split("-")[0]
                for j in mem_list:
                    if j[0]==address:
                        if j[1] == name:
                            #retrieve data
                            data = lines[i+1]
                            #make a file in computer's actual file system from this data
                            hex_to_file(data, name)
                            jobdone = True         
            if jobdone == True:
                if action == 0:
                    print("File has been sent successfully.")                
                break
