import pandas as pd
from playwright.async_api import async_playwright, Page
from datetime import datetime, timedelta
import asyncio
import re

l = pd.read_csv('data/linkedin_content.csv')

l_csv = pd.DataFrame(l)

x_cont_to_update = []
l_cont_to_update = []

def extract_unique_snippet(text: str, length: int = 60):
    # Remove emojis (because they break DOM matching)
    clean_text = re.sub(r"[^\w\s,.!?&'-]", "", text)

    # Remove extra spaces
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    # Return the first substring under length
    if len(clean_text) <= length:
        return clean_text

    return clean_text[:length].rsplit(" ", 1)[0]  # avoid cutting a word


async def extract_engagement(post):
    try:
        impressions_raw = await post.locator("text=/impressions/i").inner_text()
        impressions = re.findall(r'\d[\d,]*', impressions_raw)[0]
    except:
        impressions = "0"

    # Likes
    try:
        like_button = post.get_by_role("button", name=re.compile(r"^\d+\s+reaction")).first
        like_raw = await like_button.inner_text()
        like_num = re.findall(r'\d+', like_raw)
        likes = like_num[0] if like_num else "0"
    except Exception as e:
        likes = "0"

    # Comments
    try:
        comment_raw = await post.locator("text=/comment/i").first.inner_text()
        comment_num = re.findall(r'\d+', comment_raw)
        comments = comment_num[0] if comment_num else "0"
    except:
        comments = "0"

    return {
        "views": int(impressions),
        "likes": int(likes),
        "comments": int(comments),
    }


for index, row in l_csv.iterrows():
    createdAt =  datetime.strptime("2025-12-09 13:17:24.461200", "%Y-%m-%d %H:%M:%S.%f")
    seven_days_from_createdAt = createdAt + timedelta(days=14)
    today = datetime.now()

    if today < seven_days_from_createdAt:
        l_cont_to_update.append({
            'index': index,
            'summary': row['summary'],
            'unique_hashtag': row['unique_hashtag']
        })

async def l_lookup():
    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir="chrome",
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
            )
            page = await context.new_page()
            await page.goto('https://www.linkedin.com/in/ireneaus/recent-activity/all/', timeout=100000)

            await page.wait_for_selector('h2:has-text("All activity")')

            group_button = page.get_by_role('group', name="Select type of recent activity")
            await group_button.get_by_role('button', name="Posts").click()
            
            for row in l_cont_to_update:
                try:
                    hashtag = row["unique_hashtag"]
                    ul = page.locator(f"ul:has-text('{hashtag}')")
                    post = ul.get_by_role('listitem').filter(has_text=f"{hashtag}").nth(0)
                    result = await extract_engagement(post)
                    l_csv.loc[row['index'], 'views'] = result.get('views', l_csv.loc[row['index'], 'views'])
                    l_csv.loc[row['index'], 'comments'] = result.get('comments', l_csv.loc[row['index'], 'comments'])
                    l_csv.loc[row['index'], 'likes'] = result.get('likes', l_csv.loc[row['index'], 'likes'])

                except Exception:
                    pass
            await context.close()
            l_csv.to_csv('data/linkedin_content.csv', index=False)
            # print(l_csv)

    except Exception as e:
        print(e)


asyncio.run(l_lookup())




