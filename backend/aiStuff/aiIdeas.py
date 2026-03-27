
import base64
import io
import os
import re
import anthropic
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get('api', ''))

MAX_SIDE = 1568  # Anthropic's recommended max dimension

def _encode_image(image_path: str) -> tuple[str, str]:
    """Return (base64_data, media_type) for an image file, resized to fit Anthropic's 5MB limit."""
    img = Image.open(image_path)
    img = img.convert('RGB')

    if max(img.width, img.height) > MAX_SIDE:
        img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode('utf-8'), 'image/jpeg'


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



























