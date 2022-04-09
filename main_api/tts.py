from gtts import gTTS
import pydub
from io import BytesIO
from IPython.display import HTML, Audio
import requests



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
