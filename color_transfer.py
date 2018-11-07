import cv2
import numpy as np

def color_map(aa):
    minmin = np.min(aa)
    if minmin < 0:
        aa_mean = np.mean(aa)
        aa = aa - aa_mean
        aa_min = np.min(aa)
        ratio2 = aa_mean/np.abs(aa_min)
        aa = ratio2*aa + aa_mean
    maxmax = np.max(aa)
    if maxmax > 255:
        aa_mean = np.mean(aa)
        aa = aa - aa_mean
        ratio2 = (255 - aa_mean)/(maxmax - aa_mean)
        aa = ratio2*aa + aa_mean
    return aa

def color_transfer(fg_im, bg_im):
    fg_img = cv2.cvtColor(fg_im,cv2.COLOR_BGR2Lab)
    bg_img = cv2.cvtColor(bg_im,cv2.COLOR_BGR2Lab)
    fg_img = fg_img.astype(np.float)
    bg_img = bg_img.astype(np.float)
    fg_l,fg_a,fg_b = np.split(fg_img,3,axis = 2)
    bg_l,bg_a,bg_b = np.split(bg_img,3,axis = 2)
    fg_l_mean = np.mean(fg_l)
    fg_a_mean = np.mean(fg_a)
    fg_b_mean = np.mean(fg_b)
    bg_l_mean = np.mean(bg_l)
    bg_a_mean = np.mean(bg_a)
    bg_b_mean = np.mean(bg_b)

    fg_l_std = np.std(fg_l)
    fg_a_std = np.std(fg_a)
    fg_b_std = np.std(fg_b)
    bg_l_std = np.std(bg_l)
    bg_a_std = np.std(bg_a)
    bg_b_std = np.std(bg_b)
    ratio = 0.5
    fg_l_new = ratio*((bg_l_std/fg_l_std)*(fg_l - fg_l_mean) + bg_l_mean)+(1-ratio)*fg_l
    #print(np.max(fg_l_new),np.min(fg_l_new))
    fg_l_new = color_map(fg_l_new)
    #print(np.max(fg_l_new),np.min(fg_l_new))
    fg_a_new = ratio*((bg_a_std/fg_a_std)*(fg_a - fg_a_mean) + bg_a_mean)+(1-ratio)*fg_a
    fg_a_new = color_map(fg_a_new)
    #print(np.max(fg_a_new),np.min(fg_a_new))
    fg_b_new = ratio*((bg_b_std/fg_b_std)*(fg_b - fg_b_mean) +
            bg_b_mean)+(1-ratio)*fg_b
    fg_b_new = color_map(fg_b_new)
    #print(np.max(fg_b_new),np.min(fg_b_new))
    fg_new = fg_img.copy()
    fg_new[:,:,0] = np.squeeze(fg_l_new)
    fg_new[:,:,1] = np.squeeze(fg_a_new)
    fg_new[:,:,2] = np.squeeze(fg_b_new)
    #fg_new = 255*(fg_new - np.min(fg_new))/(np.max(fg_new) - np.min(fg_new))
    fg_new = fg_new.astype('uint8')
    #print(np.max(fg_new),np.min(fg_new))
    fg_new = cv2.cvtColor(fg_new,cv2.COLOR_Lab2BGR)
#    bg_im = cv2.resize(bg_im, (np.shape(fg_im)[1],np.shape(fg_im)[0]), interpolation=cv2.INTER_AREA)
    #print(np.shape(fg_im),np.shape(bg_im))
#    img_new = np.concatenate((fg_im,bg_im,fg_new),axis = 1)
    #print(np.shape(img_new))
#    row,col = np.shape(fg_im)[:2]
#    col = int(col*300/row)
#    row = 300
#    img_new = cv2.resize(img_new,(col*3,row) , interpolation=cv2.INTER_AREA)
    #cv2.imshow('result',img_new)
    #cv2.waitKey(0)
    return fg_new
