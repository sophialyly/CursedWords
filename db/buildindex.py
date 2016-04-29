import sys, os, re
from string import Template
from collections import defaultdict

notWord = re.compile("[^A-Za-z0-9]")
def encodeWord(word):
	response = ""
	for char in word:
		if notWord.match(char):
			response += "-" + repr(ord(char)) + "-"
		else:
			response += char
	return response

### BEGIN MAIN FUNCTION ###

chapI, pageI = 1, 1
fileTemp = Template("ch$c/p$p.txt")
index = defaultdict(list)
while True:
	while os.path.isfile(fileTemp.substitute(c=chapI, p=pageI)):
		file = open(fileTemp.substitute(c=chapI, p=pageI))
		for wordI, word in enumerate(file.read().split()):
			index[encodeWord(word)].append((chapI, pageI, wordI + 1))
		file.close()
		pageI += 1
	if pageI == 1:
		break
	print("Found chapter", chapI, "containing", pageI-1, "pages")
	chapI += 1
	pageI = 1

print("\nTotal words found:", len(index))

os.makedirs("index", exist_ok=True)
os.chdir("index")
existingIndexFiles = os.listdir()
removed = 0
for file in existingIndexFiles:
	if file[:-4] not in index.keys():
		os.remove(file)
		removed += 1
print(removed, "file(s) culled")

updated, created = 0, 0
for word, positions in index.items():
	fileContent = [",".join(str(x) for x in pos) for pos in positions]
	fileName = word + ".txt"
	if fileName in existingIndexFiles:
		existingFile = open(fileName)
		i = 0
		for line in existingFile:
			if i >= len(fileContent) or line.strip() != fileContent[i]:
				existingFile.close()
				break
			i += 1
		else:
			existingFile.close()
			if i == len(fileContent):
				continue
		updated += 1
	else:
		created += 1
	indexFile = open(fileName, mode="w")
	for line in fileContent:
		print(line, file=indexFile)
	indexFile.close()

print(created, "file(s) created")
print(updated, "file(s) updated")
print("Finished building index")
