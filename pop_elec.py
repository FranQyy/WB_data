import pandas as pd
import matplotlib.pyplot as plt

def plot_pop(filename, country_code):
	pop_reader = pd.read_csv(filename, chunksize=100)

	for line in pop_reader:
		pop_country = line[line['Country Code'] == country_code]
		pop_country = pop_country[pop_country['Series Name'] == 'Access to electricity (% of population)']

		pop_country = pop_country.drop(['Series Code', 'Country Code'], axis='columns')
		pop_country = pop_country.rename(lambda a: a[0:4] if a[0] in '0123456789' else a, axis='columns')
		
		pop_years = pop_country.iloc[:,2:]
		pop_years = pop_years.transpose()

		print(pop_years)
		pop_years_index = pop_years.index.get_values()
		pop_years_index = pop_years_index[:-1]

		try:
			pop_elec_values = pop_years.iloc[:-1,0]
		except:
			pass
		print(pop_years_index)


	df = pd.DataFrame()
	df['Values'] = [float(n) for n in pop_elec_values]
	df['Year'] = [int(n) for n in pop_years_index]

	# pop_country = pop_country.transpose()
	
	df.plot(x='Year', y='Values')
	plt.show()
	return pop_years_index

plot_pop('pop_elec.csv', 'ZWE')
