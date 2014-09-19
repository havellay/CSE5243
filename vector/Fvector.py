import string
import math

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
            v[tok]  = tf_dict[tok]*(
                        math.log(21578/self.doc_with_gram[tok])
                    )

        self.vec_tfidf[articleid] = v

    def complete_feature_vector(self, article_list, file_name_count):
        for article in article_list:
            if article.tags.get('BODY') is None:
                continue
            vectors_to_change = [self.vec_sum, self.vec_tfidf]
            for vector in vectors_to_change:
                v = vector[article.id]
                v['TOPICS_TAG_INFO']    = article.tags['TOPICS'].text
                v['PLACES_TAG_INFO']    = article.tags['PLACES'].text
                v['ARTICLE_ID_INFO']    = article.id

        # writing the feature vector to a file
        f = open('../output/featurevector'+str(file_name_count), 'w')
        for article_id in self.vec_sum:
            f.write(str(self.vec_sum[article_id]['ARTICLE_ID_INFO'])+',')
            f.write(str(self.vec_sum[article_id]['TOPICS_TAG_INFO'])+',')
            f.write(str(self.vec_sum[article_id]['PLACES_TAG_INFO'])+',')
            for key in self.vec_sum[article_id]:
                if key not in ['TOPICS_TAG_INFO', 'PLACES_TAG_INFO', 'ARTICLE_ID_INFO']:
                    f.write(str(key)+':'+str(self.vec_sum[article_id][key])+',')
            f.write('\n')
        f.close()

        f = open('../output/featurevector'+str(file_name_count+1), 'w')
        for article_id in self.vec_tfidf:
            f.write(str(self.vec_tfidf[article_id]['ARTICLE_ID_INFO'])+',')
            f.write(str(self.vec_tfidf[article_id]['TOPICS_TAG_INFO'])+',')
            f.write(str(self.vec_tfidf[article_id]['PLACES_TAG_INFO'])+',')
            for key in self.vec_tfidf[article_id]:
                if key not in ['TOPICS_TAG_INFO', 'PLACES_TAG_INFO', 'ARTICLE_ID_INFO']:
                    f.write(str(key)+':'+str(self.vec_tfidf[article_id][key])+',')
            f.write('\n')
        f.close()

        print 'Feature vector complted : examine'
        import pdb; pdb.set_trace()

fvector = Fvector()
fvector_bigram = Fvector()
fvector_trigram = Fvector()
