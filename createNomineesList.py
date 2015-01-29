import urllib2, subprocess, json, re
from BeautifulSoup import BeautifulSoup

ggurl = "http://www.goldenglobes.com/2015_72nd_Golden_Globes_Nominees"

bashCommand = "curl " + ggurl
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output = process.communicate()[0];

parsed_html = BeautifulSoup(output)
content = parsed_html.body.find('div', attrs={'class':'view-content'})

print type(content);
print type(parsed_html.body);

awards = [];
for cat in content.findAll('div', attrs={'class': re.compile('has-winner')}):
	title = cat.find('div', attrs={'class': re.compile('views-field-title')}).text;
	print title

	nominees = [];
	winner = None;
	for nominee in cat.findAll('div', attrs={'class':'views-info'}):
		name = nominee.find('div', attrs={'class':re.compile('views-field')});
		notes = cat.find('div', attrs={'class':re.compile('views-field-nominee-notes')});
		if notes is not None:
			field = {"Person" : name.text, "Notes" : notes.text.translate({ord(c): None for c in ['(',')']})};
		else:
			field = name.text;

		if re.search('gold', name['class']) is not None:
			winner = field;

		nominees.append(field);
		print name.text

	awards.append({
		"Category" : title,
		"Winner" : winner,
		"Nominees" : nominees
	})

with open('categories_nominees_winners.json', 'w') as outfile:
	json.dump({"Awards": awards}, outfile);


	 
"""
This didn't work; 403 error

headers={
	'Host': 'www.goldenglobes.com',
	'Connection': 'keep-alive',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
	'Referer': 'https://www.google.com/',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,de;q=0.6',
	'Cookie': '__cfduid=dbf066e375ef44782fa4165e5697446651422550110; _gat=1; _cb_ls=1; _SUPERFLY_nosample=1; _chartbeat4=t=zz-_wCNYyxLDnljHW_81e1Zc2KW&E=3&x=1314&c=7.85&y=8571&w=513; _ga=GA1.2.1675203478.1422550111; __atuvc=1%7C4; __atuvs=54ca663a25c835d2000; _chartbeat2=CDmhSmiM3uYBfND-h.1422550114710.1422550587212.1'
	}
req = urllib2.Request(ggurl, None, headers);

try:
	resp = urllib2.urlopen(ggurl)
	html = resp.read();
	print html
except urllib2.HTTPError, e:
	print e.fp.read() 
"""