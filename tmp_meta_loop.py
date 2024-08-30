import subprocess
import os

# List articles
articles = os.listdir('articles')
slugs = [article.split('.article.json')[0] for article in articles]

# Run the meta.py script for each article
for slug in slugs:
    subprocess.run(["python", "meta.py", "--slug", slug])