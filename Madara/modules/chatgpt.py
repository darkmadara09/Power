import requests
from Madara import telethn as tbot
from Madara.events import register

GPT_API_URL = "https://chatgpt.apinepdev.workers.dev"


@register(pattern="^/gpt (.*)")
async def chat_gpt(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)

    if query:
        # Send "Please wait" message
        processing_message = await event.reply("Please wait, generating answer...")

        try:
            # Make a request to GPT API
            response = requests.get(f"{GPT_API_URL}/?question={query}")

            if response.status_code == 200:
                # Extract the answer from the API response
                result = response.json()

                # Check if "join" key is present and remove it
                if "join" in result:
                    del result["join"]

                # Add signature to the answer
                answer = result.get("answer", "No answer received from ChatGPT.")
                signature = "\n\nᴀɴsᴡᴇʀ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [𓆩『 ᴍᴜɪᴄʜɪʀᴏ ᴜᴘᴅᴀᴛᴇs 』𓆪](https://t.me/Muichiro_xbot)"
                reply_message = answer + signature

                # Edit the "Please wait" message with the final answer
                await processing_message.edit(reply_message)
            else:
                # If there's an error with the API, inform the user
                await processing_message.edit("Error communicating with ChatGPT API.")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            await processing_message.edit(f"Error: {str(e)}. Please try again later.")
        except Exception as e:
            # Handle unexpected errors
            await processing_message.edit(f"Unexpected error: {str(e)}. Please try again later.")
    else:
        # Provide information about the correct command format
        await event.reply("Please provide a question after /gpt command. For example: /gpt What is the meaning of life?")


__mod_name__ = "𝗖𝗛𝗔𝗧𝗚𝗣𝗧"
__help__ = """
⍟ /gpt : ᴀ ᴠᴇʀʏ ɪɴᴛᴇʟʟɪɢᴇɴᴛ ᴄʜᴀᴛɢᴘᴛ.
"""
