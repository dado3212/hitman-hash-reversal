from utils import ioi_string_to_hex
import pickle

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('novel.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        hash = ioi_string_to_hex(line.strip())
        if 'vertexdata' in line:
            hash += '.VTXD'
        elif 'scatterdata' in line:
            hash += '.SCDA'
        if hash in data:
            if len(data[hash]['name']) == 0:
                print(hash)
                print(line.strip())
        else:
            print(hash)
            print(line.strip())
