from django.shortcuts import render,HttpResponse
import json
import base64
import os
# Create your views here.

def index(request):

    if request.method == 'GET':

        return render(request,'index.html')

def transfer(request):
    if request.method=='GET':

        style = request.GET.get('style')

        return render(request,'transfer.html',{'style':style})

    if request.method=='POST':
        image_base64 = request.POST.get('base64')
        index = image_base64.find(',')
        image_base64 = image_base64[index+1:]
        image_data = base64.b64decode(image_base64)
        file = open('upload_content_images/content.jpg','wb')
        file.write(image_data)
        file.close()
        style = request.POST.get('style')
        os.system('python transfer_image.py infer --style_image_path=style_image/{style}.jpg --test_images_path=upload_content_images/content.jpg'.format(style=style))
        with open("output/content.jpg", "rb") as f:  # 转为二进制格式
            base64_data = base64.b64encode(f.read())  # 使用base64进行加密
            base64_data = 'data:image/jpeg;base64,'+str(base64_data)[2:]
        print(base64_data)
        return HttpResponse(json.dumps({'base64_data':base64_data}))


def test(request):
    if request.method=='GET':

        return render(request,'shangchuan.html')