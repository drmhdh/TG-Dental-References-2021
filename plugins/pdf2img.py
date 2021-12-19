# !/usr/bin/python
# -*- coding: utf-8 -*-

# ABOUT DEV. & SOURCE CODE
#    nabilanavab, india, kerala
#    Telegram: @nabilanavab
#    Email: nabilanavab@gmail.com
#    copyright ©️ 2021 nabilanavab
#    Released Under Apache License


import os
import fitz
import shutil
import logging
import convertapi
from PIL import Image
from time import sleep
from configs import Config, Msgs
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from PyPDF2 import PdfFileWriter, PdfFileReader
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
logger = logging.getLogger(__name__)

# LOGGING INFO
# logging.basicConfig(level=logging.INFO)
#logging.getLogger("pyrogram").setLevel(logging.WARNING)

# GLOBAL VARIABLES
PDF = {}            # save images for generating pdf
media = {}          # sending group images(pdf 2 img)
PDF2IMG = {}        # save fileId of each user(later uses)
PROCESS = []        # to check current process
mediaDoc = {}       # sending group document(pdf 2 img)
PAGENOINFO = {}     # saves no.of pages that user send last
PDF2IMGPGNO = {}    # more info about pdf file(for extraction)


# SUPPORTED FILES
suprtedFile = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support
suprtedPdfFile = [
    ".epub", ".xps", ".oxps",
    ".cbz", ".fb2"
]                                       # files to pdf (zero limits)
suprtedPdfFile2 = [
    ".csv", ".doc", ".docx", ".dot",
    ".dotx", ".log", ".mpp", ".mpt",
    ".odt", ".pot", ".potx", ".pps",
    ".ppsx", ".ppt", ".pptx", ".pub",
    ".rtf", ".txt", ".vdx", ".vsd",
    ".vsdx", ".vst", ".vstx", ".wpd",
    ".wps", ".wri", ".xls", ".xlsb",
    ".xlsx", ".xlt", ".xltx", ".xml"
]                                       # file to pdf (ConvertAPI limit)


# CREATING ConvertAPI INSTANCE
if Config.CONVERT_API is not None:
    convertapi.api_secret = os.getenv("CONVERT_API")

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * 10000
    

