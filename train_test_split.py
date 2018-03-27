#!/bin/python
#Python3

# so that we will have all images in one folder as jpgs and all labels as well

import argparse
import os
import re
from shutil import copyfile
import random

def parse_args():
    parser = argparse.ArgumentParser(description="turn image to jpg and put all images/labels into single folder and rename them")
    parser.add_argument('--img_folder',dest="img",default="img",type=str)
    parser.add_argument('--label_folder',dest="label",default="label",type=str)
    parser.add_argument('--train_folder',dest="train",default="train",type=str)
    parser.add_argument('--test_folder',dest="test",default="test",type=str)
    parser.add_argument('--test_size',dest='test_size', default=0.15, type=float)
    args = parser.parse_args()
    return args

def list_files(fldr):
    f_list = []
    for root, directories, filenames in os.walk(fldr):
        for f in filenames:
            f_list.append(os.path.join(root,f))
    return f_list

args = parse_args()
assert not os.path.exists(args.train)
assert not os.path.exists(args.test)

os.makedirs(args.train)
os.makedirs(args.test)

train_img_path = os.path.join(args.train,'new_img')
train_label_path = os.path.join(args.train,'new_label')

test_img_path = os.path.join(args.test,'new_img')
test_label_path = os.path.join(args.test,'new_label')

os.makedirs(train_img_path)
os.makedirs(train_label_path)
os.makedirs(test_img_path)
os.makedirs(test_label_path)

all_data = list_files(args.label)
random.shuffle(all_data)
test_len = int(round(len(all_data) * args.test_size))

test = all_data[:test_len]
train = all_data[test_len:]

count = 0
for label in train:
    img_path = re.sub('^'+args.label,args.img,label)[:-3] + 'jpg'
    if os.path.exists(img_path):
        count += 1
        copyfile(img_path, os.path.join(train_img_path,str(count)+'.jpg'))
        copyfile(label, os.path.join(train_label_path,str(count)+'.txt'))

count = 0
for label in test:
    img_path = re.sub('^'+args.label,args.img,label)[:-3] + 'jpg'
    if os.path.exists(img_path):
        count += 1
        copyfile(img_path, os.path.join(test_img_path,str(count)+'.jpg'))
        copyfile(label, os.path.join(test_label_path,str(count)+'.txt'))

print('done')