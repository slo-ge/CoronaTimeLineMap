import csv
import json

import plotly.express as px

df = px.data.gapminder()


def read_and_map_gkz_data_to_plz_and_lat_lon():
	gkz_dict = {}
	# read the other thing
	with open('resources/gkz-liste.CSV', 'r') as file:
		reader = csv.reader(file.readlines(), delimiter=';')
		next(reader)
		for row in reader:
			gkz = row[2]
			if gkz in gkz_dict:
				continue
			else:
				gkz_dict[gkz] = [row[3][1:], row[4]]

	gem_dict_plz = {}
	# read the other thing
	with open('resources/gemliste_knz.CSV', 'r') as file:
		reader = csv.reader(file.readlines(), delimiter=';')
		next(reader)
		for row in reader:
			gkz = row[0]
			if gkz in gem_dict_plz:
				continue
			else:
				gem_dict_plz[gkz] = [row[1], row[4]]

	village_dict = {}
	with open('resources/villages_at.json', 'r') as file:
		villages = json.load(file)
		for village in villages:
			village_dict[str(village['z'])] = village

	print(gkz_dict)
	print(gem_dict_plz)
	print(village_dict)

	for key, value in gkz_dict.items():
		original_gkz, ort = value

		gkz = int(original_gkz)
		if int(gkz) and int(gkz) % 100 == 0:
			gkz += 1

		gkz = str(gkz)
		if gkz in gem_dict_plz:
			ort, plz = gem_dict_plz[gkz]
			gkz_dict[key] += gem_dict_plz[gkz]

			# append lat and lng
			if plz not in village_dict:
				gkz_dict[key] += [None, None]
			else:
				data = village_dict[plz]
				gkz_dict[key] += [data['lt'], data['lg']]

	with open('magic-gkz-map.json', 'w') as writer:
		writer.write(json.dumps(gkz_dict))
