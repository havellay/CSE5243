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
    def __init__(lex):
        self.lex = lex

class Parser:
    def __init__():
        # create instances for all kinds of tags
        [reuters_stag, reuters_etag]    = Tag('REUTERS')
        [date_stag, date_etag]          = Tag('DATE')
        [topics_stag, topics_etag]      = Tag('TOPICS')
        [places_stag, places_etag]      = Tag('PLACES')
        [d_stag, d_etag]                = Tag('D')      # Do we need this?
        [people_stag, people_etag]      = Tag('PEOPLE')
        [orgs_stag, orgs_etag]          = Tag('ORGS')
        [exchanges_stag, exchanges_etag]= Tag('EXCHANGES')
        [companies_stag, companies_etag]= Tag('COMPANIES')
        [unknown_stag, unknown_etag]    = Tag('UNKNOWN')
        [text_stag, text_etag]          = Tag('TEXT')
        [dateline_stag, dateline_etag]  = Tag('DATELINE')
        [body_stag, body_etag]          = Tag('BODY')

    def process_file(f):
        try:
            fp = open(REUTERS_DIR+f)
        except:
            print "COULDN'T OPEN "+REUTERS_DIR+f
            return FAIL

        in_reuters  = False
        s           = '1'
        buff        = ''

        while s:
            try:
                s = fp.readline()
            except:
                print "COLDN'T READ LINE"
                return FAIL

            if '<REUTERS' in s:
                startfrom   = s.index('<REUTERS')
                buff        = s[startfrom:]+' '
                in_reuters  = True
            elif in_reuters is True:
                if '</REUTERS>' in s:
                    endat   = s.index('</REUTERS>')
                    in_reuters = False
                else:
                    endat   = len(s)
                buff += s[0:endat]+' '
                if in_reuters is False:
                    article_list.append(Article(len(article_list)+1, buff))

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
