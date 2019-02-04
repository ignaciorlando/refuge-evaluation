
function colors_p = get_color_gradient(n_colors, source, target)

    if nargin < 2
        source = [10, 28, 28]/255;
        target = [120, 172, 110]/255;
    end
    
    colors_p = [linspace(source(1),target(1),n_colors)', linspace(source(2),target(2),n_colors)', linspace(source(3),target(3),n_colors)'];

end