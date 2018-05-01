#!/bin/python
#Python3

# Rescale images and pad them with white color.

import argparse
import cv2
import os
import re
from shutil import copyfile
import numpy as np

HEIGHT = 832
WIDTH = 1128

def parse_args():
    parser = argparse.ArgumentParser(description="Downsampling images to a certain scale and pad them.")
    parser.add_argument('--input',dest="old_img",default="old_img",type=str)
    parser.add_argument('--output',dest="new_img",default="new_img",type=str)
    parser.add_argument('--scale',dest="scale",default=0.5,type=float)
    args = parser.parse_args()
    return args

def padding(img):
    img_height, img_width = img.shape
    #print(img.shape)
    if WIDTH < img_width or HEIGHT < img_height:
        raise ValueError('This script can only be used to SCALE DOWN images of 1128*832.')
    t_pad = (HEIGHT - img_height)//2
    b_pad = HEIGHT - img_height - t_pad
    l_pad = (WIDTH - img_width)//2
    r_pad = WIDTH - img_width - l_pad
    # pad with mean color
    pad_with = img.mean()
    return cv2.copyMakeBorder(img, t_pad,b_pad,l_pad,r_pad,cv2.BORDER_CONSTANT, value=int(pad_with))

def list_files(fldr):
    f_list = []
    for root, directories, filenames in os.walk(fldr):
        for f in filenames:
            f_list.append(os.path.join(root,f))
    return f_list

count = 0
args = parse_args()
if args.scale>1:
    raise ValueError('This script can only be used to SCALE DOWN images (i.e. scale<1)')

if not os.path.exists(args.new_img):
    os.makedirs(args.new_img)

for img_path in list_files(args.old_img):
    new_img_path = re.sub('^'+args.old_img,args.new_img,img_path)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,None,fx=args.scale, fy=args.scale, interpolation = cv2.INTER_CUBIC)
    #print(img)
    img = padding(img)
    #print(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) 
    cv2.imwrite(new_img_path,img)

print('done')