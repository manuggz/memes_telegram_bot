from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import *
import json
from maneja_respuesta import *
from forms import LogPrincipalForm,FormEnviarMensaje
import time
from django.http import JsonResponse


# NOMBRE_USUARIO_MANUEL   = "manuggz"
# PASSWORD_USUARIO_MANUEL = "Itadakimasu3093@!"
# Logeado_manuel = False
moteles_json_texto = '[{"nombre": "HOTEL IMPERIO ", "phasta": 3000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.486132, "pdsd": 900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.939813, "zona": "EL PARA\u00cdSO", "id": 1, "estr": 1}, {"nombre": "LEXINGTON SUITES HOTEL", "phasta": 7000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.481979, "pdsd": 2500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.938573, "zona": "EL PARA\u00cdSO", "id": 2, "estr": 1}, {"nombre": "DAKOTA SUITES HOTEL", "phasta": 4000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.48435, "pdsd": 1200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.949994, "zona": "LA PAZ", "id": 3, "estr": 1}, {"nombre": "HOTEL RAMO BLANCO ", "phasta": 5000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.489768, "pdsd": 1500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.928547, "zona": "EL PARA\u00cdSO", "id": 4, "estr": 1}, {"nombre": "NOVO HOTEL EXPRESS", "phasta": 8000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.489985, "pdsd": 2700, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.921041, "zona": "EL PARA\u00cdSO", "id": 5, "estr": 1}, {"nombre": "HOTEL 42", "phasta": 3500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.492762, "pdsd": 900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.920596, "zona": "QUINTA CRESPO", "id": 6, "estr": 1}, {"nombre": "HOTEL LIDER", "phasta": 3500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.497909, "pdsd": 1700, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.919102, "zona": "QUINTA CRESPO", "id": 7, "estr": 1}, {"nombre": "HOTEL HARMONY ", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488556, "pdsd": 2000, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.880968, "zona": "BELLO MONTE", "id": 8, "estr": 1}, {"nombre": "HOTEL BEETHOVEN", "phasta": 5300, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488546, "pdsd": 2300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.877316, "zona": "BELLO MONTE", "id": 9, "estr": 1}, {"nombre": "HOTEL COLISEO", "phasta": 8000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.49196, "pdsd": 3100, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.875711, "zona": "BELLO MONTE", "id": 10, "estr": 1}, {"nombre": "HOTEL LAS AMERICAS", "phasta": 14000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.489615, "pdsd": 5500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.870642, "zona": "SABANA GRANDE", "id": 11, "estr": 1}, {"nombre": "HOTEL AMERICAN DALLAS", "phasta": 12000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488381, "pdsd": 3300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.866956, "zona": "EL ROSAL", "id": 12, "estr": 1}, {"nombre": "HOTEL RORA", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488225, "pdsd": 1200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.866588, "zona": "EL ROSAL", "id": 13, "estr": 1}, {"nombre": "HOTEL NOSTRUM", "phasta": 3500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.480305, "pdsd": 1200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.856821, "zona": "LAS MERCEDES", "id": 14, "estr": 1}, {"nombre": "HOTEL GILMAR", "phasta": 5500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488581, "pdsd": 2100, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.865531, "zona": "EL ROSAL", "id": 15, "estr": 1}, {"nombre": "HOTEL DALLAS", "phasta": 8200, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488428, "pdsd": 3750, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.865212, "zona": "EL ROSAL", "id": 16, "estr": 1}, {"nombre": "HOTEL REMA", "phasta": 3700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.490071, "pdsd": 1200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.861242, "zona": "EL ROSAL", "id": 17, "estr": 1}, {"nombre": "HOTEL GIOLY", "phasta": 4100, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.494656, "pdsd": 1500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.85582, "zona": "CHACAO", "id": 18, "estr": 1}, {"nombre": "HOTEL EL CID", "phasta": 7500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.497158, "pdsd": 3300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.850297, "zona": "LA CASTELLANA", "id": 19, "estr": 1}, {"nombre": "HOTEL PENT HOUSE", "phasta": 6400, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.496871, "pdsd": 2300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.850266, "zona": "LA CASTELLANA", "id": 20, "estr": 1}, {"nombre": "HOTEL TRINI", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.496681, "pdsd": 2200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.850313, "zona": "LA CASTELLANA", "id": 21, "estr": 1}, {"nombre": "HOTEL LA TOJA", "phasta": 7600, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.497471, "pdsd": 2450, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.866882, "zona": "EL BOSQUE", "id": 22, "estr": 1}, {"nombre": "HOTEL MEREY", "phasta": 5850, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.492519, "pdsd": 1900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.881438, "zona": "SABANA GRANDE", "id": 23, "estr": 1}, {"nombre": "HOTEL MONTPARK", "phasta": 19000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.489623, "pdsd": 8500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.870959, "zona": "BELLO MONTE", "id": 24, "estr": 1}, {"nombre": "HOTEL DALLAS SUITES", "phasta": 10100, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.478599, "pdsd": 3500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.830174, "zona": "LOS RU\u00cdCES (SUR)", "id": 25, "estr": 1}, {"nombre": "HOTEL BOSQUE DORADO", "phasta": 15500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.409322, "pdsd": 6500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.959518, "zona": "CARRETERA PANAMERICANA", "id": 26, "estr": 1}, {"nombre": "MOTEL VILLA SUITES", "phasta": 6700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.478709, "pdsd": 2350, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.962034, "zona": "LA YAGUARA", "id": 27, "estr": 1}, {"nombre": "MOTEL CANAIMA", "phasta": 4900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.354492, "pdsd": 2400, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -67.004759, "zona": "CARRETERA PANAMERICANA", "id": 28, "estr": 1}, {"nombre": "HOTEL NACIONES UNIDAS", "phasta": 3900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.490064, "pdsd": 1650, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.933528, "zona": "EL PARA\u00cdSO", "id": 29, "estr": 1}, {"nombre": "HOTEL ALLADIN", "phasta": 9900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488232, "pdsd": 1700, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.868633, "zona": "EL ROSAL", "id": 30, "estr": 1}, {"nombre": "HOTEL CARACAS CUMBERLAND", "phasta": 13800, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.493943, "pdsd": 4300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.871226, "zona": "SABANA GRANDE", "id": 31, "estr": 1}, {"nombre": "HOTEL EMBASSY SUITES", "phasta": 4300, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.49193, "pdsd": 1500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.880967, "zona": "PLAZA VENEZUELA", "id": 32, "estr": 1}, {"nombre": "HOTEL MONTA\u00d1A SUITES", "phasta": 17600, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.494764, "pdsd": 1900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.783249, "zona": "PETARE", "id": 33, "estr": 1}, {"nombre": "HOTEL PRESIDENT", "phasta": 12600, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.497381, "pdsd": 3450, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.881672, "zona": "PLAZA VENEZUELA", "id": 34, "estr": 1}, {"nombre": "THE HOTEL", "phasta": 22000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488856, "pdsd": 7500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.863842, "zona": "EL ROSAL", "id": 35, "estr": 1}, {"nombre": "HOTEL SAVOY", "phasta": 8900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.493455, "pdsd": 2350, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.871633, "zona": "SABANA GRANDE", "id": 36, "estr": 1}, {"nombre": "HOTEL SHELTER SUITES", "phasta": 19800, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.490602, "pdsd": 6500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.853475, "zona": "CHACAO", "id": 37, "estr": 1}, {"nombre": "HOTEL LIMA", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.499997, "pdsd": 1950, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.886165, "zona": "LOS CAOBOS", "id": 38, "estr": 1}, {"nombre": "HOTEL CALIFORNIA SUITES", "phasta": 18700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.479505, "pdsd": 4300, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.827853, "zona": "CALIFORNIA (SUR)", "id": 39, "estr": 1}, {"nombre": "HOTEL DUBAI SUITES", "phasta": 22000, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.481444, "pdsd": 4900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.963145, "zona": "LA YAGUARA", "id": 40, "estr": 1}, {"nombre": "HOTEL MADRID", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.48918, "pdsd": 2000, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.870702, "zona": "BELLO MONTE", "id": 41, "estr": 1}, {"nombre": "HOTEL EDU (MOTO-HOTEL)", "phasta": 3200, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.488168, "pdsd": 1100, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.869554, "zona": "BELLO MONTE", "id": 42, "estr": 1}, {"nombre": "HOTEL BROADWAY", "phasta": 10500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.490061, "pdsd": 4400, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.869806, "zona": "CHACA\u00cdTO", "id": 43, "estr": 1}, {"nombre": "HOTEL TAMPA", "phasta": 9900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.496189, "pdsd": 4900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.879079, "zona": "SABANA GRANDE", "id": 44, "estr": 1}, {"nombre": "HOTEL LA FLORESTA", "phasta": 6700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.494473, "pdsd": 3500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.848267, "zona": "ALTAMIRA", "id": 45, "estr": 1}, {"nombre": "HOTEL MEDITERRANEO", "phasta": 9900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.480041, "pdsd": 2100, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.809821, "zona": "LA URBINA", "id": 46, "estr": 1}, {"nombre": "HOTEL KING\u00b4S", "phasta": 9850, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.495226, "pdsd": 3500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.882089, "zona": "PLAZA VENEZUELA", "id": 47, "estr": 1}, {"nombre": "HOTEL YARE", "phasta": 2700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.492616, "pdsd": 700, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.880998, "zona": "PLAZA VENEZUELA", "id": 48, "estr": 1}, {"nombre": "HOTEL CHACAO CUMBERLAND", "phasta": 12300, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.492188, "pdsd": 5200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.867137, "zona": "CHACA\u00cdTO", "id": 49, "estr": 1}, {"nombre": "HOTEL LA SALLE", "phasta": 3400, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.50361, "pdsd": 1550, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.882329, "zona": "LAS PALMAS", "id": 50, "estr": 1}, {"nombre": "HOTEL NILSON", "phasta": 3300, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.502424, "pdsd": 1500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.884645, "zona": "LOS CAOBOS", "id": 51, "estr": 1}, {"nombre": "HOTEL ATL\u00c1NTIDA", "phasta": 3980, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.499085, "pdsd": 2400, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.884595, "zona": "LOS CAOBOS", "id": 52, "estr": 1}, {"nombre": "HOTEL PANORAMA", "phasta": 4500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.380263, "pdsd": 1950, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.965843, "zona": "CARRETERA PANAMERICANA", "id": 53, "estr": 1}, {"nombre": "HOTEL EL MARQU\u00c9S", "phasta": 9700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.494209, "pdsd": 4400, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.808636, "zona": "LA URBINA", "id": 54, "estr": 1}, {"nombre": "HOTEL LINCOLN SUITES", "phasta": 9700, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.495579, "pdsd": 4700, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.877805, "zona": "SABANA GRANDE", "id": 55, "estr": 1}, {"nombre": "HOTEL PLAZA PALACE", "phasta": 6400, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.495666, "pdsd": 3200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.873205, "zona": "SABANA GRANDE", "id": 56, "estr": 1}, {"nombre": "HOTEL PLAZA VENEZUELA", "phasta": 5500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.498335, "pdsd": 3500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.885031, "zona": "PLAZA VENEZUELA", "id": 57, "estr": 1}, {"nombre": "HOTEL LA MONCLOA", "phasta": 8900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.498966, "pdsd": 4900, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.871313, "zona": "LA CAMPI\u00d1A", "id": 58, "estr": 1}, {"nombre": "HOTEL RIAZOR", "phasta": 5500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.487181, "pdsd": 2200, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.863089, "zona": "EL ROSAL", "id": 59, "estr": 1}, {"nombre": "HOTEL ALEX", "phasta": 18500, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.50479, "pdsd": 7600, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.905765, "zona": "LA CANDELARIA", "id": 60, "estr": 1}, {"nombre": "HOTEL GABIAL", "phasta": 3900, "precio": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "lat": 10.49365, "pdsd": 1500, "cat_num": 2, "tipo_de_cobro": "Por hora", "lon": -66.881293, "zona": "PLAZA VENEZUELA", "id": 61, "estr": 1}]'
# Create your views here.
def index(request):
	return render(request,'base.html')

