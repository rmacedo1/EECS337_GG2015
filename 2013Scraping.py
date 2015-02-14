import urllib2, subprocess, json, re
from BeautifulSoup import BeautifulSoup

def swap(elems):
	temp = elems[0];
	elems[0] = elems[1]
	elems[1] = temp
	return elems

def strip(str):
	str = str.replace('&nbsp;', " ")
	elems = str.split(',')
	if(len(elems) < 2):
		return str
	elems = swap(elems)
	return " ".join(elems)

ggurl = "http://www.hfpa.org/browse/?param=/year/2013";

bashCommand = "curl " + ggurl
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output = process.communicate()[0];

parsed_html = BeautifulSoup(output)
content = parsed_html.body.find('div', attrs={'class':'searchResultsYear'})

awards = [];
for cat in content.findAll('h2'):

	table = cat.findNext('table')
	tableRows = table.findAll('td');
	if(len(tableRows) < 2):
		continue

	title = cat.text
	print cat.text

	nominees = [];
	
	for nominee in tableRows:
		names = nominee.findAll('a');
		notes = None
		if len(names) == 2:
			name = names[0]
			notes = names[1]
		elif len(names) == 1:
			name = names[0]
		else:
			print "Format not as expected"
			name = names[0]
			notes = names[1]

		if notes is not None:
			field = {"Person" : strip(name.text), "Notes" : strip(notes.text)};
		else:
			field = name.text;

		nominees.append(field);

	awards.append({
		"Category" : title,
		"Nominees" : nominees
	})



with open('categories_nominees_winners_2013.json', 'w') as outfile:
	json.dump({"Awards": awards}, outfile);
