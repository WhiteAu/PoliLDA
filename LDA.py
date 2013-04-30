import sys
import nltk
import numpy
from gensim import corpora, models, similarities
import gensim
import parser

########################
#Initializations
########################

#ignore = nltk.corpus.stopwords.words('english')

#grab document list and put em here.
'''
documents = []

texts = [[word for word in document.lower().split() if word not in ignore] 
         for document in documents]


tokens = sum(texts, [])
#Find all single instances of words
singletons = set(word for word in set(all_tokens) if tokens.count(word) == 1)

texts = [[word for word in text if word not in singletons]
         for text in texts]
'''
dfile  = parser.DataList(file='small_example.csv')

data = dfile.data_list

########################
#Prep Folds
########################
#make k  a sysarg!
k = 10
print 'number of \'documents\' is: %d' %len(data)
fold_size = len(data) / k
print 'fold size is: %d' %fold_size

#should randomly permute data first. Does numpy work?
'''
numpy.random.shuffle(data)
print type(data)
train_split = data[:fold_size]
test_split = data[fold_size:]
'''

#corpus = gensim.matutils.Dense2Corpus(data)

#just saying 10 for now. pass it in as a sys_arg later
lda =  models.ldamodel.LdaModel(corpus=dfile.LDA_corpus, id2word=dfile.dictionary, num_topics=10)

print 'topics:'
print lda.print_topics(10)
