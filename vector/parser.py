import os

REUTERS_DIR = '../reuters/'             # relative location of directory where
                                        # the reuters dataset is stored
    
article_list = []                       # list in which we will store instances
                                        # of Article

FAIL = 1
DONE = 0

class Article:
    def __init__(self, x, buff):
        self.id         = x
        self.full_text  = buff

class Tag:
    def __init__(self, name):
        self.name = name
        # should find some way of returning two packed tag objects?

    def take_full_text(self, fp):
        buff    = ''

        while True:
            s = fp.readline()
            if not s:
                print 'Couldn\'t read'
                return FAIL

            if '<'+self.name in s:
                startfrom   = s.index('<'+self.name)
                buff        = s[startfrom:]+' '
                in_this_tag = True
            elif in_this_tag is True:
                if '</'+self.name+'>' in s:
                    endat   = s.index('</'+self.name+'>')
                    in_this_tag = False
                else:
                    endat   = len(s)
                buff += s[0:endat]+' '
                if in_this_tag is False:
                    article_list.append(Article(len(article_list)+1, buff))
        return fp


class Parser:
    def __init__():
        # create instances for all kinds of tags
        interesting_tags = ['DATE', 'TOPICS', 'PLACES', 'D',
                            'PEOPLE', 'ORGS', 'EXCHANGES', 'COMPANIES',
                            'UNKNOWN', 'TEXT', 'DATELINE', 'BODY']
        tags = {}
        for tagnames in interesting_tags:
            tags[tagnames] = Tag(tagnames)

    def process_file(f):
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
                    s.readline()
                length = len(s) - s.index('<REUTERS')
                fp.seek(-1*length, 1)

                # now, fp is where 'REUTERS' tag begins
                # HARI : may not need this 'fp = ...'
                fp = tags['REUTERS'].take_full_text(fp)

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
    print len(article_list)
