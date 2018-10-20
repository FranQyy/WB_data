import pandas as pd
import matplotlib.pyplot as plt

def plot_pop(filename, country_code):
	pop_reader = pd.read_csv(filename, chunksize=1000)

	for line in pop_reader:
		pop_country = line[line['Country Code'] == country_code]
	
	pop_country = pop_country.drop(['Series Code', 'Country Code'], axis='columns')
	pop_country = pop_country.rename(lambda a: a[0:4] if a[0] in '0123456789' else a, axis='columns')
	
	pop_years = pop_country.iloc[:,2:]
	pop_years = pop_years.transpose()
	pop_years_index = pop_years.index.get_values()
	pop_years_index = pop_years_index[:-1]
	pop_elec_values = pop_years.iloc[:-1,0]

	pop_zp = zip(pop_years_index, pop_elec_values)
	pop_list = list(pop_zp)
	pop_dict = dict(pop_list)

	country = pop_country.loc[0,'Country Name']
	index=[]
	index.append(country)
	df = pd.DataFrame(pop_dict, index=index)
	df = df.transpose()
	df['Values'] = [float(n) for n in pop_elec_values]
	df['Year'] = [int(n) for n in pop_years_index]

	# pop_country = pop_country.transpose()
	
	df.plot(x='Year', y='Values')
	plt.show()
	return df


print(plot_pop('pop_elec.csv', 'AFG'))
