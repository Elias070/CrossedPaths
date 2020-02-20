import json

with open('C:/xampp/htdocs/WebProjects/CrossedPaths/src/elondra_data.json', 'r') as f:
    elondra_data_dict = json.load(f)

loopCount = 3
loopCount = loopCount + 1
for idx, item in enumerate(elondra_data_dict):
    if (idx+1) % loopCount == 0:
      break
    print(item['timestamp'])
    print(item['lat'])
    print(item['lon'])
    print(' ')
