
import csv
import numpy as np

from scipy.io import savemat
from os import listdir, path


def parse_boolean(input_string):
    '''
    Parse a string as a boolean
    '''
    return input_string.upper()=='TRUE'



def get_segmentation_filenames(path_to_files, extension='bmp'):
    '''
    Get all the files on a given folder with the given extension

    Input:
        path_to_files: string to a path where the segmentation files are
        [extension]: string representing the extension of the files
    Output:
        image_filenames: a list of strings with the filenames in the folder
    '''

    # initialize a list of image filenames
    image_filenames = []
    # add to this list only those filenames with the corresponding extension
    for file in listdir(path_to_files):
        if file.endswith('.' + extension):
            image_filenames = image_filenames + [ file ]

    return image_filenames



def read_csv_classification_results(csv_filename):
    '''
    Read a two-column CSV file that has the classification results inside.

    Input:
        csv_filename: full path and filename to a two column CSV file with the classification results (image filename, score)
    Output:
        image_filenames: list of image filenames, as retrieved from the first column of the CSV file
        scores: numpy array of floats, as retrieved from the second column of the CSV file
    '''

    # initialize the output variables
    image_filenames = []
    scores = []

    # open the file
    with open(csv_filename, 'r') as csv_file:
        # initialize a reader
        csv_reader = csv.reader(csv_file)
        # ignore the first row, that only has the header
        next(csv_reader)
        # and now, iterate and fill the arrays
        for row in csv_reader:
            image_filenames = image_filenames + [ row[0] ]
            scores = scores + [ float(row[1]) ]

    # turn the list of scores into a numpy array
    scores = np.asarray(scores, dtype=np.float)

    # return the image filenames and the scores
    return image_filenames, scores



def sort_scores_by_filename(target_names, names_to_sort, values_to_sort):
    '''
    This function is intended to correct the ordering in the outputs, just in case...

    Input:
        target_names: a list of names sorted in the order that we want
        names_to_sort: a list of names to sort
        values_to_sort: a numpy array of values to sort
    Output:
        sorted_values: same array than values_to_sort, but this time sorted :)
    '''

    # initialize the array of sorted values
    sorted_values = np.zeros(values_to_sort.shape)

    # iterate for each filename in the target names
    for i in range(len(target_names)):
        # assign the value to the correct position in the array
        sorted_values[i] = values_to_sort[names_to_sort.index(target_names[i])]
    
    # return the sorted values
    return sorted_values



def sort_coordinates_by_filename(target_names, names_to_sort, values_to_sort):
    '''
    This function is intended to correct the ordering in the outputs, just in case...

    Input:
        target_names: a list of names sorted in the order that we want
        names_to_sort: a list of names to sort
        values_to_sort: a numpy array of values to sort
    Output:
        sorted_values: same array than values_to_sort, but this time sorted :)
    '''

    # initialize the array of sorted values
    sorted_values = np.zeros(values_to_sort.shape)

    # iterate for each filename in the target names
    for i in range(len(target_names)):
        # assign the value to the correct position in the array
        sorted_values[i,:] = values_to_sort[names_to_sort.index(target_names[i])]
    
    # return the sorted values
    return sorted_values



def get_labels_from_training_data(gt_folder):
    '''
    Since the training data has two folder, "Glaucoma" and "Non-Glaucoma", we can use
    this function to generate an array of labels automatically, according to the image
    filenames

    Input:
        gt_folder: path to the training folder, with "Glaucoma" and "Non-Glaucoma" folder inside
    Output:
        image_filenames: filenames in the gt folders
        labels: binary labels (0: healthy, 1:glaucomatous)
    '''

    # prepare the folders to read
    glaucoma_folder = path.join(gt_folder, 'Glaucoma')
    non_glaucoma_folder = path.join(gt_folder, 'Non-Glaucoma')

    # get all the filenames inside each folder
    glaucoma_filenames = get_segmentation_filenames(glaucoma_folder)
    non_glaucoma_filenames = get_segmentation_filenames(non_glaucoma_folder)

    # concatenate them to generate the array of image filenames
    image_filenames = glaucoma_filenames + non_glaucoma_filenames

    # generate the array of labels
    labels = np.zeros(len(image_filenames), dtype=np.bool)
    labels[0:len(glaucoma_filenames)] = True

    return image_filenames, labels



def save_roc_curve(filename, tpr, fpr, auc):
    '''
    Save the ROC curve values on a .mat file

    Input:
        filename: output filename
        tpr: true positive rate
        fpr: false positive rate
        auc: area under the ROC curve
    '''

    # save the current ROC curve as a .mat file for MATLAB
    savemat(filename, {'tpr': tpr, 'fpr' : fpr, 'auc': auc})



def save_csv_classification_performance(output_filename, auc, reference_sensitivity):
    '''
    Save the AUC and the reference sensitivity values in a CSV file

    Input:
        output_filename: a string with the full path and the output file name (with .csv extension)
        auc: area under the ROC curve
        reference_sensitivity: sensitivity value for a given specificity
    '''

    # open the file
    with open(output_filename, 'w') as csv_file:
        # initialize the writer
        my_writer = csv.writer(csv_file)
        # write the column names
        my_writer.writerow(['AUC', 'Sensitivity'])
        # write the values
        my_writer.writerow([str(auc), str(reference_sensitivity)])



