
from evaluation_metrics.evaluation_metrics_for_segmentation import vertical_cup_to_disc_ratio
from evaluation_metrics.evaluation_metrics_for_classification import get_roc_curve, get_sensitivity_at_given_specificity
from util.file_management import parse_boolean, get_filenames, get_labels_from_training_data, read_gt_labels, save_roc_curve, save_csv_classification_performance, save_csv_classification_results

import numpy as np

from os import path, makedirs
from scipy.io import savemat
from scipy import misc




def evaluate_gt_vcdr_for_classification(gt_folder, output_folder, is_training=False):
    '''
    Inputs:
        gt_folder: path to the folder with all the ground truth labels (segmentation and classification)
        output_folder: path to the folder where all the results will be saved
        [is_training]: a boolean indicating if the evaluation will be performed on training or validation/test data
    Outputs:
    '''

    # get the classification labels and image filenames...
    if is_training:
        gt_classification_folder = path.join(gt_folder, 'Disc_Cup_Masks')
        gt_filenames, gt_labels = get_labels_from_training_data(gt_classification_folder)
    else:
        gt_classification_folder = gt_folder
        gt_filenames, gt_labels = read_gt_labels(path.join(gt_classification_folder, 'GT.xlsx'))
    
    # prepare the folder for segmentation
    gt_segmentation_folder = path.join(gt_folder, 'Disc_Cup_Masks')

    # prepare the output folder
    output_folder = path.join(output_folder, '__BASELINE__VCDR')
    if not path.exists(output_folder):
        makedirs(output_folder)

    # get the cup to disc ratio for each image
    vertical_cdr_values = export_vertical_cup_to_disc_ratios(gt_segmentation_folder, gt_filenames, output_folder, is_training)

    # save the vCDR values in a CSV file
    save_csv_classification_results(path.join(output_folder, 'classification_results.csv'), gt_filenames, vertical_cdr_values)

    # compute the ROC curve
    sensitivity, fpr, auc = get_roc_curve(vertical_cdr_values, gt_labels)
    # compute specificity
    specificity = 1 - fpr
    # print the auc
    print('AUC = {}'.format(str(auc)))

    # get sensitivity at reference value
    sensitivity_at_reference_value = get_sensitivity_at_given_specificity(sensitivity, specificity)
    # print the value
    print('Reference Sensitivity = {}'.format(str(sensitivity_at_reference_value)))

    # save the ROC curve
    save_roc_curve(path.join(output_folder, 'roc_curve.mat'), sensitivity, fpr, auc)
    # save a CSV file with the reference metrics
    save_csv_classification_performance(path.join(output_folder, 'evaluation_classification.csv'), auc, sensitivity_at_reference_value)
        




def export_vertical_cup_to_disc_ratios(gt_folder, image_filenames, output_folder, is_training=False):
    '''
    Export a list of vCDR values from the GT

    Input:
        gt_folder: a string representing the full path to the folder where the ground truth annotation files are
        image_filenames: names of the files with the segmentations of the optic disc and cup (without extension)
        output_folder: folder to output the cdr values
        is_training: a boolean value indicating if the evaluation is performed on training data or not
    Output:
        vertical_cdr_values: a numpy array with the vertical CDR values for each of the 
    '''

    # list of vertical cup-to-disc ratios
    vertical_cdr_values = np.zeros(len(image_filenames), dtype=np.float)

    # iterate for each image filename
    for i in range(len(image_filenames)):

        # to prevent any errors between jpg/bmp
        image_filenames[i] = path.splitext(image_filenames[i])[0] + '.bmp'

        # read the gt
        if is_training:
            gt_filename = path.join(gt_folder, 'Glaucoma', image_filenames[i] )
            if path.exists(gt_filename):
                gt_label = misc.imread(gt_filename)
            else:
                gt_filename = path.join(gt_folder, 'Non-Glaucoma', image_filenames[i])
                if path.exists(gt_filename):
                    gt_label = misc.imread(gt_filename)
                else:
                    raise ValueError('Unable to find {} in your training folder. Make sure that you have the folder organized as provided in our website.'.format(image_filenames[i]))
        else:
            gt_filename = path.join(gt_folder, image_filenames[i])
            if path.exists(gt_filename):
                gt_label = misc.imread(gt_filename)
            else:
                raise ValueError('Unable to find {} in your ground truth folder. If you are using training data, make sure to use the parameter is_training in True.'.format(image_filenames[i]))

        # evaluate the results and assign to the corresponding row in the table
        vertical_cdr_values[i] = vertical_cup_to_disc_ratio(gt_label)

    # save the cup to disc ratios in a .mat file
    savemat(path.join(output_folder, 'vertical_cup_to_disc_ratios.mat'), {'image_filenames': image_filenames, 'vertical_cdr_values' : vertical_cdr_values})

    return vertical_cdr_values







import argparse
import sys

if __name__ == '__main__':

    # create an argument parser to control the input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("gt_folder", help="a string representing the full path to the folder where the ground truth annotation files are", type=str)
    parser.add_argument("output_folder", help="folder to output the cdr values", type=str)
    parser.add_argument("--is_training", help="a boolean value indicating if the evaluation is performed on training data or not", type=str, default='False')
    args = parser.parse_args()

    # call the "main" function
    evaluate_gt_vcdr_for_classification(args.gt_folder, args.output_folder, parse_boolean(args.is_training))