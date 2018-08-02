
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
    ranking_for_optic_cup, optic_cup_dice = best_is_highest(metrics, results, 'Mean optic cup Dice')
    ranking_for_optic_disc, optic_disc_dice = best_is_highest(metrics, results, 'Mean optic disc Dice')
    ranking_for_cup_to_disc_ratio, cdr = best_is_lowest(metrics, results, 'MAE cup to disc ratio')

    # sum all the rankings and rank as the best the one with the highest sum
    scores = np.zeros(len(teams))
    scores_optic_cup = np.zeros(len(teams))
    scores_optic_disc = np.zeros(len(teams))
    scores_cup_to_disc_ratio = np.zeros(len(teams))
    for i in range(0, len(teams)):
        scores_optic_cup[i] = ranking_for_optic_cup.index(i)
        scores_optic_disc[i] = ranking_for_optic_disc.index(i)
        scores_cup_to_disc_ratio[i] = ranking_for_cup_to_disc_ratio.index(i) 
    scores = 0.35 * scores_optic_cup + 0.25 * scores_optic_disc + 0.4 * scores_cup_to_disc_ratio
    
    # sort them
    sorted_indices = list((np.argsort(scores.tolist())))

    # sort everything
    teams = np.asarray(teams, dtype=np.str)[sorted_indices].tolist()

    scores = np.asarray(scores)[sorted_indices]

    scores_optic_cup = np.asarray(scores_optic_cup)[sorted_indices]
    scores_optic_disc = np.asarray(scores_optic_disc)[sorted_indices]
    scores_cup_to_disc_ratio = np.asarray(scores_cup_to_disc_ratio)[sorted_indices]

    sorted_optic_cup_dice = np.asarray(get_metric(metrics, results, 'Mean optic cup Dice'))[sorted_indices]
    sorted_optic_disc_dice = np.asarray(get_metric(metrics, results, 'Mean optic disc Dice'))[sorted_indices]
    sorted_cdr = np.asarray(get_metric(metrics, results, 'MAE cup to disc ratio'))[sorted_indices]

    # join all the scores in a single matrix
    all_scores = np.zeros( (len(teams), 7) )
    all_scores[:,0] = scores+1
    all_scores[:,1] = scores_optic_cup+1
    all_scores[:,2] = scores_optic_disc+1
    all_scores[:,3] = scores_cup_to_disc_ratio+1
    all_scores[:,4] = sorted_optic_cup_dice
    all_scores[:,5] = sorted_optic_disc_dice
    all_scores[:,6] = sorted_cdr

    return teams, all_scores, ['Team', 'Score', 'Optic cup rank', 'Optic disc rank', 'CDR rank', 'Mean optic cup Dice', 'Mean optic disc Dice', 'MAE cup to disc ratio']



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

    reference_sensitivity = np.asarray(results[:, metrics.index('Reference Sensitivity')])[sorted_indices]

    all_scores = np.zeros( (len(teams), 2) )
    all_scores[:,0] = scores
    all_scores[:,1] = reference_sensitivity

    return teams, all_scores, ['Team', 'AUC', 'Reference Sensitivity']



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



def final_leaderboard(metrics, teams, results):
    '''
    Sort the teams for the final leaderboard

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        teams: a list of strings with the names of the teams participating
        results: a 2D numpy matrix with all the evaluation metrics
    Output:
        teams: the list of the teams, but sorted
        scores: a numpy array with the scores
        header: the names for the 2 columns
    '''

    # get the ranks for segmentation and classification
    teams_segmentation, _, _ = segmentation_leaderboard(metrics, teams, results)
    scores_segmentation = list(range(1, len(teams_segmentation)+1))
    teams_classification, _, _ = classification_leaderboard(metrics, teams, results)
    scores_classification = list(range(1, len(teams_classification)+1))

    # check if the size is different
    if not ( len(teams_segmentation) == len(teams_classification) ):
        # remove those that didn't participated in everything
        if len(teams_segmentation) < len(teams_classification):
            to_remove = list(set(teams_classification) - set(teams_segmentation))
            for i in range(len(to_remove)):
                idx = teams_classification.index(to_remove[i])
                del teams_classification[idx]
                del scores_classification[idx]
            teams = teams_segmentation
        else:
            to_remove = list(set(teams_segmentation) - set(teams_classification))
            for i in range(len(to_remove)):
                idx = teams_segmentation.index(to_remove[i])
                del teams_segmentation[idx]
                del scores_segmentation[idx]
            teams = teams_classification

    scores_segmentation = np.asarray(scores_segmentation)
    scores_classification = np.asarray(scores_classification)

    # compute the scores
    scores = np.zeros(len(teams))
    for i in range(len(teams)):
        idx_segm = teams_segmentation.index(teams[i])
        idx_class = teams_classification.index(teams[i])
        scores[i] = 0.6 * scores_segmentation[idx_segm] + 0.4 * scores_classification[idx_class]
    # sort the scores in ascending order
    sorted_indices = list((np.argsort(scores.tolist())))
    # sort everything
    teams = np.asarray(teams, dtype=np.str)[sorted_indices].tolist()
    final_scores = np.zeros((len(teams),3))
    final_scores[:,0] = scores[sorted_indices]
    for i in range(len(teams)):
        final_scores[i,1] = scores_segmentation[teams_segmentation.index(teams[i])]
        final_scores[i,2] = scores_classification[teams_classification.index(teams[i])]
        
    return teams, final_scores, ['Team', 'Scores', 'Segmentation rank', 'Classification rank']



def get_metric(metrics, results, selected_metric):
    '''
    Retrieve the selected metric from a table of results

    Input:
        metrics: a list of the metrics in results, in the same order than the columns of results
        results: a 2D numpy matrix with all the evaluation metrics
        selected_metric: a string representing the selected metric
    Output:
        metric: a column vector with the selected metric
    '''

    return results[:,metrics.index(selected_metric)]


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
    metric_to_sort = get_metric(metrics, results, selected_metric)

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
        unsorted_metric: a numpy array with the evaluation metric as retrieved, without being sorted
    '''

    # sort it in ascending order
    sorted_indices, sorted_metric = best_is_lowest(metrics, results, selected_metric)
    # invert the indices
    sorted_indices = list(reversed(sorted_indices))
    # invert the order of the metrics
    sorted_metric = list(reversed(sorted_metric))
    
    return sorted_indices, sorted_metric