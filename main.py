import json
import boto3
from PIL import Image
import io
import base64

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Check if the event is for an image upload or thumbnail generation
    print(event,"################################")
    # this api for image uplaod
    if event.get('headers', {}).get('upload_image', ''):
        # Image Upload
        image_data_ = event['body']
        image_data = base64.b64decode(image_data_)
        image_name = event['headers']['upload_image']
        # Upload the image to the S3 bucket
        s3_client.put_object(Bucket='mythumbnailimage1', Key=image_name, Body=image_data)

        return {
            'statusCode': 200,
            'body': json.dumps('Image uploaded successfully! with name {0} '.format(image_name))
        }

    if event.get('headers', {}).get('download_image', ''):
        image_name = event['headers']['download_image']
        image_obj = s3_client.get_object(Bucket='mythumbnailimage1', Key=image_name)
        image_data = image_obj['Body'].read()
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        img_obj = io.BytesIO()
        image.save(img_obj, format='JPEG')

        headers = {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename="{image_name}"',
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': base64.b64encode(img_obj.getvalue()).decode('utf-8'),
            'isBase64Encoded': True
        }
    if event.get('headers', {}).get('download_thumbnail', ''):
        # Thumbnail Generation
        # Get the image name from the event payload
        image_name = event['headers']['download_thumbnail']

        # Download the original image from S3
        image_obj = s3_client.get_object(Bucket='mythumbnailimage1', Key=image_name)
        image_data = image_obj['Body'].read()
        print(image_data)
        image = Image.open(io.BytesIO(image_data))
        thumbnail_size = (100, 100)
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail(thumbnail_size)
        thumbnail_image = thumbnail_image.convert('RGB')

        # Upload the thumbnail to S3
        thumbnail_image_obj = io.BytesIO()
        thumbnail_image.save(thumbnail_image_obj, format='JPEG')
        s3_client.put_object(Bucket='mythumbnailimage1', Key=f"thumbnails/{image_name}", Body=thumbnail_image_obj.getvalue())
        headers = {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename="{image_name}"',
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': base64.b64encode(thumbnail_image_obj.getvalue()).decode('utf-8'),
            'isBase64Encoded': True
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request.')
        }
