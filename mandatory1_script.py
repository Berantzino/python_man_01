import sys
import os
import glob
import subprocess
from urllib.request import urlopen
from urllib.error import HTTPError
import fileinput


# Opens the link and reads the content of it into a file "repository_info.txt"
def getRepoInfo():
    try:
        response = urlopen("https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100")
        txt = response.read().decode("UTF-8")
        file = open("repository_info.txt", "w")
        file.write(txt)
        file.close()
    except HTTPError as err:
        print(err)
    except Exception as err:
        print(err)

getRepoInfo()

# Opens the file "repository_info.txt"

def openFile(fileName):
    try:
        file = open(fileName)
        text = file.read()
        file.close()
    except FileNotFoundError as FNF:
        print(FNF)
    return text

text = openFile("repository_info.txt")

# Adds the starting indexes for every clone url

def getCloneUrlStartIndex(txt):
    cloneLinkIndexList = []
    i = 0
    searchString = "clone_url"
    while i < txt.count(searchString):
        if not cloneLinkIndexList:
            cloneLinkIndexList.append(txt.find(searchString, i) + 12)
            i += 1
        else:
            cloneLinkIndexList.append(txt.find(searchString, cloneLinkIndexList[-1] + 1) + 12)
            i += 1
    return searchString, cloneLinkIndexList

searchString, cloneLinkIndexList = getCloneUrlStartIndex(text)

# Grabs the link with use of the indexes above

def getCloneLinks(linkIndexList):
    cloneLinkList = []
    i = 0
    while i < text.count(searchString):
        cloneLinkList.append(text[cloneLinkIndexList[i] : text.find(",", cloneLinkIndexList[i]) -1])
        i += 1
    return cloneLinkList

cloneLinkList = getCloneLinks(cloneLinkIndexList)

# Creates new folder "repositories"

def createFolder(name):
    try:
        os.mkdir(name)
    except FileExistsError as FEE:
        print(FEE)

createFolder("repositories")

# Changes into folder "repositories"
os.chdir("repositories")

# Clones the remote repository from the list of links, pulls if they already exist
def cloneOrPullRepo():
    for url in cloneLinkList:
        if url[49:-4] not in os.listdir("."):
            subprocess.run(["git", "clone", url])
        else:
            os.chdir(url[49:-4])
            subprocess.run(["git", "pull"])
            os.chdir("..")

cloneOrPullRepo()

# go up 1 folder
os.chdir("..")

# Adds the path for every README.md file
readMePathList = glob.glob("**/README.md", recursive=True)

# Adds the required reading bullet points to a list
def findRequired(pathList):
    requiredReading = []
    for f in pathList:
        with open(f, "rt") as f1:
            lines = f1.read()
            lines = lines[lines.find("## Required reading") : lines.find("## Supplementary reading")]
            lines = lines[lines.find("## Required reading") : lines.find("### Supplementary reading")]
            lines = lines[lines.find("## Required reading") : lines.find("## Required reading paragraph")]
            requiredReading.append(lines)
    return requiredReading

requiredReading = findRequired(readMePathList)

# Creates a directory "curriculum"
createFolder("curriculum")

os.chdir("curriculum")

def writeFile(list):
    try:
        file = open("required_reading.md", "w")
        for line in list:
            file.write(line)
        file.close()
    except Exception as e:
        print(e)

writeFile(requiredReading)

# Removes "## Required reading" from the file
def removeHeader():
    try:
        f = open("required_reading.md", "r")
        lines = f.readlines()
        f.close()
        f = open("required_reading.md", "w")
        for line in lines:
            line = line.replace("## Required reading", "")
            f.write(line)
        f.close()
    except Exception as e:
        print(e)

removeHeader()


# Sort the file alphabetically
def sortFile():
    with open("required_reading.md", "r") as r:
        sortedFile = sorted(r)

    with open("required_reading.md", "w") as w:
        w.writelines(sortedFile)

sortFile()

# Remove whitespace and add spacing
for line in fileinput.FileInput("required_reading.md", inplace=1):
    if line.rstrip():
        print(line)

os.chdir("..")

subprocess.run(["cp", "-v", "curriculum/required_reading.md", "required_reading.md"])

# Push to github
#subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-a", "-m", "Required reading commit"])
subprocess.run(["git", "pull"])
subprocess.run(["git", "push"])