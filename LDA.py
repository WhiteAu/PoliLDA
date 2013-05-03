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


clean, clean_dict = dfile.make_clean(col=0)
########################
#Prep Folds
########################
#make k  a sysarg!
k = 10
print 'number of \'documents\' is: %d' %len(clean)
print 'length of document: %d' %len(clean[0])
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
lda =  models.ldamodel.LdaModel(corpus=clean, id2word=clean_dict, num_topics=10)

print lda

for k in xrange(len(clean)):
    #print lda(clean[k])
    lda.print_topic(clean[k])
print 'topics:'
print lda.print_topics(20)
