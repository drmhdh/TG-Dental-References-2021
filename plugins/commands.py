import re
import os
import json
import random
import base64
import asyncio
import logging
from Script import script
from asyncio import sleep
from pyrogram import filters, Client 
from database.users_chats_db import db
from pyrogram.errors import UserNotParticipant

from utils import get_settings, get_size, is_subscribed, temp
from database.connections_mdb import active_connection
from utils import Media, get_file_details, get_size, humanbytes
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired, FloodWait
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, PICS, LOG_CHANNEL

logger = logging.getLogger(__name__)

BATCH_FILES = {}
@Client.on_message(filters.command("start") & filters.incoming & ~filters.edited)
async def start(bot, cmd):       
    if cmd.chat.type in ['group', 'supergroup']:
        await cmd.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_MSG.format(cmd.from_user.mention if cmd.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), 
            parse_mode='html',         
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
                        ],[
                            InlineKeyboardButton("🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url="https://t.me/dental_case_study")
                        ],[
                            InlineKeyboardButton("🚀 Control Panel 🏰", callback_data="about")
                        ],[
                            InlineKeyboardButton("➕Join 🦷Discussion Group➕", url="https://t.me/dent_tech_for_u")
                        ],[
                            InlineKeyboardButton("📺 𝔻𝕖𝕞𝕠𝕟𝕤𝕥𝕣𝕒𝕥𝕚𝕠𝕟 𝕍𝕚𝕕𝕖𝕠 🧭", url="https://t.me/grand_dental_library/378?comment=75870")
                        ],[       
                            InlineKeyboardButton("🎁 Donate & Support 🎁", url="https://t.me/dental_backup/180")
                        ]
                    ]
                )
            )
        
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(cmd.chat.id):
            total=await bot.get_chat_members_count(cmd.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(cmd.chat.title, cmd.chat.id, total, "Unknown"))       
            await db.add_chat(cmd.chat.id, cmd.chat.title)
        return 
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id, cmd.from_user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(cmd.from_user.id, cmd.from_user.mention))
       
    if len(cmd.command) != 2:           
        buttons = [
            [                 
                InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
            ],[
                InlineKeyboardButton("🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url="https://t.me/dental_case_study")
            ],[
                InlineKeyboardButton("🚀 Control Panel 🏰", callback_data="about")
            ],[
                InlineKeyboardButton("➕Join 🦷Discussion Group➕", url="https://t.me/dent_tech_for_u")
            ],[                                           
                InlineKeyboardButton("📺 𝔻𝕖𝕞𝕠𝕟𝕤𝕥𝕣𝕒𝕥𝕚𝕠𝕟 𝕍𝕚𝕕𝕖𝕠 🧭", url="https://t.me/grand_dental_library/378?comment=75870")                               
            ],[
                InlineKeyboardButton("🎁 Donate & Support 🎁", url="https://t.me/dental_backup/180")
            ]
        ]                                                                                                                                  
        reply_markup = InlineKeyboardMarkup(buttons)
        await cmd.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_MSG.format(cmd.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(bot, cmd):
        try:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url=invite_link.invite_link
                )
            ]
        ]
        if cmd.command[1] != "subscribe":
            #btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{cmd.command[1]}")])
            kk, file_id = cmd.command[1].split("_", 1)
            pre = 'checksubp' if kk == 'filep' else 'checksub' 
            btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{cmd.command[1]}")])
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚",
    
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
        return
    if len(cmd.command) == 2 and cmd.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [
            [                 
                InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
            ],[
                InlineKeyboardButton("🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url="https://t.me/dental_case_study")
            ],[
                InlineKeyboardButton("🚀 Control Panel 🏰", callback_data="about")
            ],[
                InlineKeyboardButton("➕Join 🦷Discussion Group➕", url="https://t.me/dent_tech_for_u")
            ],[                                           
                InlineKeyboardButton("📺 𝔻𝕖𝕞𝕠𝕟𝕤𝕥𝕣𝕒𝕥𝕚𝕠𝕟 𝕍𝕚𝕕𝕖𝕠 🧭", url="https://t.me/grand_dental_library/378?comment=75870")                               
            ],[
                InlineKeyboardButton("🎁 Donate & Support 🎁", url="https://t.me/dental_backup/180")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await cmd.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_MSG.format(cmd.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    
    data = message.command[1]
    pre, file_id = data.split('_', 1)
    
    if data.split("-", 1)[0] == "BATCH":
        sts = await cmd.reply("Please wait")
        
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await bot.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await bot.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                
                f_caption = f"{title}"
            buttons = [
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
                    ],[
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ],[
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                ]
            try:
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=settings["file_secure"],
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=settings["file_secure"],
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
            except Exception as e:
                  
                    
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1)
        await sts.delete()
        return
    #elif file_id.split("-", 1)[0] == "DSTORE":
    elif data.split("-", 1)[0] == "DSTORE": 
       
        sts = await cmd.reply("Please wait")
        #b_string = file_id.split("-", 1)[1]
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
        msgs_list = list(range(int(f_msg_id), int(l_msg_id)+1))
        for msg in msgs_list:
            try:
                await bot.copy_message(chat_id=cmd.chat.id, from_chat_id=int(f_chat_id), cmd_id=msg, protect_content=settings["file_secure"])
                #await msg.copy(cmd.chat.id, caption=f_caption, protect_content=settings["file_secure"])
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.copy_message(chat_id=cmd.chat.id, from_chat_id=int(f_chat_id), cmd_id=msg, protect_content=settings["file_secure"])
                #await msg.copy(message.chat.id, caption=f_caption, protect_content=settings["file_secure"])  
            except Exception as e:                             
                logger.exception(e)
                continue  
            await asyncio.sleep(1)                  
        return await sts.delete()
    files_ = await get_file_details(file_id)           
    if not files_:
        try:
            msg = await bot.send_cached_media(
                chat_id=cmd.from_user.id,
                file_id=file_id,
                #protect_content=settings["file_secure"],
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            reply_markup=InlineKeyboardMarkup(buttons)
            buttons = [
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
                    ],[
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ],[
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                ]
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚 ",

                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url=invite_link.invite_link)
                            ],[
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown",
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
  
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
                    ],[
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ],[
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    #protect_content=settings["file_secure"],
                    protect_content=True if pre == 'filep' else False,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(        
            chat_id=cmd.from_user.id,
            text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚 ",     
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url=invite_link.invite_link)
                    ],[   
                        InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{cmd.command[1]}")
                    ]                                    
                ]
            )
        )
    
        if cmd.command[1] != "subscribe":                    
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚",                                          
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{cmd.command[1]}")
                        ]  
                    ]
                ) 
            )
    
    else:
        await cmd.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_MSG.format(cmd.from_user.mention if cmd.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), 
            parse_mode='html',  
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
                        ],[
                            InlineKeyboardButton("🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url="https://t.me/dental_case_study")
                        ],[
                            InlineKeyboardButton("🚀 Control Panel 🏰", callback_data="about")
                        ],[
                            InlineKeyboardButton("➕Join 🦷Discussion Group➕", url="https://t.me/dent_tech_for_u")
                        ],[
                            InlineKeyboardButton("📺 𝔻𝕖𝕞𝕠𝕟𝕤𝕥𝕣𝕒𝕥𝕚𝕠𝕟 𝕍𝕚𝕕𝕖𝕠 🧭", url="https://t.me/grand_dental_library/378?comment=75870")
                               
                        ],[
                            InlineKeyboardButton("🎁 Donate & Support 🎁", url="https://t.me/dental_backup/180")
                        ]
                    ]
                )
            )
                             
