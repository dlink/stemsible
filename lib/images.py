import os
from PIL import Image
from vlib import conf
from encryptint import encrypt_int

THUMBNAIL_SIZE = (200, 200)
config = conf.getInstance()


def _getImageFile(user_id):
    filename = '{}.jpg'.format(encrypt_int(user_id))
    path = os.path.join(config.basedir, 'web', 'uploads', filename)
    return filename, path


def getUserImage(user_id):
    filename, path = _getImageFile(user_id)
    if os.path.exists(path):
        return 'uploads/{}'.format(filename)
    return 'images/generic_icon.png'


def saveUserImage(user_id, image_file):
    filename, path = _getImageFile(user_id)
    image = Image.open(image_file)
    image.thumbnail(THUMBNAIL_SIZE)
    image.save(path, 'JPEG', quality=85)
