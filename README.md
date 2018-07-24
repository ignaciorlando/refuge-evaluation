
![Logo](https://raw.githubusercontent.com/ignaciorlando/refuge-evaluation/master/logo_refuge_header.png)

# REFUGE Challenge - Evaluation

This repository corresponds to the evaluation code used for the [REFUGE challenge](refuge.grand-challenge.org).
Please, use it as a sanity check to verify that the format of your submissions are correct. The formatting instructions are provided [here](https://refuge.grand-challenge.org/details/).

## Requirements

You will need **Python 3.6** to run the code.

The following libraries are also used:

- sklearn 0.19.3
- numpy 1.14.3
- openpyxl


## Usage

In this section we explain how to use the code.

### Evaluate a single submission

To evaluate a single submission, use the script ```evaluate_single_submission.py```.

It requires the following parameters:
- ```results_folder```: the full path to a folder with the results, organized according to the guidelines in the website.
- ```gt_folder```: full path to the folder with the ground truth annotations. Since you only have access to the training data, make sure to point to the training folder in the same format as provided in the website.
- ```--output_path``` (optional): full path to an output folder. If not provided, the results will be only printed in the screen but not saved in your hard drive.
- ```--export_table``` (optional): a boolean indicating if a table with the results per each of the images should be saved or not.
- ```--is_training``` (optional): a boolean indicating if you are using the training data for evaluation. Since you only have access to these labels, always set this parameter to ```True```.

The way this code works is relatively simple. It will analyze your ```results_folder``` and, according to its internal organization, will evaluate the results for the three tasks of the challenge. If the format is not correct, then the code will fail, so you can use it to double check the format of your submission. If you decide to complete only one of the tasks, you only need to generate the results (in the correct format) for the task that you are tackling.



### Evaluate multiple submission

To evaluate multiple submissions, use the script ```evaluate_multiple_submission.py```. 

It requires the following parameters:
- ```submissions_folder```: the full path to a folder with the submissions. The submission must be formatted as .zip files, according to the guidelines provided in the website.
- ```gt_folder```: full path to the folder with the ground truth annotations. Since you only have access to the training data, make sure to point to the training folder in the same format as provided in the website.
- ```uncompressed_files_folder```: full path to a folder in which the content of the zip files will be saved.
- ```output_path```: full path to the output folder where the results will be saved.
- ```--is_training``` (optional): a boolean indicating if you are using the training data for evaluation. Since you only have access to these labels, always set this parameter to ```True```.

This code could be useful to also check the format of your zip files. Moreover, you can apply it to get the results (on the training set) for different configurations of your algorithm. Please, remember that you need to compress the outputs of your models as zip files, and put them all in your ```submission_folder``` before calling the script.



### Generate leaderboards

To generate the leaderboards for the challenge, use the script ```generate_leaderboards.py```.
Make sure that you have executed ```evaluate_multiple_submission.py``` first, because you need to provide the table of results produce by that script.


## Frequent errors in the submissions

### Compression format
Make sure to use a .zip file and not .rar or any other compression format.

### ZIP file organization
Make sure that you compress a folder with the name of your team, containing all the results that you want to evaluate, in the format provided in the website.

### A folder inside the ZIP file
If you have compressed a folder into a zip file instead of all the files, you will create a folder inside the zip file (e.g., in the BestTeam.zip file you have a folder named "BestTeamEver" instead of the segmentation folder, the classification_results.csv and the fovea_localization_results.csv files). Please, make sure that you are compressing the files and not the folder where the files are (e.g., select all the files, right clic, select "Compress" in Ubuntu).

### Segmentation images in the wrong format

Make sure that your submission contains the segmentation masks in BMP format and not in TIFF or any other image file extension.

### File extensions in capital letters

Make sure that your files have the extension in lower case and not in upper case. Otherwise, the list of results filenames will differ from the list of ground truth labels.

### Segmentation files as RGB

Although there is a patch in the code to deal with segmentation results that were saved as RGB files (with all the channels equal), please make sure that you export them in the correct way.

### Segmentation folder without useless files

The segmentation folder should not contain useless folders or files. Make sure that it only has the bmp files with the segmentations.

### Size of the segmentation maps

Deep neural networks usually need to downsize the images before processing. Make sure that your segmentation maps have the same size as the original images. Otherwise, the evaluation will not be possible!

### CSV files without header
The evaluation code for fovea detection / glaucoma classification takes .csv files as inputs. These files have to have a header identifying each of the columns (e.g. Filename, Glaucoma risk). Make sure that you are introducing these fields in the csv file before submitting!

### CSV files that are unable to be read with Python
Make sure that you generated the CSV file in 'utf-8' encoding. Otherwise, the python library will not be able to read the file.

