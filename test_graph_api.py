from pymongo import MongoClient
import AccessTokens
## local mongodb connection
client = MongoClient("localhost", 27017)
db = client["test"]
collection = db["fb_raw"]

import requests

def get_page_posts(page):
	nba_fb_posts = []

	access_token = AccessTokens.fb_access_token

	base_url = "https://graph.facebook.com/v2.5/%s/posts?limit=100&access_token=%s" %(page, access_token)

	r = requests.get(base_url)
	response = r.json()
	nba_fb_posts.extend(response["data"])

	print nba_fb_posts[-1]

	while(len(nba_fb_posts)<500):
		until = response["paging"]["next"].split("&until=")[1]
		next_url = "https://graph.facebook.com/v2.5/%s/posts?limit=100&_paging_token=%s&until=%s&access_token=%s" %(page, response["paging"]["next"], until, access_token)
		r = requests.get(next_url)
		response = r.json()
		nba_fb_posts.extend(response["data"])
		print len(nba_fb_posts), nba_fb_posts[-1]

	result = collection.insert_many(nba_fb_posts)
	print result.inserted_ids[:10]

if __name__ == '__main__':
	get_page_posts("nba")
	get_page_posts("nbatv")