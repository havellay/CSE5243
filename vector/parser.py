import os
import nltk
import string
import math

from nltk.stem.porter import *
from nltk.corpus import stopwords

REUTERS_DIR = '../reuters/'             # relative location of directory where
                                        # the reuters dataset is stored
    
article_list = []                       # list in which we will store instances
                                        # of Article

FAIL = 1
DONE = 0

stemmer = PorterStemmer()

class Fvector:
    vec_sum     = {}            # feature vector that contains the sum of the
                                # different tokens in the tag

    vec_tfidf   = {}            # feature vector that contains TFIDF of tokens

    doc_with_word   = {}        # a dict that stores the number of docs that
                                # contain a word
    abs_doc_with_word = {}      #

    def add_to_vec_sum(self, articleid, tokens):
        max_freq = 0
        v   = {}
        for tok in tokens:
            tok = string.lower(tok)
            if v.get(tok) is None:
                v[tok]  = 1
            else:
                v[tok]  += 1

            if self.abs_doc_with_word.get(tok) is None:
                self.abs_doc_with_word[tok] = 1
            else:
                self.abs_doc_with_word[tok] += 1

            max_freq    = max(v[tok], max_freq)

        for tok in v: #Unique words - v
            tok = string.lower(tok)
            v[tok]  = 0.5 + (0.5*v[tok])/max_freq
            if self.doc_with_word.get(tok) is None:
                self.doc_with_word[tok]  = 1
            else:
                self.doc_with_word[tok]  += 1

        self.vec_sum[articleid] = v

    def add_to_tf_idf(self, articleid, tokens):
        tf_dict = vec_sum[articleid]
        v       = {}
        tokset  = set(tokens)

        for tok in tokset:
            tok = string.lower(tok)
            v[tok]  = tf_dict[tok]*(
                        math.log(len(article_list)/self.doc_with_word[tok])
                    )

        self.vec_tfidf[articleid] = v

fvector = Fvector()

class Article:
    def __init__(self, x):
        self.id     = x                 # an 'id' is actually not needed at all

        self.tags   = {}                # a dictionary containing all the tags
                                        # in an article

    def take_this_tag(self, tag_name, tag_text, tag_tokens):
        self.tags[tag_name] = Tag(tag_name, tag_text, tag_tokens)
        # should we make sure whether there is already a tag with this name? It
        # could become an issue for tags such as <D> of which there might
        # already be a copy

class Tag:
    def __init__(self, name, text='', tokens=[]):
        self.name   = name
        self.text   = text
        self.tokens = tokens

    def tagify_to_article(self, article, fp):
        hit_count   = 0
        while True:

            # This is purely a hack; need to fix what happens
            # for the last article
            if len(article_list) % 1000 == 0:
                hit_count   += 1
                if hit_count == 10:
                    break

            s = fp.readline()
            if not s:
                print 'Couldn\'t read'
                return FAIL

            startfrom   = 0
            endat       = len(s)

            if '<'+self.name in s:
                startfrom   = s.index('>', s.index('<'+self.name)+1)+1
                in_this_tag = True
            if s == '\n':
                continue
            if in_this_tag is True and '</'+self.name+'>' in s:
                endat       = s.index('</'+self.name+'>')
                in_this_tag = False
                # we are done processing the tag in question
                # and so, can break here
                extracted   = s[startfrom:endat-1]          # 'extracted'
                self.text   += extracted
                break

            extracted   = s[startfrom:endat-1]          # 'extracted'

            # ideally, extracted should begin with '<' if there is a
            # nested tag
            if '<' in extracted:
                if extracted[extracted.index('<')+1] is not '/':
                    # this text signifies the name of the nested tag that
                    # we are extracting
                    begins_at   = extracted.index('<')+1
                    space_at    = tag_ends_at   = len(extracted)+1000

                    if ' ' in extracted[begins_at:]:
                        space_at    = extracted.index(' ', begins_at+1)
                    if '>' in extracted[begins_at:]:
                        tag_ends_at = extracted.index('>', begins_at+1)

                    if space_at < tag_ends_at:
                        tag_until   = space_at
                    else:
                        tag_until   = tag_ends_at

                    nested_tag  = extracted[begins_at:tag_until]

                    length  = len(s) - s.index('<'+nested_tag) + 1
                    # it looks like this should be .... -1 ^

                    fp.seek(-1*length, 1)
                    parser.worker_tags[nested_tag].tagify_to_article(article, fp)

                    extracted   = ''
                    s           = ''
                    # import ipdb; ipdb.set_trace()
                    continue
                    # break
                else:
                    print 'should never reach here'
                    import ipdb; ipdb.set_trace()
                    break
                    hari = 1   # just skipping closing tags

            # think about whether to store stripped strings
            self.text   += extracted+' '
            s   = s[endat + len(self.name+'>'):]

        # we have all the text at this point; we should
        # do the token processing at this stage.
        if self.name == 'BODY':
            exclude = set(string.punctuation)
            text = ''
	    for ch in  self.text:
                if ch in exclude:
                    text += ' '
                else:
                    text += ch

            # text    = ''.join(ch for ch in self.text if ch not in exclude)
            all_tokens = text.split()
            all_tokens = [w for w in all_tokens if not w in stopwords.words('english')]
            all_tokens = [w for w in all_tokens if w.isdigit() is False]
            for tok in all_tokens:
                self.tokens.append(stemmer.stem(tok))
            fvector.add_to_vec_sum(article.id, self.tokens)
            # fvector.add_to_tf_idf(article.id, self.tokens)

        # this new tag should be appended to an Article
        article.take_this_tag(self.name, self.text, self.tokens)
        # if len(self.text) is 0:
        #     print '{} doesn\'t have any text'.format(self.name)

        self.text   = ''
        self.tokens = []

        if len(article_list) % 1000 == 0 or len(article_list) == 10578:
            fp.seek(0,2)
            return fp

        length  = len(s) - s.index('>', endat) + 1
        # import ipdb; ipdb.set_trace()       # make sure that this is alright
        fp.seek(-1*length, 1)
        return fp

