import os
from trie      import Trie, _iter_nonempty
from string    import Template, ascii_lowercase
from itertools import zip_longest

def escape(word):
	word = word.lower()
	encoded = ''
	for char in word:
		if char.isalnum():
			encoded += char
		else:
			encoded += '-' + str(ord(char)) + '-'
	return encoded

def unescape(word):
	sections = word.split('-')
	decoded = ''
	plain = True
	for s in sections:
		if plain:
			decoded += s
		else:
			decoded += chr(int(s))
		plain = not plain
	return decoded

### READ ALL CHAPTERS ###

chap_i, page_i = 1, 1
filetemp = Template('ch$c/p$p.txt')
index = Trie()
while True:
	while os.path.isfile(filetemp.substitute(c=chap_i, p=page_i)):
		with open(filetemp.substitute(c=chap_i, p=page_i),encoding='utf-8') as file:
			word_i = 1
			for line in file:
				for word in line.split():
					index.setdefault(word, []).append((chap_i, page_i, word_i))
					word_i += 1
		page_i += 1
	if page_i == 1:
		break
	print('Found chapter', chap_i, 'containing', page_i-1, 'pages', flush=True)
	chap_i += 1
	page_i = 1

print('Total words found:', len(index), flush=True)

### SCAN EXISTING INDEX, DELETE AS APPROPRIATE ###

os.makedirs('index', exist_ok=True)
os.chdir('index')
ex_files = {}
removed = 0
for ex_folder in os.listdir():
	if not os.path.isdir(ex_folder):
		print('Odd file found in index:', ex_folder, flush=True)
	else:
		ex_files[ex_folder] = os.listdir(ex_folder)
		files_left = False
		for ex_file in ex_files[ex_folder]:
			if unescape(ex_file[:-4]) not in index:
				os.remove(ex_folder + '/' + ex_file)
				removed += 1
			else:
				files_left = True
		if not files_left:
			os.rmdir(ex_folder)
		
print(removed, 'file(s) culled', flush=True)

### UPDATE/CREATE INDEX FILES ###

updated, created = 0, 0
for letter, basenode in index._root.next.items():
	if letter in ascii_lowercase:
		folder = letter
	else:
		folder = '0'
	for node in _iter_nonempty(basenode):
		word, positions = node.key, node.value
		filecontent = [','.join(str(x) for x in pos) for pos in positions]
		filename = escape(word) + '.txt'
		if folder in ex_files and filename in ex_files[folder]:
			ex_file = open(folder + '/' + filename,encoding='utf-8')
			i = 0
			for line in ex_file:
				if i >= len(filecontent) or line.strip() != filecontent[i]:
					ex_file.close()
					break
				i += 1
			else:
				ex_file.close()
				if i == len(filecontent):
					continue
			updated += 1
		else:
			created += 1
		os.makedirs(folder, exist_ok=True)
		with open(folder + '/' + filename,mode='w',encoding='utf-8') as indexFile:
			for line in filecontent:
				print(line, file=indexFile)
os.chdir(os.pardir)

print(created, 'file(s) created', flush=True)
print(updated, 'file(s) updated', flush=True)

### UPDATE/CREATE SUGGESTION FILES ###

os.makedirs('suggest', exist_ok=True)
os.chdir('suggest')

def build_suggest(node):
	global removed, updated, created
	
	# Print progress
	build_suggest.progress += 1
	percent = (100 * build_suggest.progress) // index.num_nodes()
	if percent >= build_suggest.next_milestone:
		print(percent, '%', sep='', flush=True)
		build_suggest.next_milestone += 10
	
	# Output file for this node
	needwrite = False
	if os.path.isfile('s.txt'):
		with open('s.txt', encoding='utf-8') as file:
			for ex_word, new_word in zip_longest(file, node.suggest):
				if not ex_word:
					needwrite = True
					updated += 1
					break
				ex_word = ex_word.strip()
				if len(ex_word) != 0 and ex_word != new_word[0]:
					needwrite = True
					updated += 1
					break
	else:
		needwrite = True
		created += 1
	if needwrite:
		with open('s.txt', mode='w', encoding='utf-8') as file:
			for word in node.suggest:
				print(''.join(word[0]), file=file)
	
	# Check subfolders
	for entry in os.scandir():
		if entry.is_dir() and unescape(entry.name) not in node.next:
			for root, dirs, files in os.walk(entry.name, topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
					removed += 1
				for name in dirs:
					os.rmdir(os.path.join(root, name))
		elif entry.is_file() and entry.name != 's.txt':
			os.remove(entry.name)
			removed += 1
	
	# Recurse
	for letter, n in node.next.items():
		folder = escape(letter)
		os.makedirs(folder, exist_ok=True)
		os.chdir(folder)
		build_suggest(n)
		os.chdir(os.pardir)

index.gensuggestions(10)

print('Building suggestions: 0%', flush=True)
removed, updated, created = 0, 0, 0
build_suggest.progress, build_suggest.next_milestone = 0, 10
build_suggest(index._root)
print(removed, 'file(s) culled', flush=True)
print(created, 'file(s) created', flush=True)
print(updated, 'file(s) updated', flush=True)

print('Finished building index')
