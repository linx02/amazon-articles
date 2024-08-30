from g4f.client import Client
import json
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("--slug", type=str, required=True)

client = Client()

# open slug.json
with open("articles/" + argparser.parse_args().slug + ".article.json", "r") as f:
    data = json.load(f)

with open("templates/meta.txt", "r") as f:
    template = f.read()

prompt = template.format(
    product_title=data["title"]
)

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)

print(chat_completion.choices[0].message.content or "")

if '```' in chat_completion.choices[0].message.content:
    chat_completion.choices[0].message.content = chat_completion.choices[0].message.content.split('```')[-2]

if 'json' in chat_completion.choices[0].message.content:
    chat_completion.choices[0].message.content = chat_completion.choices[0].message.content.split('json')[-1]

try:
    json.loads(chat_completion.choices[0].message.content)
except:
    print("Error: The response is not a valid JSON.")
    exit()

# open slug.txt
with open('meta/' + argparser.parse_args().slug + ".meta.json", "w") as f:
    f.write(chat_completion.choices[0].message.content.strip())