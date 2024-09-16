import os

with open('to_scrape.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

dp = []
for line in lines:
    dp.append(line.split('dp/')[1].split('/')[0])

existing = os.listdir('articles')
existing = [f.split('.')[0] for f in existing]

for d in dp:
    if d in existing:
        print(d)