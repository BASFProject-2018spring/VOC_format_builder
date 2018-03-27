#!/bin/python

# build VOC compatible dataset

import argparse
from PIL import Image
import os
import re
from shutil import copyfile
import numpy as np
def parse_args():
    parser = argparse.ArgumentParser(description="build VOC dataset")
    parser.add_argument('--voc_folder',dest="voc",default="VOC2007",type=str)
    parser.add_argument('--img_folder',dest="img",default="aug_img",type=str)
    parser.add_argument('--label_folder',dest="label",default="aug_label",type=str)
    parser.add_argument('--test_num',dest="test",default=1,type=int)
    parser.add_argument('--val_num',dest="val",default=1,type=int)
    args = parser.parse_args()
    return args

def list_files(fldr):
    f_list = []
    for root, directories, filenames in os.walk(fldr):
        for f in filenames:
            f_list.append(os.path.join(root,f))
    return f_list

def txt_to_xml(txt_str,img_cnt,img_full_path):
    str_list = txt_str.split()
    im = Image.open(img_full_path)
    width, height = im.size
    xml = """<annotation>
\t<folder>VOC2007</folder>
\t<filename>"""
    xml = xml + str(img_cnt)+'.jpg'+ """</filename>
\t<source>
\t\t<database>The VOC2007 Database</database>
\t\t<annotation>PASCAL VOC2007</annotation>
\t\t<image>flickr</image>
\t\t<flickrid>338944910</flickrid>
\t</source>
\t<owner>
\t\t<flickrid>UNKNOWN</flickrid>
\t\t<name>UNKNOWN</name>
\t</owner>
\t<size>
\t\t<width>"""+str(width)+"""</width>
\t\t<height>"""+str(height)+"""</height>
\t\t<depth>3</depth>
\t</size>
\t<segmented>0</segmented>
"""
    i = 1
    for _ in range(int(str_list[0])):
        xmin = int(str_list[i])
        xmin += 1
        if xmin <= 1:
            xmin = 2
        i+=1
        ymin = int(str_list[i])
        ymin += 1
        if ymin <=1 :
            ymin = 2
        i+=1
        xmax = int(str_list[i])
        xmax += 1
        if xmax >= width-1:
            xmax = width - 1
        i+=1
        ymax = int(str_list[i])
        ymax += 1
        if ymax >= height - 1:
            ymax = height - 1
        i+=1
        clabel = str(str_list[i])
        i+=1
        xml = xml + """\t<object>
\t\t<name>"""+clabel.lower().replace('-','')+"""</name>
\t\t<pose>Left</pose>
\t\t<truncated>0</truncated>
\t\t<difficult>0</difficult>
\t\t<bndbox>
\t\t\t<xmin>"""+str(xmin)+"""</xmin>
\t\t\t<ymin>"""+str(ymin)+"""</ymin>
\t\t\t<xmax>"""+str(xmax)+"""</xmax>
\t\t\t<ymax>"""+str(ymax)+"""</ymax>
\t\t</bndbox>
\t</object>
"""
    xml = xml+"</annotation>\n"
    return xml


args = parse_args()
if os.path.exists(args.voc):
    raise ValueError('VOC already exists! Delete the whole folder before regenerate database!')

img_list = list_files(args.img)
os.makedirs(args.voc)
os.makedirs(os.path.join(args.voc,'Annotations'))
os.makedirs(os.path.join(args.voc,'JPEGImages'))
os.makedirs(os.path.join(args.voc,'ImageSets'))
os.makedirs(os.path.join(args.voc,'ImageSets/Main'))
os.makedirs(os.path.join(args.voc,'ImageSets/Layout'))
os.makedirs(os.path.join(args.voc,'ImageSets/Segmentation'))

length = len(img_list)
wlist = list(range(1,length+1))
np.random.shuffle(wlist)
test_list = [str(x) for x in wlist[:args.test]]
val_list = [str(x) for x in wlist[args.test:args.test+args.val]]
train_list = [str(x) for x in wlist[args.test+args.val:]]

open(os.path.join(args.voc,'ImageSets/Main/train.txt'),'w').write("\n".join(train_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Layout/train.txt'),'w').write("\n".join(train_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Segmentation/train.txt'),'w').write("\n".join(train_list)+"\n")

open(os.path.join(args.voc,'ImageSets/Main/test.txt'),'w').write("\n".join(test_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Layout/test.txt'),'w').write("\n".join(test_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Segmentation/test.txt'),'w').write("\n".join(test_list)+"\n")

open(os.path.join(args.voc,'ImageSets/Main/val.txt'),'w').write("\n".join(val_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Layout/val.txt'),'w').write("\n".join(val_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Segmentation/val.txt'),'w').write("\n".join(val_list)+"\n")

train_list.extend(val_list)

open(os.path.join(args.voc,'ImageSets/Main/trainval.txt'),'w').write("\n".join(train_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Layout/trainval.txt'),'w').write("\n".join(train_list)+"\n")
open(os.path.join(args.voc,'ImageSets/Segmentation/trainval.txt'),'w').write("\n".join(train_list)+"\n")

for count in range(1,length+1):
    copyfile(os.path.join(args.img,str(count)+".jpg"), os.path.join(args.voc,'JPEGImages/'+str(count)+'.jpg'))
    xml = txt_to_xml(open(os.path.join(args.label,str(count)+".txt"),'r').read(),count,os.path.join(args.img,str(count)+".jpg"))
    open(os.path.join(args.voc,'Annotations/'+str(count)+'.xml'),'w').write(xml)
print('done')
