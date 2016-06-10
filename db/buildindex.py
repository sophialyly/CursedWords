import os, re
from string import Template
from collections import defaultdict

alphaRE = re.compile("[a-z]")
def encodeWord(word):
	word = word.lower()
	if re.match(alphaRE, word[0]):
		folder = word[0]
	else:
		folder = "0"
	encoded = ""
	for char in word:
		if char.isalnum():
			encoded += char
		else:
			encoded += "-" + repr(ord(char)) + "-"
	return folder, encoded

### BEGIN MAIN FUNCTION ###

chapI, pageI = 1, 1
fileTemp = Template("ch$c/p$p.txt")
index = defaultdict(lambda : defaultdict(list))
while True:
	while os.path.isfile(fileTemp.substitute(c=chapI, p=pageI)):
		with open(fileTemp.substitute(c=chapI, p=pageI),encoding="utf-8") as file:
			wordI = 1
			for line in file:
				for word in line.split():
					folder, encoded = encodeWord(word)
					index[folder][encoded].append((chapI, pageI, wordI))
					wordI += 1
		pageI += 1
	if pageI == 1:
		break
	print("Found chapter", chapI, "containing", pageI-1, "pages")
	chapI += 1
	pageI = 1

print("\nTotal words found:", sum(len(folder) for folder in index.values()))

os.makedirs("index", exist_ok=True)
os.chdir("index")
existingIndexFiles = {}
for folder in os.listdir():
	if not os.path.isdir(folder):
		print("Odd file found in index:", folder)
	else:
		existingIndexFiles[folder] = os.listdir(folder)
removed = 0
for folder, files in existingIndexFiles.items():
	if folder not in index:
		for file in files:
			os.remove(folder + "/" + file)
			removed += 1
		os.rmdir(folder)
	else:
		for file in files:
			if file[:-4] not in index[folder]:
				os.remove(folder + "/" + file)
				removed += 1
		
print(removed, "file(s) culled")

updated, created = 0, 0
for folder in index:
	for word, positions in index[folder].items():
		fileContent = [",".join(str(x) for x in pos) for pos in positions]
		fileName = word + ".txt"
		if folder in existingIndexFiles and fileName in existingIndexFiles[folder]:
			existingFile = open(folder + "/" + fileName,encoding="utf-8")
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
		os.makedirs(folder, exist_ok=True)
		with open(folder + "/" + fileName,mode="w",encoding="utf-8") as indexFile:
			for line in fileContent:
				print(line, file=indexFile)

print(created, "file(s) created")
print(updated, "file(s) updated")
print("Finished building index")
