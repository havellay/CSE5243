import string

from Fvector import fvector,fvector_bigram,fvector_trigram
from nltk.corpus import stopwords
from nltk.stem.porter import *

article_list = []                       # list in which we will store instances
                                        # of Article

stemmer = PorterStemmer()

FAIL = 1
DONE = 0

class Tag:
    def __init__(
            self, name=None, text='', monograms=[],
            bigrams=[], trigrams=[], parser=None,
            topiclist=[], placelist=[],
        ):
        self.name       = name
        self.text       = text
        self.monograms  = monograms
        self.bigrams    = bigrams
        self.trigrams   = trigrams
        self.parser     = parser
        self.topiclist  = topiclist
        self.placelist  = placelist

    def tagify_to_article(self, article, fp):
        # this method should be split into smaller functions
        hit_count   = 0
        while True:
            # FIX
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
                    self.parser.worker_tags[nested_tag].tagify_to_article(article, fp)

                    extracted   = ''
                    s           = ''
                    continue
                else:
                    print 'should never reach here'
                    import pdb; pdb.set_trace()
                    break

            self.text   += extracted+' '
            s   = s[endat + len(self.name+'>'):]

        def get_rid_of_D(param):
            temp_str = ''
            exc = set('<>D /')
            for ch in param:
                if ch in exc:
                    temp_str += ' '
                else:
                    temp_str += ch
            string_list = temp_str.split()
            return string_list

        # we need to clean the 'TOPICS' and 'PLACES'
        if self.name == 'TOPICS':
            self.topiclist  = get_rid_of_D(self.text)

        if self.name == 'PLACES':
            self.placelist  = get_rid_of_D(self.text)

        # we have all the text at this point; we should
        # do the token processing at this stage.
        if self.name == 'BODY':
            exclude = set(string.punctuation)

            # text    = ''.join(ch for ch in self.text if ch not in exclude)
            # can we change the following code to a statement like above?
            text = ''
	    for ch in  self.text:
                if ch in exclude:
                    text += ' '
                else:
                    text += ch

            all_monos   = text.split()
            try:
                self.monograms = [string.lower(stemmer.stem(w)) for w in all_monos if not w in stopwords.words('english') and not w.isdigit() and len(w) > 1]
            except UnicodeWarning:
                print 'Unicode warning; no worry'
            
            count = 0
            firstParam = secondParam = thirdParam = 0
            for tok in self.monograms:
                if count == 0:
                    firstParam = tok
                    count+=1
                    continue
                elif count == 1:
                    secondParam = tok
                    count+=1
                    continue
                else:
                    thirdParam = tok
                    count+=1
 
                # FIX value loss here
                self.bigrams.append((firstParam,secondParam))
                if count != 1:
                    self.trigrams.append((firstParam,secondParam,thirdParam))
                firstParam = secondParam
                secondParam = thirdParam

            fvector.add_to_vec_sum(article.id,self.monograms)
            fvector_bigram.add_to_vec_sum(article.id, self.bigrams)
            fvector_trigram.add_to_vec_sum(article.id, self.trigrams)

        # this new tag should be appended to an Article
        article.take_this_tag(
                tag_name=self.name,
                tag_text=self.text,
                tag_monograms=self.monograms,
                tag_bigrams=self.bigrams,
                tag_trigrams=self.trigrams,
                tag_topiclist=self.topiclist,
                tag_placelist=self.placelist,
            )

        self.text       = ''
        self.monograms  = []
        self.bigrams    = []
        self.trigrams   = []
        self.topiclist  = []
        self.placelist  = []

        # THIS SHOULD BE FIXED
        if len(article_list) % 1000 == 0 or len(article_list) == 21578:
            fp.seek(0,2)
            return fp

        try:
            length  = len(s) - s.index('>', endat) + 1
        except:
            fp.seek(0,2)
            return fp
        fp.seek(-1*length, 1)
        return fp
