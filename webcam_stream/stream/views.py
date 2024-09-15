# 뷰 정의! 웹캠 영상 처리 함수, 템플릿 렌더링 함수 포함
import cv2
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
from django.shortcuts import render
import random

def get_frame():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1) 

        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def live_stream(request):
    return StreamingHttpResponse(get_frame(), content_type="multipart/x-mixed-replace;boundary=frame")

def index(request):
    return render(request, 'stream/index.html')


def get_object_location(request):
    # 랜덤 좌표 생성 (예시로 X, Y는 640x640 캔버스 내의 좌표로 제한)
    x = random.randint(0, 640)
    y = random.randint(0, 640)
    
    # 좌표를 JSON 형식으로 반환
    return JsonResponse({'x': x, 'y': y})
