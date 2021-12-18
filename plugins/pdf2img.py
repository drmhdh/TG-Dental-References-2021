from os import error, system, name
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message, Document 
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError
logger = logging.getLogger(__name__)

if not os.path.isdir("pdf"):
    os.mkdir("pdf")
    
async def eor(event, text, **args):
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
        ok = await event.edit(text, link_preview=link_preview, parse_mode=parse_mode)

    
    
    
@ultroid_cmd(
    pattern="pdf ?(.*)",
)
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
