# Imports
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from nltk.corpus import wordnet
from nltk import word_tokenize
import string
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')



# Get default English stopwords and extend with punctuation
_stopwords = nltk.corpus.stopwords.words('english')
_stopwords.extend(string.punctuation)
_stopwords.append('')
_lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
_stemmer = nltk.stem.snowball.SnowballStemmer('english')

def _get_wordnet_pos(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wordnet.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wordnet.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wordnet.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wordnet.ADV)
    else:
        return (pos_tag[0], wordnet.NOUN)

def match_titles(a, b):

    """Check if a and b are matches."""
    pos_a = map(_get_wordnet_pos, nltk.pos_tag(word_tokenize(a)))
    pos_b = map(_get_wordnet_pos, nltk.pos_tag(word_tokenize(b)))
    
    lemmae_a = [_lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                    if token.lower().strip(string.punctuation) not in _stopwords]
    lemmae_b = [_lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                    if token.lower().strip(string.punctuation) not in _stopwords]
    
    # tokens_a = [token.lower().strip(string.punctuation) for token in word_tokenize(a) \
    #                 if token.lower().strip(string.punctuation) not in _stopwords]
    # tokens_b = [token.lower().strip(string.punctuation) for token in word_tokenize(b) \
    #                 if token.lower().strip(string.punctuation) not in _stopwords]
    # stems_a = [_stemmer.stem(token) for token in tokens_a]
    # stems_b = [_stemmer.stem(token) for token in tokens_b]

    return (lemmae_a == lemmae_b)
    # return (stems_a == stems_b)
    