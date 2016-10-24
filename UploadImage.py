from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

access_key = '7E1ZYNajHehnCRrBAutgcdz3Q5T4_2bgxXq8_TnB'
secret_key = 'gm-Wbv8-N5NanZS-l2CuKiYvChCfBA4Evzv8DhIE'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'lxctest'

#上传到七牛后保存的文件名
key = 'my-python-logo.png';

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = './小小荔枝_广州市/56.jpg'

ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
