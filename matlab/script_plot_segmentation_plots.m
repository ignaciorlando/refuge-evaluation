
% script_plot_segmentation_plots
% Plot segmentation results as box plots of Dice and MAE

%% run the configuration and setup necessary variables

close all

% run the configuration
config_plot_segmentation_plots;

% pick the indices
switch variable_to_plot
    case 'dice-optic-disc'
        rank_id = 'OpticDiscRank';
        mean_perf_id = 'MeanOpticDiscDice';
        per_image_result_id = 'Disc_Dice';
        y_label = 'Dice index (optic disc)';
    case 'dice-optic-cup'
        rank_id = 'OpticCupRank';
        mean_perf_id = 'MeanOpticCupDice';
        per_image_result_id = 'Cup_Dice';
        y_label = 'Dice index (optic cup)';
    case 'mae-cdr'
        rank_id = 'CDRRank';
        mean_perf_id = 'MAECupToDiscRatio';
        per_image_result_id = 'AE_CDR';
        y_label = 'Mean absolute error (CDR)';
end

% use the score on the final leaderboard for sorting if necessary
if sorted_from_leaderboard
    mean_perf_id = 'Score';
end

%% open the average performance

% get mean table
mean_table = readtable(fullfile(leaderboard_path, 'segmentation_leaderboard.csv'));

% extract the teams names
teams_names = table2array(mean_table(:,1));

%% sort the team names using the Dice ranking for the optic disc

% get the idx
[rank, idx] = sort(table2array(mean_table(:, strcmp(mean_table.Properties.VariableNames, rank_id))));
idx = idx(end:-1:1);
% sort the teams names
teams_names = teams_names(idx);
% sort the average performance
avg_performance = mean_table(idx, strcmp(mean_table.Properties.VariableNames, mean_perf_id));

%% plot the Dice values

% initialize the figure
figure(1);
% initialize the legend
tick_labels = cell(length(teams_names), 1);
% get the colors
colors = distinguishable_colors(length(teams_names));
% initialize the matrix of boxes to plot
values_for_plot = [];

% load the roc curve and plot current results
for i = 1 : length(teams_names)
    % load the table
    loaded_table = readtable(fullfile(input_path, teams_names{i}, 'evaluation_table_segmentation.csv'));
    % plot the curve
    if isempty(values_for_plot)
        values_for_plot = table2array(loaded_table(:, strcmp(loaded_table.Properties.VariableNames, per_image_result_id)));
    else
        values_for_plot = cat(2, values_for_plot, table2array(loaded_table(:, strcmp(loaded_table.Properties.VariableNames, per_image_result_id))));
    end
    % get current team name
    if any(teams_names{i}=='_')
        current_team_name = char(extractBefore(teams_names{i}, '_'));
    else
        current_team_name = teams_names{i};
    end
    disp(current_team_name);
    % add the team to the legend
    tick_labels{i} = current_team_name;
end

% setup the plot
boxplot(values_for_plot, 'Notch', 'on');
ax = gca;
ax.YGrid = 'on';
box on
xticklabels(tick_labels);
xtickangle(45)
xlabel('Teams');
ylabel(y_label);
% save the figure
save_current_figure(gcf, output_path, variable_to_plot, '', output_formats);
