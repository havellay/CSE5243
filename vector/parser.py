import os

REUTERS_DIR = '../reuters/'             # relative location of directory where
                                        # the reuters dataset is stored
    
article_list = []                       # list in which we will store instances
                                        # of Article

FAIL = 1
DONE = 0

class Article:
    def __init__(self, x):
        self.id     = x                 # an 'id' is actually not needed at all

        self.tags   = {}                # a dictionary containing all the tags
                                        # in an article

    def take_this_tag(self, tag_name, tag_text, tag_tokens):
        self.tags[tag_name] = Tag(tag_name, tag_text, tag_tokens)
        # should we make sure whether there is already a tag with this name? It
        # could become an issue for tags such as <D> of which there might already
        # be a copy

class Tag:
    def __init__(self, name, text='', tokens=[]):
        self.name   = name
        self.text   = text
        self.tokens = tokens

    def tagify_to_article(self, article, fp):
        while True:
            s = fp.readline()
            if not s:
                print 'Couldn\'t read'
                return FAIL

            if '<'+self.name in s:
                startfrom   = s.index('<'+self.name)
                self.text   += s[startfrom:]+' '
                in_this_tag = True
            elif in_this_tag is True:
                if '</'+self.name+'>' in s:
                    endat   = s.index('</'+self.name+'>')
                    in_this_tag = False
                else:
                    endat   = len(s)
                self.text   += s[0:endat]+' '
                if in_this_tag is False:
                    # we are done processing the tag in question
                    # and so, can break here
                    break

        # we have all the text at this point; we should
        # do the token processing at this stage.

        # this new tag should be appended to an Article
        article.take_this_tag(self.name, self.text, self.tokens)
        self.text   = ''
        self.tokens = []
        return fp

class Parser:
    tags = {}

    def __init__(self):
        # create instances for all kinds of tags
        interesting_tags = ['REUTERS', 'DATE', 'TOPICS', 'PLACES', 'D',
                            'PEOPLE', 'ORGS', 'EXCHANGES', 'COMPANIES',
                            'UNKNOWN', 'TEXT', 'DATELINE', 'BODY']

        # 'tags' is a dictionary containing instances of tags that are just
        # meant to be worker tag objects; they won't hold any data in them
        # each tag will have methods that process plain text and invoke
        # an article's take_this_tag() method which clones the tag and then,
        # the contents of the worker tags are cleared
        for tagnames in interesting_tags:
            self.tags[tagnames] = Tag(tagnames)

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
                self.tags['REUTERS'].tagify_to_article(article, fp)

        print 'DONE WITH {}'.format(f)
        return DONE

def main():
    # Finding all the files in the REUTERS directory
    for f in os.listdir(REUTERS_DIR):
        if f.endswith('.sgm'):
            parser = Parser()
            parser.process_file(f)
            # call the vector finder class or something for each file

if __name__ == "__main__":
    main()
    print 'Processed {} articles'.format(len(article_list))
