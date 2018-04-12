#!/usr/bin/python3
import os, sys, json
from tqdm import tqdm

test = sys.argv[1]
path = sys.argv[2]
json_files = [json.load(open(os.path.join(path,f))) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


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
