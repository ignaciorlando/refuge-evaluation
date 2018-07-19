
import numpy as np


def segmentation_leaderboard(metrics, teams, results):
    '''
    Sort the teams according to the segmentation leaderboard criterion

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        teams: a list of strings with the names of the teams participating
        results: a 2D numpy matrix with all the evaluation metrics
    Output:
        teams: the list of the teams, but sorted
        scores: a numpy matrix with 4 columns: overall segmentation score, ranking for optic cup, ranking for optic disc and ranking for cup to disc ratio
        header: the names for the 4 columns
    '''

    # identify indices of elements with NaNs
    idx = np.where(np.logical_not(np.isnan(results[:,metrics.index('Mean optic cup Dice')])))[0]
    # delete them from teams
    teams = np.asarray(teams)[idx]
    # delete rows
    results = results[idx,:]

    # rank for each segmentation metric
    ranking_for_optic_cup, _ = best_is_highest(metrics, results, 'Mean optic cup Dice')
    ranking_for_optic_disc, _ = best_is_highest(metrics, results, 'Mean optic disc Dice')
    ranking_for_cup_to_disc_ratio, _ = best_is_lowest(metrics, results, 'MAE cup to disc ratio')

    # sum all the rankings and rank as the best the one with the highest sum
    scores = (np.asarray(ranking_for_optic_cup) + np.asarray(ranking_for_optic_disc) + np.asarray(ranking_for_cup_to_disc_ratio)).tolist()
    sorted_indices = list((np.argsort(scores)))

    # sort everything
    teams = np.asarray(teams, dtype=np.str)[sorted_indices].tolist()
    scores = np.asarray(scores)[sorted_indices]
    ranking_for_optic_cup = np.asarray(ranking_for_optic_cup)[sorted_indices]
    ranking_for_optic_disc = np.asarray(ranking_for_optic_disc)[sorted_indices]
    ranking_for_cup_to_disc_ratio = np.asarray(ranking_for_cup_to_disc_ratio)[sorted_indices]

    # join all the scores in a single matrix
    all_scores = np.zeros( (len(teams), 4) )
    all_scores[:,0] = scores
    all_scores[:,1] = ranking_for_optic_cup
    all_scores[:,2] = ranking_for_optic_disc
    all_scores[:,3] = ranking_for_cup_to_disc_ratio

    return teams, all_scores, ['Team', 'Score', 'Optic cup rank', 'Optic disc rank', 'CDR rank']



def classification_leaderboard(metrics, teams, results):
    '''
    Sort the teams according to the classification leaderboard criterion (highest AUC)

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        teams: a list of strings with the names of the teams participating
        results: a 2D numpy matrix with all the evaluation metrics
    Output:
        teams: the list of the teams, but sorted
        scores: a numpy array with the AUC values sorted in descending order
        header: the names for the 2 columns
    '''

    # identify indices of elements with NaNs
    idx = np.where(np.logical_not(np.isnan(results[:,metrics.index('AUC')])))[0]
    # delete them from teams
    teams = np.asarray(teams)[idx]
    # delete rows
    results = results[idx,:]

    # rank for the auc
    sorted_indices, scores = best_is_highest(metrics, results, 'AUC')

    # sort everything
    teams = np.asarray(teams, dtype=np.str)[sorted_indices].tolist()

    return teams, scores, ['Team', 'AUC']



def fovea_location_leaderboard(metrics, teams, results):
    '''
    Sort the teams according to the fovea location leaderboard criterion (lowest distance)

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        teams: a list of strings with the names of the teams participating
        results: a 2D numpy matrix with all the evaluation metrics
    Output:
        teams: the list of the teams, but sorted
        scores: a numpy array with the Euclidean distances to the gt fovea sorted in descending order
        header: the names for the 2 columns
    '''

    # identify indices of elements with NaNs
    idx = np.where(np.logical_not(np.isnan(results[:,metrics.index('Mean Euclidean distance')])))[0]
    # delete them from teams
    teams = np.asarray(teams)[idx]
    # delete rows
    results = results[idx,:]

    # rank for the auc
    sorted_indices, scores = best_is_lowest(metrics, results, 'Mean Euclidean distance')

    # sort everything
    teams = np.asarray(teams, dtype=np.str)[sorted_indices].tolist()

    return teams, scores, ['Team', 'Mean Euclidean distance']
    


def best_is_lowest(metrics, results, selected_metric):
    '''
    Get a list of indices to sort the teams according to a given metric, considering that
    the lowest result is the best one

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        results: a 2D numpy matrix with all the evaluation metrics
        selected_metric: a string representing the selected metric
    Output:
        sorted_indices: indices sorted in ascending order
        sorted_metric: a numpy array with the evaluation metric used for sorting, sorted
    '''

    # get the values of the metric to sort
    metric_to_sort = results[:,metrics.index(selected_metric)]

    # get the sorted indices
    sorted_indices = np.argsort(metric_to_sort).tolist()
    # sort the metric
    sorted_metric = metric_to_sort[sorted_indices]

    return sorted_indices, sorted_metric



def best_is_highest(metrics, results, selected_metric):
    '''
    Get a list of indices to sort the teams according to a given metric, considering that
    the highest result is the best one

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        results: a 2D numpy matrix with all the evaluation metrics
        selected_metric: a string representing the selected metric
    Output:
        sorted_indices: indices sorted in descending order
        sorted_metric: a numpy array with the evaluation metric used for sorting, sorted
    '''

    # sort it in ascending order
    sorted_indices, _ = best_is_lowest(metrics, results, selected_metric)
    # invert the indices
    sorted_indices = list(reversed(sorted_indices))

    # get the values of the metric to sort
    metric_to_sort = results[:,metrics.index(selected_metric)]
    # sort the metric
    sorted_metric = metric_to_sort[sorted_indices]
    
    return sorted_indices, sorted_metric