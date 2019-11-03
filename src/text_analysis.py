import re
from typing import List

import rake_nltk
from rake_nltk import Metric
import nltk
def find_deg(l, x):
    t = len(l)
    for i in l:
        t += i.count(" ")
    q = t
    for i, e in enumerate(l):
        if re.search(fr'\b({x})\b', e, re.I):
            return (q - (e.count(" "))/(2*t)) / t
        q -= 1 + e.count(" ")
    return 0.0

def find_freq(l,x):
    if x in l:
        return 1-l.index(x)/len(l)
    return 0.25

good=['FW', 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NPS', 'RB', 'RBR', 'RBS', 'RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'WP', 'WRB']
def get_important(splitted:List[str]):
    print("split",splitted)
    print("aaa")
    freq_r = rake_nltk.Rake(max_length=3, ranking_metric=Metric.WORD_FREQUENCY)
    print("bb")
    freq_r.extract_keywords_from_text(" and ".join(splitted))
    freq_phrases = freq_r.get_ranked_phrases()

    deg_r = rake_nltk.Rake(max_length=3, ranking_metric=Metric.WORD_DEGREE)
    deg_r.extract_keywords_from_text(" ".join(splitted))
    deg_phrases=deg_r.get_ranked_phrases()

    freq_data={i:find_freq(freq_phrases,i.lower()) for i in splitted}
    deg_data={i: find_deg(deg_phrases,i.lower()) for i in splitted}
    data={}
    for k,freq_v in freq_data.items():
        deg_v=deg_data[k]
        data[k]=freq_v+deg_v
    part_of_speech=nltk.pos_tag(splitted)
    print(part_of_speech)
    for i,part in part_of_speech:
        if part not in good:
            data[i]*=0.5
    """
FW foreign word
JJ adjective 'big'
JJR adjective, comparative 'bigger'
JJS adjective, superlative 'biggest'
NN noun, singular 'desk'
NNS noun plural 'desks'
NNP proper noun, singular 'Harrison'
NNPS proper noun, plural 'Americans'
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBZ verb, 3rd person sing. present takes
WP wh-pronoun who, what
WRB wh-abverb where, when
"""
    # print("deg_phrases",deg_phrases)
    # print("deg_data",deg_data)
    # print("freq_phrases",freq_phrases)
    # print("freq_data",freq_data)
    return [j[0] for j in sorted(data.items(),key=lambda i:-i[1])[:3]]