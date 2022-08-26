import re
from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from nltk.sem import extract_rels


def extract_entities(text):
	entities = []
	sents = sent_tokenize(text)
	chunks = [ ne_chunk(pos_tag(word_tokenize(sent)),\
	binary=True) for sent in sents]
	for chunk in chunks:
		print chunk
		for tree in chunk.subtrees():
			if tree.node == "NE":
				entity = ' '.join(leaf[0] for leaf in tree.leaves())
				entities.append(entity)
	return entities


def ne_rel_extract(text):
	REL = re.compile(r'.*\bin\b(?!\b.+ing)')
	sents = sent_tokenize(text)
	chunk = [ ne_chunk(pos_tag(word_tokenize(sent))) for sent in sents]
	print chunk

	class doc():
		pass

	doc.headline = ['sample']
	doc.text = chunk

	for r in extract_rels('ORG','LOC',doc,corpus='ieer',pattern=REL):
		print r
#http://stackoverflow.com/questions/7851937/extract-relationships-using-nltk
#http://stackoverflow.com/questions/12264593/how-to-extract-relationship-from-text-in-nltk?rq=1
#http://stackoverflow.com/questions/9595983/tools-for-text-simplification-java/9606606#9606606
#http://www.csc.villanova.edu/~matuszek/spring2012/snippets.html
#http://www.comp.nus.edu.sg/~kanmy/courses/practicalNLP_2008/
#http://blog.mafr.de/2011/01/06/near-duplicate-detection/ #DUP Detect
#https://bitbucket.org/sedlakf/blog-clustering/src
#http://www.litfuel.net/plush/?postid=200 #Entity Disambiguation
#https://gist.github.com/1505755 KM sklearn
#https://github.com/amsqr/NaiveSumm/blob/master/naivesumm.py Text Summary
#http://pixelmonkey.org/pub/nlp-training/
#https://github.com/Parsely/python-nlp-slides/blob/master/index.rst
#https://bitbucket.org/fccoelho/scholarscrap/src
#https://github.com/amsqr/NaiveSumm/blob/master/naivesumm.py
#https://github.com/aswadrangnekar/document-clustering
if __name__ == "__main__":
	sent = "XYZ Inc. in Philadelphia . Paracetamole is in Crocin."
	#entities = extract_entities(sent)
	#print entities
	ne_rel_extract(sent)
