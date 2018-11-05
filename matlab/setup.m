
% setup.m
% use this script to setup the matlab code
% --------------------------------------------

% add the utils folder to the path
addpath(genpath('util'));

% add the configuration folder if it does not exist
if exist('config', 'dir') == 0
    mkdir('config');
end

% copy the configuration files only if they don't exist in the /config
% folder
all_config_files = listdir('default_config/*.m');
for i = 1 : length(all_config_files)
    % copy the file if it does not exist on the destination folder
    if exist(fullfile('config', all_config_files{i}), 'file') == 0
        copyfile(fullfile('default_config', all_config_files{i}), 'config');
    end
end

% add the config files path to the path
addpath(genpath('config'));