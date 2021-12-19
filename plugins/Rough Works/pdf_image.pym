#!/usr/bin/env python3

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
import glob
import os
import shutil
import time


from os import error, system, name
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message, Document 
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError

logger = logging.getLogger(__name__)


"""Ultroid = Client(
    "TG-Dental-References-2021",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)"""
            
            


"""def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: not e.via_bot_id and not e.fwd_from
    args["chats"] = black_list_chats
    args["blacklist_chats"] = True
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        args["pattern"] = re.compile(hndlr + pattern)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    args["outgoing"] = True
    if "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return events.NewMessage(**args)


friday_on_cmd = admin_cmd
j_cmd = admin_cmd
command = ultroid_cmd
register = ultroid_cmd"""


"""async def eor(event, text, **args):
    link_preview = args.get("link_preview", False)
    parse_mode = args.get("parse_mode", "md")
    time = args.get("time", None)
    if not event.out:
        reply_to = event.reply_to_msg_id or event
        ok = await event.client.send_message(
            event.chat_id,
            text,
            link_preview=link_preview,
            parse_mode=parse_mode,
            reply_to=reply_to,
        )
    else:
        ok = await event.edit(text, link_preview=link_preview, parse_mode=parse_mode)"""



#from . import *

if not os.path.isdir("pdf"):
    os.mkdir("pdf")



def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
    # With time and addition of Stuff
    # Decorator has turned lengthy and non attractive.
    # Todo : Make it better..
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args["pattern"]
    black_chats = args.get("chats", None)
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    fullsudo = args.get("fullsudo", False)
    allow_all = args.get("allow_all", False)
    type = args.get("type", ["official"])
    only_devs = args.get("only_devs", False)
    allow_pm = args.get("allow_pm", False)
    if isinstance(type, str):
        type = [type]
    if "official" in type and DUAL_MODE:
        type.append("dualmode")

    args["forwards"] = False
    if pattern:
        args["pattern"] = compile_pattern(pattern, hndlr)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    args["blacklist_chats"] = True
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if black_chats is not None:
        if len(black_chats) == 0:
            args["chats"] = []
        else:
            args["chats"] = black_chats
    



@Client.on_message(
    pattern="pdf ?(.*)",
)
async def pdfseimg(self, event):
    
  
    #pattern="pdf ?(.*)",
    


        
   
       
    

    ok = await event.get_reply_message()
    #ok = await event.reply("```Analysing...```")
    
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
