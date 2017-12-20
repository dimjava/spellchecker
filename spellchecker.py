# -*- coding: utf-8 -*-

import cPickle as pickle
import re
from nltk.metrics import edit_distance
from soundex import soundex, is_ascii
from mmh3 import hash as mhash

alpha = 2.5

sound_dict = {}
frequences = {}
frequences2 = {}
total_dict = set()

def sentence_prob(words):
	p = 1.0

	for i in range(len(words) - 1):
		w1 = words[i]
		w2 = words[i + 1]
		key = mhash('&'.join([w1, w2]))
		if key in frequences2:
			p *= frequences2[key]
	if mhash(words[-1]) in frequences:
		p *= frequences[mhash(words[-1])]

	return p

def probs_generator(orig_words, candidates, word_idx, words):
	if word_idx == len(candidates) - 1:
		for w in candidates[-1]:
			words[-1] = w
			diff = 0
			for i in range(len(orig_words)):
				diff += edit_distance(orig_words[i], words[i])

			p_orig_fix = alpha ** (-diff)
			p_fix = sentence_prob(words)

			yield {'orig|fix': p_orig_fix, 'fix': p_fix, 'words': words}
	else:
		for word in candidates[word_idx]:
			words[word_idx] = word

			for mp in probs_generator(orig_words, candidates, word_idx + 1, words):
				yield mp

def get_best(query_words, candidates):
	p_orig = sentence_prob(query_words)
	
	mmax = -1
	fix_words = []
	for mp in probs_generator(query_words, candidates, 0, ['' for i in range(len(query_words))]):
		if not mp:
			break

		p_orig_fix, p_fix, words = mp['orig|fix'], mp['fix'], mp['words']
		p = (p_orig_fix * p_fix) / p_orig
		# print(p_orig, p_fix, p_orig_fix)
		# print(' '.join(words))
		if p > mmax:
			mmax = p
			fix_words = [w for w in words]
	return fix_words

if __name__ == '__main__':
	with open('souds.bin', 'rb') as sounds:
		sound_dict = pickle.load(sounds)
	with open('freqs.bin', 'rb') as freqs:
		frequences = pickle.load(freqs)
	with open('freqs2.bin', 'rb') as freqs2:
		frequences2 = pickle.load(freqs2)
	with open('dict.bin', 'rb') as total:
		total_dict = pickle.load(total)

	query = raw_input()

	while query:
		# print('QUERY: ' + query)

		query = query.strip().lower()
		if not is_ascii(query):
			query = query.decode('utf-8').lower().encode('utf-8')

		words = re.split(' |\.|\,', query)
		words = filter(lambda x: x != '', words)
		max_cand = min(int(10000.0 ** (1.0 / len(words))), 10)
		result = []
		# word_probs = []
		candidates_query = []
		for word in words:
			candidates = set()

			word = word.strip()
			if mhash(word) in total_dict:
				candidates.add(word)

			mmax = -1
			mfix = word
			sndx = soundex(word)

			# print(sndx)
			# print(sndx in sound_dict)
			if sndx in sound_dict:
				candidates |= set(sound_dict[sndx])
			ppp = sorted([(frequences[mhash(word)] if mhash(word) in frequences else 1.0, word) for word in candidates])[-1:-max_cand:-1]
			ppp = list(map(lambda x: x[1], ppp))
			if len(ppp) == 0:
				ppp.append(word)
			# print('ppp',ppp)
			# candidates_query.append(set(candidates))
			candidates_query.append(set(ppp))

		result = get_best(words, candidates_query)
		# print(word_probs)
		# print('\t'.join([query, ' '.join(result)]))
		print(' '.join(result))
		try:
			query = raw_input()
		except:
			break