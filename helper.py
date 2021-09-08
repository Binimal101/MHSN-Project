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
	"""
	
	"""
	def get_weather():
		URL = "https://weather.com/weather/today/l/40.39,-74.10?par=google"
		html = requests.get(URL)
		soup = BeautifulSoup(html.text, 'lxml')
		context = soup.find(attrs={'aria-label' : 'Current Conditions for Middletown Township, NJ Weather'})
		results = context.find_all(attrs={'data-testid':'TemperatureValue'})
		results.append(soup.find(attrs={'data-testid':'wxPhrase'}))

		results = [int(x.text[:-1]) if '°' in x.text else x.text for x in results]
		split_results = [[x for x in results if type(x) == int], [x for x in results if type(x) == str and not x == '--']]

		if len([x for x in split_results[0] if type(x) == int]) == 2:
			high = '--'
			low = sorted(split_results[0])[0]
			current = sorted(split_results[0])[-1]
		elif len([x for x in split_results[0] if type(x) == int]) == 3:	
			high = sorted(split_results[0], reverse=True)[0]
			low = sorted(split_results[0])[0]
			current = sorted(split_results[0])[1]


		context = soup.find(attrs={'aria-label' : 'Current Conditions for Middletown Township, NJ Weather'})
		unavailable = False
		for iter, content in enumerate(context.div):
			# print(content.get('class')[0])
			try:
				if 'CurrentConditions--header' in content.get('class')[0]:
					continue
				elif 'CurrentConditions--dataWrapperInner' in content.get('class')[0]:
					continue
				elif 'CurrentConditions--' in content.get('class')[0]: #to make sure we have the right divider while navigating which outliers shouldn't be included
					context = content #sets new context to search
					break
			except:
				unavailable = True
		if not unavailable:
			description = context.span.text

		final = {
			'forecast' : split_results[1][0],
			'hilo' : f"{high}/{low}",
			'current' : current,
			'description' : description if not unavailable else None
		}
		return final
	
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