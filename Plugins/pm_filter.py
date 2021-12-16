#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, BUTTON, START_MSG, CHANNELS, ADMINS, PICS, SINGLE_BUTTON, API_KEY, P_TTI_SHOW_OFF, IMDB, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
import asyncio
import pyrogram
import ast
import re
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster ,temp, get_size
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.users_chats_db import db
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from Script import script
import random
from database.filters_mdb import(
   del_all,
   find_filter,
   get_filters,
)

BUTTONS = {}
BOT = {}

@Client.on_message(filters.command('echo') & filters.group)
async def echo(bot, message):   
    ADMIN = int("532323191")
    if message.from_user.id == ADMIN:           
        if message.text:
            txt=message.text.replace("/echo", " ")
        else:
            return
        if message.reply_to_message and message.text:
            try:
                await bot.send_message(chat_id=message.chat.id, text=txt, reply_to_message_id=message.reply_to_message.message_id)
            except:
                await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.reply_to_message.message_id)          
        if message.reply_to_message and not message.text:
            title=message.caption 
            await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id, reply_to_message_id=message.reply_to_message.message_id, caption=title.replace("/echo", " "))        
        if not message.reply_to_message and message.text:         
            await bot.send_message(chat_id=message.chat.id, text=txt, reply_to_message_id=message.message_id)
        if not message.reply_to_message and not message.text:
            title=message.caption            
            await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id, reply_to_message_id=message.message_id, caption=title.replace("/echo", " ") )
    else:
        await message.reply_text("<b>That's not for you bruh 😅</b>")

    #except Exception as e:
    #await message.reply(f"<b>Error!!</b>\n \n<code>{e}</code>")

@Client.on_message(filters.command('gsend') & filters.private)
async def gsend(client, message):
    ADMIN = int("532323191")
    if message.from_user.id == ADMIN: 
               if message.reply_to_message:
                                    chatid=int(message.text.replace("/gsend"," "))
                                    await client.copy_message(chat_id=chatid, from_chat_id=ADMIN, message_id=message.reply_to_message.message_id)
                                    await message.reply_text("<b>✅ Message Successfully Send to the Group</b>")
               else:
                    await message.reply_text("<b>Use this command as the reply of any Message to Send in Group</b>")                         
    else:
         await message.reply_text("<b>That's not for you bruh 😅</b>")

