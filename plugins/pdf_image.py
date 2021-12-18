"""#!/usr/bin/env python3"""

"""from pdf2image import convert_from_path
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
input_dir = Path("input")

if __name__ == "__main__":
    for file in Path("input").glob(pattern="*.pdf"):
        images = convert_from_path(file, size=1920)
        for image in images:
            image.save(str(output_dir) + "/" + file.stem + ".png")"""


import os 
from os import error, system, name
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message, Document 
logger = logging.getLogger(__name__)
import re

"""Client = Client(
    "TG-Dental-References-2021",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)"""
            
            
import glob

import shutil
import time




from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError

from . import *

if not os.path.isdir("pdf"):
    os.mkdir("pdf")


@Client_cmd(
    pattern="pdf ?(.*)",
(


async def pdfseimg(event):
    


    ok = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (ok and (ok.document and (ok.document.mime_type == "application/pdf"))):
        await eor(event, "`Reply The pdf u Want to Download..`")
        return
    xx = await eor(event, get_string("com_1"))
    file = ok.media.document
    k = time.time()
    filename = "hehe.pdf"
    result = await downloader(
        "pdf/" + filename,
        file,
        xx,
        k,
        "Downloading " + filename + "...",
    )
    await xx.delete()
    pdfp = "pdf/hehe.pdf"
    pdfp.replace(".pdf", "")
    pdf = PdfFileReader(pdfp)
    if not msg:
        ok = []
        for num in range(pdf.numPages):
            pw = PdfFileWriter()
            pw.addPage(pdf.getPage(num))
            fil = os.path.join("pdf/ult{}.png".format(num + 1))
            ok.append(fil)
            with open(fil, "wb") as f:
                pw.write(f)
        os.remove(pdfp)
        for z in ok:
            await event.client.send_file(event.chat_id, z)
        shutil.rmtree("pdf")
        os.mkdir("pdf")
        await xx.delete()
    elif "-" in msg:
        ok = int(msg.split("-")[-1]) - 1
        for o in range(ok):
            pw = PdfFileWriter()
            pw.addPage(pdf.getPage(o))
            with open(os.path.join("ult.png"), "wb") as f:
                pw.write(f)
            await event.reply(
                file="ult.png",
            )
            os.remove("ult.png")
        os.remove(pdfp)
    else:
        o = int(msg) - 1
        pw = PdfFileWriter()
        pw.addPage(pdf.getPage(o))
        with open(os.path.join("ult.png"), "wb") as f:
            pw.write(f)
        os.remove(pdfp)
        try:
            await event.reply(file="ult.png")
        except PhotoSaveFileInvalidError:
            await event.reply(file="ult.png", force_document=True)
        os.remove("ult.png")            
