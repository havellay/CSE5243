import string

from Fvector import fvector
from nltk.corpus import stopwords
from nltk.stem.porter import *

article_list = []                       # list in which we will store instances
                                        # of Article

stemmer = PorterStemmer()

FAIL = 1
DONE = 0

class Tag:
    def __init__(self, name=None, text='', tokens=[], parser=None):
        self.name   = name
        self.text   = text
        self.tokens = tokens
        self.parser = parser

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
                    self.parser.worker_tags[nested_tag].tagify_to_article(article, fp)

                    extracted   = ''
                    s           = ''
                    continue
                else:
                    print 'should never reach here'
                    import ipdb; ipdb.set_trace()
                    break

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

            # tokens as monograms
            fvector.add_to_vec_sum(article.id, self.tokens)

            # tokens as bigrams
            self.bigrams = []
            count = 0
            for v in self.tokens:
                if count == 0:
                    firstparam = v
                    count += 1
                    continue
                secondparam = v
                self.bigrams.append((firstparam, secondparam))
                firstparam = secondparam

            fvector.add_to_vec_sum(article.id, self.bigrams)

        # this new tag should be appended to an Article
        article.take_this_tag(self.name, self.text, self.tokens)

        self.text   = ''
        self.tokens = []

        if len(article_list) % 1000 == 0 or len(article_list) == 10578:
            fp.seek(0,2)
            return fp

        length  = len(s) - s.index('>', endat) + 1
        fp.seek(-1*length, 1)
        return fp
