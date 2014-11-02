import pickle
import time


def KNNTest():

    with open('KNN_trigram.pickle') as f:
        vector = pickle.load(f)[0]

    # vector = vector[0:5000]
        
    # import pdb; pdb.set_trace()
    # split as training data and testing data
    initial_trainset    = vector[0:int(0.6*len(vector))]
    trainset    = []
    trainlabel  = []
    testset     = vector[int(0.6*len(vector))+1:]
    testlabel   = []
    topics      = {}

    label_count = 0

    # assign a unique number to each element
    # in the topic labels of vector
    for v in initial_trainset:
        topiclist = v[0]
        del v[0]
        # placelist = v[0]
        del v[0]    # --> getting rid of placelist
        for topic in topiclist:
            # if topic == 'earn':
            #     continue
            # for vectors with multiple topics
            # make multiple vectors each containing 
            # only one topic
            if topics.get(topic) is None:
                topics[topic]   = label_count
                label_count     += 1
            trainset.append(v)
            trainlabel.append(topics.get(topic))
            # might have to do something similar 
            # to what is above for placelist
    del initial_trainset

    for v in testset:
        testlabel.append([v[0]])
        del v[0]
        # we aren't using placelist right now,
        # we can revisit this later
        # placelist = v[0]
        del v[0]    # --> getting rid of placelist

    # using 'trainset', 'trainlabel' we can create our model now
    # import pdb; pdb.set_trace()
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB(alpha=1, fit_prior=True)

    offline_start = time.time()
    clf.fit(trainset, trainlabel)
    offline_time = offline_start - time.time()

    count = 0
    correct = 0
    unique_predicted = {}
    online_start = time.time()
    for v in testset:
        predicted   = clf.predict(v)
        predicted_label = [x for x in topics if topics[x] == predicted]
        unique_predicted[predicted_label[0]] = 1

        for act in testlabel[count]:
            for val in act:
                if topics.get(val) == predicted:
                    correct+=1
        count   += 1
    online_time = online_start - time.time()
    print 'correctness %'
    print (correct/(count*1.0))*100.0
    print 'unique topics'
    print len([blah for blah in unique_predicted])
    print 'offline_time'
    print offline_time
    print 'online time'
    print online_time
    a = 1
    # import pdb; pdb.set_trace()

if __name__ == "__main__":
    KNNTest()
