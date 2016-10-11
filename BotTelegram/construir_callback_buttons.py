# Construye los botones que se muestran debajo de una imagen aleatoria
import sys
from BotTelegram.enviar_mensajes_usuario import parsear_xml_object

def construir_link_imagen_borrador(imagen_borrador):
    link_image = str(imagen_borrador.pk)

    if sys.getsizeof(link_image) > 64:
        link_image = ""

    return link_image

def construir_link_image(imagen):
    link_image = str(imagen.pk)

    if sys.getsizeof(link_image) > 64:
        link_image = ""

    return link_image


# Construye los botones que se muestran debajo de una imagen aleatoria
def construir_callback_buttons(imagen):

    link_image = construir_link_image(imagen)

    mark_keyboard = {
        "inline_keyboard":
            [
                [
                    {
                        "text": "Random",
                        "callback_data": "Random"
                    }
                    ,
                    {
                        "text": "Next",
                        "callback_data": "Next,"  + link_image,
                    }
                ],
                [
                    {
                        "text": "Create",
                        "callback_data": "Create," + link_image,
                    }
                ],
            ]
    }

    return mark_keyboard

def construir_callbackbuttons_create(datos_imagen_borrador, xml_string):

    #link_image = construir_link_imagen_borrador(datos_imagen_borrador)

    mark_keyboard = {
        "inline_keyboard":
            [
                [
                    {
                        "text": parsear_xml_object(xml_string.find("change_upper_text"))["text"],
                        "callback_data": "SetUpperText,"
                    }
                    ,
                    {
                        "text": parsear_xml_object(xml_string.find("change_lower_text"))["text"],
                        "callback_data": "SetLowerText,"
                    }
                ],
                [
                    {
                        "text": parsear_xml_object(xml_string.find("change_color"))["text"] +
                                +str(datos_imagen_borrador.color),
                        "callback_data": "SetColor,",
                    }
                ],
            ]
    }

    return mark_keyboard
