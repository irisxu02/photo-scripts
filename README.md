# Automation scripts for photography

`python organize.py --<flag> <root_dir_path>`

1. Extract all files from subdirectories into root directory
--extract

2. Convert heic to jpg using `heif-convert`. Install using: `sudo apt-get install libheif-examples`
--convert

3. Separate photos by month and place in folders labeled yyyy-mm
--time

4. Separate photos by type with the folder name being the name of the file extension (e.g. arw, jpg, png)
- extensions should not be case sensitive
- jpg, JPG, jpeg , JPEG should all be in the same folder
--type

5. Script to identify any photos of food and place in a folder named 'food'
Trained food detector on [Food-5K dataset](https://www.epfl.ch/labs/mmspg/downloads/food-image-datasets/)
