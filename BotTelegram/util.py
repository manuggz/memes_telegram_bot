# Separa el texto enviado por el usuario en la forma "comando resto"
# Ejemplo:
# "/comando ASDASd"
# regresa ("comando","ASDASd")
#
# "/comando@MemesBot Test - Test , Red"
# regresa ("comando","Test - Test , Red")
#
# "yao ming"
# regresa ("yao ming","")
def extraer_comando(text):
    if not text: return ("","")

    text = text.strip()
    comando = ""

    for i in range(0, len(text)):

        if (text[0] == "/" and text[i] == ' '): return (comando, text[i + 1:])

        if text[i] == '@' and text[i:i + len("MemesBot")]:
            return (comando, text[i + len("MemesBot") + 1:])

        comando += text[i]

    return (comando, "")
