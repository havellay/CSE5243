import string

class Fvector:
    def __init__(self):
        self.vec_sum     = {}   # feature vector that contains the sum of the
                                # different tokens in the tag

        self.vec_tfidf   = {}   # feature vector that contains TFIDF of tokens

        self.doc_with_gram   = {}
                                # a dict that stores the number of docs that
                                # contain a gram

        self.gram_count_in_data = {}
                                # a dict that stores the number of times the 
                                # gram occurs across document
        
    def add_to_vec_sum(self, articleid, tokens):
        max_freq= 0
        v       = {}

        for tok in tokens:
            if v.get(tok) is None:
                v[tok]  = 1
            else:
                v[tok]  += 1

            if self.gram_count_in_data.get(tok) is None:
                self.gram_count_in_data[tok] = 1
            else:
                self.gram_count_in_data[tok] += 1

            max_freq    = max(v[tok], max_freq)

        for tok in v: #Unique grams - v
            v[tok]  = 0.5 + (0.5*v[tok])/max_freq
            if self.doc_with_gram.get(tok) is None:
                self.doc_with_gram[tok]  = 1
            else:
                self.doc_with_gram[tok]  += 1

        self.vec_sum[articleid] = v

    def add_to_tf_idf(self, articleid, tokens):
        tf_dict = self.vec_sum[articleid]
        v       = {}
        tokset  = set(tokens)

        for tok in tokset:
            tok = string.lower(tok)
            v[tok]  = tf_dict[tok]*(
                        math.log(21578/self.doc_with_gram[tok])
                    )

        self.vec_tfidf[articleid] = v

fvector = Fvector()
fvector_bigram = Fvector()
fvector_trigram = Fvector()
