from pymongo import MongoClient
import pickle
## local mongodb connection
client = MongoClient("localhost", 27017)
db = client["test"]
collection = db["nba_raw"]

import nltk
from nltk.tag.stanford import NERTagger
tagger = NERTagger("stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz", "stanford-ner-2014-06-16/stanford-ner.jar", encoding='utf-8')

def stanford_ner(text):
    for sent in nltk.sent_tokenize(text):
        ne_tagged_sent = tagger.tag(nltk.word_tokenize(sent))[0]
        named_entities = get_continuous_chunks(ne_tagged_sent)
        named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
        named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

        print named_entities_str_tag, "\n"
                # if tup[1]!="O" and tup[1]!="B":

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if (tag != "O") and (tag != "B"):
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

def nltk_ner(text):
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if len(chunk)==1:
                print chunk
                raw_input("--")

if __name__ == '__main__':
    i=0
    list_of_sentences = []

    for tweet in collection.find():
        try:
            text = tweet["text"].decode("utf-8")
            print "\nTWEET %d:" %(i), text
            tkzd_sentences = [nltk.word_tokenize(tkzd_sent) for tkzd_sent in nltk.sent_tokenize(text)]
            list_of_sentences.extend(tkzd_sentences)

            i+=1

        except Exception as error:
            if "utf" in str(error):
                pass
            else:
                print "SOMETHING HAPPENED"
    
    print "\nxxxxxxxxxxx-------------xxxxxxxxxxx\n"
    print len(list_of_sentences)
    print i
    # raw_input("...continue?")

    IOB_sentences = tagger.tag_sents(list_of_sentences)
    print len(IOB_sentences)
    twitter_ners = {}
    for ne_tagged_sent in IOB_sentences:
        named_entities = get_continuous_chunks(ne_tagged_sent)
        named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
        named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

        if len(named_entities_str_tag)>0:
            for string, tag in named_entities_str_tag:
                try:
                    twitter_ners[tag].append(string)
                except:
                    twitter_ners[tag] = [string]

    for k,v in twitter_ners.items():
        print k, len(v)
    fp = open("twitter_ners_pkl", "w")
    pickle.dump(twitter_ners, fp)
    fp.close()
    print "twitter ners pickle successfully created"