def mostrarMensajes(request):
	return render(request,'mensajes.html',{'mensajes':Mensaje.objects.all()})

def mostrarUsuarios(request):

	if request.method == "POST":
		form = FormEnviarMensaje(request.POST)
		if form.is_valid():
			enviarMensajeATodosUsuarios(form.cleaned_data['mensaje'])

	return render(request,'usuarios.html',{'usuarios':Usuario.objects.all()})

def mostrarMoteles(request):

	if request.method == "GET":
		return HttpResponse(moteles_json_texto)

	return HttpResponse('Matate!')

def mostrarUsuario(request,id_usuario):
	id_usuario = int(id_usuario)
	usuario_r = get_object_or_404(Usuario, pk=id_usuario) 
	mensajes = Mensaje.objects.filter(usuario=usuario_r)

	if request.method == "POST":
		form = FormEnviarMensaje(request.POST)
		if form.is_valid():
			enviarMensajeTexto(id_usuario,form.cleaned_data['mensaje'])

                  
	return render(request,'usuario.html',{'usuario':usuario_r,'total_ms_en':len(mensajes),
										  'mensajes':mensajes})	


@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		time.sleep(1)
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		# mensaje = u"/help sendme"
		# chid = 12500
		# upid = 25208203
		# responder_usuario({u'message': {u'chat': {u'first_name': u'Manuel', u'id': 109518141, u'username': u'manuggz', u'last_name': u'Gonzalez'}, u'text': mensaje, u'from': {u'first_name': u'Manuel', u'id': 109518141, u'username': u'manuggz', u'last_name': u'Gonzalez'}, u'date': 1437074942, 
		# 	u'message_id': chid}, u'update_id': upid})
		return redirect('/BotTelegram/')
	return HttpResponse('OK')
