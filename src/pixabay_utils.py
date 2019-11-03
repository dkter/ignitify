from typing import List
import random

import requests

def get_video(queries: List[str]):
    while queries:
        response = requests.get("https://pixabay.com/api/videos/", params={
            "key": "14149815-c222f29ef726a4a76984900b9",
            "q": "+".join(queries),
        })

        j = response.json()
        if j["total"]:
            return random.choice(j["hits"])["videos"]["medium"]["url"]
        del queries[-1]
