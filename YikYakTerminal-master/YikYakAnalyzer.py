#Pickle protocol only works for python 3 :(

import os
import pickle
import datetime
import copy
import API
import collections
import matplotlib.pyplot as plt
import numpy as np
import re
import string

stopfile = 'stopwords'

with open(stopfile) as f:
    stopwords = f.read().split()

for c in string.punctuation:
	for i in range(len(stopwords)):
		stopwords[i] = stopwords[i].replace(c,"")

yak_ensembles = {}
start_time = 0
time = 0
for i,fn in enumerate(os.listdir('data_experiment')):
	if i == 0 or i == 1: continue
	date = datetime.datetime.strptime(fn, '%Y-%m-%d-%H-%M-%S.p')
	if i == 2:
		start_time = copy.copy(date)
	else:
		time = (date - start_time).total_seconds()
	with open('data_experiment/'+fn, 'rb') as infile:
		yak_ensembles[time] = pickle.load(infile)

yaks = collections.defaultdict(list)

for time in sorted(list(yak_ensembles.keys())):
	for yak in yak_ensembles[time]:
		yaks[yak.message_id].append((time, yak))

yak_likes = {}
yak_num_comments = {}
words = collections.defaultdict(int)
like_time_dict = collections.defaultdict(int)
for yak in yaks.values():
	current_yak = yak[-1][1]
	sentences = re.split(r"(?<!^)\s*[.\n]+\s*(?!$)", current_yak.message)
	for s in sentences:
		for c in string.punctuation:
			s = s.replace(c,"")
		for word in s.split():
			words[word.lower()] += 1
	for comment in current_yak.comments:
		sentences = re.split(r"(?<!^)\s*[.\n]+\s*(?!$)", comment.comment)
		for s in sentences:
			for c in string.punctuation:
				s = s.replace(c,"")
			for word in s.split():
				words[word.lower()] += 1
	yak_likes[current_yak.message] = [(time, y.likes) for time, y in yak]
	for time, y in yak:
		like_time_dict[time] += y.likes
	yak_num_comments[current_yak.message] = [(time, y.num_comments) for time, y in yak]

times = sorted(like_time_dict.keys(),reverse=True)

for i in range(len(times)-1):
	like_time_dict[times[i]] -= like_time_dict[times[i+1]]

like_time_dict[times[0]] = like_time_dict[times[1]]


words = sorted(dict(words).items(),key = lambda x: x[1])
words_nonstop = {key:value for key,value in words if key not in stopwords}
words_nonstop = sorted(dict(words_nonstop).items(),key = lambda x: x[1])

from matplotlib import cm 

colors = cm.rainbow(np.linspace(0, 1, len(yak_likes)))

plt.ion()

sorted_yak_likes = sorted(yak_likes.values(),key = lambda x: x[0][0])

for i,yak_like in enumerate(sorted_yak_likes):
	if(yak_like[-1][1] > 10):
		like_plot = np.asarray(yak_like)
		plt.plot(like_plot[:,0],like_plot[:,1],c=colors[i])

plt.ylim([-10,500])

