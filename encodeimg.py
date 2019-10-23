from base64 import b64encode
from base64 import b64decode
import boto3
import json
import decimal
import os
import datetime
import base64
import urllib

try:
    stri="https://www.google.co.in"
    data=urllib.urlopen(stri)
    print("Connected")
    os.system("sudo omxplayer -o local internet.mp3")
except:
    print("Not connected")
    os.system("sudo omxplayer -o local ntconnection.mp3")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Get the service resource.
dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIAI7CLBFF6JOOGVTAQ',
    aws_secret_access_key='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',region_name='us-east-1')
rekognition = boto3.client("rekognition",aws_access_key_id='AKIAI7CLBFF6JOOGVTAQ',
    aws_secret_access_key='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',region_name='us-east-1')
client = boto3.client("sns",aws_access_key_id="AKIAI7CLBFF6JOOGVTAQ",
    aws_secret_access_key="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",region_name="us-east-1")
client_1 = boto3.client('s3',aws_access_key_id='AKIAI7CLBFF6JOOGVTAQ',
    aws_secret_access_key='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')

path="/home/pi/AWS_Cloud/main_code/"
table = dynamodb.Table('Regiusers')
pe="Image,username"
response = table.scan(
    ProjectionExpression=pe,
    )
res=[]
for i in response['Items']:
    res.append(json.dumps(i,cls=DecimalEncoder))

threshold=80
bucket_name='bucketwce002'
#src_image='dips3.jpg'
print("Now be ready your image will be captured by Camera")
os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/speech.mp3")
t = datetime.datetime.now()
data=t.strftime("%H_%M_%S")
os.system("sudo fswebcam -r 640X480  --no-banner --save /home/pi/AWS_Cloud/main_code/{}.jpg".
          format(data))
print("Image captured: "+data)
src_image=''+path+'{}.jpg'.format(data)
print(src_image)

source_bytes = open(src_image,'rb')
response=rekognition.detect_faces(Image={'Bytes':source_bytes.read()},Attributes=['ALL'])
source_bytes.close()
    

if response['FaceDetails']==[]:
    print("Face Not Detected")
    os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/notdetected.mp3")


    
while not response['FaceDetails']:
    print("Capture Image")
    #time.sleep(30)
    os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/speech.mp3")
    print("Now be ready your image will be captured by Camera")
    t = datetime.datetime.now()
    data=t.strftime("%H_%M_%S")
    os.system("sudo fswebcam -r 640X480  --no-banner --save /home/pi/AWS_Cloud/main_code/{}.jpg".format(data))
    src_image=''+path+'{}.jpg'.format(data)
    #print(data)
    #print("Image captured: "+data)
    source_bytes = open(src_image,'rb')
    response=rekognition.detect_faces(Image={'Bytes':source_bytes.read()},Attributes=['ALL'])
    source_bytes.close()

print("Suceess in Capture")
os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/captured.mp3")


client_1.upload_file(src_image,bucket_name,src_image,ExtraArgs={'ACL':'public-read'})
simi_list=[]
for i in range(len(res)):
    j=json.loads(res[i])
    re_data=j['Image']['B']
    re_user=j['username']
    t = datetime.datetime.now()
    data=t.strftime("%H-%M-%S")
    tar_image=''+path+'{}.jpg'.format(data)
    fh=open(tar_image,"wb")
    fh.write(re_data.decode('base64'))
    fh.close()
    #tar_image=b64decode(re_data)
    #print(tar_image)
    source_bytes = open(src_image, 'rb')
    target_bytes = open(tar_image, 'rb')

    response1 = rekognition.compare_faces(
       SourceImage = {
        'Bytes':source_bytes.read()
    },
    TargetImage = {
        'Bytes':target_bytes.read()
    }
       )
    source_bytes.close()
    target_bytes.close()
    os.remove(tar_image)
    source_face=response1['SourceImageFace']
    matches=response1['FaceMatches']
    for match in matches:
        print "Target Face ({Confidence}%)".format(**match['Face'])
        print "  Similarity : {}%".format(match['Similarity'])
        simi=match['Similarity']
        simi_list.append([simi,tar_image,re_user])

os.remove(src_image)



print(simi_list)
if simi_list==[]:
    url = '{}/{}/{}'.format(client_1.meta.endpoint_url,'bucketwce002',src_image)
    print(url)
    client.publish(
        PhoneNumber="+918459445789",
        Message="Hi someone is at your door :"+url,
        )
    
    

    
'''print(max(simi_list))
eg=max(simi_list)
if not eg:
    url = '{}/{}/{}'.format(client.meta.endpoint_url,'bucketwce002',src_image)
    print(url)
    client.publish(
        PhoneNumber="+918888149815",
        Message="Hi someone is at your door"+"url",
        )  
    '''
if simi_list:
    match_username=max(simi_list)
    print(match_username[2])
    u_name=match_username[2]
    simi_val=match_username[0]
    if simi_val:
        os.system("sudo omxplayer -o local welcome.mp3")
        client.publish(
            PhoneNumber="+918459445789",
            Message="Hi"+" "+u_name+" is at your door",
            )
    else:
        url = '{}/{}/{}'.format(client_1.meta.endpoint_url,'bucketwce002',src_image)
        print(url)
        client.publish(
            PhoneNumber="+918459445789",
            Message="Hi someone is at your door"+"url",
            )  

#url = '{}/{}/{}'.format(client.meta.endpoint_url,'bucketwce002','dips1.jpg')





