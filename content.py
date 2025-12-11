import pandas as pd
from scripts.generate_content import generate_ai_content, generate_linkedin_image
import json
from datetime import datetime
import csv
import asyncio
from scripts.post_content import post_to_linkedin


async def start():
    try:
        linkedin_table = pd.read_csv("data/linkedin_content.csv")

        
        content = generate_ai_content(linkedin_table=linkedin_table.to_string())
        
        # linkedin_content = {
        #     'title': '',
        #     'content': '',
        #     'unique_hashtag': ''
        # }

        linkedin_content = content["linkedin"]

        linkedin_content["createdAt"] = datetime.now()
        linkedin_content["likes"] = 0
        linkedin_content["views"] = 0
        linkedin_content["comments"] = 0
        linkedin_content['summary'] = content['linkedin']['content'].split('.')[0]

        res = await post_to_linkedin(linkedin_content['content'])

        if res:
            del linkedin_content['content']

            with open("data/linkedin_content.csv", "a", newline="") as l:
                lWriter = csv.DictWriter(l, fieldnames=linkedin_content.keys())
                # lWriter.writeheader()
                lWriter.writerow(linkedin_content)

       
    except Exception as e:
        print(str(e))


asyncio.run(start())