@Client.on_message((filters.private, filters.group) & filters.document & filters.user(ADMINS))
async def documents(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )    
        
        isPdfOrImg = message.document.file_name
        fileSize = message.document.file_size
        fileNm, fileExt = os.path.splitext(isPdfOrImg)
        
        if Config.MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            
            try:
                bigFileUnSupport = await bot.send_message(
                    message.chat.id,
                    Msgs.bigFileUnSupport.format(Config.MAX_FILE_SIZE, Config.MAX_FILE_SIZE)
                )
                
                sleep(5)
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = bigFileUnSupport.message_id
                )
                
            except Exception:
                pass
        
        elif fileExt.lower() in suprtedFile:
            
            
            try:
                imageDocReply = await bot.send_message(
                    message.chat.id,
                    "`Downloading your Image..⏳`",
                    reply_to_message_id = message.message_id
                )
                
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                
                await message.download(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                )
                
                img = Image.open(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                ).convert("RGB")
                
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                    Msgs.imageAdded.format(len(PDF[message.chat.id]))
                )
            
            except Exception as e:
                
                await imageDocReply.edit(
                    Msgs.errorEditMsg.format(e)
                )
                
                sleep(5)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = imageDocReply.message_id
                )
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
        
        elif fileExt.lower() == ".pdf":
            
            try:
                if message.chat.id in PROCESS:
                    
                    await message.reply_text(
                        '`Doing Some other Work.. 🥵`'
                    )
                    return
                
                pdfMsgId = await bot.send_message(
                    message.chat.id,
                    "`Processing.. 🚶`"
                )
                
                await message.download(
                    f"{message.message_id}/pdftoimage.pdf"
                )
                
                doc = fitz.open(f'{message.message_id}/pdftoimage.pdf')
                noOfPages = doc.pageCount
                
                PDF2IMG[message.chat.id] = message.document.file_id
                PDF2IMGPGNO[message.chat.id] = noOfPages
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = pdfMsgId.message_id
                )
                
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                
                pdfMsgId = await message.reply_text(
                    Msgs.pdfReplyMsg.format(noOfPages),
                    reply_markup = ForceReply(),
                    parse_mode = "md"
                )
                
                doc.close()
                shutil.rmtree(f'{message.message_id}')
            
            except Exception as e:
                
                try:
                    PROCESS.remove(message.chat.id)
                    doc.close()
                    shutil.rmtree(f'{message.message_id}')
                    
                    await pdfMsgId.edit(
                        Msgs.errorEditMsg.format(e)
                    )
                    sleep(15)
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = pdfMsgId.message_id
                    )
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = message.message_id
                    )
                
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile:
            
            try:
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                pdfMsgId = await message.reply_text(
                    "`Downloading your file..⏳`",
                )
                
                await message.download(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                
                await pdfMsgId.edit(
                    "`Creating pdf..`💛"
                )
                
                Document = fitz.open(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                
                b = Document.convert_to_pdf()
                
                pdf = fitz.open("pdf", b)
                pdf.save(
                    f"{message.message_id}/{fileNm}.pdf",
                    garbage = 4,
                    deflate = True,
                )
                pdf.close()
                
                await pdfMsgId.edit(
                    "`Started Uploading..`🏋️"
                )
                
                sendfile = open(
                    f"{message.message_id}/{fileNm}.pdf", "rb"
                )
                
                await bot.send_document(
                    chat_id = message.chat.id,
                    document = sendfile,
                    thumb = Config.PDF_THUMBNAIL,
                    caption = f"`Converted: {fileExt} to pdf`"
                )
                await pdfMsgId.edit(
                    "`Uploading Completed..❤️`"
                )
                
                shutil.rmtree(f"{message.message_id}")
                
                sleep(5)
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                await bot.send_message(
                    message.chat.id, Msgs.feedbackMsg,
                    disable_web_page_preview = True
                )
            
            except Exception as e:
                
                try:
                    shutil.rmtree(f"{message.message_id}")
                    await pdfMsgId.edit(
                        Msgs.errorEditMsg.format(e)
                    )
                    sleep(15)
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = pdfMsgId.message_id
                    )
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = message.message_id
                    )
                    
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile2:
            
            if os.getenv("CONVERT_API") is None:
                
                pdfMsgId = await message.reply_text(
                    "`Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                )
                sleep(15)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = pdfMsgId.message_id
                )
            
            else:
                
                try:
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    pdfMsgId = await message.reply_text(
                        "`Downloading your file..⏳`",
                    )
                    
                    await message.download(
                        f"{message.message_id}/{isPdfOrImg}"
                    )
                    
                    await pdfMsgId.edit(
                        "`Creating pdf..`💛"
                    )
                    
                    try:
                        await convertapi.convert(
                            "pdf",
                            {
                                "File": f"{message.message_id}/{isPdfOrImg}"
                            },
                            from_format = fileExt[1:],
                        ).save_files(
                            f"{message.message_id}/{fileNm}.pdf"
                        )
                        
                    except Exception:
                        
                        try:
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                "ConvertAPI limit reaches.. contact Owner"
                            )
                            
                        except Exception:
                            pass
                    
                    sendfile = open(
                        f"{message.message_id}/{fileNm}.pdf", "rb"
                    )
                    await bot.send_document(
                        chat_id = message.chat.id,
                        Document = sendfile,
                        thumb = Config.PDF_THUMBNAIL,
                        caption = f"`Converted: {fileExt} to pdf`",
                    )
                    
                    await pdfMsgId.edit(
                        "`Uploading Completed..`🏌️"
                    )
                    
                    shutil.rmtree(f"{message.message_id}")
                    
                    sleep(5)
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    await bot.send_message(
                        message.chat.id, Msgs.feedbackMsg,
                        disable_web_page_preview = True
                    )
                
                except Exception:
                    pass
        
        else:
            
            try:
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                unSuprtd = await bot.send_message(
                    message.chat.id, "`unsupported file..🙄`"
                )
                sleep(15)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = unSuprtd.message_id
                )
                
            except Exception:
                pass
            
    except Exception:
        pass
            
            
    
