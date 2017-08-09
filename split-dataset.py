import random
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True,
                    help="Input image directory path")
parser.add_argument("--train_fraction", type=float, default=0.8,
                    help="percentage of images to use for training set")
parser.add_argument("--test_fraction", type=float, default=0.2,
                    help="percentage of images to use for test set")
parser.add_argument("--sort", action="store_true",
                    help="if set, sort the images instead of shuffling them")
a = parser.parse_args()

random.seed(0)

files = glob.glob(os.path.join(a.input_dir, "*.png"))
files.sort()

assignments = []
assignments.extend(["train"] * int(a.train_fraction * len(files)))
assignments.extend(["test"] * int(a.test_fraction * len(files)))
assignments.extend(["val"] * int(len(files) - len(assignments)))

if not a.sort:
    random.shuffle(assignments)

for name in ["train", "val", "test"]:
    if name in assignments:
        d = os.path.join(a.input_dir, name)
        if not os.path.exists(d):
            os.makedirs(d)

print(len(files), len(assignments))
for inpath, assignment in zip(files, assignments):
    outpath = os.path.join(a.input_dir, assignment, os.path.basename(inpath))
    print(inpath, "->", outpath)
    os.rename(inpath, outpath)
