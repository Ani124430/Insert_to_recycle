from django.http import Jsonresponse
import random
import base64
import mimetypes
import os
import re
import anthropic
import time
client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

def decode(image):
    ext = image.rsplit('.', 1)[-1].lower()
    media = mimetypes.guess_type(ext)
    if media is None:
        media = 'image/jpeg'
    with open(image, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8'), media

def mockResponse():
    responses = [
        "Self-watering planter using the bottle base.",
        "Custom bird feeder with wooden spoon perches.",
        "Desk organizer for pens and USB drives.",
        "Vertical herb garden for a kitchen window.",
        "Eco-friendly piggy bank for loose change."
    ]
    time.sleep(0.5) 
    return responses

def score_reuse_result(waste_path, result_path):
    score = random.randint(40, 95)
    explanations = [
        "Impressive transformation — the item was given a completely new purpose with clear effort.",
        "Great creativity shown here, turning something useless into a practical everyday object.",
        "Solid reuse idea with good execution, though the finish could be a bit more polished.",
        "Very original concept — not an obvious choice, which makes it stand out on the leaderboard.",
        "The item was repurposed effectively and the result looks sturdy and well thought out.",
        "Nice work — the construction is clean and the new use makes a lot of practical sense.",
        "A simple but clever reuse that required minimal materials and produced a useful result.",
        "Strong effort visible in the details — this clearly took time and careful planning.",
        "The transformation is creative but the final result could be more refined to score higher.",
        "Excellent upcycle — the original material is barely recognizable in its new form.",
    ]
    return {'score': score, 'explanation': random.choice(explanations)}

def giveidea(image_path, use_mock=True):
    if use_mock:
        return mockResponse()
    
    try:
        base64_string, media_type = decode(image_path)
        
        message_data = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_string,
                    }
                },
                {
                    "type": "text", 
                    "text": (
                        "Look at this waste or trash item in the photo. "
                        "Give me exactly 5 creative, specific, and original ideas for how a student could reuse or upcycle it. "
                        "No extra explanation — just the numbered list."
                    )
                }
            ]
        }

        response = client.messages.create(
            model='claude-3-5-sonnet-20240620', 
            max_tokens=1024,
            messages=[message_data]
        )

        text = response.content[0].text.strip()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        ideas = []
        for line in lines:
            cleaned = re.sub(r'^[\d]+[.):\-\s]+', '', line).strip()
            if cleaned:
                ideas.append(cleaned)

        return ideas[:5]

    except Exception as e:
        print(f"Error: {e}")
        return ["Error: AI was unable to process the image."]
"""


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

   