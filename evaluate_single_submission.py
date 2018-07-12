
import argparse
import sys
import csv

from os import path, makedirs

from evaluation_metrics import evaluation_metrics_for_segmentation, evaluation_metrics_for_classification, evaluation_metrics_for_fovea_location
from util.file_management import parse_boolean


def evaluate_single_submission(results_folder, gt_folder, output_path=None, export_table=False, is_training=False):
    '''
    Evaluate the results of a single submission

    Input:
        results_folder: full path to the submitted results
        gt_folder: full path to the ground truth files
        [output_path]: a folder where the results will be saved. If not provided, the results are not saved
        [export_table]: a boolean value indicating if the table will be exported or not
        [is_training]: a boolean value indicating if the evaluation is performed on training data or not
    Output:
        mean_cup_dice: the mean Dice coefficient for the optic cups
        mean_disc_dice: the mean Dice coefficient for the optic disc
        mae_cdr: the mean absolute error for the vertical cup to disc ratio

    '''

    # evaluate the segmentation results -----------------

    # prepare the segmentation folder
    segmentation_folder = path.join(results_folder, 'segmentation')
    # prepare the gt labels folder for segmentation
    gt_segmentation_folder = path.join(gt_folder, 'Disc_Cup_Masks')

    # evaluate the segmentation results
    mean_cup_dice, mean_disc_dice, mae_cdr = evaluation_metrics_for_segmentation.evaluate_segmentation_results(segmentation_folder, gt_segmentation_folder, 
                                                                                                               output_path=output_path, 
                                                                                                               export_table=export_table,
                                                                                                               is_training=is_training)
    # initialize a tuple with all the results for segmentation
    segmentation_performance = [ mean_cup_dice, mean_disc_dice, mae_cdr ]


    # evaluate the classification results -----------------

    # prepare the path to the classification results
    classification_filename = path.join(results_folder, 'classification_results.csv')
    # prepare the gt labels folder for classification
    if is_training:
        gt_classification_folder = gt_segmentation_folder
    else:
        gt_classification_folder = gt_folder
    # get the AUC and the reference sensitivity values
    auc, reference_sensitivity = evaluation_metrics_for_classification.evaluate_classification_results(classification_filename, gt_classification_folder, 
                                                                                                       output_path=output_path,
                                                                                                       is_training=is_training)
    # initialize a tuple with all the results for classification
    classification_performance = [ auc, reference_sensitivity ]


    # evaluate the fovea location results -----------------

    # prepare the path to the fovea location results
    fovea_location_filename = path.join(results_folder, 'fovea_location_results.csv')
    # prepare the filename to the fovea location gt
    gt_filename = path.join(gt_folder, 'Fovea_location.xlsx')
    # get the mean euclidean distance
    fovea_location_performance = evaluation_metrics_for_fovea_location.evaluate_fovea_location_results(fovea_location_filename, gt_filename,
                                                                                                       output_path=output_path)

    return segmentation_performance, classification_performance, fovea_location_performance





if __name__ == '__main__':

    # create an argument parser to control the input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("results_folder", help="full path to the submitted results", type=str)
    parser.add_argument("gt_folder", help="full path to the ground truth files", type=str)
    parser.add_argument("--output_path", help="a folder where the results will be saved. If not provided, the results are not saved", type=str, default=None)
    parser.add_argument("--export_table", help="a boolean value indicating if the table will be exported or not", type=str, default='False')
    parser.add_argument("--is_training", help="a boolean value indicating if the evaluation is performed on training data or not", type=str, default='False')
    args = parser.parse_args()

    # call the "main" function
    evaluate_single_submission(args.results_folder, args.gt_folder, args.output_path, parse_boolean(args.export_table), parse_boolean(args.is_training))
    
    
    