@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)  
async def give_filter(client, message):
    
    group_id = message.chat.id
    name = message.text
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)
            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    logger.exception(e)
                break 
        
    else:
        await auto_filter(client, message)
        
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url=invite_link.invite_link)
                        ],
                        [
                            InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                        ]
                       
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADEAMAAvnZ4VSjsvEouvHC4RYE')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
           await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
        else:
           await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_  == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        k = await query.message.edit('This Movie Not Found In DataBase')
        await asyncio.sleep(10)
        await k.delete()            

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        
        else:
            await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
   
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed) or (clicked in AUTH_USERS) or (clicked in ADMINS):   

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
                
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                ]
                ,
                [    
                    InlineKeyboardButton('➕ Join 🦷 Discussion Group ➕', url='https://t.me/dent_tech_for_u')
                ]
                ,
                [
                    InlineKeyboardButton('🔮 Status', callback_data='stats')    
                ]
                ,
                [                
                    InlineKeyboardButton('🏠 Home', callback_data='hamid'),
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            await query.message.edit(text="<b>Developer : <a href='https://t.me/dent_tech_for_books'>📚🅳🆃 📖 🆁🅾🅾🅼📚</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://t.me/dent_tech_library'>🔬𝔻𝕖𝕟𝕥 𝕋𝕖𝕔𝕙 𝕃𝕚𝕓𝕣𝕒𝕣𝕪📚</a>\nDiscussion Group: <a href='https://t.me/dent_tech_for_u'>Click Here</a>\n𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎: <a href='https://t.me/dental_case_study'>Click Here</a></b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "stats":
            buttons = [
                [
                InlineKeyboardButton('👩‍🦯 Back', callback_data='about'),
                InlineKeyboardButton('♻️', callback_data='rfrsh')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            total = await Media.count_documents()
            users = await db.total_users_count()
            chats = await db.total_chat_count()
            monsize = await db.get_db_size()
            free = 536870912 - monsize
            monsize = get_size(monsize)
            free = get_size(free)
            await query.message.edit_text(
                text=script.STATUS_TXT.format(total, users, chats, monsize, free),
                reply_markup=reply_markup,
                parse_mode='html' 
                )
                
                
        elif query.data == "rfrsh":
            await query.answer("Fetching MongoDb DataBase")
            buttons = [
                [
                InlineKeyboardButton('👩‍🦯 Back', callback_data='about'),
                InlineKeyboardButton('♻️', callback_data='rfrsh')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            total = await Media.count_documents()
            users = await db.total_users_count()
            chats = await db.total_chat_count()
            monsize = await db.get_db_size()
            free = 536870912 - monsize
            monsize = get_size(monsize)
            free = get_size(free)
            await query.message.edit_text(
                text=script.STATUS_TXT.format(total, users, chats, monsize, free),
                reply_markup=reply_markup,
                parse_mode='html'
                )

 
        elif query.data == "hamid":
            buttons = [[
                InlineKeyboardButton("🔎 Search", switch_inline_query_current_chat='')
                ],[
                InlineKeyboardButton("🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url="https://t.me/dental_case_study")
                ],[
                InlineKeyboardButton("🚀 Control Panel 🏰", callback_data="about")
                ],[
                InlineKeyboardButton("➕Join 🦷Discussion Group➕", url="https://t.me/dent_tech_for_u")
                ],[            
                InlineKeyboardButton("🎁 Donate & Support 🎁", url="https://t.me/dental_backup/180")
            ]]   
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.START_MSG.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                
                parse_mode='html'
            )
  
        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
        
                    ]
                    ,
                    [
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ]
                
                    ,
                    [
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                ]
            await query.answer()
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_id,
                caption=f_caption,
                reply_markup=InlineKeyboardMarkup(buttons)
                )              
    
        elif query.data.startswith("checksub"):
            
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart. Be a Channel Member..😒",show_alert=True)
                return
            
               
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [  
                    
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
                    ]
                    ,
                    [
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ]
                    ,
                    [
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
            else:
                await query.answer("🥳 You are Already a Member. Enjoy...🤗",show_alert=True)
                
                  
        elif query.data == "pages":
            await query.answer()
        elif query.data == "close":
            await query.message.delete()
    else:
        await query.answer("Thats not for you!!",show_alert=True)                                                 
    if query.data == "close_data":
        await query.message.delete()                         
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return      
        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title
        else:
            return
        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)               
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()
        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Thats not for you!!",show_alert=True)        
    elif "groupcb" in query.data:
        await query.answer()
        group_id = query.data.split(":")[1]        
        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return

    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"                                                                                      
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )     


    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)

   
   
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        filedetails = await get_file_details(file_id)
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        for files in filedetails:
            title = files.file_name
            size=get_size(files.file_size)
            f_caption=files.caption
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                except Exception as e:
                     print(e)
                     f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                
                buttons = [
                    [
                        InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')
        
                    ]
                    ,
                    [
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ]
                
                    ,
                    [
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )

            try:
                if AUTH_CHANNEL and not await is_subscribed(client, query):
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                    return
                elif P_TTI_SHOW_OFF:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                    return
                else:
                    await client.send_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption
                        )
                    await query.answer('Check PM, I have sent files in pm',show_alert = True)
            except UserIsBlocked:
                await query.answer('Unblock the bot mahn !',show_alert = True)
            except PeerIdInvalid:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
            except Exception as e:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
      

      
async def auto_filter(client, message, spoll=False): #async def auto_filter(client, msg, spoll=False):
    clicked = message.from_user.id
    try:
        typed = message.message.reply_to_message.from_user.id
    except:
        typed = message.from_user.id
        pass
    if (clicked == typed) or (clicked in AUTH_USERS) or (clicked in ADMINS):
        if not spoll:
            #message = msg
            if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
                return
            if 2 < len(message.text) < 100:
                btn = []
                search = message.text
                nyva=BOT.get("username")
                if not nyva:
                    botusername=await client.get_me()
                    nyva=botusername.username
                    BOT["username"]=nyva
                files = await get_filter_results(query=search)
                if files:
                    for file in files:
                        file_id = file.file_id
                        filename = f"[{get_size(file.file_size)}] {file.file_name}"
                        btn.append(
                           [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                            )
                else:
                    return
                if not btn:
                    return
        
    
                if len(btn) > 10: 
                    btns = list(split_list(btn, 10)) 
                    keyword = f"{message.chat.id}-{message.message_id}"
                    BUTTONS[keyword] = {
                        "total" : len(btns),
                        "buttons" : btns
                    }
                else:
                    buttons = btn
                    buttons.append(
                        [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
                    )
                    if BUTTON:
                        buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
                    poster=None
                    if API_KEY:
                        poster=await get_poster(search)
                    if poster:
                        await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))

                    else:
                        await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
                    return

                data = BUTTONS[keyword]
                buttons = data['buttons'][0].copy()

                buttons.append(
                    [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
                )    
                buttons.append(
                    [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
                poster=None
                if API_KEY:
                    poster=await get_poster(search)
                if poster:
                    await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))
                else:
                    await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b> \n\n🅒 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 🅒  \n🔎🦷✨ @dental_case_study \n🔐 𝗝𝗢𝗜𝗡 ⤴️ 𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 🚀", reply_markup=InlineKeyboardMarkup(buttons))

                imdb = await get_poster(search, file=(files[0]).file_name) if IMDB else None
                if imdb:
                    cap = IMDB_TEMPLATE.format(
                        query = search,
                    )
                else:
                    cap = f"Here is what i found for your query {search}"
        
                if spoll:
                    await msg.message.delete()
   
     

    else:
        await query.answer("It Will Not Work for You, as It was Not Requested by You 😒",show_alert=True)     
       
   
