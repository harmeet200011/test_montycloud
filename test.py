import requests
from PIL import Image
import io
import base64


def upload():
    with open('image.jpg', 'rb') as file:
        image_data = file.read()
    image_data_base64 = base64.b64encode(image_data).decode('utf-8')

    headers = {'Content-Type': 'application/json', "upload_image": "try", "download_image": "", "download_thumbnail": ""}

    response = requests.post('https://1j88hjvlk9.execute-api.ap-south-1.amazonaws.com/default/mythumbnailimage1', data=image_data_base64, headers=headers)
    print(response.json())



def download_image():
    headers_thumb = {'Content-Type': 'image/jpeg', "upload_image": "", "download_image": "try", "download_thumbnail": ""}

    response = requests.get('https://1j88hjvlk9.execute-api.ap-south-1.amazonaws.com/default/mythumbnailimage1',
                             headers=headers_thumb)
    if response.status_code == 200:
        # Get the image data from the response
        image_data_base64 = response.content

        # Decode the base64-encoded image data
        image_data = base64.b64decode(image_data_base64)

        # Create an Image object from the image data
        image = Image.open(io.BytesIO(image_data))

        # Display the image (optional)
        image.show()

        # Save the image to a file (optional)
        image.save('downloaded.jpg', format='JPEG')


def generate_view_thumbnail():
    headers_thumb = {'Content-Type': 'image/jpeg', "upload_image": "", "download_image": "", "download_thumbnail": "try"}

    response = requests.get('https://1j88hjvlk9.execute-api.ap-south-1.amazonaws.com/default/mythumbnailimage1',
                             headers=headers_thumb)
    if response.status_code == 200:
        # Get the image data from the response
        image_data_base64 = response.content

        # Decode the base64-encoded image data
        image_data = base64.b64decode(image_data_base64)

        # Create an Image object from the image data
        image = Image.open(io.BytesIO(image_data))

        # Display the image (optional)
        image.show()

        # Save the image to a file (optional)
        image.save('downloaded_thumb.jpg', format='JPEG')


if __name__ =="__main__":
    download_image()