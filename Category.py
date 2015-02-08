import json

class Category:
	def __init__(self, name, subcats=[]):
		self.name = name
		self.subcats = subcats
	def __str__(self):
		return str({"Super" : self.name, "Subs": [x.__str__() for x in self.subcats]})
	def addSubcat(subcat):
		self.subcats.append(subcat)

def splitRecursive(str, splits):
	splitStrs = [];
	for s in splits:
		splitStrs.append(str.split(s));
	for l in splitStrs:
		if len(l) > 1:
			try:
				splits.remove(",")
			except ValueError:
				pass
			return [l[0]]+ splitRecursive(l[1], splits);
	return [str];

def stripTrailingWhitespace(b):
	while b[-1] == " ":
		b = b[0:-1]
	while b[0] == " ":
		b = b[1:len(b)]
	return b;

def findCats(h, n):
	if n >= len(h[0]):
		return []
	else:
		cats = [];
		groups = group(h, n)
		for g in groups:
			name = g[0][n]
			subcats = findCats(g, n+1)
			cats.append(Category(name, subcats))
		return cats

def group(superlist, n):
	cmp = superlist[0][n]
	groups = [];
	currentgroup = [];
	for lst in superlist:
		if lst[n] == cmp:
			currentgroup.append(lst)
		else:
			cmp = lst[n];
			groups.append(currentgroup)
			currentgroup = [lst]
	groups.append(currentgroup);
	return groups


def createCategories(categoryFN="categories_nominees_winners.json"):
	splits = ["in a","In A", ",", " - "];
	with open(categoryFN) as infile:
		awards = json.load(infile)["Awards"];

	hierachies = [];
	for award in awards:
		category = award["Category"];
		temp = splitRecursive(category, splits);
		temp = [stripTrailingWhitespace(b) for b in temp];
		hierachies.append(temp);

	hierachies = sorted(hierachies)
	categories = findCats(hierachies, 0)
	return categories





	
