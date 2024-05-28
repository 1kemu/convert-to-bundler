# Convert to Bundler file

Create the bundler output format files. ([Bundler](https://www.cs.cornell.edu/~snavely/bundler/))


## What is it used for?
You can visualize camera poses by loading Bundler file into CloudCompare.  
Like this.

<img width="550" src=./imgs/cc_demo.png >

## Dependencies
- Numpy
- Pandas
- OpenCV
- PyYAML

## Preparation

### Input data

- camera pose file:  
  This file contains 13 columns as [`image_id`, `r11`, `12`, `13`, `r21`, `r22`, `r23`, `r31`, `r32`, `r33`, `t1`, `t2`, `t3`]. `image_id` is image file name (without extension) if you use image files. Otherwise, you can set any values as you like. `r11` ... `r33` are elements of camera pose matrix. `t1` ... `t3` are elements of camera position. Direction of camera coordinate axis is {x, y, z} = {right, down, front} (same as OpenCV).  
  You can alse reference `sample_input.csv`.
- camera intrinsic parameters (optional):  
  You can input intrinsic parameters. If you do not provide them, default value will be used (and it may work properly in mose cases).
- images files (optional):  
   You can input image files (assumed to `.jpg` format) corresponding to camera poses.

### Configuration

Edit config.yaml to set your configuration.

- pose_file_path: Path to camera pose file.
- output_dir: output directory.
- images_dir: images directory.
- params:
  - f: focal length.
  - k1, k2: coefficients of distortion function.

## Run

```bash
python converter.py --config /path/to/config/file
```

## Output

- bundler.out:  
  Bundler format file that contains camera pose information.
  You also need other files (`.jpg` and `list.txt`) when you visualize camera pose using CloudCompare.

- list.txt:
  It is list of path to images corresponding to camera whose pose you will visualize. If you do not prepare images, path to dummy image is listed.

- .jpg file:
   If you do not prepare images, dummy image is created.
