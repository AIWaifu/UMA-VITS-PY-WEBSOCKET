import requests
import json
import websockets
import asyncio
import random
import string
import base64
from cleaners import zh_ja_mixture_cleaners


characters = ['0:特别周', '1:无声铃鹿', '2:东海帝王', '3:丸善斯基',
              '4:富士奇迹', '5:小栗帽', '6:黄金船', '7:伏特加',
              '8:大和赤骥', '9:大树快车', '10:草上飞', '11:菱亚马逊',
              '12:目白麦昆', '13:神鹰', '14:好歌剧', '15:成田白仁',
              '16:鲁道夫象征', '17:气槽', '18:爱丽数码', '19:青云天空',
              '20:玉藻十字', '21:美妙姿势', '22:琵琶晨光', '23:重炮',
              '24:曼城茶座', '25:美普波旁', '26:目白雷恩', '27:菱曙',
              '28:雪之美人', '29:米浴', '30:艾尼斯风神', '31:爱丽速子',
              '32:爱慕织姬', '33:稻荷一', '34:胜利奖券', '35:空中神宫',
              '36:荣进闪耀', '37:真机伶', '38:川上公主', '39:黄金城市',
              '40:樱花进王', '41:采珠', '42:新光风', '43:东商变革',
              '44:超级小溪', '45:醒目飞鹰', '46:荒漠英雄', '47:东瀛佐敦',
              '48:中山庆典', '49:成田大进', '50:西野花', '51:春乌拉拉',
              '52:青竹回忆', '53:微光飞驹', '54:美丽周日', '55:待兼福来',
              '56:Mr.C.B', '57:名将怒涛', '58:目白多伯', '59:优秀素质',
              '60:帝王光环', '61:待兼诗歌剧', '62:生野狄杜斯', '63:目白善信',
              '64:大拓太阳神', '65:双涡轮', '66:里见光钻', '67:北部玄驹',
              '68:樱花千代王', '69:天狼星象征', '70:目白阿尔丹', '71:八重无敌',
              '72:鹤丸刚志', '73:目白光明', '74:樱花桂冠', '75:成田路',
              '76:也文摄辉', '77:吉兆', '78:谷野美酒', '79:第一红宝石',
              '80:真弓快车', '81:骏川手纲', '82:凯斯奇迹', '83:小林历奇',
              '84:北港火山', '85:奇锐骏', '86:秋川理事长']

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
    # print(zh_ja_mixture_cleaners("[JA]こんにちわ。[JA]"))
    # print(zh_ja_mixture_cleaners("[ZH]你好。[ZH]"))
    # print(zh_ja_mixture_cleaners("[JA]こんにちわ。[JA]，[ZH]你好。[ZH]"))
    #

    examples = [
                ['haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......haa\u2193......','29:米浴', '日本語', 1, 0.667, 0.8, True],
                ['お疲れ様です，トレーナーさん。', '1:无声铃鹿', '日本語', 1, 0.667, 0.8, False],
                ['張り切っていこう！', '67:北部玄驹', '日本語', 1, 0.667, 0.8, False],
                ['何でこんなに慣れでんのよ，私のほが先に好きだっだのに。', '10:草上飞', '日本語', 1, 0.667, 0.8, False],
                ['授業中に出しだら，学校生活終わるですわ。', '12:目白麦昆', '日本語', 1, 0.667, 0.8, False],
                ['お帰りなさい，お兄様！', '29:米浴', '日本語', 1, 0.667, 0.8, False],
                ['私の処女をもらっでください！', '29:米浴', '日本語', 1, 0.667, 0.8, False]
    ]

    ws_url = "wss://plachta-vits-umamusume-voice-synthesizer.hf.space/queue/join"

    response = asyncio.get_event_loop().run_until_complete(get_audio(*examples[2]))
    output = response['output']
    text_output, audio_output, phoneme_output, duration_output = output['data']

    audio_output = audio_output.lstrip("data:audio/wav;base64,")
    decode_string = base64.b64decode(audio_output)
    with open("output.wav", "wb") as f:
        f.write(decode_string)
