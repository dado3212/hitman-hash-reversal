from utils import ioi_string_to_hex
import pickle

with open('hashes.pickle', 'rb') as handle:
    data = pickle.load(handle)

with open('reverse.pickle', 'rb') as handle:
    reverse = pickle.load(handle)

num = 0
num_with_mat = 0
for file in data:
    if data[file]['type'] == 'TEXT' and len(data[file]['name']) > 0:
        num += 1
        found_material = False
        if file in reverse:
            for d in reverse[file]:
                if d in data:
                    if data[d]['type'] == 'MATI' and len(data[d]['name']) > 0:
                        found_material = True
        if found_material:
            num_with_mat += 1
        else:
            print(data[file]['name'])
            if file in reverse:
                print(reverse[file])
                for d in reverse[file]:
                    print(data[d]['name'])
            else:
                print("No reverse data")
            print()
        # for depends in data[file]['depends']:

print(num)
print(num_with_mat)
