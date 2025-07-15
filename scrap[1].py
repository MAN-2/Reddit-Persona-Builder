#This is the data scrapper script that scapes from REddit User

import requests
import json
import os
from pathlib import Path
from sharedusername import get_username
username = get_username()

print(f"[DEBUG scrap1] imported username = {username}")

HEADERS = {"User-Agent": "Mozilla/5.0"}  # to avoid being identified as bot and getting error

def fetch_user_data(username):
    base_url = f"https://www.reddit.com/user/{username}/.json"
    posts = []
    after = None

    for _ in range(10):  
        url = base_url + (f"?after={after}" if after else "") # used to fetch pages , base and then next if it exists
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print("Error fetching:", res.status_code)
            break

        data = res.json()
        children = data.get("data", {}).get("children", []) # these contains all the posts , comments and other stuff

        for item in children:
            kind = item["kind"]
            content = item["data"]

            if kind == "t1":  # for comment
                body = content.get("body", "")
                permalink = "https://www.reddit.com" + content.get("permalink", "")
                posts.append({
                    "type": "comment",
                    "body": body,
                    "permalink": permalink,
                    "source": {
                        "text": body[:100],  
                        "permalink": permalink
                    }
                })

            elif kind == "t3":  # for post
                body = content.get("selftext", "")
                title = content.get("title", "")
                permalink = "https://www.reddit.com" + content.get("permalink", "")
                combined = f"{title}\n\n{body}".strip()
                posts.append({
                    "type": "post",
                    "body": combined,
                    "permalink": permalink,
                    "source": {
                        "text": title[:100] if title else body[:100],
                        "permalink": permalink
                    }
                })

        after = data.get("data", {}).get("after")
        if not after:
            break

    return posts

def save_posts(username, posts):
    Path("data").mkdir(exist_ok=True)
    with open(f"data/{username}.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2) #saving these in JSON

if __name__ == "__main__":
    
    if not username:
        print(" Please enter a valid Reddit username.")
    else:
        print(f"Scraping reddit user: {username}")
        data = fetch_user_data(username)
        save_posts(username, data)
        print(f" Saved {len(data)} items to data/{username}.json")
