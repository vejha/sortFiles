#!/usr/bin/env python3
import glob
import os
import shutil
import hashlib
import sys


def moveFiles(extList, dstFolder):
    for i in extList:
        fileList = glob.glob(i)
        if fileList:  # Check if the list is empty
            for fileName in fileList:
                dstFile = os.path.join(dstFolder, fileName)
                if os.path.isfile(dstFile):
                    # Resolve files with the same name
                    if md5(fileName) == md5(dstFile):
                        os.remove(dstFile)
                    else:
                        oldFileName = fileName
                        fileName = fileName + ' (1)'
                        os.rename(oldFileName, fileName)
                shutil.move(fileName, dstFolder)


def moveDirs(folderList, dstFolder):
    dirList = glob.glob('*/')
    print(dirList)
    for dirName in dirList:
        try:
            dirNoSuffix = dirName.split(' [')
            print(dirNoSuffix[0])
            if dirNoSuffix[0] in folderList:
                continue
        except:
            continue
        shutil.move(dirName, dstFolder)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def mkDir(dirName):
    try:
        os.makedirs(dirName)
    except:
        pass


def noFiles(dir_name):
    file_list = os.listdir(dir_name)  # dir is your directory path
    root = os.getcwd()
    for item in file_list:
        if item[0] == '.':
            file_list.remove(item)
        if os.path.isfile(os.path.join(root, item)):
            item
    return len(file_list)


# os.path.getmtime(file) # Time of file modification

# os.path.getctime(file) # Time of file creation

#############################################################################################
dst_dir = None
if len(sys.argv):
    dst_dir = sys.argv[1]

if dst_dir and os.path.exists(dst_dir):
    os.chdir(dst_dir)
else:
    try:
        os.chdir(os.path.dirname(__file__))
    except:
        pass

# Folder names and File extensions

folderExt = dict(Archives=('*.rar', '*.zip', '*.7z', '*.iso', '*.arc', '*.tar.gz', '*.tar.xz', '*.tgz', '*.deb'),
                 Images=('*.jpeg', '*.jpg', '*.JPG', '*.png', '*.PNG', '*.gif', '*.bmp', '*.svg', '*.fig'),
                 Documents=('*.doc', '*.docx', '*.xls', '*.xlsx', '*.odt', '*.ods', '*.ppt', '*.pptx'),
                 PDFs=('*.pdf', '*.PDF', '*.xxx'),
                 Videos=('*.avi', '*.mp4', '*.mpeg', '*.mpg', '*.mkv', '*.flv', '*.mov', '*.wmv'),
                 Audio=('*.mp3', '*.flac', "*.wma", '*.wav', '*.3gpp'),
                 Executables=('*.exe', '*.bat', '*.sh', '*.jar'),
                 Other=('*.txt', '*.csv', '*.STL', '*.drl', '*.gbr', '*.dxf', '*.gcode'))


# Folder names
folderList = folderExt.keys()

for folderName in folderList:
    fileExt = folderExt[folderName]
    oldName = glob.glob(folderName + "*")
    if len(oldName) == 0:
        mkDir(folderName)
        oldName = folderName
    else:
        oldName = oldName[0]

    # Move files
    moveFiles(fileExt, oldName)

    # Count files in folders and change their names
    folderCount = str(noFiles(oldName))
    # print(folderCount)
    newName = folderName + " [" + folderCount + "]"
    os.rename(oldName, newName)


# Sort folder
folderName = 'Folders'
oldName = glob.glob(folderName + "*")
if len(oldName) == 0:
    mkDir(folderName)
    oldName = folderName
else:
    oldName = oldName[0]

moveDirs(folderList, oldName)
# Count files in folders and change their names
folderCount = str(noFiles(oldName))
newName = 'Folders' + " [" + folderCount + "]"
os.rename(oldName, newName)
