from django.http import Jsonresponse

api = 'AIzaSyDuohZ2DUFLKDoA48IaXkf8ysV5iohj5OY'

def GiveIdeas(image):
    prompt = "Role: You are a world-class upcycling expert and creative designer. Task: The user has an image with an object. Provide 3 highly creative, non-obvious ways to repurpose this item into a functional item. Format: Return a numbered list. For each idea, include a 'Difficulty Level' (1-5)."
    response = api.generate_content([prompt, image])
    if not response:
        return Jsonresponse("Error", status = 400)
    return Jsonresponse(response)