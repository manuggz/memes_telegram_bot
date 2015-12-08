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
moteles_json_texto ='''[
    {
        "zona": "LOS CAOBOS", 
        "phasta": 3300, 
        "precio": 1, 
        "pdsd": 1500, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538615/HOTEL_NILSON_abuc9c.jpg", 
        "nombre": "HOTEL NILSON", 
        "id": 51
    }, 
    {
        "zona": "LOS CAOBOS", 
        "phasta": 3980, 
        "precio": 1, 
        "pdsd": 2400, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL ATL\u00c1NTIDA", 
        "id": 52
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 8000, 
        "precio": 2, 
        "pdsd": 3100, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538595/HOTEL_COLISEO_gsmojh.jpg", 
        "nombre": "HOTEL COLISEO", 
        "id": 10
    }, 
    {
        "zona": "LA CASTELLANA", 
        "phasta": 7500, 
        "precio": 2, 
        "pdsd": 3300, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL EL CID", 
        "id": 19
    }, 
    {
        "zona": "CHACA\u00cdTO", 
        "phasta": 12300, 
        "precio": 2, 
        "pdsd": 5200, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL CHACAO CUMBERLAND", 
        "id": 49
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 6400, 
        "precio": 2, 
        "pdsd": 3200, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL PLAZA PALACE", 
        "id": 56
    }, 
    {
        "zona": "QUINTA CRESPO", 
        "phasta": 3500, 
        "precio": 1, 
        "pdsd": 1700, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538644/HOTEL_LIDER_wmokdo.jpg", 
        "nombre": "HOTEL LIDER", 
        "id": 7
    }, 
    {
        "zona": "LA CASTELLANA", 
        "phasta": 6400, 
        "precio": 1, 
        "pdsd": 2300, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL PENT HOUSE", 
        "id": 20
    }, 
    {
        "zona": "CARRETERA PANAMERICANA", 
        "phasta": 4900, 
        "precio": 1, 
        "pdsd": 2400, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "MOTEL CANAIMA", 
        "id": 28
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 9900, 
        "precio": 1, 
        "pdsd": 1700, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL ALLADIN", 
        "id": 30
    }, 
    {
        "zona": "LA URBINA", 
        "phasta": 9900, 
        "precio": 1, 
        "pdsd": 2100, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538548/HOTEL_MEDITERRANEO_ghtha5.jpg", 
        "nombre": "HOTEL MEDITERRANEO", 
        "id": 46
    }, 
    {
        "zona": "LA PAZ", 
        "phasta": 4000, 
        "precio": 1, 
        "pdsd": 1200, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449546854/DAKOTA_SUITES_HOTEL_orswxh.jpg", 
        "nombre": "DAKOTA SUITES HOTEL", 
        "id": 3
    }, 
    {
        "zona": "LAS MERCEDES", 
        "phasta": 3500, 
        "precio": 1, 
        "pdsd": 1200, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL NOSTRUM", 
        "id": 14
    }, 
    {
        "zona": "EL PARA\u00cdSO", 
        "phasta": 5000, 
        "precio": 1, 
        "pdsd": 1500, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538607/HOTEL_RAMO_BLANCO_hcwvq2.jpg", 
        "nombre": "HOTEL RAMO BLANCO ", 
        "id": 4
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 1200, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL RORA", 
        "id": 13
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 13800, 
        "precio": 2, 
        "pdsd": 4300, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538641/HOTEL_CARACAS_CUMBERLAND_vgmqcx.jpg", 
        "nombre": "HOTEL CARACAS CUMBERLAND", 
        "id": 31
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 9850, 
        "precio": 2, 
        "pdsd": 3500, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538565/HOTEL_KING_S_hfbl4s.jpg", 
        "nombre": "HOTEL KING\u00b4S", 
        "id": 47
    }, 
    {
        "zona": "LA CAMPI\u00d1A", 
        "phasta": 8900, 
        "precio": 2, 
        "pdsd": 4900, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL LA MONCLOA", 
        "id": 58
    }, 
    {
        "zona": "CHACAO", 
        "phasta": 4100, 
        "precio": 1, 
        "pdsd": 1500, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL GIOLY", 
        "id": 18
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 3700, 
        "precio": 1, 
        "pdsd": 1200, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL REMA", 
        "id": 17
    }, 
    {
        "zona": "LAS PALMAS", 
        "phasta": 3400, 
        "precio": 1, 
        "pdsd": 1550, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538570/HOTEL_LA_SALLE_tjipkf.jpg", 
        "nombre": "HOTEL LA SALLE", 
        "id": 50
    }, 
    {
        "zona": "QUINTA CRESPO", 
        "phasta": 3500, 
        "precio": 1, 
        "pdsd": 900, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538669/HOTEL_42_ocopma.jpg", 
        "nombre": "HOTEL 42", 
        "id": 6
    }, 
    {
        "zona": "EL PARA\u00cdSO", 
        "phasta": 3000, 
        "precio": 1, 
        "pdsd": 900, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538593/HOTEL_IMPERIO_kud46i.jpg", 
        "nombre": "HOTEL IMPERIO ", 
        "id": 1
    }, 
    {
        "zona": "LOS CAOBOS", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 1950, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538557/HOTEL_LIMA_jf6uzu.jpg", 
        "nombre": "HOTEL LIMA", 
        "id": 38
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 3200, 
        "precio": 1, 
        "pdsd": 1100, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538620/HOTEL_EDU_MOTO-HOTEL_i30xcx.jpg", 
        "nombre": "HOTEL EDU (MOTO-HOTEL)", 
        "id": 42
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 2000, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538554/HOTEL_MADRID_vrkkvh.jpg", 
        "nombre": "HOTEL MADRID", 
        "id": 41
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 2700, 
        "precio": 1, 
        "pdsd": 700, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538674/HOTEL_YARE_g2yy0f.jpg", 
        "nombre": "HOTEL YARE", 
        "id": 48
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 8900, 
        "precio": 1, 
        "pdsd": 2350, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538658/HOTEL_SAVOY_pyex2n.jpg", 
        "nombre": "HOTEL SAVOY", 
        "id": 36
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 5500, 
        "precio": 1, 
        "pdsd": 2200, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL RIAZOR", 
        "id": 59
    }, 
    {
        "zona": "CARRETERA PANAMERICANA", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 1950, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL PANORAMA", 
        "id": 53
    }, 
    {
        "zona": "LA URBINA", 
        "phasta": 9700, 
        "precio": 2, 
        "pdsd": 4400, 
        "cat_num": 1, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL EL MARQU\u00c9S", 
        "id": 54
    }, 
    {
        "zona": "EL PARA\u00cdSO", 
        "phasta": 7000, 
        "precio": 1, 
        "pdsd": 2500, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "LEXINGTON SUITES HOTEL", 
        "id": 2
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 5300, 
        "precio": 1, 
        "pdsd": 2300, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538611/HOTEL_BEETHOVEN_tipvvx.jpg", 
        "nombre": "HOTEL BEETHOVEN", 
        "id": 9
    }, 
    {
        "zona": "ALTAMIRA", 
        "phasta": 6700, 
        "precio": 2, 
        "pdsd": 3500, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538635/HOTEL_LA_FLORESTA_nigsma.jpg", 
        "nombre": "HOTEL LA FLORESTA", 
        "id": 45
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 9700, 
        "precio": 2, 
        "pdsd": 4700, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL LINCOLN SUITES", 
        "id": 55
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 12600, 
        "precio": 2, 
        "pdsd": 3450, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538590/HOTEL_PRESIDENT_dmsy8s.jpg", 
        "nombre": "HOTEL PRESIDENT", 
        "id": 34
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 9900, 
        "precio": 2, 
        "pdsd": 4900, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538657/HOTEL_TAMPA_vknrri.jpg", 
        "nombre": "HOTEL TAMPA", 
        "id": 44
    }, 
    {
        "zona": "CHACA\u00cdTO", 
        "phasta": 10500, 
        "precio": 2, 
        "pdsd": 4400, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538637/HOTEL_BROADWAY_byf4ux.jpg", 
        "nombre": "HOTEL BROADWAY", 
        "id": 43
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 5500, 
        "precio": 1, 
        "pdsd": 2100, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL GILMAR", 
        "id": 15
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 5500, 
        "precio": 2, 
        "pdsd": 3500, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538565/HOTEL_PLAZA_VENEZUELA_muoe6p.jpg", 
        "nombre": "HOTEL PLAZA VENEZUELA", 
        "id": 57
    }, 
    {
        "zona": "CHACAO", 
        "phasta": 19800, 
        "precio": 3, 
        "pdsd": 6500, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538582/HOTEL_SHELTER_SUITES_a1avjy.jpg", 
        "nombre": "HOTEL SHELTER SUITES", 
        "id": 37
    }, 
    {
        "zona": "LA CANDELARIA", 
        "phasta": 18500, 
        "precio": 3, 
        "pdsd": 7600, 
        "cat_num": 2, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL ALEX", 
        "id": 60
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 2000, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538630/HOTEL_HARMONY_rjpjbk.jpg", 
        "nombre": "HOTEL HARMONY ", 
        "id": 8
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 5850, 
        "precio": 1, 
        "pdsd": 1900, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538565/HOTEL_MEREY_v6rukw.jpg", 
        "nombre": "HOTEL MEREY", 
        "id": 23
    }, 
    {
        "zona": "EL PARA\u00cdSO", 
        "phasta": 3900, 
        "precio": 1, 
        "pdsd": 1650, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538580/HOTEL_NACIONES_UNIDAS_ga9e78.jpg", 
        "nombre": "HOTEL NACIONES UNIDAS", 
        "id": 29
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 4300, 
        "precio": 1, 
        "pdsd": 1500, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538659/HOTEL_EMBASSY_SUITES_kxsezr.jpg", 
        "nombre": "HOTEL EMBASSY SUITES", 
        "id": 32
    }, 
    {
        "zona": "PLAZA VENEZUELA", 
        "phasta": 3900, 
        "precio": 1, 
        "pdsd": 1500, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL GABIAL", 
        "id": 61
    }, 
    {
        "zona": "LA YAGUARA", 
        "phasta": 6700, 
        "precio": 1, 
        "pdsd": 2350, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449546852/MOTEL_VILLA_SUITES_ts6yfe.jpg", 
        "nombre": "MOTEL VILLA SUITES", 
        "id": 27
    }, 
    {
        "zona": "LA CASTELLANA", 
        "phasta": 4500, 
        "precio": 1, 
        "pdsd": 2200, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL TRINI", 
        "id": 21
    }, 
    {
        "zona": "EL BOSQUE", 
        "phasta": 7600, 
        "precio": 1, 
        "pdsd": 2450, 
        "cat_num": 3, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538659/HOTEL_LA_TOJA_ejyldr.jpg", 
        "nombre": "HOTEL LA TOJA", 
        "id": 22
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 12000, 
        "precio": 2, 
        "pdsd": 3300, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL AMERICAN DALLAS", 
        "id": 12
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 8200, 
        "precio": 2, 
        "pdsd": 3750, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL DALLAS", 
        "id": 16
    }, 
    {
        "zona": "LOS RU\u00cdCES (SUR)", 
        "phasta": 10100, 
        "precio": 2, 
        "pdsd": 3500, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538654/HOTEL_DALLAS_SUITES_mixrz3.jpg", 
        "nombre": "HOTEL DALLAS SUITES", 
        "id": 25
    }, 
    {
        "zona": "CALIFORNIA (SUR)", 
        "phasta": 18700, 
        "precio": 2, 
        "pdsd": 4300, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538613/HOTEL_CALIFORNIA_SUITES_hkzhlc.jpg", 
        "nombre": "HOTEL CALIFORNIA SUITES", 
        "id": 39
    }, 
    {
        "zona": "LA YAGUARA", 
        "phasta": 22000, 
        "precio": 2, 
        "pdsd": 4900, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538664/HOTEL_DUBAI_SUITES_rkejww.jpg", 
        "nombre": "HOTEL DUBAI SUITES", 
        "id": 40
    }, 
    {
        "zona": "PETARE", 
        "phasta": 17600, 
        "precio": 1, 
        "pdsd": 1900, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538561/HOTEL_MONTAA_SUITES_yv7ool.jpg", 
        "nombre": "HOTEL MONTA\u00d1A SUITES", 
        "id": 33
    }, 
    {
        "zona": "EL PARA\u00cdSO", 
        "phasta": 8000, 
        "precio": 2, 
        "pdsd": 2700, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449546853/NOVO_HOTEL_EXPRESS_kqxdfx.jpg", 
        "nombre": "NOVO HOTEL EXPRESS", 
        "id": 5
    }, 
    {
        "zona": "SABANA GRANDE", 
        "phasta": 14000, 
        "precio": 3, 
        "pdsd": 5500, 
        "cat_num": 5, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL LAS AMERICAS", 
        "id": 11
    }, 
    {
        "zona": "ALTAMIRA", 
        "phasta": 21000, 
        "precio": 3, 
        "pdsd": 7600, 
        "cat_num": 5, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "THE VIP HOTEL", 
        "id": 62
    }, 
    {
        "zona": "BELLO MONTE", 
        "phasta": 19000, 
        "precio": 3, 
        "pdsd": 8500, 
        "cat_num": 5, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://res.cloudinary.com/manuggz/image/upload/v1449538626/HOTEL_MONTPARK_lz37kg.jpg", 
        "nombre": "HOTEL MONTPARK", 
        "id": 24
    }, 
    {
        "zona": "EL ROSAL", 
        "phasta": 22000, 
        "precio": 3, 
        "pdsd": 7500, 
        "cat_num": 5, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "THE HOTEL", 
        "id": 35
    }, 
    {
        "zona": "CARRETERA PANAMERICANA", 
        "phasta": 15500, 
        "precio": 3, 
        "pdsd": 6500, 
        "cat_num": 4, 
        "tipo_de_cobro": "Por horas", 
        "estr": 3, 
        "foto": "http://www.wannafly.hk/images/mgthumbnails/751x394-images-HRH_4.jpg", 
        "nombre": "HOTEL BOSQUE DORADO", 
        "id": 26
    }
]'''

moteles = json.loads(moteles_json_texto)

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
