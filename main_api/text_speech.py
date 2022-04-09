from gtts import gTTS
import pydub
from io import BytesIO
from IPython.display import HTML, Audio
import requests
import urllib.request
import json
import speech_recognition as sr




def english_tts(text):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    # print(type(myobj))
    # myobj.save("welcome.mp3")

    fp = BytesIO()
    myobj.write_to_fp(fp)
    fp.seek(0)

    result = fp.read()

    return result

def russian_tts(text):

    FOLDER_ID = 'b1gi3idig5rf0ob1ff72'
    TOKEN = 't1.9euelZqZk5WKmpXKzM7OjI-ekJbGj-3rnpWaiseWlYqLiomeyMjPlpLNns7l8_dkeDpt-e9ldnhb_t3z9yQnOG3572V2eFv-.idqiSUpUwcwzucowewtBfXDBxeLA4UfMkx8BOQbUIVWHkG7172e77XQU4ixGX4EmB2sWOd_sQbt48vQAkPe3Dg'

    headers = {
        'Authorization': f"Bearer {TOKEN}",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'folderId={FOLDER_ID}&text={text}'.encode('utf-8')

    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)

    # Convert to mp3
    fp = BytesIO()
    fp.write(response.content)
    fp.seek(0)
    result = BytesIO()
    pydub.AudioSegment.from_file(fp).export(result, format="mp3")

    result.seek(0)

    result = result.read()

    return result

def bytes_to_format(data, format):
    # Load into ByteIO
    fp = BytesIO()
    fp.write(data)
    fp.seek(0)

    # Convert
    result = BytesIO()
    pydub.AudioSegment.from_file(fp).export(result, format=format)

    result.seek(0)

    result = result.read()

    return result

def russian_stt(mp3_bytes):
    FOLDER_ID = 'b1gi3idig5rf0ob1ff72'
    IAM_TOKEN = 't1.9euelZqZk5WKmpXKzM7OjI-ekJbGj-3rnpWaiseWlYqLiomeyMjPlpLNns7l8_dkeDpt-e9ldnhb_t3z9yQnOG3572V2eFv-.idqiSUpUwcwzucowewtBfXDBxeLA4UfMkx8BOQbUIVWHkG7172e77XQU4ixGX4EmB2sWOd_sQbt48vQAkPe3Dg'


    data = bytes_to_format(mp3_bytes, 'ogg')

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        print(decodedData.get("result"))
    return decodedData.get("result")

def english_stt(mp3_bytes):

    fp = BytesIO()
    fp.write(mp3_bytes)
    fp.seek(0)
    r = sr.Recognizer()
    with sr.AudioFile(fp) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
        return text