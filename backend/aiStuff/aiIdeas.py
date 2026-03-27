from django.http import Jsonresponse
import base64
import mimetypes
import os
import re
import anthropic



"""
def decode(image):
    ext = image.rsplit('.', 1)[-1].lower()
    media = mimetypes.guess_type(ext)
    if media is None:
        media = 'image/jpeg'
    with open(image, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8'), media

client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

def GiveIdeas(image):
    use = decode(image)
    result = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": use  
            },
            {
                "type": "text", 
                "text": (
                    "Look at this waste or trash item in the photo. "
                    "Give me exactly 5 creative, specific, and original ideas for how a student could reuse or upcycle it. "
                    "Each idea should be something practical that a teenager can actually do at home or school. "
                    "Format your response as a numbered list, one idea per line, like this:\n"
                    "1. Idea one\n"
                    "2. Idea two\n"
                    "3. Idea three\n"
                    "4. Idea four\n"
                    "5. Idea five\n"
                    "No extra explanation — just the numbered list."
                )
            }
        ]
    }
    response = client.messages.create(
        model='',
        max_tokens=1024,
        messages=result
    )
    text = response.content[0].text.strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines[:5] if len(lines) >= 5 else lines

"""

   