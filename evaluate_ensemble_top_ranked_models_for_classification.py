
from evaluation_metrics.evaluation_metrics_for_classification import get_roc_curve, get_sensitivity_at_given_specificity
from util.file_management import parse_boolean, get_filenames, get_labels_from_training_data, read_gt_labels, save_roc_curve, save_csv_classification_performance, read_csv_classification_results, sort_scores_by_filename

import numpy as np

from os import path, makedirs, listdir
from scipy.io import savemat
from scipy import misc




def evaluate_ensemble_top_ranked_models_for_classification(ensemble_folder, gt_folder, output_folder, is_training=False):
    '''
    Inputs:
        ensemble_folder: path to a folder with the classification results of each team for the ensemble
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
    
    # prepare the output folder
    output_folder = path.join(output_folder, '__BASELINE__ENSEMBLE')
    if not path.exists(output_folder):
        makedirs(output_folder)

    # get the cup to disc ratio for each image
    ensemble_scores = ensemble_models(ensemble_folder, gt_filenames, output_folder)

    # compute the ROC curve
    sensitivity, fpr, auc = get_roc_curve(ensemble_scores, gt_labels)
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
        


def ensemble_models(ensemble_folder, gt_filenames, output_folder):
    '''
    Inputs:

    Outputs:
    '''

    # retrieve team names for the ensemble
    teams_names = listdir(ensemble_folder)

    # initialize the ensemble of scores
    ensemble_scores = np.zeros((len(gt_filenames), len(teams_names)), dtype=np.float)

    # iterate for each team name
    for i in range(0, len(teams_names)):
        # read the prediction filename
        image_filenames, predicted_scores = read_csv_classification_results(path.join(ensemble_folder, teams_names[i], 'classification_results.csv'))
        # sort the new scores using the same order as before
        predicted_scores = sort_scores_by_filename(gt_filenames, image_filenames, predicted_scores)
        # normalize scores
        ensemble_scores[:,i] = predicted_scores / np.max(predicted_scores)

    return np.mean(ensemble_scores, axis=1)

    







import argparse
import sys

if __name__ == '__main__':

    # create an argument parser to control the input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('ensemble_folder', help="path to a folder with the classification results of each team for the ensemble", type=str)
    parser.add_argument("gt_folder", help="a string representing the full path to the folder where the ground truth annotation files are", type=str)
    parser.add_argument("output_folder", help="folder to output the cdr values", type=str)
    parser.add_argument("--is_training", help="a boolean value indicating if the evaluation is performed on training data or not", type=str, default='False')
    args = parser.parse_args()

    # call the "main" function
    evaluate_ensemble_top_ranked_models_for_classification(args.ensemble_folder, args.gt_folder, args.output_folder, parse_boolean(args.is_training))