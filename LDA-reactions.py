import sys
import nltk
import numpy
import logging #lda topics prints to log file
from gensim import corpora, models, similarities
import gensim
import parserR

########################
#Initializations
########################

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dfile  = parserR.DataList(file='reactions_oct3_4project.csv')
#'reactions_oct3_4project.csv'
#'small_example.csv'
clean, clean_dict = dfile.make_clean(col=0)
corpora.MmCorpus.serialize('clean.mm', clean)
corpora.svmlightcorpus.SvmLightCorpus.serialize('clean.svm',clean)#save as svm for mallet
cor = corpora.MmCorpus('clean.mm')
########################
#Prep Folds
########################
#make k  a sysarg!
k = 10
print 'number of \'documents\' is: %d' %len(clean)
print 'length of document: %d' %len(clean[0])
#fold_size = len(data) / k
#print 'fold size is: %d' %fold_size

#should randomly permute data first. Does numpy work?
'''
numpy.random.shuffle(data)
print type(data)
train_split = data[:fold_size]
test_split = data[fold_size:]
'''

#corpus = gensim.matutils.Dense2Corpus(data)

#just saying 10 for now. pass it in as a sys_arg later
lda =  models.ldamodel.LdaModel(corpus=cor, id2word=clean_dict, num_topics=100)
#lda = models.ldamodel.LdaModel(corpus=cor, id2word=clean_dict, num_topics=20, update_every=0, passes=10)

print lda
print cor
#for k in xrange(len(clean)):
    #print lda(clean[k])
#    lda.print_topic(clean[k])
#lda.print_topic(cor)
print 'topics:'
lda.print_topics(10)
