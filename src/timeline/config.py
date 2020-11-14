GEO_SETTING = dict(
	#scope='europe',
	landcolor="#c1c1c1",
	countrycolor="white",
	projection_type='mercator',
	showsubunits=True,
	lonaxis_range=[9.3, 17.5],
	lataxis_range=[46, 49.5],
	showcountries=True,
)

SLIDERS_DICT = {
	"active": 0,
	"yanchor": "top",
	"xanchor": "left",
	"currentvalue": {
		"font": {"size": 20},
		"visible": True,
		"xanchor": "right"
	},
	"transition": {"duration": 300, "easing": "cubic-in-out"},
	"pad": {"b": 10, "t": 50},
	"len": 0.9,
	"x": 0.1,
	"y": 0,
	"steps": []
}

BUTTON_MENU_DICT = {
	"buttons": [
		{
			"args": [None, {
				"frame": {"duration": 500, "redraw": True},
				"fromcurrent": True, "transition": {
					"duration": 300,
					"easing": "quadratic-in-out"}
			}],
			"label": "Play",
			"method": "animate"
		},
		{
			"args": [[None], {
				"frame": {"duration": 0, "redraw": True},
				"mode": "immediate",
				"transition": {"duration": 0}
			}],
			"label": "Pause",
			"method": "animate"
		}
	],
	"direction": "left",
	"pad": {"r": 10, "t": 87},
	"showactive": False,
	"type": "buttons",
	"x": 0.1,
	"xanchor": "right",
	"y": 0,
	"yanchor": "top"
}


def get_slider_dict(step, txt):
	return {"args": [
		[step],
		{
			"frame": {"duration": 300, "redraw": True},
			"mode": "immediate",
			"transition": {"duration": 300}
		}
	],
		"label": txt,
		"method": "animate"
	}
