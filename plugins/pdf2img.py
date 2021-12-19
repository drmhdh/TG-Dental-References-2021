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
    
    
# if message is /extract
@Client.on_message(filters.command(["extract"]) & filters.document, filters.private, filters.group)
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
