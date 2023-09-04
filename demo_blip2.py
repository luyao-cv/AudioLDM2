import openai

#输入文本处理程序
import numpy as np
# from paddlemix import Appflow
# import paddle
import scipy
from PIL import Image
from flask import Flask, request


app = Flask(__name__)

# openai.api_key = "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"  # 更换为自己的密钥

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]

blip_to_ldm_prompt = """
Create a brief description of a specific musical style that matches the following sentence.:
"{}".

Here are some output examples:

examples 1: "A modern hip-hop beat with punchy bass and rapid-fire lyrics, reflecting urban life and culture."

examples 2: "A funky bass guitar grooving in sync with drums."

examples 3: "A cjeerful ukulele strumming in a beachside jam."

examples 4: "Melodic pop song in trance progressive, award winning, epic sound, climax."

examples 5: "A forest of wind chimes singing a soothing melody in the breeze."

examples 6: "Birds singing sweetly in a blooming garden."

examples 7: "A modern synthesizer ceating futuristic soundscapes."

examples 8: "A traditional Irish fiddle playing a lively reel. "

examples 9: "The enchanting sound of a harp being plucked."

examples 10: "A saxophone weaves a soulful melody, accompanied by the iconic Super Mario music, creating a nostalgic fusion that merges smooth jazz with retro gaming vibes."

examples 11: "The vibrant beat of Brazilian samba drums intertwines with a catchy trap beat, while EDM synthesizers add a unique electronic flair, resulting in a dynamic and energetic sound with an ethereal quality."

examples 12: "Delicate harp arpeggios blend with angelic choir vocals, creating a heavenly and ethereal atmosphere that enchants and uplifts the spirit."

examples 13: "Embark on a whimsical journey with the playful melodies and light-hearted rhythms of a delightful indie folk tune, capturing the spirit of a bounding deer in full stride." 

examples 14: "Dance music with strong, upbeat tempo, and repetitive rhythms, include sub-genres like house, techno, EDM, trance, and many more."

examples 15: "Scary music with dissonant harmonies, irregular rhythms, and unconventional use of instruments."

examples 16: "Pop music that upbeat, catchy, and easy to listen, high fidelity, with simple melodies, electronic instruments and polished production."

examples 17: "This is a piece that would be suitable as calming study music or music for sleeping. It features a relaxing and soothing motif on the piano, being backed by a distant, high pitched and sustained violin."

"""
# def ChatGPT_Bot(input):
#     if input:
#         messages.append({"role": "user", "content": input})
#         chat = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo", messages=messages
#         )
#         reply = chat.choices[0].message.content
#         messages.append({"role": "assistant", "content": reply})
#         return reply


blip2_prompt = 'describe the image'
# task_blip = Appflow(app="auto_label", models=["paddlemix/blip2-caption-opt2.7b"])
# x = ChatGPT_Bot("你好")
# print(x)

def img2prompt(x, result_blip, prompt):
    if not result_blip:
        # result_blip = task_blip(image=x,blip2_prompt = blip2_prompt)['prompt']
        result_blip = "test blip2"
    if not prompt:
        pre_prompt = blip_to_ldm_prompt.format(result_blip)
        # prompt = ChatGPT_Bot(pre_prompt)
        # prompt = "test chatgpt"
        prompt = result_blip

    print(result_blip)
    print(prompt)
    return result_blip, prompt

@app.route("/blip2",methods=["POST"])
def post_prompt():
    input_json = request.get_json()
    _path,result_blip, prompt = input_json['path'],input_json['result_blip'],input_json['prompt']
    # '/paddle/luyao15/project/PaddleMIX/violin.jpg'
    result_blip, prompt = img2prompt(_path, result_blip, prompt)
    return dict(result_blip=result_blip, prompt=prompt)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8912,debug=False)
