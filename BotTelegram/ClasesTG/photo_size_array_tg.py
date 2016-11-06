
#This object represents one size of a photo or a file / sticker thumbnail.
class PhotoSize:

    def __init__(self,dict_photo_size):

        self.file_id = dict_photo_size['file_id']
        self.width = dict_photo_size['width']
        self.height = dict_photo_size['height']
        self.file_size = dict_photo_size.get('file_size',-1)

    def __str__(self):

        return "< file_id: " + str(self.file_id) + \
               " , < " + str(self.width) +  ", " + str(self.height)  + " : " + str(self.file_size) + " >"

class PhotoSizeArray:

    def __init__(self, array_string):

        self.photos_size = []
        for ps in array_string:
            self.photos_size.append(PhotoSize(ps))

    def maximo_tam(self):
        if not self.photos_size: return None

        maximo = self.photos_size[0]
        for ps in self.photos_size:
            if ps.file_size > maximo.file_size:
                maximo = ps

        return maximo
