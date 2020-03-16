import settings
import boto3
import base64
import uuid
import re
import jwt


def decode_image(imgstring):
    filename = None
    base64_reg = r",(.*)"
    content_type_reg = r"(.*);"

    file = re.findall(base64_reg, imgstring, re.MULTILINE)
    content_type = re.findall(content_type_reg, imgstring, re.MULTILINE)

    try:
        content_type = content_type[0].split('/')
        type = content_type[0]
        extension = content_type[1]

        if type != 'data:image':
            print('error')
        else:
            imgdata = base64.b64decode(file[0])
            filename = './' + str(uuid.uuid4()) + '.' + extension
            with open(filename, 'wb') as f:
                f.write(imgdata)
    except Exception as e:
        print(str(e))
        return None

    return filename


def upload_image_gcp(img_path):

    client = boto3.client('s3', region_name='eu-central-1')
    client.upload_file(img_path, settings.IMAGE_BUCKET, str(uuid.uuid4()) + '.png', ExtraArgs={'ACL': 'public-read'})

    image_url = "https://pes-image-bucket.s3.eu-central-1.amazonaws.com/" + str(uuid.uuid4()) + '.png'

    return image_url


def get_id_form_token(token):
    decoded_token = jwt.decode(token, verify=False)
    print(decoded_token)
    return decoded_token['uid']
