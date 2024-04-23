<h2> ImageMask-Dataset-ORCA (2024/04/24)</h2>

This is a simple ImageMask Dataset for Oral Cancer Image Segmentation.<br>
The dataset used here has been taken from the following web-site<br>
<b>ORCA: ORal Cancer Annotated dataset</b><br>
<pre>https://sites.google.com/unibas.it/orca/home</pre><br>
We have generated test, train, and valid datasets of 512x512 pixel-size from the original ORCA,
because the pixel-size of all images and masks of the dataset is 4500x4500, and too large to 
use for training of an ordinary segmentation model.<br> 
<br>
<table>
<tr>
<td>
<b>Oral cancer image sample </b><br>
<img src="./samples/images/TCGA-CN-4723-01Z-00-DX1.13483e7b-9322-4d39-8cd6-91e898bf2ee9_0.png" width="512" height="auto">
</td>
<td>
<b>Oral cancer mask sample </b><br>
<img  src="./samples/masks/TCGA-CN-4723-01Z-00-DX1.13483e7b-9322-4d39-8cd6-91e898bf2ee9_0_mask.png" width="512" height="auto">

</td>
</tr>
</table>
<br>

You can download our 512x512 resized <b>ORCA-ImageMask-Dataset</b> from the google drive
<a href="https://drive.google.com/file/d/1cOSiTXeU_l8duN_DNTyPFnfeZEuMKodn/view?usp=sharing">
ORCA-ImageMask-Dataset-V1.zip
</a>
<br>

<h3>1. Dataset Citation</h3>
<pre>
If you use the ORCA data, please cite:
F.  Martino,  D.D.  Bloisi,  A.  Pennisi,  M. Fawakherji,  G. Ilardi,  D. Russo,  D. Nardi,  S. Staibano, F. Merolla
"Deep Learning-based Pixel-wise Lesion Segmentation on Oral Squamous Cell Carcinoma Images"
Applied Sciences: 2020, 10(22), 8285; https://doi.org/10.3390/app10228285  [PDF]
</pre>
<br>

<h3>2. ImageMask Dataset Generation</h3>

If you would like to generate your own ImageMask-Dataset, please download the two original master datataset of  
<a href="https://drive.google.com/drive/folders/1XfplgYK5JWzzYWXQhrPUQujXNKUDK-WR">validation_100</a> 
and <a href="https://drive.google.com/drive/folders/1A_xiKTwBNO9XS_NzdDvWJNAx_z1nRnpS">test_100</a> in the following download page.<br> 
<a href="https://sites.google.com/unibas.it/orca/download">Download</a>,
and place the downloaded files under valid and test repectively.<br> 

Please run the following command for Python script <a href="./ImageMaskDatasetGenerator.py">ImageMaskDatasetGenerator.py</a>.
<br>
<pre>
> python ImageMaskDatasetGenerator.py
</pre>
This script executes the following two processings.<br><br>

<b>Step 1:</b><br>
From dataset
<pre>
./valid
  +-- *.png
  +-- *_mask.png
  ...
</pre>
the script splits *png and *_mask.png files in valid folder into images and masks folders under <b>./ORCA_master</b> as shown below.
<br>
Please note that in this step, the orignal images and masks are slightly augmented by flipping and rotation image processings. 
<pre> 
./ORCA_master
 +--images
 |   +-- *.jpg
 |   +-- *.jpg
 |  ...
 +--masks 
     +-- *.jpg
     +-- *.jpg
     ... 
</pre>

<b>Step2:</b><br>
Froom dataset
<pre>
./test
  +-- *.png
  +-- *_mask.png
  ...
</pre>
the script splits *png and *_mask.png files in test folder into images and masks folders under <b>./ORCA-ImageMask-Dataset-V1</b> as shown below.
<pre> 
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
</pre>

To create these new dataset with images and mask subdataset, all images and masks of the original dataset are
resized to be 512x512 pixel-size. 

Pleser run the following command for Python <a href="./split_master.py">split_master.py</a> 
<br>
<pre>
>python split_master.py
</pre>
, by which train and valid subdatasets are created under <b>./ORCA-ImageMask-Dataset-V1</b>.<br>
<pre>
./ORCA-ImageMask-Dataset-V1
├─test
│  ├─images
│  └─masks
├─train
│  ├─images
│  └─masks
└─valid
    ├─images
    └─masks
</pre>
<hr>
Train images sample<br>
<img src="./asset/train_images.png" width=1024 heigh="auto"><br><br>
Train mask sample<br>
<img src="./asset/train_masks.png" width=1024 heigh="auto"><br><br>


Dataset Statictics <br>
<img src="./ORCA-ImageMask-Dataset-V1_Statistics.png" width="512" height="auto"><br>

