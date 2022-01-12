import os
from pyrogram import filters, Client


@Client.on_message(filters.incoming & ~filters.edited)
async def newrequest(client, message):       



if message.text.startswith("#request"):
    try:
        req=message.text.replace("#request", " ")
        if req == " ":      
            await message.reply("What..?")
        else:
             await client.send_message(chat_id=int("-1001110994526"), text=f"<b>#NewRequest\n \n \n🧿 Book's Name:{req}\n \n🧿 Requested By: {message.from_user.mention}\n \n🧿 User ID:</b> <code>{message.from_user.id}</code>\n \n<b>🧿 Chat: {message.chat.title}\n \n🧿 Chat ID:</b> <code>{message.chat.id}</code>")
             await message.reply("<b>Your request successfully submitted to admins ✅\nThey will add it as soon as possible!<b>")
    except Exception as e:
        await message.reply(f"Error occurred!\n \n{e}")
