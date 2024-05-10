import os

def pickcomputer(): #when changing which computer I'm using
    paths = ["C:/Users/avboy/Documents/GitHub_Personal",
             "C:/Users/Avery B/Documents/My Documents/GitHub",
             "G:/Avery's funny business/Github"]
    for directory in paths:
        if os.path.exists(directory):
            return directory

    print("Error assigning computer directory in file pickcomputer.py.")
    exit()

directory = pickcomputer()