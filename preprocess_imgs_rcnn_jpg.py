#!/bin/python
#Python3

# so that we will have all images in one folder as jpgs and all labels as well

import argparse
from PIL import Image
import os
import re
from shutil import copyfile
def parse_args():
    parser = argparse.ArgumentParser(description="turn image to jpg and put all images/labels into single folder and rename them")
    parser.add_argument('--old_img_folder',dest="old_img",default="old_img",type=str)
    parser.add_argument('--old_label_folder',dest="old_label",default="old_label",type=str)
    parser.add_argument('--new_img_folder',dest="new_img",default="new_img",type=str)
    parser.add_argument('--new_label_folder',dest="new_label",default="new_label",type=str)
    parser.add_argument('--quality',dest="quality",default=95,type=int)
    args = parser.parse_args()
    return args

def list_files(fldr):
    f_list = []
    for root, directories, filenames in os.walk(fldr):
        for f in filenames:
            f_list.append(os.path.join(root,f))
    return f_list

def save_img(old,new,quality):
    Image.open(old).save(new,quality=quality)

count = 0
args = parse_args()
if not os.path.exists(args.new_img):
    os.makedirs(args.new_img)
if not os.path.exists(args.new_label):
    os.makedirs(args.new_label)
for label in list_files(args.old_label):
    img_path = re.sub('^'+args.old_label,args.old_img,label)[:-3] + 'jpg'
    if os.path.exists(img_path) and int(open(label,'r').readline()) != 0:
        count += 1
        save_img(img_path,os.path.join(args.new_img,str(count)+'.jpg'),args.quality)
        copyfile(label, os.path.join(args.new_label,str(count)+'.txt'))

print('done')
