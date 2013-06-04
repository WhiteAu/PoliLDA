############################
LDA for Political Discourse
Authors: Amanda Strickler and Scott White
############################

############################
DEPENDENCIES
############################
This project requires the correct installation of gensim and all of its dependencies. Instructions here:
http://radimrehurek.com/gensim/install.html

Additionally, it requires Python. All other includes are python libraries that should be included in a default python installation.
If not, the required libraries are:
csv
re
sys
pickle

############################
RUNNING THE CODE
############################
This project was successfully tested on Ubuntu and CentOS distributions. Macintosh and Windows executions will likely fail.

By default, the project runs preprocesses data found under folder resources/data/reactions_oct3_4project.csv
using the coded transcript information found under 
resources/corpora/STATEMENTS2-oct3_coded_transcript_sync.csv

This is easiest done by using the provided resources Prof. Resnik gave for Political Discourse and dropping LDA-reactions.py and parserR.py in the base containing folder and running it from there.


The code can be run from the command line as follows:
###FULL DATA, NO COLUMNS DROPPED (See report)
% python LDA-reactions.py full

###CULLED DATA, COLUMNS DROPPED (See report)
% python LDA-reactions.py trunc
