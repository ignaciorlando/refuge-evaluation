
% config_plot_segmentation_plots
% configuration file for script_plot_segmentation_plots

% path to the folder with each team results
input_path = '../../submissions/test-temp';
% path to the folder with the leaderboard
leaderboard_path = '../../submissions/test-results';

% path to the folder where the figure will be saved
output_path = '../../submissions/test-figures';
% output formats
output_formats = {'fig', 'pdf'};

% pick the variable that you want to plot
variable_to_plot = 'dice-optic-disc';
%variable_to_plot = 'dice-optic-cup';
%variable_to_plot = 'mae-cdr';

% boolean indicating if the teams will be sorted using the final score on
% the leaderboard or not
sorted_from_leaderboard = false;
%sorted_from_leaderboard = true;