def save_csv_fovea_location_performance(output_filename, distance):
    '''
    Save the mean Euclidean distance on a CSV file

    Input:
        output_filename: a string with the full path and the output file name (with .csv extension)
        distance: mean Euclidean distance
    '''

    # open the file
    with open(output_filename, 'w') as csv_file:
        # initialize the writer
        my_writer = csv.writer(csv_file)
        # write the column names
        my_writer.writerow(['Mean Euclidean distance'])
        # write the values
        my_writer.writerow([str(distance)])



def save_csv_segmentation_table(table_filename, image_filenames, cup_dices, disc_dices, ae_cdrs):
    '''
    Save the table of segmentation results as a CSV file.

    Input:
        table_filename: a string with the full path and the table filename (with .csv extension)
        image_filenames: a list of strings with the names of the images
        cup_dices: a numpy array with the same length than the image_filenames list, with the Dice coefficient for each optic cup
        disc_dices: a numpy array with the same length than the image_filenames list, with the Dice coefficient for each optic disc
        ae_cdrs: a numpy array with the same length than the image_filenames list, with the absolute error of the vertical cup to disc ratio
    '''

    # write the data
    with open(table_filename, 'w') as csv_file:
        # initialize the writer
        table_writer = csv.writer(csv_file)
        # write the column names
        table_writer.writerow(['Filename', 'Cup-Dice', 'Disc-Dice', 'AE-CDR'])
        # write each row
        for i in range(len(image_filenames)):
            table_writer.writerow( [image_filenames[i], str(cup_dices[i]), str(disc_dices[i]), str(ae_cdrs[i])] )



def save_csv_fovea_location_table(table_filename, image_filenames, distances):
    '''
    Save the table of Euclidean distances results as a CSV file.

    Input:
        table_filename: a string with the full path and the table filename (with .csv extension)
        image_filenames: a list of strings with the names of the images
        distances: a 1D numpy array with the Euclidean distances of the prediction, for each image
    '''

    # write the data
    with open(table_filename, 'w') as csv_file:
        # initialize the writer
        table_writer = csv.writer(csv_file)
        # write the column names
        table_writer.writerow(['Filename', 'Euclidean distance'])
        # write each row
        for i in range(len(image_filenames)):
            table_writer.writerow( [image_filenames[i], str(distances[i])] )



def save_csv_mean_segmentation_performance(output_filename, mean_cup_dice, mean_disc_dice, mae_cdrs):
    '''
    Save a CSV file with the mean performance

    Input:
        output_filename: a string with the full path and the table filename (with .csv extension)
        mean_cup_dice: average Dice coefficient for the optic cups
        mean_disc_dice: average Dice coefficient for the optic discs
        mae_cdrs: mean absolute error of the vertical cup to disc ratios
    '''

    # write the data
    with open(output_filename, 'w') as csv_file:
        # initialize the writer
        table_writer = csv.writer(csv_file)
        # write the column names
        table_writer.writerow(['Cup-Dice', 'Disc-Dice', 'AE-CDR'])
        # write each row
        table_writer.writerow( [ str(mean_cup_dice), str(mean_disc_dice), str(mae_cdrs)] )



def read_fovea_location_results(csv_filename):
    '''
    Read a CSV file with 3 columns: the first contains the filenames, and the second/third have
    the (x,y) coordinates, respectively.

    Input:
        csv_filename: full path and filename to a three columns CSV file with the fovea location results (image filename, x, y)
    Output:
        image_filenames: list of image filenames, as retrieved from the first column of the CSV file
        coordinates: a 2D numpy array of coordinates
    '''

    # initialize the output variables
    image_filenames = []
    coordinates = None

    # open the file
    with open(csv_filename, 'r') as csv_file:
        # initialize a reader
        csv_reader = csv.reader(csv_file)
        # ignore the first row, that only has the header
        next(csv_reader)
        # and now, iterate and fill the arrays
        for row in csv_reader:
            # append the filename
            image_filenames = image_filenames + [ row[0] ]
            # append the coordinates
            current_coordinates = np.asarray( row[1:], dtype=np.int )
            if coordinates is None:
                coordinates = current_coordinates
            else:
                coordinates = np.vstack( (coordinates, current_coordinates))

    return image_filenames, coordinates



import openpyxl

def read_gt_fovea_location(xlsx_filename):
    '''
    Read a XLSX file with 3 columns: the first contains the filenames, and the second/third have
    the (x,y) coordinates, respectively.

    Input:
        xlsx_filename: full path and filename to a three columns XLSX file with the fovea location results (image filename, x, y)
    Output:
        image_filenames: list of image filenames, as retrieved from the first column of the CSV file
        coordinates: a 2D numpy array of coordinates
    '''

    # initialize the output variables
    image_filenames = []
    coordinates = None

    # read the xlsx file
    book = openpyxl.load_workbook(xlsx_filename)
    current_sheet = book.active

    # iterate for each row
    for row in current_sheet.iter_rows(min_row=2, min_col=1):
        # append the filename
        image_filenames = image_filenames + [ row[1].value ]
        # append the coordinates
        current_coordinates = np.asarray( [ row[2].value, row[3].value ], dtype=np.int )
        if coordinates is None:
            coordinates = current_coordinates
        else:
            coordinates = np.vstack( (coordinates, current_coordinates))

    return image_filenames, coordinates