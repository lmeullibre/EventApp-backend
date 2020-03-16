from database import db
from database.models import User
from datetime import datetime
from api.utils import decode_image, upload_image_gcp


def add_user(data):
    name = data.get('name')
    mail = data.get('mail')
    photo = data.get('photo')
    birth_date = datetime.strptime(data.get('birth_date'), "%Y-%m-%dT%H:%M:%S.%fZ")
    password = data.get('password')
    bio = data.get('bio')
    telephone = data.get('telephone')
    instagram = data.get('instagram')

    image_path = decode_image(photo)
    if image_path is not None:
        photo_url = upload_image_gcp(image_path)
    else:
        photo_url = photo

    new_user = User(name, mail, photo_url, birth_date, password, bio, telephone, instagram)
    db.session.add(new_user)
    db.session.commit()


def update_user(id, data):
    user = User.query.get(id)
    if data.get('name') is not None:
        user.name = data.get('name')
    if data.get('mail') is not None:
        user.mail = data.get('mail')
    if data.get('photo') is not None:
        user.photo = data.get('photo')
    if data.get('birth_date') is not None:
        user.birth_date = datetime.strptime(data.get('birth_date'), "%Y-%m-%dT%H:%M:%S.%fZ")
    if data.get('bio') is not None:
        user.bio = data.get('bio')
    if data.get('telephone') is not None:
        user.telephone = data.get('telephone')
    if data.get('instagram') is not None:
        user.instagram = data.get('instagram')

    db.session.add(user)
    db.session.commit()


def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user
