import os
import cv2
import random
import numpy as np
from color_transfer import color_transfer
def generate_detection_image(img_name,bg_name,source_path):
    img = cv2.imread(os.path.join(source_path + '/人', img_name))
    mask = cv2.imread(os.path.join(source_path + '/masks',
        img_name.split('.')[0]+'.jpeg'))
    bg = cv2.imread(os.path.join(source_path + '/风景', bg_name))
    img = color_transfer(img,bg)
    mask = mask/255
    ratio = 1
    bg_row,bg_col = np.shape(bg)[:2]
    img_row,img_col = np.shape(img)[:2]
    while(img_row>=bg_row or img_col>=bg_col):
        ratio += 0.5
        img_row,img_col = int(img_row/ratio),int(img_col/ratio)
    img = cv2.resize(img,(img_col,img_row),interpolation=cv2.INTER_AREA)
    mask = cv2.resize(mask,(img_col,img_row),interpolation = cv2.INTER_AREA)
    b_box_row,b_box_col = img_row,img_col
    b_box_up = np.random.randint(bg_row - b_box_row)
    b_box_left = np.random.randint(bg_col - b_box_col)
    b_box_down = b_box_up + b_box_row
    b_box_right = b_box_left + b_box_col
    bg_small = bg[b_box_up:b_box_down,b_box_left:b_box_right]
    blend_img = mask*img + (1-mask)*bg_small
    bg[b_box_up:b_box_down,b_box_left:b_box_right] = blend_img
    b_box = [b_box_left,b_box_up,b_box_right,b_box_down]
    return bg, b_box

#cv2.imshow('blend_img',bg)
#cv2.waitKey(0)
save_path = './blend_result'
isCreated = os.path.exists(save_path)
if not isCreated:
    os.mkdir(save_path)

source_path = './source_material'
image_file_names = next(os.walk(os.path.join(source_path,'人')))[2]
background_file_names = next(os.walk(os.path.join(source_path,'风景')))[2]
for i in range(300):
    img_name = random.choice(image_file_names)
    bg_name = random.choice(background_file_names)
    if img_name.split('.')[-1]!='jpg' and img_name.split('.')[-1]!='jpeg':
        continue
    if bg_name.split('.')[-1]!='jpg' and bg_name.split('.')[-1]!='jpeg':
        continue
    print(img_name)
    print(bg_name)
    result,b_box = generate_detection_image(img_name,bg_name,source_path)
    new_name = img_name.split('.')[0] + '_' + bg_name.split('.')[0] + '.jpg'
    cv2.imwrite(os.path.join(save_path,new_name),result)
    print('completed generate %d image'%i)
