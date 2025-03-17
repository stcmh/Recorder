import cv2 as cv

video_file = 'http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8'

# Read the given video file
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given video, ' + video_file

fps = 30
wait_msec = int(1000 / fps)
is_recording = False
out = None
flip_horizontal = False
overlay_image = cv.imread('button.png')
overlay_resized = cv.resize(overlay_image, (25, 25))

while True:
    # Get an image from 'video' 
    valid, img = video.read()
    if not valid:
        break

    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
   
    x, y = 50, 50    
   
    # Show the image
    frame = int(video.get(cv.CAP_PROP_POS_FRAMES))
    
    if flip_horizontal:
        img = cv.flip(img, 1) 
            
    # 녹화 중이면 비디오 저장
    if is_recording:
        if out is None:
            # 녹화 파일 이름 설정
            fourcc = cv.VideoWriter_fourcc(*'MJPG')
            out = cv.VideoWriter('output.avi', fourcc, fps, (int(video.get(3)), int(video.get(4))))
            
        out.write(img)
        # 녹화 중 버튼 표시
        img[y:y+overlay_resized.shape[0], x:x+overlay_resized.shape[1]] = overlay_resized
   
    # 화면에 영상 출력
    cv.imshow('Video Player', img)

    # Process the key event
    key = cv.waitKey(max(int(wait_msec / 1), 1))
    
    if key == ord(' '): 
        is_recording = not is_recording
        if is_recording:
            print("녹화 중")
            
        else:
            print("녹화 종료")
            if out is not None:
                out.release()
                out = None
                
    if key == 44 or key == 46: # , or . key
        flip_horizontal = not flip_horizontal
        
    if key == 27:  # exit
        break

# 종료 후 파일 닫기
if out is not None:
    out.release()

video.release()
cv.destroyAllWindows()
