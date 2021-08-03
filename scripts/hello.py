import sys
import json

data = sys.argv[1]
print(data)

args = json.loads(data)
print('hello ' + (args['name'] if 'name' in args.keys() else 'world') + '!')