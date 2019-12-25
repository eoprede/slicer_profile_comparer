import configparser
import dictdiffer 
import os 
import random

def read_config_file(file):
	try:
		config = configparser.RawConfigParser()
		config.read(file)
		return config
	except configparser.MissingSectionHeaderError: 
		config2 = configparser.RawConfigParser()
		with open(file, 'r') as f:
			config_string = '[standalone:'+os.path.basename(file)+']\n' + f.read()
		config2.read_string(config_string)
		return config2

def figure_out_all_params(config, section):
	tp = section.split(":")[0] #type of config, filament, printer, etc
	inherits = []
	params = {}
	for key in config[section]:
		if key == "inherits" and config[section][key]:
			inherits = config[section][key].split(";")
		else:
			params = dict(list({key:config[section][key]}.items()) + list(params.items())) 
	for i in inherits:
		try:
			params = dict(list(figure_out_all_params(config, tp+":"+i.strip()).items()) + list(params.items())) 
		except KeyError as e: 
			print ("Ran into issue when looking for inherited key " + str(e))
	return params

def list_all_valid_configs(config):
	data={}
	for k in config.keys():
		split_key = k.split(":")
		# key is of a format type:name, common values are enclosed in **
		# we don't need any of them
		if len(split_key) == 2 and split_key[1][0] != "*" and split_key[1][-1] != "*":
			# create dict key if not present
			if not split_key[0] in data:
				data.update({split_key[0]:[]})
			data[split_key[0]].append(split_key[1])
	return data 

def create_config_dictionaries_for_file(config, valid_configs):
	data = {}
	for k in valid_configs.keys():
		for vc in valid_configs[k]:
			data.update({k+":"+vc:figure_out_all_params(config, k+":"+vc)})
	return data

def process_config_file(config_file, data={}):
	print ("Processing config file "+config_file)
	config = read_config_file(config_file)
	data.update(create_config_dictionaries_for_file(config, list_all_valid_configs(config)))
	return data

def print_profiles(data):
	for k in data.keys():
		print (k)

def get_profile_list(data):
	out = []
	for k in data.keys():
		out.append(k)
	return out

def print_config_diff(profile1, profile2):
	for diff in list(dictdiffer.diff(profile1, profile2)):         
		print (diff)

def return_config_diff(profile1, profile2):
	out = {"added":[], "removed": [], "changed":{}}
	for diff in list(dictdiffer.diff(profile1, profile2)):
		if diff[0] is "change":
			out["changed"].update({diff[1]:diff[2]})
		elif diff[0] is "remove":
			out["removed"]+=diff[2]
		elif diff[0] is "added":
			out["added"]+=diff[2]
	return out

def menu(data):
	while True:
		print ("Type print to display available profiles")
		print ("Type add filepath to add config file")
		print ("Type compare profile1 to profile2")
		print ("Type quit to exit")

		command = input("Please enter command: ")

		(firstWord, *rest) = command.split(maxsplit=1)

		if firstWord == "print":
			print_profiles(data)
		elif firstWord == "add":
			data = process_config_file(rest[0], data)
		elif firstWord == "quit":
			break
		elif firstWord == "compare":
			try:
				profiles = rest[0].split(" to ")
				print (profiles)
				print_config_diff(data[profiles[0]], data[profiles[1]])
			except:
				print ("Error while processing comparion and my creator is too lazy to generate more specific error message.")
		else:
			print ("Incorrect selection, try again")


def run():

	data = {}

	print ("Welcome to Slicer Config Comparer")
	menu(data)


if __name__ == '__main__':
    run()