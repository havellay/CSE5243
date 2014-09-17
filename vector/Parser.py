import os
import nltk
import string
import math

from Fvector import Fvector, fvector
from Article import Article
from Tag import Tag, article_list

REUTERS_DIR = '../reuters/'             # relative location of directory where
                                        # the reuters dataset is stored

FAIL = 1
DONE = 0

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
            self.worker_tags[tagnames] = Tag(name=tagnames, parser=self)

    def process_file(self, f):
        with open(REUTERS_DIR+f) as fp:
            # process 'REUTERS' from here; that will take care of the rest
            # of the tags because :
            #  - it is the first tag of interest in the document
            #  - the whole article is contained in it

            while True:
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

    # all document and article sdone, we can find the tf-idf
    # for art in article_list:
    #     bodytag = art.tags.get('BODY')
    #     if bodytag is not None:
    #         fvector.add_to_tf_idf(art.id, bodytag.tokens)

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
    ninetyninetoone(fvector.word_count_in_data)

    import ipdb; ipdb.set_trace()

