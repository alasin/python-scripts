import os
import sys
import glob
import argparse
from shutil import copyfile


def compare(a, b):
    a_num = int(a.split('.')[0])
    b_num = int(b.split('.')[0])
    if a_num < b_num:
        return -1
    elif a_num == b_num:
        return 0
    else:
        return 1


parser = argparse.ArgumentParser(
    description='Combine image datasets from different directories')
parser.add_argument("--input_dirs", required=True,
                    help="1 or more input directories or a file containing list of directories", nargs="+")
parser.add_argument("--output_dir", required=True, help="Output directory")
parser.add_argument("--extension", required=True, type=str,
                    help="File extension (png, jpg etc.)")
a = parser.parse_args()

input_dirs = a.input_dirs
output_dir = a.output_dir

img_type = '.' + a.extension

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
    count = 1
else:
    regex = output_dir + '*' + img_type
    img_list = glob.glob(regex)
    count = len(img_list) + 1

if len(input_dirs) == 1:
    if not os.path.isdir(input_dirs[0]):
        with open(input_dirs[0]) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        input_dirs = content

for dir_name in input_dirs:
    if not os.path.isdir(dir_name):
        continue

    if dir_name[-1] != '/':
        dir_name = dir_name + '/'

    img_list = []
    regex = dir_name + '*' + img_type
    img_list = glob.glob(regex)

    file_name_list = []
    for val in img_list:
        file_name = val.split(dir_name)[1]
        file_name_list.append(file_name)

    file_name_list.sort(compare)
    print "Copying files from %s" % dir_name
    for val in file_name_list:
        count_str = "%06d" % count
        src_img_name = dir_name + val
        dst_img_name = output_dir + '/' + count_str + img_type

        copyfile(src_img_name, dst_img_name)
        count = count + 1

    # print file_num_list
