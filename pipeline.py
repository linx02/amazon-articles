import subprocess
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("--url", type=str, required=True)

url = argparser.parse_args().url
slug = url.split('dp/')[1].split('/')[0]

# Run the scrape.py script
subprocess.run(["python", "scrape.py", "--url", url])

# Run the article.py script
subprocess.run(["python", "article.py", "--slug", slug])

# Run the pros_cons.py script
subprocess.run(["python", "pros_cons.py", "--slug", slug])

# Run the stitch.py script
amazon_link = input("Enter the Amazon link: ")
subprocess.run(["python", "stitch.py", "--slug", slug, "--amazon-link", amazon_link])