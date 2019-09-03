#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 13:36:23 2019

@author: carlos.inocencio
"""
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
from zipfile import ZipFile
from pyunpack import Archive
from matplotlib import rcParams

Archive('dest_2015gw.zip').extractall('~/Desktop/states/')


Mex = gpd.read_file('México_Estados.shp').set_index('ESTADO')
#Mex = gpd.read_file('states/dest_2015gw.shp')
#Mex.plot()

dataframe = pd.read_csv('RNPEDFC_1.csv').rename(columns={"Entidad en que se le vio por ultima vez": "Estado"})
grouped = dataframe.groupby(['Estado']).count().drop('NO ESPECIFICADO')
grouped = grouped.rename(columns={"Edad": "Count"})
grouped = grouped[['Count']]
Mex = Mex.join(grouped)
poblacion = pd.DataFrame([{
        'Chihuahua': 3556574,
        'Sonora': 2850330,
        'Coahuila': 2954915,
        'Durango': 1754754,
        'Oaxaca': 3967889,
        'Tamaulipas': 3441698,
        'Jalisco': 7844830,
        'Zacatecas': 1579209,
        'Baja California Sur': 712029,
        'Chiapas': 5217908,
        'Veracruz': 8112505,
        'Baja California': 3315766,
        'Nuevo León': 5119504,
        'Guerrero': 3533251,
        'San Luis Potosí': 2717820,
        'Michoacán': 4584471,
        'Sinaloa': 2966321,
        'Campeche': 899931,
        'Quintana Roo': 1501562,
        'Yucatán': 2097175,
        'Puebla': 6168883,
        'Guanajuato': 5853677,
        'Nayarit': 1181050,
        'Tabasco': 2395272,
        'México': 16187608,
        'Hidalgo': 2858359,
        'Querétaro': 2038372,
        'Colima': 711235,
        'Aguascalientes': 1312544,
        'Morelos': 1903811,
        'Tlaxcala': 1272847,
        'Distrito Federal': 8918653
        }]).transpose().rename(columns={0:'poblacion'})
Mex = Mex.join(poblacion)
Mex['rate'] = Mex['Count']/Mex['poblacion']

Mex['Count_rank'] = Mex['Count'].rank(ascending=False, method='first').astype('int')
Mex['rate_rank'] = Mex['rate'].rank(ascending=False, method='first').astype('int')

Mex['coords'] = Mex['geometry'].apply(lambda x: x.representative_point().coords[:])
Mex['coords'] = [coords[0] for coords in Mex['coords']]


####
#Absolute representation
###
absolute = Mex.sort_values('Count_rank').reset_index().set_index('Count_rank')
absolute.plot(column='Count', cmap='YlOrBr', edgecolor='grey', figsize=(10,5)).axis('off')

for idx, row in absolute.iterrows():
    text = plt.annotate(s=idx, xy=row['coords'],horizontalalignment='center')
    text.set_fontsize(5)
text_list = plt.figtext(0.82,0.25,absolute['ESTADO'].to_string(header = None), fontsize=5, horizontalalignment='left')
plt.figtext(0.6,0.8,'Total missing people \n reports in Mexico', fontsize=12, horizontalalignment='center', fontweight= 'semibold')
#rcParams.update({'figure.autolayout': True})
plt.savefig('Total_dis.png', format='png', dpi = 300, bbox_inches='tight')


####
#Relative representation
###
relative = Mex.sort_values('rate_rank').reset_index().set_index('rate_rank')
relative.plot(column='rate', cmap='YlOrBr', edgecolor='grey', figsize=(10,5)).axis('off')
for idx, row in relative.iterrows():
    text = plt.annotate(s=idx, xy=row['coords'],horizontalalignment='center')
    text.set_fontsize(5)
    
plt.figtext(0.82,0.25, relative['ESTADO'].to_string(header=None), fontsize=5, horizontalalignment='left')
plt.figtext(0.6,0.8,'Relative missing people \n reports in Mexico', fontsize=12, horizontalalignment='center', fontweight='semibold')
plt.savefig('Relative_dis.png', format='png', dpi = 300, bbox_inches='tight')


import imageio
images = []
filenames= ['Total_dis.png','Relative_dis.png','Total_dis.png','Relative_dis.png']
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('map.gif', images, duration=1.5)
