function filenames = listdir(folder)
% LISTDIR Get filenames from elements inside the given folder

    % retrieve filenames from folder
    filenames = dir(folder);
    filenames = { filenames.name };
    % remove dots
    filenames(strcmp(filenames, '.')) = [];
    filenames(strcmp(filenames, '..')) = [];

end