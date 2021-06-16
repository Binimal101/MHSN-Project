#main imports
from flask import Flask, render_template, url_for
from npm.bindings import npm_install, npm_run
import requests, json
#file imports
from helper import aware

app = Flask(__name__)

today_is = aware.get_day_type()
temperature, forecast, high_low = aware.get_weather()

@app.route('/')
def home():
	#Runs on get request; Means it'll run on new sessions and when the user refreshes
	today_is = aware.get_day_type()
	temperature, forecast, high_low = aware.get_weather()
	JSON = requests.get('https://zenquotes.io/api/random').text; quote = str(json.loads(JSON)[0]['q'])
	
	if 'cloud' in forecast.lower():
		type_ = 'Cloudy.jpg'
	elif 'sun' in forecast.lower():
		type_ = 'Sunny.jpeg'
	elif 'snow' in forecast.lower():
		type_ = 'Snowy.jpeg'
	elif 'thunder' in forecast.lower() or 'lightning' in forecast.lower():
		type_ = 'Thunder.jpeg'
	elif 'rain' in forecast.lower() or 'shower' in forecast.lower():
		type_ = 'Rainy.jpeg'
	else:
		type_ = 'Unknown.jpg'
	
	weather_image = url_for('static', filename=f'images/{type_}')
	
	return render_template('MHSN.html', conditions=forecast, current=temperature, high_low=high_low, weather_image=weather_image, quote=quote, today_is=today_is)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)

