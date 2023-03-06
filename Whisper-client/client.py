import logging
import ffmpeg
import sys
import json
import requests
import googletrans
from enum import Enum


def format_json(json_obj):
    if type(json_obj) is str:
        json_obj = json.loads(json_obj)
    if type(json_obj) is dict:
        return json.dumps(json_obj, sort_keys=True, indent=4, separators=(",", ":"))
    else:
        logging.error("Invalid json object, can't format'")
        return ""


class MediaType(Enum):
    ONLY_AUDIO = (1,)
    ONLY_VIDEO = (2,)
    AUDIO_AND_VIDEO = 3
    NONE = 4


def check_media_type(filepath) -> MediaType:
    """
    check_media_type checks the media type of a file using ffprobe.
    filepath: the path to the file to check
    returns: MediaType enum
    """
    filetype = ffmpeg.probe(filepath)
    logging.debug("Filetype: {}".format(format_json(filetype)))

    if "streams" not in filetype:
        logging.error("No streams found, can't detect media type")
        return MediaType.NONE

    streams = filetype["streams"]
    has_video = False
    has_audio = False
    for stream in streams:
        if "codec_type" in stream:
            if stream["codec_type"] == "video":
                has_video = True
            elif stream["codec_type"] == "audio":
                has_audio = True

    if has_video and has_audio:
        logging.info("Media type is AUDIO_AND_VIDEO")
        return MediaType.AUDIO_AND_VIDEO
    elif has_video:
        logging.info("Media type is ONLY_VIDEO")
        return MediaType.ONLY_VIDEO
    elif has_audio:
        logging.info("Media type is ONLY_AUDIO")

    return MediaType.ONLY_AUDIO


def transcribe_audio(audio_data) -> str:
    url = "http://192.168.0.110:9000/asr"
    file = {"audio_file": audio_data}
    uploadData = {"task": "transcribe", "output": "srt"}
    return requests.post(url, params=uploadData, files=file).text


def translate(str, target_lang):
    tran = googletrans.Translator()
    ret = tran.translate(text=str, dest=target_lang)
    return ret.text


def translate_srt(srt, target_lang):
    lines = srt.splitlines()
    count = 0
    result = []
    for i in range(len(lines)):
        if count > 0 and "-->" in lines[i - 1]:
            print(lines[i])
            # result.append(translate(lines[i], target_lang))
            result.append(lines[i])
        count += 1
    return "\n".join(result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error("Please provide a file to process")
        logging.error("Usage: python client.py <file>")

    file_type = check_media_type(sys.argv[1])
    if file_type == MediaType.ONLY_AUDIO:
        srt = transcribe_audio(open(sys.argv[1], "rb"))
        cnsrt = translate_srt(srt, "zh-cn")
        print(cnsrt)
