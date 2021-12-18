import os
from os import error, system, name
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message, Document 
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from telethon.sync import TelegramClient, events

from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError
logger = logging.getLogger(__name__)

if not os.path.isdir("pdf"):
    os.mkdir("pdf")
 

"""def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
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
            pass"""

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
# get the pattern from the decorator
"""if pattern is not None:
    if pattern.startswith("\#"):
            # special fix for snip.py
        args["pattern"] = re.compile(pattern)
    else:
        args["pattern"] = re.compile("\." + pattern)
        cmd = "." + pattern
        try:
            CMD_LIST[file_test].append(cmd)
        except:
            CMD_LIST.update({file_test: [cmd]})"""
 
#@Client.on_message(event.NewMessage(incoming=True, pattern="pdf ?(.*)"))  
#@Client.on_messagevent.NewMessage(incoming=True, pattern="pdf ?(.*)")
    

    
    

 
#@Client.on_message(filter.command(["pdf"])
    
#@Client.on_message(event.NewMessage(incoming=True, pattern="pdf ?(.*)"))

@Client.on_message(filters.command(["pdf"]))
    
    
async def pdfseimg(event):
    ok = await event.reply("`...Analysing...`")
    msg = event.pattern_match.group(1)
    if not (ok and (ok.document and (ok.document.mime_type == "application/pdf"))):
        await event.reply("`Reply The pdf u Want to Download..`")
                          
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
