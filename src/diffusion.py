from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, StableDiffusionUpscalePipeline, AutoencoderKL
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed
import argparse
import random
import discord
import asyncio

def magic_prompt(text):
    magic_prompt_id = "Gustavosta/MagicPrompt-Stable-Diffusion"
    generator = pipeline('text-generation', model=magic_prompt_id)
    set_seed(random.randint(0, 100))
    text = generator(text, num_return_sequences=1, do_sample = True, max_length=200)
    return text[0]['generated_text']

def generate_image(text):
    #load model
    text = magic_prompt(text)
    model_id = "johnslegers/epic-diffusion"
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, vae=vae)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")

    prompt = text
    image = pipe(prompt, num_inference_steps=20, guidance_scale = 9).images[0]
    image.save("test.png")

def context_wrapped_generate_image(text, ctx):
    # generate_image(text)
    print("peepee")
    image = "test.png"
    asyncio.run(ctx.send(file=discord.File(image)))

if __name__ == "__main__":
    #get args
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="text to generate image from")
    args = parser.parse_args()
    generate_image(args.text)

    