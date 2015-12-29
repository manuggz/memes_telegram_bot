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
moteles_json_texto = '[{"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 1, "lat": "10.486132", "nombre": "HOTEL IMPERIO ", "zona": "EL PARA\u00cdSO", "phasta": 3000, "precio": 1, "pdsd": 900, "long": "-66.93981300"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 2, "lat": "10.481979", "nombre": "LEXINGTON SUITES HOTEL", "zona": "EL PARA\u00cdSO", "phasta": 7000, "precio": 1, "pdsd": 2500, "long": "-66.938573"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 3, "lat": "10.484350", "nombre": "DAKOTA SUITES HOTEL", "zona": "LA PAZ", "phasta": 4000, "precio": 1, "pdsd": 1200, "long": "-66.949994"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 4, "lat": "10.489768", "nombre": "HOTEL RAMO BLANCO ", "zona": "EL PARA\u00cdSO", "phasta": 5000, "precio": 1, "pdsd": 1500, "long": "-66.928547"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 5, "lat": "10.489985", "nombre": "NOVO HOTEL EXPRESS", "zona": "EL PARA\u00cdSO", "phasta": 8000, "precio": 1, "pdsd": 2700, "long": "-66.921041"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 6, "lat": "\n\n\u00a010.492762 ", "nombre": "HOTEL 42", "zona": "QUINTA CRESPO", "phasta": 3500, "precio": 1, "pdsd": 900, "long": "-66.920596"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 7, "lat": "10.497909", "nombre": "HOTEL LIDER", "zona": "QUINTA CRESPO", "phasta": 3500, "precio": 1, "pdsd": 1700, "long": "-66.919102"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 8, "lat": "10.488556", "nombre": "HOTEL HARMONY ", "zona": "BELLO MONTE", "phasta": 4500, "precio": 1, "pdsd": 2000, "long": "-66.880968"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 9, "lat": "10.488546", "nombre": "HOTEL BEETHOVEN", "zona": "BELLO MONTE", "phasta": 5300, "precio": 1, "pdsd": 2300, "long": "-66.877316"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 10, "lat": "10.491960", "nombre": "HOTEL COLISEO", "zona": "BELLO MONTE", "phasta": 8000, "precio": 1, "pdsd": 3100, "long": "-66.875711"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 11, "lat": "10.489615", "nombre": "HOTEL LAS AMERICAS", "zona": "SABANA GRANDE", "phasta": 14000, "precio": 1, "pdsd": 5500, "long": "-66.870642"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 12, "lat": "10.488381", "nombre": "HOTEL AMERICAN DALLAS", "zona": "EL ROSAL", "phasta": 12000, "precio": 1, "pdsd": 3300, "long": "-66.866956"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 13, "lat": "10.488225", "nombre": "HOTEL RORA", "zona": "EL ROSAL", "phasta": 4500, "precio": 1, "pdsd": 1200, "long": "-66.866588"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 14, "lat": "10.480305", "nombre": "HOTEL NOSTRUM", "zona": "LAS MERCEDES", "phasta": 3500, "precio": 1, "pdsd": 1200, "long": "-66.856821"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 15, "lat": "10.488581", "nombre": "HOTEL GILMAR", "zona": "EL ROSAL", "phasta": 5500, "precio": 1, "pdsd": 2100, "long": "-66.865531"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 16, "lat": "10.488428", "nombre": "HOTEL DALLAS", "zona": "EL ROSAL", "phasta": 8200, "precio": 1, "pdsd": 3750, "long": "-66.865212"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 17, "lat": "10.490071", "nombre": "HOTEL REMA", "zona": "EL ROSAL", "phasta": 3700, "precio": 1, "pdsd": 1200, "long": "-66.861242"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 18, "lat": "10.494656", "nombre": "HOTEL GIOLY", "zona": "CHACAO", "phasta": 4100, "precio": 1, "pdsd": 1500, "long": "-66.855820"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 19, "lat": "10.497158", "nombre": "HOTEL EL CID", "zona": "LA CASTELLANA", "phasta": 7500, "precio": 1, "pdsd": 3300, "long": "-66.850297"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 20, "lat": "10.496871", "nombre": "HOTEL PENT HOUSE", "zona": "LA CASTELLANA", "phasta": 6400, "precio": 1, "pdsd": 2300, "long": "-66.850266"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 21, "lat": "10.496681", "nombre": "HOTEL TRINI", "zona": "LA CASTELLANA", "phasta": 4500, "precio": 1, "pdsd": 2200, "long": "-66.850313"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 22, "lat": "10.497471", "nombre": "HOTEL LA TOJA", "zona": "EL BOSQUE", "phasta": 7600, "precio": 1, "pdsd": 2450, "long": "-66.866882"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 23, "lat": "10.492519", "nombre": "HOTEL MEREY", "zona": "SABANA GRANDE", "phasta": 5850, "precio": 1, "pdsd": 1900, "long": "-66.881438"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 24, "lat": "10.489623", "nombre": "HOTEL MONTPARK", "zona": "BELLO MONTE", "phasta": 19000, "precio": 1, "pdsd": 8500, "long": "-66.870959"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 25, "lat": "10.478599", "nombre": "HOTEL DALLAS SUITES", "zona": "LOS RU\u00cdCES (SUR)", "phasta": 10100, "precio": 1, "pdsd": 3500, "long": "-66.830174"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 26, "lat": "10.409322", "nombre": "HOTEL BOSQUE DORADO", "zona": "CARRETERA PANAMERICANA", "phasta": 15500, "precio": 1, "pdsd": 6500, "long": "-66.959518"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 27, "lat": "10.478709", "nombre": "MOTEL VILLA SUITES", "zona": "LA YAGUARA", "phasta": 6700, "precio": 1, "pdsd": 2350, "long": "-66.962034"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 28, "lat": "10.354492", "nombre": "MOTEL CANAIMA", "zona": "CARRETERA PANAMERICANA", "phasta": 4900, "precio": 1, "pdsd": 2400, "long": "-67.004759"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 29, "lat": "10.490064", "nombre": "HOTEL NACIONES UNIDAS", "zona": "EL PARA\u00cdSO", "phasta": 3900, "precio": 1, "pdsd": 1650, "long": "-66.933528"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 30, "lat": "10.488232", "nombre": "HOTEL ALLADIN", "zona": "EL ROSAL", "phasta": 9900, "precio": 1, "pdsd": 1700, "long": "-66.868633"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 31, "lat": "10.493943", "nombre": "HOTEL CARACAS CUMBERLAND", "zona": "SABANA GRANDE", "phasta": 13800, "precio": 1, "pdsd": 4300, "long": "-66.871226"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 32, "lat": "10.491930", "nombre": "HOTEL EMBASSY SUITES", "zona": "PLAZA VENEZUELA", "phasta": 4300, "precio": 1, "pdsd": 1500, "long": "-66.880967"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 33, "lat": "10.494764", "nombre": "HOTEL MONTA\u00d1A SUITES", "zona": "PETARE", "phasta": 17600, "precio": 1, "pdsd": 1900, "long": "-66.783249"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 34, "lat": "10.497381", "nombre": "HOTEL PRESIDENT", "zona": "PLAZA VENEZUELA", "phasta": 12600, "precio": 1, "pdsd": 3450, "long": "-66.881672"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 35, "lat": "10.488856", "nombre": "THE HOTEL", "zona": "EL ROSAL", "phasta": 22000, "precio": 1, "pdsd": 7500, "long": "-66.863842"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 36, "lat": "10.493455", "nombre": "HOTEL SAVOY", "zona": "SABANA GRANDE", "phasta": 8900, "precio": 1, "pdsd": 2350, "long": "-66.871633"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 37, "lat": "10.490602", "nombre": "HOTEL SHELTER SUITES", "zona": "CHACAO", "phasta": 19800, "precio": 1, "pdsd": 6500, "long": "-66.853475"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 38, "lat": "10.499997", "nombre": "HOTEL LIMA", "zona": "LOS CAOBOS", "phasta": 4500, "precio": 1, "pdsd": 1950, "long": "-66.886165"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 39, "lat": "10.479505", "nombre": "HOTEL CALIFORNIA SUITES", "zona": "CALIFORNIA (SUR)", "phasta": 18700, "precio": 1, "pdsd": 4300, "long": "-66.827853"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 40, "lat": "10.481444", "nombre": "HOTEL DUBAI SUITES", "zona": "LA YAGUARA", "phasta": 22000, "precio": 1, "pdsd": 4900, "long": "-66.963145"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 41, "lat": "10.489180", "nombre": "HOTEL MADRID", "zona": "BELLO MONTE", "phasta": 4500, "precio": 1, "pdsd": 2000, "long": "-66.870702"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 42, "lat": "10.488168", "nombre": "HOTEL EDU (MOTO-HOTEL)", "zona": "BELLO MONTE", "phasta": 3200, "precio": 1, "pdsd": 1100, "long": "-66.869554"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 43, "lat": "10.490061", "nombre": "HOTEL BROADWAY", "zona": "CHACA\u00cdTO", "phasta": 10500, "precio": 1, "pdsd": 4400, "long": "-66.869806"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 44, "lat": "10.496189", "nombre": "HOTEL TAMPA", "zona": "SABANA GRANDE", "phasta": 9900, "precio": 1, "pdsd": 4900, "long": "-66.879079"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 45, "lat": "10.494473", "nombre": "HOTEL LA FLORESTA", "zona": "ALTAMIRA", "phasta": 6700, "precio": 1, "pdsd": 3500, "long": "-66.848267"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 46, "lat": "10.480041", "nombre": "HOTEL MEDITERRANEO", "zona": "LA URBINA", "phasta": 9900, "precio": 1, "pdsd": 2100, "long": "-66.809821"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 47, "lat": "10.495226", "nombre": "HOTEL KING\u00b4S", "zona": "PLAZA VENEZUELA", "phasta": 9850, "precio": 1, "pdsd": 3500, "long": "-66.882089"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 48, "lat": "10.492616", "nombre": "HOTEL YARE", "zona": "PLAZA VENEZUELA", "phasta": 2700, "precio": 1, "pdsd": 700, "long": "-66.880998"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 49, "lat": "10.492188", "nombre": "HOTEL CHACAO CUMBERLAND", "zona": "CHACA\u00cdTO", "phasta": 12300, "precio": 1, "pdsd": 5200, "long": "-66.867137"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 50, "lat": "10.503610", "nombre": "HOTEL LA SALLE", "zona": "LAS PALMAS", "phasta": 3400, "precio": 1, "pdsd": 1550, "long": "-66.882329"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 51, "lat": "10.502424", "nombre": "HOTEL NILSON", "zona": "LOS CAOBOS", "phasta": 3300, "precio": 1, "pdsd": 1500, "long": "-66.884645"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 52, "lat": "10.499085", "nombre": "HOTEL ATL\u00c1NTIDA", "zona": "LOS CAOBOS", "phasta": 3980, "precio": 1, "pdsd": 2400, "long": "-66.884595"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 53, "lat": "10.380263", "nombre": "HOTEL PANORAMA", "zona": "CARRETERA PANAMERICANA", "phasta": 4500, "precio": 1, "pdsd": 1950, "long": "-66.965843"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 54, "lat": "10.494209", "nombre": "HOTEL EL MARQU\u00c9S", "zona": "LA URBINA", "phasta": 9700, "precio": 1, "pdsd": 4400, "long": "-66.808636"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 55, "lat": "10.495579", "nombre": "HOTEL LINCOLN SUITES", "zona": "SABANA GRANDE", "phasta": 9700, "precio": 1, "pdsd": 4700, "long": "-66.877805"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 56, "lat": "10.495666", "nombre": "HOTEL PLAZA PALACE", "zona": "SABANA GRANDE", "phasta": 6400, "precio": 1, "pdsd": 3200, "long": "-66.873205"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 57, "lat": "10.498335", "nombre": "HOTEL PLAZA VENEZUELA", "zona": "PLAZA VENEZUELA", "phasta": 5500, "precio": 1, "pdsd": 3500, "long": "-66.885031"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 58, "lat": "10.498966", "nombre": "HOTEL LA MONCLOA", "zona": "LA CAMPI\u00d1A", "phasta": 8900, "precio": 1, "pdsd": 4900, "long": "-66.871313"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 59, "lat": "10.487181", "nombre": "HOTEL RIAZOR", "zona": "EL ROSAL", "phasta": 5500, "precio": 1, "pdsd": 2200, "long": "-66.863089"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 60, "lat": "10.504790", "nombre": "HOTEL ALEX", "zona": "LA CANDELARIA", "phasta": 18500, "precio": 1, "pdsd": 7600, "long": "-66.905765"}, {"tipo_de_cobro": "Por hora", "estr": 1, "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", "cat_num": 2, "id": 61, "lat": "10.493650", "nombre": "HOTEL GABIAL", "zona": "PLAZA VENEZUELA", "phasta": 3900, "precio": 1, "pdsd": 1500, "long": "-66.881293"}]'
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
