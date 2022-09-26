from utils import ioi_string_to_hex
import pickle

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('new.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        a = line.strip().split(',')
        name_t = a[0]
        file_t = a[1]
        file_d = file_t[:-6] + 'pc_mipblock1'
        name_d = ioi_string_to_hex(file_d) + '.TEXD'
        if name_d in data and len(data[name_d]['name']) == 0:
            print(name_d + ',' + file_d)
