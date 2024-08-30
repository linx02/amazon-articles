# data = {
#   title
#   date
#   readTime
#   article_markdown
#   pros
#   cons
#   image
#   amazon_link
#   slug
# }

import math

def estimate_reading_time(file_path, words_per_minute=200):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Count the number of words in the text
        words = text.split()
        num_words = len(words)
        
        # Estimate reading time in minutes
        reading_time = num_words / words_per_minute
        
        # Return the reading time rounded to the nearest whole number
        return math.ceil(reading_time)
    
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

import datetime
import json
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("--slug", type=str, required=True)
argparser.add_argument("--amazon-link", type=str, required=True)

slug = argparser.parse_args().slug
amazon_link = argparser.parse_args().amazon_link

with open(slug + ".txt", "r") as f:
    article = f.read()

with open(slug + ".info.json", "r") as f:
    info = json.load(f) 

with open(slug + ".pros_cons.json", "r") as f:
    pros_cons = json.load(f)

data = {
    "title": info["product_title"],
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    "readTime": str(estimate_reading_time(slug + ".txt")) + " min read",
    "article_markdown": article,
    "pros": pros_cons["pros"],
    "cons": pros_cons["cons"],
    "image": info["image"],
    "amazon_link": amazon_link,
    "slug": slug,
}

with open(slug + ".article.json", "w") as f:
    json.dump(data, f, indent=4)

# https://amzn.to/3Z83iXm