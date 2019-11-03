from typing import List
import random

import requests
import shutterstock_utils

def get_video(queries: List[str], last_id=-1):
    while queries:
        response = requests.get("https://pixabay.com/api/videos/", params={
            "key": "14149815-c222f29ef726a4a76984900b9",
            "q": "+".join(queries),
            "safesearch": "true",
            "video_type": "film",
        })

        j = response.json()
        if j["total"]:
            hit = random.choice(j["hits"])
            print(hit["pageURL"])
            if hit["id"] == last_id != -1:
                return shutterstock_utils.get_video(queries), -1
            else:
                return hit["videos"]["medium"]["url"], hit["id"]
        del queries[-1]
    return None, -1
