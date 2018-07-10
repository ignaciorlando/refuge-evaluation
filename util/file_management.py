
import csv

from os import listdir


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
            image_filenames = image_filenames + file

    return image_filenames



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
    with open(table_filename, 'wb') as csv_file:
        # initialize the writer
        table_writer = csv.writer(csv_file)
        # write the column names
        table_writer.writerow(['Filename', 'Cup-Dice', 'Disc-Dice', 'AE-CDR'])
        # write each row
        for i in range(len(image_filenames)):
            table_writer.writerow( [image_filenames[i], str(cup_dices[i]), str(disc_dices[i]), str(ae_cdrs[i])] )



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
    with open(output_filename, 'wb') as csv_file:
        # initialize the writer
        table_writer = csv.writer(csv_file)
        # write the column names
        table_writer.writerow(['Cup-Dice', 'Disc-Dice', 'AE-CDR'])
        # write each row
        table_writer.writerow( [ str(mean_cup_dice), str(mean_disc_dice), str(mae_cdrs)] )