import tkinter
import tkinter.filedialog
import tkinter.messagebox

import PIL
from PIL import ImageTk
from PIL import Image
import cv2
import numpy


# 이미지 서치 함수
def find_pic():
    file = tkinter.filedialog.askopenfilename(title="그림파일 찾아주는 요정", initialdir="/", filetypes = [("image files", "*.png")])
    if file == '':
        tkinter.messagebox.showwarning("경고", "파일을 추가 하세요")
    else:
        tkinter.messagebox.showinfo(title="선택된 이미지", message=file)
        ## 이미지 수정
        # 원본 이미지
        img_arr = numpy.fromfile(file, numpy.uint8)
        cur_img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        global selected_img
        selected_img = cur_img
        # 가로 세로
        height, width = cur_img.shape[:2]
        # 가로 대 세로의 비율이 8:3 이 기준
        # 가로가 길면
        if (height / width) > (3/8):
            param = 96/height
        # 세로가 길면
        else:
            param = 256/width
        # 사이즈가 바뀐 이미지
        resized_img = cv2.resize(cur_img, None, fx=param, fy=param, interpolation=cv2.INTER_AREA)
        # 색상 체계 변환
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        # tkinter 객체로 변환
        resized_img_arr = Image.fromarray(resized_img)
        imgtk = ImageTk.PhotoImage(image=resized_img_arr)
    
        # 이미지 라벨
        label_image.config(image=imgtk)
        label_image.image = imgtk
        
        # 이미지 변경 버튼 활성화
        rotate_button.config(state="active")
        rotate_button.state = "active"

        vertical_button.config(state="active")
        vertical_button.state = "active"

        horizontal_button.config(state="active")
        horizontal_button.state = "active"


# 이미지 회전 함수
def rotate_pic():
    # 저장되어 있는 이미지
    global selected_img
    img = selected_img
    # 가로 세로
    height, width = selected_img.shape[:2]
    # 틱 카운트 + 1
    global tick_count
    tick_count += 1
    # 회전
    M= cv2.getRotationMatrix2D((width/2, height/2), tick_count * -90, 1)
    dst = cv2.warpAffine(img, M,(width, height))
    # 가로 세로
    height, width = dst.shape[:2]
    # 가로 대 세로의 비율이 8:3 이 기준
    # 가로가 길면
    if (height / width) > (3/8):
        param = 96/height
    # 세로가 길면
    else:
        param = 256/width
    # 사이즈가 바뀐 이미지
    resized_img = cv2.resize(dst, None, fx=param, fy=param, interpolation=cv2.INTER_AREA)
    # 색상 체계 변환
    resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    global fixed_img
    fixed_img = resized_img
    # tkinter 객체로 변환
    resized_img_arr = Image.fromarray(resized_img)
    imgtk = ImageTk.PhotoImage(image=resized_img_arr)
    # 이미지 라벨
    label_final.config(image=imgtk)
    label_final.image = imgtk


# 이미지 위 아래 이동 함수
def move_vertical():
    # 이미지
    global fixed_img
    img = fixed_img
    # 가로 세로
    height, width = img.shape[:2]
    # 위로 이동
    M = numpy.float32([[1,0,0],[0,1,1]])
    dst = cv2.warpAffine(img, M,(width, height))
    fixed_img = dst
    # tkinter 객체로 변환
    resized_img_arr = Image.fromarray(dst)
    imgtk = ImageTk.PhotoImage(image=resized_img_arr)
    # 이미지 라벨
    label_final.config(image=imgtk)
    label_final.image = imgtk   


window=tkinter.Tk()

# 기본 설정
window.title("마비노기 그림대화 생성기 V 0.1.0")
window.geometry("400x600+100+100")
window.resizable(False, False)

# 기본 텍스트
label=tkinter.Label(window, text="그림 파일을 선택하세요", width=640)
label.pack()

## 이미지 선택
# 선택된 이미지
selected_img = None
# 변경된 이미지
fixed_img = None
# 사이즈가 변경된 이미지가 생성될 라벨
label_image = tkinter.Label(window, width=640)
# 최종 이미지가 생성될 라벨
label_final = tkinter.Label(window, width=640)

# 그림 선택 버튼
pic_select_button = tkinter.Button(window, command=find_pic, text="그림 파일 찾으러 가기")
pic_select_button.pack()

label_image.pack()

## 그림 회전 버튼
# 클릭한 횟수
tick_count = 0
rotate_button = tkinter.Button(window, command=rotate_pic, text="90도 회전하기", state="disabled")
rotate_button.pack()

## 그림 수직 이동 버튼
vertical_button = tkinter.Button(window, command=move_vertical, text="위로 이동하기", state="disabled")
vertical_button.pack()
## 그림 수평 이동 버튼
horizontal_button = tkinter.Button(window, text="아래로 이동하기", state="disabled")
horizontal_button.pack()

label_final.pack()

window.mainloop()