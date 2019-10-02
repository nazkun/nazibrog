""".ocr <language>\nUsage: Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi)\nAvailable Languages: .ocrlanguages"""
from telethon import events
import os
import requests
import logging
from uniborg.util import admin_cmd


async def ocr_space_file(filename,
                         overlay=False,
                         api_key=Config.OCR_SPACE_API_KEY,
                         language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@borg.on(admin_cmd(pattern="ocr (.*)", outgoing=True))
async def ocr(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        await event.edit("`Reading...`")
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        lang_code = event.pattern_match.group(1)
        downloaded_file_name = await borg.download_media(
            await event.get_reply_message(), Config.TMP_DOWNLOAD_DIRECTORY)
        test_file = await ocr_space_file(filename=downloaded_file_name,
                                         language=lang_code)
        try:
            ParsedText = test_file["ParsedResults"][0]["ParsedText"]
        except BaseException:
            await event.edit(
                "`Couldn't read it.`\n`I guess I need new glasses.`")
        else:
            await event.edit(
                f"`Here's what I could read from it:`\n\n{ParsedText}")
        os.remove(downloaded_file_name)


@borg.on(admin_cmd("ocrlanguages"))
async def get_ocr_languages(event):
    if event.fwd_from:
        return
    languages = {}
    languages["English"] = "eng"
    languages["Arabic"] = "ara"
    languages["Bulgarian"] = "bul"
    languages["Chinese (Simplified)"] = "chs"
    languages["Chinese (Traditional)"] = "cht"
    languages["Croatian"] = "hrv"
    languages["Czech"] = "cze"
    languages["Danish"] = "dan"
    languages["Dutch"] = "dut"
    languages["Finnish"] = "fin"
    languages["French"] = "fre"
    languages["German"] = "ger"
    languages["Greek"] = "gre"
    languages["Hungarian"] = "hun"
    languages["Korean"] = "kor"
    languages["Italian"] = "ita"
    languages["Japanese"] = "jpn"
    languages["Polish"] = "pol"
    languages["Portuguese"] = "por"
    languages["Russian"] = "rus"
    languages["Slovenian"] = "slv"
    languages["Spanish"] = "spa"
    languages["Swedish"] = "swe"
    languages["Turkish"] = "tur"
    a = json.dumps(languages, sort_keys=True, indent=4)
    await event.edit(str(a))


