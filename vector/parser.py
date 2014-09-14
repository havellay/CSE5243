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
        import ipdb; ipdb.set_trace()
        while True:
            s = fp.readline().strip()
            if not s:
                print 'Couldn\'t read'
                return FAIL

            startfrom   = 0
            endat       = len(s)

            if '<'+self.name in s:
                startfrom   = s.index('>', s.index('<'+self.name)+1)+1
                in_this_tag = True
            else:
                if in_this_tag is True and '</'+self.name+'>' in s:
                    endat       = s.index('</'+self.name+'>')
                    in_this_tag = False
                    # we are done processing the tag in question
                    # and so, can break here
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
                    fp.seek(-1*length, 1)
                    parser.tags[nested_tag].tagify_to_article(article, fp)

                    extracted   = ''
                    s           = ''
                    break
                else:
                    hari = 1   # just skipping closing tags

            # think about whether to store stripped strings
            self.text   += extracted+' '
            s   = s[endat + len(self.name+'>'):]

        # we have all the text at this point; we should
        # do the token processing at this stage.
        

        # this new tag should be appended to an Article
        article.take_this_tag(self.name, self.text, self.tokens)
        self.text   = ''
        self.tokens = []

        fp.seek(-1*len(s), 1)
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

parser = Parser()

def main():
    # Finding all the files in the REUTERS directory
    for f in os.listdir(REUTERS_DIR):
        if f.endswith('.sgm'):
            parser.process_file(f)
            # call the vector finder class or something for each file

if __name__ == "__main__":
    main()
    print 'Processed {} articles'.format(len(article_list))
    import ipdb; ipdb.set_trace()
