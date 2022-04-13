#main imports
from flask import Flask, render_template, url_for
import requests, json
#file imports
from helper import aware
def run_flask_app():
	app = Flask(__name__)

	today_is = aware.get_day_type()
	weather_dict = aware.get_weather()

	if weather_dict['description'] is not None:
		description = weather_dict['description']
	else:
		description = None

	current = weather_dict['current']
	forecast = weather_dict['forecast']
	high_low = weather_dict['high_low']

	@app.route('/')
	def home():
		#Runs on get request; Means it'll run on new sessions and when the user refreshes
		today_is = aware.get_day_type()
		weather_dict = aware.get_weather()
		
		if weather_dict['description'] is not None:
			description = weather_dict['description']
		else:
			description = None
		current = weather_dict['current']
		forecast = weather_dict['forecast']
		high_low = weather_dict['high_low']

		#For quote generation
		JSON = requests.get('https://zenquotes.io/api/random').text
		quote = str(json.loads(JSON)[0]['q'])
		
		#Get background image based on weather context
		if 'cloud' in forecast.lower():
			type_ = 'Cloudy.jpg'
		elif 'sun' in forecast.lower() or 'clear' in forecast.lower() or 'fair' in forecast.lower():
			type_ = 'Sunny.jpeg'
		elif 'snow' in forecast.lower():
			type_ = 'Snowy.jpeg'
		elif 'thunder' in forecast.lower() or 'lightning' in forecast.lower():
			type_ = 'Thunder.jpeg'
		elif 'rain' in forecast.lower() or 'shower' in forecast.lower() or 'drizzle' in forecast.lower():
			type_ = 'Rainy.jpeg'
		else:
			type_ = 'Unknown.jpg'
		
		weather_image = url_for('static', filename=f'images/{type_}')
		#Starts website
		return render_template('MHSN.html', forecast=forecast, current=current, high_low=high_low, weather_image=weather_image, quote=quote, today_is=today_is, description=description)

	if __name__ == '__main__':
		app.run(host="0.0.0.0", port=8081, debug=True)

run_flask_app()