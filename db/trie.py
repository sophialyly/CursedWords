class _TrieNode(object):
	__slots__ = 'next', 'key', 'suggest', 'value'
	
	def __init__(self, key=None, value=None):
		self.next = {}
		self.key = key
		self.suggest = []
		self.value = value
	
	def setvalue(self, key, value):
		self.key = key
		self.value = value
	
	def hasvalue(self):
		return self.key != None

class Trie:
	def __init__(self, copy=[], **kwargs):
		self._root = _TrieNode()
		self._length = 0
		try:
			for key, value in copy.items():
				self[key] = value
		except:
			for key, value in copy:
				self[key] = value
		for key, value in kwargs.items():
			self[key] = value
	
	def __len__(self):
		return self._length
	
	def __contains__(self, key):
		node = _find_node(self._root, key)
		return node != None and node.hasvalue()
	
	def __getitem__(self, key):
		node = _find_node(self._root, key)
		if node != None and node.hasvalue():
			return node.value
		else:
			raise KeyError
	
	def __setitem__(self, key, value):
		node = self._root
		for char in key:
			if char not in node.next:
				node.next[char] = _TrieNode()
			node = node.next[char]
		if not node.hasvalue():
			self._length += 1
		node.setvalue(key, value)
	
	def __delitem__(self, key):
		node = self._root
		lastbranch = None
		for char in key:
			if char in node.next:
				if lastbranch == None or len(node.next) > 1:
					lastdict = node.next
					lastbranch = char
				node = node.next[char]
			else:
				raise KeyError
		if not node.hasvalue():
			raise KeyError
		if lastbranch != None and len(node.next) == 0: # No children
			del lastdict[lastbranch]
		else:
			del node.value
		self._length -= 1
	
	def __iter__(self):
		return self.keys()
	
	def clear(self):
		self._root = _TrieNode()
		self._length = 0
	
	def get(self, key, default=None):
		try:
			self.__getitem__(key)
		except KeyError:
			return default
	
	def setdefault(self, key, default=None):
		node = self._root
		for char in key:
			if char not in node.next:
				node.next[char] = _TrieNode()
			node = node.next[char]
		if node.hasvalue():
			return node.value
		else:
			self._length += 1
			node.setvalue(key, default)
			return default
	
	def keys(self):
		return (node.key for node in _node_iter(self._root))
	
	def values(self):
		return (node.value for node in _node_iter(self._root))
	
	def items(self):
		return ((node.key, node.value) for node in _node_iter(self._root))
	
	def prefix_keys(self, prefix):
		node = _find_node(self._root, prefix)
		if node != None:
			return (n.key for n in _node_iter(node))
		else:
			return iter(())
	
	def prefix_values(self, prefix):
		node = _find_node(self._root, prefix)
		if node != None:
			return (n.value for n in _node_iter(node))
		else:
			return iter(())
	
	def prefix_items(self, prefix):
		node = _find_node(self._root, prefix)
		if node != None:
			return ((n.key, n.value) for n in _node_iter(node))
		else:
			return iter(())
	
	def prefix_suggest(self, prefix):
		node = _find_node(self._root, prefix)
		if node != None:
			return (x[0] for x in node.suggest)
		else:
			return iter(())
	
	def has_prefix(self, prefix):
		return _find_node(self._root, prefix) != None
	
	def gensuggestions(self, maxlength):
		_recurse_suggest(self._root, maxlength)
		
def _recurse_suggest(node, maxlength):
	s = []
	for n in node.next.values():
		s.extend(_recurse_suggest(n, maxlength))
	s.sort(key=lambda x: x[1], reverse=True)
	s = s[:maxlength]
	if node.hasvalue():
		s.insert(0, node.value)
	node.suggest = s[:maxlength]
	return s

def _find_node(node, prefix):
	for char in prefix:
		if char in node.next:
			node = node.next[char]
		else:
			return None
	return node

def _node_iter(node):
	if node.hasvalue():
		yield node
	for n in node.next.values():
		yield from _node_iter(n)