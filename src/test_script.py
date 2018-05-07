#!/usr/bin/python3
import os, sys, json
from tqdm import tqdm

test = sys.argv[1]
path = sys.argv[2]
json_files = [json.load(open(os.path.join(path,f))) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

#def test_duplicate_schedules():
#	i = 0
#	while i < len(json_files):
#		j = i + 1
#		while j < len(json_files):
#			if json_files[i]["instructions"] == json_files[j]["instructions"] and json_files[i]["cycles"] == json_files[j]["cycles"]:
#				for k, v in json_files[i].items():
#					if v != json_files[j][k]:
#						print("{}:\n{}\n{}".format(k, v, json_files[j][k]))
#						print("\n\n==================================")
#				sys.exit(0)
#			j += 1
#		i += 1

def test_schedule():
	schedules = [(j["instructions"],j["cycles"]) for j in json_files]
	for schedule in tqdm(schedules):
		occurences = schedules.count(schedule)
		if occurences != 1:
			print("{} occurs {} times".format(schedule, occurences))
			break


def test_registers():
	registers = [j["registers"] for j in json_files]
	for register in tqdm(registers):
		occurences = registers.count(register)
		if occurences != 1:
			print("{} occurs {} times".format(register, occurences))
			break

function = {
	"registers": test_registers,
	"schedule": test_schedule,
}

function[test]()
