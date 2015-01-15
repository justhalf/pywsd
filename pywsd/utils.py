#!/usr/bin/env python -*- coding: utf-8 -*-
#
# Python Word Sense Disambiguation (pyWSD): Misc utility functions
#
# Copyright (C) 2014-2015 alvations
# URL:
# For license information, see LICENSE.md

from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag, word_tokenize

def remove_tags(text):
  """ Removes <tags> in angled brackets from text. """
  import re
  tags = {i:" " for i in re.findall("(<[^>\n]*>)",text.strip())}
  no_tag_text = reduce(lambda x, kv:x.replace(*kv), tags.iteritems(), text)
  return " ".join(no_tag_text.split())
  
def offset_to_synset(offset):
    """ 
    Look up a synset given offset-pos 
    (Thanks for @FBond, see http://moin.delph-in.net/SemCor)
    >>> synset = offset_to_synset('02614387-v')
    >>> print '%08d-%s' % (synset.offset, synset.pos)
    >>> print synset, synset.definition
    02614387-v
    Synset('live.v.02') lead a certain kind of life; live in a certain style
    """
    return wn._synset_from_pos_and_offset(str(offset[-1:]), int(offset[:8]))

def semcor_to_synset(sensekey):
    """
    Look up a synset given the information from SemCor sensekey format.
    (Thanks for @FBond, see http://moin.delph-in.net/SemCor)
    >>> ss = semcor_to_offset('live%2:42:06::')
    >>> print '%08d-%s' % (ss.offset, ss.pos)
    >>> print ss, ss.definition
    02614387-v
    Synset('live.v.02') lead a certain kind of life; live in a certain style
    """
    return wn.lemma_from_key(sensekey).synset

def semcor_to_offset(sensekey):
    """
    Converts SemCor sensekey IDs to synset offset.
    >>> print semcor_to_offset('live%2:42:06::')
    02614387-v
    """
    synset = wn.lemma_from_key(sensekey).synset
    offset = '%08d-%s' % (synset.offset, synset.pos)
    return offset




porter = PorterStemmer()
wnl = WordNetLemmatizer()

'''
#TODO: various tokenizers.
from nltk import word_tokenize
def tokenize(sentence, option="split"):
  if option == "split": # Simply splits by whitespaces.
    return sentence.split()
  if option == "word_tokenize": # Uses NLTK word_tokenize().
    return word_tokenize(sentence)
'''

'''
#TODO: various stem / lemmatizers.
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
def stem(word, option="wnlemma")
  if option == "wnlemma":
    return wnl.lemmatize(word)
  if option == "porter":
    return porter.stem(word)
'''

def lemmatize(ambiguous_word, pos=None, neverstem=False):
    """
    Tries to convert a surface word into lemma, and if lemmatize word is not in
    wordnet then try and convert surface word into its stem.
    
    This is to handle the case where users input a surface word as an ambiguous 
    word and the surface word is a not a lemma.
    """
    if pos:
        lemma = wnl.lemmatize(ambiguous_word, pos=pos)
    else:
        lemma = wnl.lemmatize(ambiguous_word)
    stem = porter.stem(ambiguous_word)
    # Ensure that ambiguous word is a lemma.
    if not wn.synsets(lemma):
        if neverstem:
            return ambiguous_word
        if not wn.synsets(stem):
            return ambiguous_word
        else:
            return stem
    else:
     return lemma
 
# To check default parameters of simple_lesk()
## a = inspect.getargspec(simple_lesk)
## print zip(a.args[-len(a.defaults):],a.defaults)


def penn2morphy(penntag):
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return ''

def lemmatize_sentence(sentence, neverstem=False, keepWordPOS=False):
    words, lemmas, poss = [], [], []
    for word, pos in pos_tag(word_tokenize(sentence)):
        pos = penn2morphy(pos)
        lemmas.append(lemmatize(word.lower(), pos,neverstem=neverstem))
        poss.append(pos)
        words.append(word)
    if keepWordPOS:
        return words, lemmas, [None if i == '' else i for i in poss]
    return lemmas