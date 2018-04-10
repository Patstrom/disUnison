import os, sys, json

path = sys.argv[1]

json_files = [json.load(open(os.path.join(path,f))) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

register_permutations = [j["registers"] for j in json_files]

for permutation in register_permutations:
	occurences = register_permutations.count(permutation)
	if occurences != 1:
		print("{} occurs {} times".format(permutation, occurences))
		break

