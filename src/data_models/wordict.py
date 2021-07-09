#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
#	Name    : wordict
#	Author  : Ting
#   Version : 1
#   Purpose : Check the proposition of the word 
#
###############################################################################

import logging
import traceback
import textwrap
from nltk.corpus import wordnet as wn
import enchant 
# import __builtin__


POS = {
    'v': 'verb', 'a': 'adjective', 's': 'satellite adjective', 
    'n': 'noun', 'r': 'adverb'}


word_check = enchant.Dict("en_US")


# def define_word(self, word='good', pos=None):
def define_word(word='good', pos=None, orig_word=''):
	if word_check.check(word):

		noun_only = True  # Also means the word is most likely an article 
		def_set = []  # Declare empty list
		for i, syn in enumerate(wn.synsets(word, pos)):
			wordef = {'syns': [n.replace('_', ' ') for n in syn.lemma_names()], 
					  'atns': [a.name() for m in syn.lemmas() for a in m.antonyms()],
					  'pos': POS[syn.pos()]
					  }
			def_set.append(wordef)

			if wordef.get('pos') != 'noun': 
				noun_only = False 

			if wordef.get('atns') and wordef.get('pos') != 'noun': 
				print(wordef.get('atns')[0], wordef.get('pos'))
				return wordef.get('atns')[0]


		try:
			if orig_word is '' and noun_only:
				return

			for wordef in def_set: 
				for word_syn in wordef.get('syns'): 
					if word_syn not in [word, orig_word] and len(wordef.get('syns')) > 1: 
						return define_word(word=word_syn, orig_word=word)
		except Exception as e: 
			print(e)

		# for key, value in wordef.iteritems(): 				
			# setattr(self.define_word.__func__, key, value)

		# return def_set

	return


if __name__ == '__main__':
	print(define_word())
	print('-----------')
	print(define_word('near'))
	print('-----------')
	print(define_word('great'))
	print('-----------')
	print(define_word('Trump'))
	print('-----------')
	print(define_word('erftgyhuijo'))
	print('-----------')
	print(define_word('the'))
	print('-----------')
	print(define_word('be'))
	print('-----------')
	print(define_word('capability'))
	# print define_word('good').__dict__
	# print define_word('good').pos


# Reference
# http://stackoverflow.com/questions/21395011/python-module-with-access-to-english-dictionaries-including-definitions-of-words
# https://github.com/geekpradd/PyDictionary
# http://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
# http://www.velvetcache.org/2010/03/01/looking-up-words-in-a-dictionary-using-python
# http://stackoverflow.com/questions/6103907/fully-parsable-dictionary-thesaurus
# http://stackoverflow.com/questions/24192979/how-to-generate-a-list-of-antonyms-for-adjectives-in-wordnet-using-python

# http://stackoverflow.com/questions/338101/python-function-attributes-uses-and-abuses
# http://adambeagle.com/blog/python-function-attributes-i/
# http://stackoverflow.com/questions/3109289/how-can-python-function-access-its-own-attributes
# https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide
# http://stackoverflow.com/questions/9523370/adding-attributes-to-instance-methods-in-python


# class WorDict(object): 

	# def __init__(self): 
	# 	self.define_word()

# ### For building a word map
# for i in wn.all_synsets():
#     if i.pos() in ['a', 's', 'r', 'v']: # If synset is not noun 
#         for j in i.lemmas(): # Iterating through lemmas for each synset.
#         	j.name()  # The word 
#             if j.antonyms(): # If adj has antonym.
# 				j.antonyms()[0].name()  # The antonym 
#             if j.synonyms(): # If adj has synonyms.
# 				j.synonyms()[0].name()  # The synonyms 

# def get_pol():