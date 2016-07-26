import os
from string import Template
from trie import Trie, _node_iter

def encodeWord(word):
	word = word.lower()
	encoded = ''
	for char in word:
		if char.isalnum():
			encoded += char
		else:
			encoded += '-' + repr(ord(char)) + '-'
	return encoded

### READ ALL CHAPTERS ###

chapI, pageI = 1, 1
fileTemp = Template('ch$c/p$p.txt')
index = Trie()
while True:
	while os.path.isfile(fileTemp.substitute(c=chapI, p=pageI)):
		with open(fileTemp.substitute(c=chapI, p=pageI),encoding='utf-8') as file:
			wordI = 1
			for line in file:
				for word in line.split():
					encoded = encodeWord(word)
					index[encoded].setdefault([]).append((chapI, pageI, wordI))
					wordI += 1
		pageI += 1
	if pageI == 1:
		break
	print('Found chapter', chapI, 'containing', pageI-1, 'pages')
	chapI += 1
	pageI = 1
index.gensuggestions(10)

print('\nTotal words found:', len(index))

### SCAN EXISTING INDEX, DELETE AS APPROPRIATE ###

os.makedirs('index', exist_ok=True)
os.chdir('index')
existingIndexFiles = {}
removed = 0
for ex_folder in os.listdir():
	if not os.path.isdir(ex_folder):
		print('Odd file found in index:', ex_folder)
	else:
		existingIndexFiles[ex_folder] = os.listdir(ex_folder)
		if not index.has_prefix(ex_folder):
			for ex_file in existingIndexFiles[ex_folder]:
				os.remove(ex_folder + '/' + ex_file)
				removed += 1
			os.rmdir(ex_folder)
		else:
			for ex_file in existingIndexFiles[ex_folder]:
				if ex_file[:-4] not in index:
					os.remove(ex_folder + '/' + ex_file)
					removed += 1
		
print(removed, 'file(s) culled')

### UPDATE/CREATE INDEX FILES ###

updated, created = 0, 0
for letter, basenode in index._root.next:
	if letter in string.ascii_lowercase:
		folder = letter
	else:
		folder = '0'
	for node in _node_iter(basenode):
		word, positions = node.value
		fileContent = [','.join(str(x) for x in pos) for pos in positions]
		fileName = word + '.txt'
		if folder in existingIndexFiles and fileName in existingIndexFiles[folder]:
			existingFile = open(folder + '/' + fileName,encoding='utf-8')
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
		with open(folder + '/' + fileName,mode='w',encoding='utf-8') as indexFile:
			for line in fileContent:
				print(line, file=indexFile)

print(created, 'file(s) created')
print(updated, 'file(s) updated')
print('Finished building index')
