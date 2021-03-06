############README############
Team 2, Golden Globes Assignment
Kristin Funch, Rosio Macedo, Luke Olney, Jacob Samson

To run, navigate to the EECS337_GG2015 directory and enter the command “python GoldenGlobesNLP.py [filename] [outfile]”, where filename is the json file containing tweets for the year you would like analyzed and outfile is the name of the file where the answers where be dumped. If an outfile is not given, the name of the output file will be "answers.json".

This routine will also give both the results for our sentiment analysis (as funGoals.json). 

To run the text interface, run "python interface.py interfaceDict.json".

Our project depends on the json, nltk, re, curses, BeautifulSoup, locale, urllib2, dill and subprocess libraries.

We did not consult with any repositories in creating our solution.

Our code is highly adaptable, both to other years of golden globes data and (with minimal changes) 
to other awards shows altogether. All core analysis of tweets is entirely based on scraped data 
and the tweet corpus, with the exception of some key golden globes and tweet related words 
(i.e. "Golden","RT","GoldenGlobes") used to eliminate high-frequency, unhelpful words from candidate selection. 
While the scraping and interface are golden-globe (but not year) specific, these concessions were 
necessary design choices to keep the solution concise and workable.
