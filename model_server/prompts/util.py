def get_system_prompt(path: str):
    with open("model_server/prompts/" + path, "r") as f:
        system_prompt = f.read()

    return system_prompt


if __name__ == "__main__":
    print(get_system_prompt("chat.txt"))
