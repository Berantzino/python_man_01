import sys
import os
import glob
import subprocess
from urllib.request import urlopen
from urllib.error import HTTPError
import fileinput


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
# Clone repos

try:
    file = open("repository_info.txt")
    txt = file.read()
    file.close()
except FileNotFoundError as FNF:
    print(FNF)

cloneLinkIndexList = []

i = 0
searchString = "clone_url"
while i < txt.count(searchString):
    if not cloneLinkIndexList:
        cloneLinkIndexList.append(txt.find(searchString, i) + 12)
        print("cloneLinkIndexList is empty")
        i += 1
    else:
        cloneLinkIndexList.append(txt.find(searchString, cloneLinkIndexList[-1] + 1) + 12)
        print(cloneLinkIndexList[-1])
        i += 1

cloneLinkList = []

i = 0
while i < txt.count(searchString):
    cloneLinkList.append(txt[cloneLinkIndexList[i] : txt.find(",", cloneLinkIndexList[i]) -1])
    i += 1

try:
    os.mkdir("repositories")
except FileExistsError as FEE:
    print(FEE)

os.chdir("repositories")

for url in cloneLinkList:
    if url[49:-4] not in os.listdir("."):
        subprocess.run(["git", "clone", url])
    else:
        os.chdir(url[49:-4])
        subprocess.run(["git", "pull"])
        os.chdir("..")

os.chdir("..")

readMePathList = []

# print(readMeList)
readMePathList = glob.glob("**/README.md", recursive=True)
# adds the content from the README.md files to a list

readMeContentList = []

for path in readMePathList:
    try:
        file = open(path)
        txt = file.read()
        readMeContentList.append(txt)
        file.close()
    except FileNotFoundError as FNF:
        print(FNF)
"""
i = 0
while i < len(readMePathList):
    try:
        file = open(readMePathList[i])
        txt = file.read()
        readMeContentList.append(txt)
        file.close()
        i += 1
    except FileNotFoundError as FNF:
        print(FNF)
"""
#print(readMeContentList)

requiredReading = []

for f in readMePathList:
    with open(f, "rt") as f1:
        lines = f1.read()
        lines = lines[lines.find("## Required reading") : lines.find("## Supplementary reading")]
        lines = lines[lines.find("## Required reading") : lines.find("### Supplementary reading")]
        lines = lines[lines.find("## Required reading") : lines.find("## Required reading paragraph")]
        requiredReading.append(lines)

# Creates a directory "curriculum"
try:
    os.mkdir("curriculum")
except FileExistsError as FEE:
    print(FEE)

os.chdir("curriculum")

try:
    print("create md")
    file = open("required_reading.md", "w")
    for line in requiredReading:
        file.write(line)
    file.close()
except Exception as e:
    print(e)

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


with open("required_reading.md", "r") as r:
    sortedFile = sorted(r)

with open("required_reading.md", "w") as w:
    w.writelines(sortedFile)

# Remove whitespace and add spacing
for line in fileinput.FileInput("required_reading.md", inplace=1):
    if line.rstrip():
        print(line)

# Push to github
#subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-a", "-m", '"Required reading commit"'])
subprocess.run(["git", "pull"])
subprocess.run(["git", "push"])