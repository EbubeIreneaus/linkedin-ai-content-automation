from playwright.async_api import async_playwright
import asyncio


# async def post_to_x(content: str):
#     try:
#         async with async_playwright() as p:
#             context = await p.chromium.launch_persistent_context(
#                 user_data_dir="chrome",
#                 args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
#                 headless=False
#             )
#             page = await context.new_page()
#             await page.goto('https://x.com')
            
#             text_field = page.locator('[data-testid="tweetTextarea_0"]')
#             await text_field.wait_for(state="visible")
            
#             content_paragraphs = content.split('\n')

#             for paragraph in content_paragraphs:
#                 await text_field.press_sequentially(paragraph)
#                 await text_field.press('Shift+Enter')

#             send_button = page.locator('[data-testid="tweetButtonInline"]')
#             await send_button.wait_for(state='visible')
#             await send_button.click(force=True)

#             await page.wait_for_timeout(5000)

#             await text_field.clear()
            
#             await page.wait_for_timeout(5000)

#             await context.close()

#     except Exception as e:
#         pass

async def post_to_linkedin(content: str):
    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir='chrome',
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
                headless=False
            )
            page = await context.new_page()
            await page.goto('https://linkedin.com/feed', timeout=100000)

            post_dialog_button = page.get_by_role('button', name="Start a post")
            await post_dialog_button.wait_for(state="visible")
            await post_dialog_button.click(force=True)

            editor = page.get_by_role('textbox', name="Text editor for creating content")
            await editor.wait_for(state='visible')
            await editor.focus()

            content_paragraphs = content.split('\n')

            for paragraph in content_paragraphs:
                await editor.press_sequentially(paragraph)
                await editor.press('Enter')

            await asyncio.sleep(15)

            post_button = page.get_by_role('button', name="Post", exact=True)
            await post_button.wait_for(state='visible')
            await post_button.click()

            await asyncio.sleep(10)

            dismiss_btn = page.get_by_role('button', name='Dismiss').nth(0)
            await dismiss_btn.wait_for(state="visible", timeout=5000)
            await dismiss_btn.click()

            await asyncio.sleep(10)

            await context.close()
        return True
    except Exception as e:
        print("Linkedin Error: ", e)
        return False