@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
                
@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')

@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')

@Client.on_message(filters.command('search'))
async def search(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/search"):
        await cmd.reply_text(
            
            text=(f"</b>Helo, {cmd.from_user.mention} \n🕹  Press Search Button and Type Your Keyword to Search Available References📖</b>"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
                    ]
                ]
            )
        )
        
@Client.on_message(filters.command('ping'))
async def ping(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/ping"):
        #await cmd.reply_text(
            m=await cmd.reply_text("<code>○</code>")
            n=await m.edit("<code>🏓Ping..!!</code>")
            o=await n.edit("<code>○○</code>")
            p=await o.edit("<code>🏓Pong..!!</code>")
            q=await p.edit("<code>○○○</code>")
            await q.edit("<code>Iam Alive...👻</code>")
            await sleep(4)
            await m.delete()                                    
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
                    ]
                ]
            )
               
@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer()
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

 
  
@Client.on_message(filters.command('settings'))
async def settings(bot, cmd):
    userid = cmd.from_user.id if cmd.from_user else None
    if not userid:
        return await cmd.reply(f"You are anonymous admin. Use /connect {cmd.chat.id} in PM")
    chat_type = cmd.chat.type
    

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await bot.get_chat(grpid)
                title = chat.title
            except:
                await cmd.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await cmd.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = cmd.chat.id
        title = cmd.chat.title

    else:
        return

    st = await bot.get_chat_member(grp_id, userid)
    if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
    ):
        return


    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                
            
            
                InlineKeyboardButton(
                    'Bot PM',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["botpm"] else '❌ No',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'File Secure',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["file_secure"] else '❌ No',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'IMDB',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["imdb"] else '❌ No',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            
            [
                InlineKeyboardButton(
                    'Welcome',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ Yes' if settings["welcome"] else '❌ No',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await cmd.reply_text(
            
            text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
        
        
        
@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("Checking template")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
    ):
        return
    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"Successfully changed template for {title} to\n\n{template}")