class Parser:
    worker_tags = {}

    def __init__(self):
        # create instances for all kinds of tags
        interesting_tags = ['REUTERS', 'DATE', 'TOPICS', 'PLACES', 'D',
                            'PEOPLE', 'ORGS', 'EXCHANGES', 'COMPANIES',
                            'UNKNOWN', 'TEXT', 'DATELINE', 'BODY', 
                            'TITLE', 'AUTHOR', 'MKNOTE']

        # 'tags' is a dictionary containing instances of tags that are just
        # meant to be worker tag objects; they won't hold any data in them
        # each tag will have methods that process plain text and invoke
        # an article's take_this_tag() method which clones the tag and then,
        # the contents of the worker tags are cleared
        for tagnames in interesting_tags:
            self.worker_tags[tagnames] = Tag(tagnames)

    def process_file(self, f):
	
        with open(REUTERS_DIR+f) as fp:
            # process 'REUTERS' from here; that will take care of the rest
            # of the tags because :
            #  - it is the first tag of interest in the document
            #  - the whole article is contained in it

            while True:
		print f
                s = fp.readline()
                if not s:
                    break

                # seek the file object to the beginning of the 'REUTERS' tag
                while '<REUTERS' not in s:
                    s = fp.readline()
                length = len(s) - s.index('<REUTERS')
                fp.seek(-1*length, 1)

                # now, fp is where 'REUTERS' tag begins
                article = Article(len(article_list)+1)
                article_list.append(article)
                self.worker_tags['REUTERS'].tagify_to_article(article, fp)
                # print 'article {} done'.format(article.id)

        print 'DONE WITH {}'.format(f)
        return DONE

parser = Parser()

def ninetyninetoone(count_list):
    maximum = 0
    minimum = 100
    for v in count_list:
        maximum = max(count_list[v], maximum)
        minimum = min(count_list[v], minimum)

    freq_range = maximum - minimum
    interesting_upper = maximum - 0.01*freq_range
    interesting_lower = minimum + 0.01*freq_range

    considering_this = []
    for v in count_list:
        if count_list[v] <= interesting_upper and count_list[v] >= interesting_lower:
            considering_this.append(v)
    import ipdb; ipdb.set_trace()

def main():
    # Finding all the files in the REUTERS directory
    for f in os.listdir(REUTERS_DIR):
        if f.endswith('.sgm'):
            parser.process_file(f)
            # call the vector finder class or something for each file

if __name__ == "__main__":
    main()
    print 'Processed {} articles'.format(len(article_list))

    not_needed  = []
    needed      = []

    for v in fvector.doc_with_word:
        if fvector.doc_with_word[v] == 1:
            not_needed.append(v)
        else:
            needed.append(v)

    ninetyninetoone(fvector.doc_with_word)
    ninetyninetoone(fvector.abs_doc_with_word)

    import ipdb; ipdb.set_trace()

