# Construye los botones que se muestran debajo de una imagen aleatoria
import sys
from BotTelegram.enviar_mensajes_usuario import parsear_xml_object


SET_UPPER_TEXT = "SetUpperText"
SET_LOWER_TEXT = "SetLowerText"
SET_COLOR_TEXT = "SetColorText"

## Construye un link hacia la imagen que referencia un boton tal como /create o /next
def construir_link_image(imagen):
    link_image = str(imagen.pk)

    if sys.getsizeof(link_image) > 64:
        link_image = ""

    return link_image


# Construye los botones que se muestran debajo de una imagen aleatoria
# /random o boton:[Random]
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
                ],[
                    {
                        "text": "Next",
                        "callback_data": "Next,"  + link_image,
                    },
                ],[
                    {
                        "text": "Create",
                        "callback_data": "Create," + link_image,
                    }
                ],
            ]
    }

    return mark_keyboard

## Construye los botones que se muestran debajo de una imagen producto de /create o Boton:[Create]
def construir_callbackbuttons_create(xml_string):

    mark_keyboard = {
        "inline_keyboard":
            [
                [
                    {
                        "text": parsear_xml_object(xml_string.find("change_upper_text"))["text"],
                        "callback_data": SET_UPPER_TEXT + ","
                    }
                ], [
                {
                        "text": parsear_xml_object(xml_string.find("change_lower_text"))["text"],
                        "callback_data": SET_LOWER_TEXT + ","
                    },
            ], [
                {
                        "text": parsear_xml_object(xml_string.find("change_color"))["text"],
                        "callback_data": SET_COLOR_TEXT + ",",
                    }
                ],
            ]
    }

    return mark_keyboard
