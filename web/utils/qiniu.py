from qiniu import Auth, put_stream, etag, BucketManager
import qiniu.config
from django.conf import settings
import uuid

access_key = settings.QINIU['ACCESS_KEY']
secret_key = settings.QINIU['SECRET_KEY']
bucket_name = settings.QINIU['BUCKET']

#构建鉴权对象
q = Auth(access_key, secret_key)

def upload(key, file_obj, filename, filesize):
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_stream(token, key, file_obj, filename, filesize)
    return ret, info

def get_token(key):
    token = q.upload_token(bucket_name, key, 3600)
    return token

def delete_file(key):
    #初始化BucketManager
    bucket = BucketManager(q)
    #删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    return ret, info