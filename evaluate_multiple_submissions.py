
from os import path, makedirs

from shutil import rmtree

from evaluate_single_submission import evaluate_single_submission
from util.file_management import unzip_submission, get_filenames, parse_boolean, export_table_of_results, export_table_of_results



def evaluate_multiple_submissions(submissions_folder, gt_folder, uncompressed_files_folder, output_path, is_training=False):
    '''
    Input:
        submissions_folder:
        gt_folder:
        [is_training]:
    '''

    # identify all the zip files in the submissions folder
    submission_files = get_filenames(submissions_folder, 'zip')

    # initialize the list of teams
    teams = []
    # initialize the lists of results
    segmentation_results = []
    classification_results = []
    fovea_detection_results = []
    # initialize the output folders
    if path.exists(uncompressed_files_folder):
        rmtree(uncompressed_files_folder)
    makedirs(uncompressed_files_folder)
    if not path.exists(output_path):
        makedirs(output_path)

    # iterate for each submission file
    for i in range(len(submission_files)):

        # get current team name
        current_team_name = submission_files[i]
        current_team_name = current_team_name[:-4]
        print('\n' + current_team_name)
        print('-------------------------------')
        # generate a new output path for the current submission
        current_results_folder = path.join(uncompressed_files_folder, current_team_name)
        if not path.exists(current_results_folder):
            makedirs(current_results_folder)
        
        # unzip the submission
        unzip_submission(path.join(submissions_folder, submission_files[i]), current_results_folder)

        # get current results
        current_segmentation_perf, current_classification_perf, current_fovea_location_perf = evaluate_single_submission(current_results_folder, gt_folder, 
                                                                                                                         output_path=current_results_folder, export_table=True, is_training=is_training, team_name=current_team_name)

        # attach everything to the arrays
        teams = teams + [ current_team_name ]
        segmentation_results = segmentation_results + [ current_segmentation_perf ]
        classification_results = classification_results + [ current_classification_perf ]
        fovea_detection_results = fovea_detection_results + [ current_fovea_location_perf ]

    # export a table of results (unordered)
    export_table_of_results(path.join(output_path, 'table_of_results.csv'),
                            teams, segmentation_results, classification_results, fovea_detection_results)



import argparse
import sys

if __name__ == '__main__':

    # create an argument parser to control the input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("submissions_folder", help="full path to the submitted results", type=str)
    parser.add_argument("gt_folder", help="full path to the ground truth files", type=str)
    parser.add_argument("uncompressed_files_folder", help="temporary folder for saving the uncompressed results", type=str)
    parser.add_argument("output_path", help="a folder where the results will be saved", type=str)
    parser.add_argument("--is_training", help="a boolean value indicating if the evaluation is performed on training data or not", type=str, default='False')
    args = parser.parse_args()

    # call the "main" function
    evaluate_multiple_submissions(args.submissions_folder, args.gt_folder, args.uncompressed_files_folder, args.output_path, parse_boolean(args.is_training))
