import numpy as np

from os import path, makedirs

from util.file_management import read_fovea_location_results, read_gt_fovea_location, sort_coordinates_by_filename, save_csv_fovea_location_table, save_csv_fovea_location_performance



def euclidean_distance(gt_coordinates, fovea_coordinates):
    '''
    Measure the Euclidean distance between the fovea coordinates of the gt and the fovea

    Input:
        gt_coordinates: a 2D numpy array of coordinates for the fovea, according to the ground truth
        fovea_coordinates: a 2D numpy array of coordinates for the fovea, according to the algorithm
    Output:
        euclidean_distances: a 1D numpy array with the Euclidean distance
    '''

    # compute the euclidean distance
    euclidean_distances = np.sqrt(np.sum((gt_coordinates - fovea_coordinates)**2, axis=1))

    return euclidean_distances



def evaluate_fovea_location_results(prediction_filename, gt_filename, output_path=None, is_training=False):
    '''
    Evaluate the results of a fovea location algorithm

    Input:
        prediction_filename: full path with file name to a .csv file with the fovea location gt annotations
        gt_filename: full path with file name to a .csv file with the fovea location results of an automated algorithm
        [output_path]: a folder where the results will be saved. If not provided, the results are not saved
        [is_training]: a boolean indicating whether we are using training data or not
    '''

    # read the prediction filename
    image_filenames, predicted_coordinates = read_fovea_location_results(prediction_filename)
    # read the gt filename
    gt_image_filenames, gt_coordinates = read_gt_fovea_location(gt_filename, is_training)

    # sort the gt filenames using the same order as predicted
    gt_coordinates = sort_coordinates_by_filename(image_filenames, gt_image_filenames, gt_coordinates)

    # get the distance between the gt and the predicted coordinates
    euclidean_distances = euclidean_distance(gt_coordinates, predicted_coordinates)

    # get the mean value
    mean_euclidean_distances = np.mean(euclidean_distances)
    # print the auc
    print('Mean Euclidean distance = {}'.format(str(mean_euclidean_distances)))

    # if the output path is given, export the results
    if not (output_path is None):

        # create the folder if necessary
        if not path.exists(output_path):
            makedirs(output_path)

        # save a CSV with the fovea location table
        table_filename = path.join(output_path, 'evaluation_table_fovea_location.csv')
        save_csv_fovea_location_table(table_filename, image_filenames, euclidean_distances)

        # save a CSV with the
        fovea_location_results_filename = path.join(output_path, 'evaluation_fovea_location.csv')
        save_csv_fovea_location_performance(fovea_location_results_filename, mean_euclidean_distances)

    return mean_euclidean_distances