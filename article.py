from g4f.client import Client
import json
import argparse
from g4f.Provider import Allyfy

argparser = argparse.ArgumentParser()

argparser.add_argument("--slug", type=str, required=True)

client = Client()

# open slug.json
with open(argparser.parse_args().slug + ".info.json", "r") as f:
    data = json.load(f)

with open("templates/article.txt", "r") as f:
    template = f.read()

data["reviews"] = [f"{i+1} - {review}" for i, review in enumerate(data["reviews"])]

prompt = template.format(
    product_title=data["product_title"],
    product_facts=data["product_facts"],
    reviews="\n".join(data["reviews"]),
)

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    provider=Allyfy
)

print(chat_completion.choices[0].message.content or "")

# open slug.txt
with open(argparser.parse_args().slug + ".txt", "w") as f:
    f.write(chat_completion.choices[0].message.content)