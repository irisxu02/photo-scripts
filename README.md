# Automation scripts for photography

## Basic organization
```
python organize.py --<flag> <root_dir_path>
```
**Extract all files from subdirectories into root directory**

`--extract`

**Convert heic to jpg using `heif-convert`. Install using: `sudo apt-get install libheif-examples`**

`--convert`

**Separate photos by month and place in folders labeled yyyy-mm**

`--time`

**Separate photos by type with the folder name being the name of the file extension (e.g. arw, jpg, png)**
- extensions should not be case sensitive
- jpg, JPG, jpeg , JPEG will all be put in the same folder

`--type`

## Identify photos of food and place them in a folder named 'food'
Food image classifier trained on [Food-5K dataset](https://www.epfl.ch/labs/mmspg/downloads/food-image-datasets/)

```
python find_food.py <root_dir_path> 
```

