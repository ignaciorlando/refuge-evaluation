
% script_plot_roc_curves
% Plot ROC curves for all the teams

close all

%% run the configuration and setup necessary variables

% run the configuration
config_plot_roc_curves;

% retrieve teams names
teams_names = listdir(input_path);

% check for baselines
is_baseline = regexpcmp(teams_names, '__BASELINE__*');
if any(is_baseline)
    baselines = teams_names(is_baseline);
    teams_names(is_baseline) = [];
end

%% sort the team names by their AUC and load the results of the baselines

% initialize the array of auc values
auc_values = zeros(length(teams_names), 1);
auc_values_baselines = zeros(length(baselines), 1);

% load all the auc values
for i = 1 : length(teams_names)
    % load the roc curve
    loaded_roc = load(fullfile(input_path, teams_names{i}, 'roc_curve.mat'));
    % assign the auc value
    auc_values(i) = loaded_roc.auc;
end

% same for the baselines
for j = 1 : length(baselines)
    % load the roc curve
    loaded_roc = load(fullfile(input_path, baselines{j}, 'roc_curve.mat'));
    % assign the auc value
    auc_values_baselines(j) = loaded_roc.auc;
end

% sort the auc values and retrieve the indices
[auc_values, idx] = sort(auc_values);
idx = idx(end:-1:1);
auc_values = auc_values(end:-1:1);
% sort the team names
teams_names = teams_names(idx);

%% plot the ROC curves

% initialize the figure
figure(1);
close all
hold on
% initialize the legend
legend_for_roc = cell(length(teams_names) + length(baselines), 1);
% get the colors
colors = distinguishable_colors(length(teams_names) + length(baselines));

% load the roc curve and plot current results
for i = 1 : length(teams_names)
    % load the roc curve
    loaded_roc = load(fullfile(input_path, teams_names{i}, 'roc_curve.mat'));
    % plot the curve
    plot(loaded_roc.fpr, loaded_roc.tpr, 'LineWidth', 1.5);%, 'Color', colors(i,:));
    % get current team name
    if any(teams_names{i}=='_')
        current_team_name = char(extractBefore(teams_names{i}, '_'));
    else
        current_team_name = teams_names{i};
    end
    disp(current_team_name);
    % add the team to the legend
    legend_for_roc{i} = [current_team_name, ' - AUC=', num2str(round(auc_values(i), 4))];
end

i=i+1;
for j = 1 : length(baselines)
    % load the roc curve
    loaded_roc = load(fullfile(input_path, baselines{j}, 'roc_curve.mat'));
    % plot the curve
    plot(loaded_roc.fpr, loaded_roc.tpr, 'LineWidth', 1.5, 'LineStyle', ':');%, 'Color', colors(i,:), 'LineStyle', ':');
    switch baselines{j}
        case '__BASELINE__VCDR'
            current_baseline_name = 'vCDR from ground truth';
        case '__BASELINE__ENSEMBLE'
            current_baseline_name = 'Ensemble';
    end
    disp(current_baseline_name);
    % add the baseline to the legend
    legend_for_roc{i} = [current_baseline_name, ' - AUC=', num2str(round(auc_values_baselines(j), 4))];
    i=i+1;
end

% setup the plot
box on
grid on
xlim([0.0 1.0]);
xticks(0.0:0.1:1.0);
ylim([0.0 1.0]);
xlabel('FPR (1 - Specificity)');
ylabel('TPR');
legend(legend_for_roc, 'Location', 'southeast');
% save the figure
save_current_figure(gcf, output_path, 'roc_curves', '', output_formats);

% if zoom is required
if zoom_plot
    % zoom in
    xlim([0.0 0.5]);
    xticks(0.0:0.05:0.5);
    ylim([0.5 1.0]);
    yticks(0.5:0.05:1.0);
    % save the figure
    save_current_figure(gcf, output_path, 'roc_curves_zoomed', '', output_formats);
end

%% plot only the top N teams

% initialize the figure
figure(2);
hold on
% initialize the legend
legend_for_roc = cell(top_N + length(baselines), 1);
% get the colors
new_colors = cat(1, colors(1:top_N,:), colors(size(colors,1)-length(baselines)+1:end,:));

% load the roc curve and plot current results
for i = 1 : top_N
    % load the roc curve
    loaded_roc = load(fullfile(input_path, teams_names{i}, 'roc_curve.mat'));
    % plot the curve
    plot(loaded_roc.fpr, loaded_roc.tpr, 'LineWidth', 1.5, 'LineStyle', '-');%, 'Color', new_colors(i,:));
    % get current team name
    if any(teams_names{i}=='_')
        current_team_name = char(extractBefore(teams_names{i}, '_'));
    else
        current_team_name = teams_names{i};
    end
    disp(current_team_name);
    % add the team to the legend
    legend_for_roc{i} = [current_team_name, ' - AUC=', num2str(round(auc_values(i), 4))];
end

i=i+1;
for j = 1 : length(baselines)
    % load the roc curve
    loaded_roc = load(fullfile(input_path, baselines{j}, 'roc_curve.mat'));
    % plot the curve
    plot(loaded_roc.fpr, loaded_roc.tpr, 'LineWidth', 1.5, 'LineStyle', ':');%, 'Color', new_colors(i,:));%, 'LineStyle', ':');
    switch baselines{j}
        case '__BASELINE__VCDR'
            current_baseline_name = 'vCDR from ground truth';
        case '__BASELINE__ENSEMBLE'
            current_baseline_name = 'Ensemble';
    end
    disp(current_baseline_name);
    % add the baseline to the legend
    legend_for_roc{i} = [current_baseline_name, ' - AUC=', num2str(round(auc_values_baselines(j), 4))];
    i=i+1;
end

% setup the plot
box on
grid on
xlim([0.0 1.0]);
xticks(0.0:0.1:1.0);
ylim([0.0 1.0]);
xlabel('FPR (1 - Specificity)');
ylabel('TPR');
legend(legend_for_roc, 'Location', 'southeast');
% save the figure
save_current_figure(gcf, output_path, strcat('top_', num2str(top_N), '_roc_curves'), '', output_formats);

% if zoom is required
if zoom_plot
    % zoom in
    xlim([0.0 0.5]);
    xticks(0.0:0.05:0.5);
    ylim([0.5 1.0]);
    yticks(0.5:0.05:1.0);
    % save the figure
    save_current_figure(gcf, output_path, strcat('top_', num2str(top_N), '_roc_curves_zoomed'), '', output_formats);
end