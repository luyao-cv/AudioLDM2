# import torch
import scipy

import gradio as gr
# import torch
# from diffusers import AudioLDM2Pipeline
import openai
import gradio as gr
from gradio.components import Textbox
import gradio as gr
#输入文本处理程序
import numpy as np
import scipy
from PIL import Image
import requests
import json

# make Space compatible with CPU duplicates
# if torch.cuda.is_available():
#     device = "cuda"
#     torch_dtype = torch.float16
# else:
#     device = "cpu"
#     torch_dtype = torch.float32

# load the diffusers pipeline
repo_id = "cvssp/audioldm2"
# pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch_dtype).to(device)

# set the generator for reproducibility
# generator = torch.Generator(device)

def text2audio(x, result_blip, prompt, num_inference_steps, negative_textbox, duration, guidance_scale, random_seed, n_candidates):
    if x is None:
        raise gr.Error("Please provide a image input.")
    
    
    img_path = "tmp.png"
    x.save(img_path)
    
    # img2prompt(_path, result_blip, prompt)

    input_json = {
        "path":img_path,
        "result_blip":result_blip,
        "prompt": prompt
    }
    
    results = requests.post("http://10.21.226.179:8912/blip2", json=input_json)
    # print(results.text)
    result_json = json.loads(results.text)
    
    result_blip, prompt = result_json['result_blip'],result_json['prompt']
    
    # waveforms = pipe(
    #     prompt,
    #     audio_length_in_s=duration,
    #     guidance_scale=guidance_scale,
    #     num_inference_steps=num_inference_steps,
    #     negative_prompt=negative_textbox,
    #     num_waveforms_per_prompt=n_candidates if n_candidates else 1,
    #     generator=generator.manual_seed(int(random_seed)),
    # )["audios"]
    

    waveforms = ["chatgpt.mp4"]
    # gr.make_waveform((16000, waveforms[0]), bg_image="bg.png")
    return waveforms[0], result_blip, prompt, negative_textbox, num_inference_steps, duration

iface = gr.Blocks()

with iface:

    with gr.Group():

        image_input = gr.Image(type="pil")
        
        with gr.Column():
            with gr.Column():
                gr.Markdown(value="""
                <font size=2> prompt输出, 可自行修改</font>
                """)
                Text_blip2 = gr.Textbox(label="blip2输出...")
                Text_chatgpt = gr.Textbox(label="chatgpt输出...")
                # gr.ClearButton([Text_blip2, Text_chatgpt], value="清空，不清空默认使用该prompt")


        with gr.Column():
            gr.Markdown(value="""
            <font size=2> 参数设置</font>
            """)

            with gr.Row():
                negative_textbox = gr.Textbox(label="negative prompt", value="low quality")


        with gr.Accordion("Click to modify detailed configurations", open=False):
            seed = gr.Number(
                value=45,
                label="Seed",
                info="Change this value (any integer number) will lead to a different generation result.",
            )
            duration = gr.Slider(5, 15, value=10, step=2.5, label="Duration (seconds)")
            guidance_scale = gr.Slider(
                0,
                7,
                value=3.5,
                step=0.5,
                label="Guidance scale",
                info="Larger => better quality and relevancy to text; Smaller => better diversity",
            )
            n_candidates = gr.Slider(
                1,
                5,
                value=3,
                step=1,
                label="Number waveforms to generate",
                info="Automatic quality control. This number control the number of candidates (e.g., generate three audios and choose the best to show you). A larger value usually lead to better quality with heavier computation",
            )
            num_inference_steps = gr.Slider(label="迭代步数，步数越大越接近扩散模型的结果", value=200, minimum = 1, maximum = 1000)

        outputs = gr.Video(label="Output", elem_id="output-video")
        btn = gr.Button("generate music")

    btn.click(
        text2audio,
        inputs=[image_input, Text_blip2, Text_chatgpt, num_inference_steps, negative_textbox, duration, guidance_scale, seed, n_candidates],
        outputs=[outputs, Text_blip2, Text_chatgpt, negative_textbox, num_inference_steps, duration]
    )
    
iface.launch(share=True, server_name="0.0.0.0", server_port=8911)