# Copyright 2023-2024 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# ImageMaskDatasetGenerator.py
# 2024/04/24 antillia.com

import os
import sys
import shutil
import cv2
import glob
import traceback


class ImageMaskDatasetGenerator:
  
  def __init__(self, width=512, height=512, input_dir="./valid", output_dir="./ORCA_master/", augmentation=True):
    self.W          = width
    self.H          = height
    self.input_dir  = input_dir
    self.output_dir = output_dir
    self.augmentation= False
      
    self.hflip    = False
    self.vflip    = False
    self.rotation = False
    self.ANGLES   = []
    self.augmentation = augmentation

    if self.augmentation:
      self.hflip    = True
      self.vflip    = True
      self.rotation = True
      self.ANGLES   = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

    if os.path.exists(self.output_dir):
      shutil.rmtree(self.output_dir)

    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

    self.output_images_dir = os.path.join(self.output_dir, "images")
    if not os.path.exists(self.output_images_dir):
      os.makedirs(self.output_images_dir)

    self.output_masks_dir  = os.path.join(self.output_dir, "masks")
    if not os.path.exists(self.output_masks_dir):
      os.makedirs(self.output_masks_dir)

  def generate(self):
    mask_files = glob.glob(self.input_dir + "/*_mask.png")
    for mask_file in mask_files:
      image_file = mask_file.replace("_mask", "")
      if not os.path.exists(mask_file) or not os.path.exists(image_file):
        print("----- Unmatched mask_file {} and image_file {}".format(mask_file, image_file))
        input("----- error ")
        continue

      mask = cv2.imread(mask_file)
      mask = cv2.resize(mask, (self.W, self.H))
      basename = os.path.basename(mask_file)
      basename = basename.replace("_mask.png", ".jpg")
      output_mask_file = os.path.join(self.output_masks_dir, basename)
      cv2.imwrite(output_mask_file, mask)
      print("=== Saved{}".format(output_mask_file))

      self.augment(mask, basename, self.output_masks_dir, border=(0, 0, 0))

      image_file = mask_file.replace("_mask", "")
      image  = cv2.imread(image_file)
      image = cv2.resize(image, (self.W, self.H))
      basename = os.path.basename(image_file)
      basename = basename.replace(".png", ".jpg")
      output_image_file = os.path.join(self.output_images_dir, basename)
      cv2.imwrite(output_image_file, image)
      print("=== Saved{}".format(output_image_file))

      self.augment(image, basename, self.output_images_dir, border=(255,255,255))


  def augment(self, image, basename, output_dir, border):
    if self.hflip:
      flipped = self.horizontal_flip(image)
      output_filepath = os.path.join(output_dir, "hflipped_" + basename)
      cv2.imwrite(output_filepath, flipped)
      print("--- Saved {}".format(output_filepath))

    if self.vflip:
      flipped = self.vertical_flip(image)
      output_filepath = os.path.join(output_dir, "vflipped_" + basename)
      cv2.imwrite(output_filepath, flipped)
      print("--- Saved {}".format(output_filepath))

    if self.rotation:
      self.rotate(image, basename, output_dir, border)

  def horizontal_flip(self, image): 
    print("shape image {}".format(image.shape))
    if len(image.shape)==3:
      return  image[:, ::-1, :]
    else:
      return  image[:, ::-1, ]

  def vertical_flip(self, image):
    if len(image.shape) == 3:
      return image[::-1, :, :]
    else:
      return image[::-1, :, ]

  def rotate(self, image, basename, output_dir, border):
    for angle in self.ANGLES:      

      center = (self.W/2, self.H/2)
      rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)

      rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(self.W, self.H), borderValue=border)
      output_filepath = os.path.join(output_dir, "rotated_" + str(angle) + "_" + basename)
      cv2.imwrite(output_filepath, rotated_image)
      print("--- Saved {}".format(output_filepath))
      
      
"""
Step 1:
From
./valid
  +-- *.png
  +-- *_mask.png
  ...

Split *png and _mask.png files into images and masks folders. 
./ORCA_master
 +--images
 |   +-- *.jpg
 |   +-- *.jpg
 |  ...
 +--masks 
     +-- *.jpg
     +-- *.jpg
     ...
"""
"""
Step 2:
From
./test
  +-- *.png
  +-- *_mask.png
  ...

Split *png and _mask.png files into images and masks folders. 
./ORCA-ImageMask-Dataset-V1
   +-- test
     +--images
     |   +-- *.jpg
     |   +-- *.jpg
     |  ...
     +--masks 
       +-- *.jpg
       +-- *.jpg
       ...
"""


if __name__ == "__main__":
  
  try:
    # 1 generate 
    #   ./ORCA_master
    #      +-- images 
    #      +-- masks 
    #  from the orginal valid dataset with augmentation=True
    #
    generator = ImageMaskDatasetGenerator(width=512, height=512, 
                                          input_dir="./valid", 
                                          output_dir="./ORCA_master/", 
                                          augmentation=True)
    generator.generate()
    
    # 2 generate 
    # ./ORCA-ImageMask-Dataset-V1
    #     +--test
    #         +--images
    #         +--masks
    #
    #  from the original test dataset without augmentation
    # 
    generator = ImageMaskDatasetGenerator(width=512, height=512, 
                                          input_dir="./test", 
                                          output_dir="./ORCA-ImageMask-Dataset-V1/test/", 
                                          augmentation=False)
    generator.generate()

  except:
    traceback.print_exc()
