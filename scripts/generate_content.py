import pandas as pd
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import re
from io import BytesIO
from PIL import Image
from helpers.ai_helper import linkedin_image_prompt
from datetime import datetime
import json


load_dotenv()


from helpers.ai_helper import content_generate_prompt

client = genai.Client()


def generate_ai_content(linkedin_table: pd.DataFrame):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=f"""
{content_generate_prompt}

Table for Platform: Linkedin

{linkedin_table}
"""
        )
        clean_response =re.sub(r"```[a-zA-Z]*\n?|```", "", response.text).strip()
        return json.loads(clean_response)

    except Exception as e:
        print(str(e))

def generate_linkedin_image(title):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[linkedin_image_prompt(title)]
        )

        for part in response.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = part.as_image()
                image.save(f"/data/images/{'-'.join(title.split(' '))-datetime.now()}.png")
                print(image)
    except Exception as e:
        print(f"Error Generating Image {str(e)}")