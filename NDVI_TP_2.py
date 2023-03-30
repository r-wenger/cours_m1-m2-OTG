import csv
from random import randint
import numpy as np
import time
import os

import osgeo.gdal as gdal
import osgeo.ogr as ogr
import osgeo.osr as osr
from osgeo.gdalconst import *

#Chemin vers le dossier de l'image S2
path_sentinel_folder = './SENTINEL2B_20190724-103744-210_L2A_T32ULU_C_V2-2'

#Chemin vers la bande du rouge
dataset_band_red = gdal.Open(os.path.join(path_sentinel_folder, 'SENTINEL2B_20190724-103744-210_L2A_T32ULU_C_V2-2_FRE_B4.tif'))
#Lire la bande 1 contenue dans le dataset, convertir en tableau et caster en float
array_img_red = dataset_band_red.GetRasterBand(1).ReadAsArray().astype(float)

#Chemin vers la bande du PIR
dataset_band_pir = gdal.Open(os.path.join(path_sentinel_folder, 'SENTINEL2B_20190724-103744-210_L2A_T32ULU_C_V2-2_FRE_B8.tif'))
array_img_pir = dataset_band_pir.GetRasterBand(1).ReadAsArray().astype(float)

output = './ndvi.tif'
#Le numerateur puis le denominateur
numerator = (array_img_pir - array_img_red)
denominator = (array_img_pir + array_img_red)

#L'eau absorbe toutes les longueurs d'onde du visible -> division par zéro ne fonctionne pas et renvoie des NAN, on convertit ces valeurs à 0
#Faire une division en utilisant Numpy
ndvi = np.divide(numerator, denominator)
#Utiliser la fonction numpy nan to num pour convertir les nan
ndvi = np.nan_to_num(ndvi)

#Ecrire le fichier NDVI avec la bonne projection et le bon format de données dans votre répertoire de travail. Attention, il faudra executer deux fois cette cellule à cause d'un bug sur gdal ..
geo_transform = dataset_band_red.GetGeoTransform()
driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create(output, ndvi.shape[1], ndvi.shape[0], 1, gdal.GDT_Float32)
dst_ds.SetProjection(dataset_band_red.GetProjection())
dst_ds.SetGeoTransform(geo_transform)
dst_ds.GetRasterBand(1).WriteArray(ndvi)

#Sinon on peut aussi remplacer les 0 dans le pir et le rouge par des 1
'''array_img_pir = np.where(array_img_pir == 0, 1, array_img_pir)
array_img_red = np.where(array_img_red == 0, 1, array_img_red)
#et calculer le NDVI ensuite :
ndvi = (array_img_pir - array_img_red)/(array_img_pir + array_img_red)'''
#normalement, plus de divisions par 0 :-)
