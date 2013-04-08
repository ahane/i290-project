import json
a = []
for line in open('harvard.sample.json'):
    try:
        b = json.loads(line)
        a.append(b)
    except:
        pass
