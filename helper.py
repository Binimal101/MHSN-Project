from bs4 import BeautifulSoup
import requests, os


class aware:
	def get_day_type():
		URL = 'https://www.middletownk12.org/Domain/23'
		html = requests.get(URL)
		soup = BeautifulSoup(html.text, 'lxml')
		element = soup.find('span', style='bgcolor: #FF8000;')
		day = 'A' if 'A-day' in element.text else 'B' if 'B-day' in element.text else 'UNKNOWN'
		return day
	
	def get_weather():
		
		URL = 'https://weather.com/weather/today/l/40.39,-74.10?par=google'
		html = requests.get(URL)
		soup = BeautifulSoup(html.text, 'lxml')
        # Try to look for parent div, see if that changes from day to day
        # Both temperature and forecast elements are located inside of the parent div
		temperature = soup.find('span', class_='CurrentConditions--tempValue--MHmYY')
		temperature = temperature.text
		forecast = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p')
		forecast = forecast.text
		hi_low = soup.find('div', class_='CurrentConditions--tempHiLoValue--3T1DG')
		high_low = ''
		
		for thing in hi_low:
			try:
				high_low = high_low + thing.text
			except AttributeError:
				high_low = high_low + thing
		return temperature, forecast, high_low
	
	def from_military_to_standard(hour, minute=None, str=None):
		if hour == 12:
			ampm = 'PM'
		elif hour == 24:
			ampm = 'AM'
		elif hour > 12:
			hour -= 12
			ampm = 'PM'
		elif hour < 12:
			ampm = 'AM'
		if str == True and minute is not None:
			return f'{hour}:{minute} {ampm}'
		else:
			return hour, ampm
	
	def fix_zero(minute, second):
		if second < 10:
			second = '0' + str(second)
		if minute < 10:
			minute = '0' + str(minute)
		return minute, second


clear = lambda: os.system('clear')