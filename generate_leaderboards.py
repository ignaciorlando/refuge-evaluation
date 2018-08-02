
from os import path

from util.file_management import read_table_of_results, export_ranking
from util.leaderboard_criteria import segmentation_leaderboard, classification_leaderboard, fovea_location_leaderboard, final_leaderboard


def generate_leaderboard(results_table_filename, leaderboard_filename, criterion):
    '''
    Generate a leaderboard based on a given criterion
    
    Input:
        results_table_filename: full path and filename to the CSV file with the results
        leaderboard_filename: full path and filename of the output CSV leaderboard filename
        criterion: the leaderboard criterion (as retrieved from util.leaderboard_criteria)
    '''

    # read the table of results
    metrics, teams, results = read_table_of_results(results_table_filename)

    # sort according to the provided criterion
    sorted_teams, sorted_results, header = criterion(metrics, teams, results)

    # export the ranking
    export_ranking(leaderboard_filename, header, sorted_teams, sorted_results)




import argparse
import sys

if __name__ == '__main__':

    # create an argument parser to control the input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("results_table_filename", help="full path and filename to the CSV file with the results", type=str)
    parser.add_argument("output_path", help="output path", type=str)
    args = parser.parse_args()

    # call the "main" function
    generate_leaderboard(args.results_table_filename, path.join(args.output_path, 'segmentation_leaderboard.csv'), segmentation_leaderboard)
    generate_leaderboard(args.results_table_filename, path.join(args.output_path, 'classification_leaderboard.csv'), classification_leaderboard)
    generate_leaderboard(args.results_table_filename, path.join(args.output_path, 'fovea_location_leaderboard.csv'), fovea_location_leaderboard)
    generate_leaderboard(args.results_table_filename, path.join(args.output_path, 'final_leaderboard.csv'), final_leaderboard)