function save_current_figure(current_figure, output_path, filename, figure_tag, formats)

    % iterate for each of the file formats
    for i = 1 : length(formats)
        
        % the current path will be output_path / unit / some tag / image
        % format
        if ~strcmp(figure_tag, '')
            current_path = fullfile(output_path, figure_tag, formats{i});
        else
            current_path = fullfile(output_path, formats{i});
        end
        mkdir(current_path);
        % full output filename
        full_output_filename = fullfile(current_path, filename);
        if strcmp(formats{i}, 'fig')
            savefig(current_figure, full_output_filename);
        else
            current_figure.PaperPositionMode = 'auto';
            fig_pos = current_figure.PaperPosition;
            current_figure.PaperSize = [fig_pos(3) fig_pos(4)];
            print(current_figure, fullfile(current_path, filename), ['-d', formats{i}]);
        end
        
    end

end