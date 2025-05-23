from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image
from groq import Groq
load_dotenv()

#-----------------------------------------------------------------------------------------------------------------
image_path ="image/acne.jpg"
# im = Image.open(image_path)
# im.show()

def extract_text_from_image(image,format):
    buffered = BytesIO()
    image.save(buffered,format=format)
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{image_base64}"

image = Image.open(image_path)
pic = extract_text_from_image(image,format="JPEG")

#-----------------------------------------------------------------------------------------------------------------
client = Groq()
model = "meta-llama/llama-4-scout-17b-16e-instruct"
query = input("enter quert:")

messages = [{"role":"user",
             "content":[
                 {"type":"text","text":query},
                 {"type":"image_url","image_url":{"url":pic}}
             ]

             }]

chat_completion = client.chat.completions.create(
    messages=messages,
    model=model
)
print(chat_completion.choices[0].message.content)
