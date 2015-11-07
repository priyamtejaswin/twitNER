import pickle, difflib

def find_popular(entity_dict):
    popular = {}
    for entity_type, list_of_entities in entity_dict.items():
        popular[entity_type] = {}
        for entity in list_of_entities:
            if popular[entity_type].get(entity, -1)!=-1:
                popular[entity_type][entity]+=1

            else:
                closest_match = difflib.get_close_matches(entity, set(popular[entity_type].keys()), n=1, cutoff=0.5)            
                if len(closest_match)==1:
                    popular[entity_type][closest_match[0]]+=1
                else:
                    popular[entity_type][entity] =1
    return popular

def find_common(fb, tw):
    fb_popular, tw_popular = find_popular(fb), find_popular(tw)
    print "--from facebook--"
    for entity_type, list_of_entities in fb_popular.items():
        print entity_type.upper(), sorted(list_of_entities.items(), key=lambda x:x[1], reverse=True)[:5], "\n"

    print "--from twitter--"
    for entity_type, list_of_entities in tw_popular.items():
        print entity_type.upper(), sorted(list_of_entities.items(), key=lambda x:x[1], reverse=True)[:5], "\n"

    print "--common--"
    common_entity_types = set(fb_popular.keys()).intersection(set(tw_popular.keys()))
    for entity_type in common_entity_types:
        common_entities = set(fb_popular[entity_type].keys()).intersection(set(tw_popular[entity_type].keys()))
        if len(common_entities)>0:
            print entity_type.upper(), sorted([(e, fb_popular[entity_type][e]+tw_popular[entity_type][e]) for e in common_entities], reverse=True, key=lambda tup:tup[1])[:5]

if __name__ == '__main__':
    fb = pickle.load(open("facebook_ners_pkl", "r"))
    tw = pickle.load(open("twitter_ners_pkl", "r"))

    ritter_fb = pickle.load(open("ritter_fb_nes_pkl", "r"))
    ritter_tw = pickle.load(open("ritter_tw_nes_pkl", "r"))

    print "\n********************************Using Stanford NER**************************************\n"
    find_common(fb, tw)

    print "\n********************************Using Alan Ritters twitter specific parser**************************************\n"
    find_common(ritter_fb, ritter_tw)