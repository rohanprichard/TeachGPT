def get_system_prompt():
    prompt = ""
    with open("model_server/prompts/chat.txt", "r") as f:
        prompt = f.read()
    return prompt


def generate_context(name, subject, year, course):
    pass
