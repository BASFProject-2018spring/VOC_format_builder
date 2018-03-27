# VOC format builder

## Preprocess

After labeling with the labeling tool, we would have an `Image` folder and a `Label` folder with same inner structure (i.e. for all `.bmp` file in `Image`, we have a `.txt` file with same relative path in `Label`). If you have multiple image folders and label folders, you should combine all image folders into one image folder and same for label folders, with same inner folder structure.

Run `preprocess_imgs_rcnn.py` will convert BMP images to JPG images and rename all files to `number.txt` or `number.jpg` directly under `image` or `label` folder.

The command is

``` bash
python preprocess_imgs_rcnn.py --old_img_folder Image --old_label_folder Label --new_img_folder new_img --new_label_folder new_lbl --quality 95
```

`quality` specifies the quality of the generated jpgs.

`preprocess_imgs_rcnn_jpg.py` does the same job except that it expects the input iamges to be jpgs.


## Build VOC folder

The `voc_dataset_build.py` build a VOC2007 format data folder based on the above step, which includes XML building and coordinate shifting.

Suppose you want N test images and V validation images, you should use the following command:

```bash
python voc_dataset_build.py --voc_folder VOC2007 --img_folder new_img --label_folder new_lbl --test_num N --val_num V
```

The generated folder VOC2007 will be in VOC format.
