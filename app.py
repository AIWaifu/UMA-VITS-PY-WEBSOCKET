import requests
import json
import websockets
import asyncio
import random
import string
import base64

class VITS:
    def __init__(self):
        self.url = "https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer"
        self.Text = ""
        self.character = ""

    def get_voice(self, text, speaker, lang, speed, pitch, volume, is_html):
        payload = {
            'text': text,
            'speaker': speaker,
            'lang': lang,
            'speed': speed,
            'pitch': pitch,
            'volume': volume,
            'is_html': is_html
        }
        r = requests.post(self.url, data=payload)
        return r.content


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


async def get_audio(text, chara, lang, duration, ns, nsw, has_symbol):
    async with websockets.connect(ws_url) as websocket:
        session_hash = random_string(10)
        response = await websocket.recv()
        print(response)
        payload_hash = {
            "session_hash": session_hash,
            "fn_index": 3
        }
        await websocket.send(json.dumps(payload_hash))
        response = await websocket.recv()
        print(response)
        response = await websocket.recv()
        print(response)
        payload_data = {
            "fn_index": 3,
            "data": [
                text,
                chara,
                lang,
                duration,
                ns,
                nsw,
                has_symbol],
            "session_hash": session_hash
        }
        await websocket.send(json.dumps(payload_data))
        response = await websocket.recv()
        # print(response)
        response = await websocket.recv()
        return json.loads(response)


if __name__ == "__main__":
    payload2 = ["こんにちわ。", "0:特别周", "日本語", 1, 0.667, 0.8, False]
    payload1 = ['haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......', '29:米浴', '日本語', 1, 0.667, 0.8, True]
    #print(get_voice(*payload1))
    ws_url = "wss://plachta-vits-umamusume-voice-synthesizer.hf.space/queue/join"
    response = asyncio.get_event_loop().run_until_complete(get_audio(*payload1))
    output = response['output']
    text_output, audio_output, phoneme_output, duration_output = output['data']
    audio_output = audio_output.lstrip("data:audio/wav;base64,")
    decode_string = base64.b64decode(audio_output)
    with open("output.wav", "wb") as f:
        f.write(decode_string)