# if message is /extract
@Client.on_message(filters.command(["extract"]) & (filters.document & (filters.private, filters.group) & filters.user(ADMINS)))
async def extract(bot, message):
    
    try:
        if message.chat.id in PROCESS:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await message.reply_text("`Doing Some Work..🥵`", quote=True)
            return
        
        needPages = message.text.replace('/extract ', '')
        
        if message.chat.id not in PDF2IMG:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await bot.send_message(
                message.chat.id,
                "`send me a pdf first..🤥`"
            )
            return
        
        else:
            pageStartAndEnd = list(needPages.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                
                await bot.send_message(
                    message.chat.id,
                    "`I just asked you starting & ending 😅`"
                )
                return
            
            elif len(pageStartAndEnd) == 2:
                try:
                    
                    if (1 <= int(pageStartAndEnd[0]) <= PDF2IMGPGNO[message.chat.id]):
                        
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1]) <= PDF2IMGPGNO[message.chat.id]):
                            PAGENOINFO[message.chat.id] = [False, int(pageStartAndEnd[0]), int(pageStartAndEnd[1]), None]    #elmnts in list (is singlePage, start, end, if single pg number)
                            
                        else:
                            await bot.send_message(
                                message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber 😅`"
                            )
                            return
                        
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber 😅`"
                        )
                        return
                    
                except:
                    
                    await bot.send_message(
                        message.chat.id,
                        "`Syntax Error: noSuchPageNumbers 🤭`"
                    )
                    return
            
            elif len(pageStartAndEnd) == 1:
                
                if pageStartAndEnd[0] == "/extract":
                    
                    if (PDF2IMGPGNO[message.chat.id]) == 1:
                        PAGENOINFO[message.chat.id] = [True, None, None, 1]
                        #elmnts in list (is singlePage, start, end, if single pg number)
                    
                    else:
                        PAGENOINFO[message.chat.id] = [False, 1, PDF2IMGPGNO[message.chat.id], None]
                        #elmnts in list (is singlePage, start, end, if single pg number)
                    
                elif 0 < int(pageStartAndEnd[0]) <= PDF2IMGPGNO[message.chat.id]:
                    PAGENOINFO[message.chat.id] = [True, None, None, pageStartAndEnd[0]]
                
                else:
                    await bot.send_message(
                        message.chat.id,
                        '`Syntax Error: noSuchPageNumber 🥴`'
                    )
                    return
            
            else:
                await bot.send_message(
                    message.chat.id,
                    "`Syntax Error: pageNumberMustBeAnIntiger 🧠`"
                )
                return
            
            if PAGENOINFO[message.chat.id][0] == False:
                
                if pageStartAndEnd[0] == "/extract":
                    await bot.send_message(
                        message.chat.id,
                        text = f"Extract images from `{PAGENOINFO[message.chat.id][1]}` to `{PAGENOINFO[message.chat.id][2]}` As:",
                        disable_web_page_preview = True,
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Images 🖼️️",
                                        callback_data = "multipleImgAsImages"
                                    ),
                                    InlineKeyboardButton(
                                        "Document 📁 ",
                                        callback_data = "multipleImgAsDocument"
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "PDF 🎭",
                                        callback_data = "multipleImgAsPdfError"
                                    )
                                ]
                            ]
                        )
                    )
                
                else:
                    await bot.send_message(
                        message.chat.id,
                        text = f"Extract images from `{PAGENOINFO[message.chat.id][1]}` to `{PAGENOINFO[message.chat.id][2]}` As:",
                        disable_web_page_preview = True,
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Images 🖼️️",
                                        callback_data = "multipleImgAsImages"
                                    ),
                                    InlineKeyboardButton(
                                        "Document 📁 ",
                                        callback_data = "multipleImgAsDocument"
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "PDF 🎭",
                                        callback_data = "multipleImgAsPdf"
                                    )
                                ]
                            ]
                        )
                    )
                
            if PAGENOINFO[message.chat.id][0] == True:
                
                await bot.send_message(
                    message.chat.id,
                    text = f"Extract page number: `{PAGENOINFO[message.chat.id][3]}` As:",
                    disable_web_page_preview = True,
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Images 🖼️️",
                                    callback_data = "asImages"
                                ),
                                InlineKeyboardButton(
                                    "Document 📁 ",
                                    callback_data = "asDocument"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "PDF 🎭",
                                    callback_data = "asPdf"
                                )
                            ]
                        ]
                    )
                )
                
    except Exception:
        
        try:
            del PAGENOINFO[message.chat.id]
            PROCESS.remove(message.chat.id)
            
        except Exception:
            pass
