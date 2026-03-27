
import base64
import os
import re
import anthropic
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get('api', ''))

def _encode_image(image_path: str) -> tuple[str, str]:
    """Return (base64_data, media_type) for an image file."""
    ext = image_path.rsplit('.', 1)[-1].lower()
    media_type_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'}
    media_type = media_type_map.get(ext, 'image/jpeg')
    with open(image_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8'), media_type


def giveIdea(image_path: str, use_mock = True) -> list:
    """
    Send a waste/trash photo to Claude Vision.
    Returns a list of 5 creative reuse ideas as strings.
    """

    b64, media_type = _encode_image(image_path)
    my_messages = [{
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                    'source': {'type': 'base64', 'media_type': media_type, 'data': b64}
                },
                {
                    'type': 'text',
                    'text': (
                        'Look at this waste or trash item in the photo. '
                        'Give me exactly 5 creative, specific, and original ideas for how a student could reuse or upcycle it. '
                        'Each idea should be something practical that a teenager can actually do at home or school. '
                        'Format your response as a numbered list, one idea per line, like this:\n'
                        '1. Idea one\n'
                        '2. Idea two\n'
                        '3. Idea three\n'
                        '4. Idea four\n'
                        '5. Idea five\n'
                        'No extra explanation — just the numbered list.'
                    )
                }
            ]
        }]
    
    response = client.messages.create(
        model='claude-opus-4-6',
        max_tokens=1024,
        messages=my_messages
    )
    text = response.content[0].text.strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    ideas = []
    for line in lines:
        cleaned = re.sub(r'^[\d]+[.):\-\s]+', '', line).strip()
        if cleaned:
            ideas.append(cleaned)
    return ideas[:5] if len(ideas) >= 5 else ideas


def score_reuse_result(waste_path: str, result_path: str) -> dict:
    """
    Compare the original waste photo with the reuse result photo.
    Returns {'score': int (1-100), 'explanation': str}.
    """
    b64_waste, mt_waste = _encode_image(waste_path)
    b64_result, mt_result = _encode_image(result_path)
    response = client.messages.create(
        model='claude-opus-4-6',
        max_tokens=512,
        messages=[{
            'role': 'user',
            'content': [
                {'type': 'image', 'source': {'type': 'base64', 'media_type': mt_waste, 'data': b64_waste}},
                {'type': 'image', 'source': {'type': 'base64', 'media_type': mt_result, 'data': b64_result}},
                {
                    'type': 'text',
                    'text': (
                        'The first image shows a waste or trash item BEFORE reuse. '
                        'The second image shows the RESULT after someone reused or upcycled it. '
                        'Score how well they reused the item from 1 to 100 based on:\n'
                        '- Creativity (40%): how original and imaginative the idea is\n'
                        '- Effort (30%): how much work clearly went into making it\n'
                        '- Usefulness (30%): how practical or functional the result is\n\n'
                        'Reply with EXACTLY this format and nothing else:\n'
                        'SCORE: <number between 1 and 100>\n'
                        'EXPLANATION: <one sentence explaining the score>'
                    )
                }
            ]
        }]
    )
    text = response.content[0].text.strip()
    score = 50  # safe fallback
    explanation = 'Good effort at reusing this item!'
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('SCORE:'):
            try:
                score = int(line.replace('SCORE:', '').strip())
            except ValueError:
                pass
        elif line.startswith('EXPLANATION:'):
            explanation = line.replace('EXPLANATION:', '').strip()
    return {'score': max(1, min(100, score)), 'explanation': explanation}































"""
import random
import base64
import mimetypes
import os
import re
import anthropic
import time
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("api"))

def decode(image):
    ext = image.rsplit('.', 1)[-1].lower()
    media_type_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'}
    media_type = media_type_map.get(ext, 'image/jpeg')
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

def scoreRes(waste_path, result_path):
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

def giveIdea(image_path, use_mock=True):
    if use_mock:
        return mockResponse()
    print(image_path)
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
        print(message_data)
        response = client.messages.create(
            model='claude-4-5-haiku', 
            max_tokens=1024,
            messages=[message_data]
        )
        print(response)
        text = response.content[0].text.strip()
        print(text)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        ideas = []
        for line in lines:
            cleaned = re.sub(r'^[\d]+[.):\-\s]+', '', line).strip()
            if cleaned:
                ideas.append(cleaned)

        return ideas[:5]

    except Exception as e:
        print("muahahahah")
        print(f"Error: {e}")
        return ["Error: AI was unable to process the image."]



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

   