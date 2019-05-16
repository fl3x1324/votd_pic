import requests
import boto3
from os import environ
from datetime import datetime
import json
import re

yvApiKey = environ.get('YV_API_KEY')
yvApiBaseUrl = 'https://developers.youversionapi.com/1.0'

s3 = boto3.resource('s3')


def votd_fetch_kjv(object, context):
    headers = {'accept': 'application/json',
               'x-youversion-developer-token': yvApiKey}
    day_of_year = datetime.now().timetuple().tm_yday
    response = requests.get(yvApiBaseUrl + '/verse_of_the_day/' +
                            str(day_of_year) + '?version_id=1', headers=headers)
    payload = response.content.decode('utf-8')
    if response.status_code == 200:
        # print(payload)
        img_url = re.search('http.+', json.loads(payload)
                            ['image']['url']).group(0)
        print(img_url)
        print('Day: ' + str(day_of_year))
        img_req_headers = {'accept': 'image/jpeg'}
        img_response = requests.get(img_url, img_req_headers)
        file_name = str(day_of_year) + '/' + 'votd.jpg'
        bucket_name = 'votd-img'
        votd_upload_image(file_name, bucket_name, img_response.content)


def votd_upload_image(file_name, bucket_name, data):
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=data)

votd_fetch_kjv(None, None)
