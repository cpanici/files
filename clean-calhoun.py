try:
	print('Loading libraries...')
	import pandas as pd
	import numpy as np
except:
	print('ERROR: Make sure pandas and numpy libraries are installed.')

try:
	print('Reading data file...')
	df = pd.read_csv('calhoun.csv')
except:
	print('ERROR: Make sure data file is located in this folder and named calhoun.csv')

print('Cleaning...')
df[['Birth', 'Death']] = df['Dates'].str.split('-', expand=True)
df.drop('Dates', 1, inplace=True)

def remove_stream(s):
    c=0
    if 'CLICK' in s:
        try:
            i = s.index('\n')
            return s[i+1:]
        except:
            return ''
    else: return s

searchfor = ['Cleveland', 'Akron', 'Bedford']

df['Services']= df['Services'].apply(lambda s: remove_stream(s) if type(s) == str else s)

homes = {'Akron': ('STEWART & CALHOUN FUNERAL HOME', '529 W. Thornton St. Akron, OH 44307'),
            'Cleveland': ('CALHOUN FUNERAL HOME – LAKE SHORE BLVD.', '17010 Lake Shore Blvd. Cleveland, OH 44110'),
            'Bedford': ('CALHOUN FUNERAL HOME – ROCKSIDE ROAD', '23000 Rockside Rd. Bedford Heights, OH 44146')}

df['Funeral Home Name'] = ''
df['Funeral Home Address'] = ''

for location in searchfor:
    df['Funeral_Home_Name'] = np.where((df['Visitation'].str.contains(location, na=False)) |
                                       (df['Services'].str.contains(location, na=False)),
                                         homes[location][0], df['Funeral Home Name'])
    df['Funeral_Home_Address'] = np.where((df['Visitation'].str.contains(location, na=False)) | 
                                          (df['Services'].str.contains(location, na=False)),
                                        homes[location][1], df['Funeral Home Address'])

df = df[['Name', 'Birth', 'Death', 'Obituary_Text', 'Visitation', 'Services', 'Funeral_Home_Name', 'Funeral_Home_Address', 'Image']]

try:
	print('Writing cleaned data to csv...')
	df.to_csv('calhoun - cleaned.csv', index=False)
	print('Cleaned data saved in this folder as calhoun - cleaned.csv')
except:
	print('ERROR: Failed to write cleaned data to csv.')