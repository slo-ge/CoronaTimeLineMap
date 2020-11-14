import csv
import datetime
import json
from collections import OrderedDict
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

from timeline.config import GEO_SETTING, BUTTON_MENU_DICT, get_slider_dict, SLIDERS_DICT

df = px.data.gapminder()



# class TimeLineGKZ(object):
# 	0 Time: str
# 	1 Bezirk: str
# 	2 GKZ: str
# 	3 AnzEinwohner: str
# 	4 AnzahlFaelle: str
# 	5 AnzahlFaelleSum: str
# 	6 AnzahlFaelle7Tage: str
# 	7 SiebenTageInzidenzFaelle: str
# 	8 AnzahlTotTaeglich: str
# 	9 AnzahlTotSum: str
# 	10 AnzahlGeheiltTaeglich: str
# 	11 AnzahlGeheiltSum: str

@dataclass
class SimpleCountyRow(object):
	time: datetime.datetime
	county: str
	population: int
	cases: int
	gkz: int
	ort2: str = None
	ort3: str = None
	plz: str = None
	lat: str = None
	lng: str = None


def get_county_data():
	URL = 'https://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv'
	text = requests.get(URL).content.decode('utf-8')
	lines = text.splitlines()

	lines.pop(0)

	simple_counties = []

	with open('magic-gkz-map.json', 'r') as reader:
		gkz_dict = json.loads(reader.read())

	reader = csv.reader(lines, delimiter=';', )
	for row in reader:
		time = datetime.datetime.strptime(row[0].split(' ')[0], '%d.%m.%Y')
		bezirk = row[1]
		population = row[3]
		AnzahlFaelle = int(row[4])
		gkz = row[2]

		if gkz == '900':
			gkz = '901'  # vienna special case

		simple_county = SimpleCountyRow(time, bezirk, population, AnzahlFaelle, gkz)
		gkz, ort2, ort3, plz, lat, lng = gkz_dict[simple_county.gkz]
		simple_county.ort2 = ort2
		simple_county.ort3 = ort3
		simple_county.plz = plz
		simple_county.lat = lat
		simple_county.lng = lng

		if not lat or not lng:
			raise ('No lat or lng for:', simple_county)

		simple_counties.append(simple_county)

	return simple_counties


def bubble_map_infections():
	simple_counties: List[SimpleCountyRow] = get_county_data()

	grouped = OrderedDict()
	for item in simple_counties:
		if item.time not in grouped:
			grouped[item.time] = [item]
		else:
			grouped[item.time].append(item)

	write_graph(grouped)


def write_graph(grouped: Dict):
	frames = []
	with open('austria.json', 'r') as reader:
		geojson = json.load(reader)
		print(geojson)

	for date, simple_counties in grouped.items():
		df = pd.DataFrame({
			'date_str': [str(item.time) for item in simple_counties],
			'date': [item.time for item in simple_counties],
			'lat': [item.lat for item in simple_counties],
			'lon': [item.lng for item in simple_counties],
			'value': [item.cases for item in simple_counties]
		})
		absolute = sum(df['value'])
		date_str = date.strftime('%d.%m.%Y')
		frame = go.Frame(
			layout=dict(title=f' {date_str}, total: {absolute}'),
			name=date_str,
			data=[go.Scattergeo(
				locationmode='USA-states',
				lon=df['lon'],
				lat=df['lat'],
				text=df['value'],
				marker=dict(
					size=df['value'],
					autocolorscale=False,
					line_color='rgb(10,10,10)',
					line_width=0.5,
					sizemode='area',
					colorscale='ylorrd',  # https://plotly.com/python/builtin-colorscales/
					color=df['value'],
					opacity=0.7
				)
			)])
		frames.append(frame)
		SLIDERS_DICT['steps'].append(get_slider_dict(date_str, txt=f' {date_str}, total: {absolute}'))

	fig = go.Figure(
		data=frames[-1].data[0],
		frames=frames
	)

	fig.update_layout(
		title=f'Timeline der Coronazahlen nach Bezirk',
		updatemenus=[BUTTON_MENU_DICT],
		geo=GEO_SETTING,
		sliders=[SLIDERS_DICT]
	)

	fig.show()
	fig.write_html('bubble.html')
