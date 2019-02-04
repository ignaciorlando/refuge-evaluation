function TF = regexpcmp(str,expr,option)
% FUNCTION regexpcmp
% Checks if a string matches a regular expression.  Similar behavior to strcmp.
%
% Syntax:
% TF = regexpcmp(str,expr)
% TF = regexpcmp(str,expr,'ignorecase')
%
% str must be a string or cell array of strings
% expr must be a valid regular expression
% 'ignorecase' option ignores the case of the regular expression
%
% TF is a logical array which is true when a match is found, false otherwise
%
%
% See also: strcmp, regexp
%

% Created by: Jason Kaeding
%       Date: 22 Jul 2010

%% Revision Information

%% Check inputs
error(nargchk(2,3,nargin,'struct'));
regfun = @regexp;
if nargin > 2
    switch lower(option)
        case 'ignorecase'
            regfun = @regexpi;
        otherwise
            error('regexpcmp:InvalidOption','Invalid option: %s',option);
    end
end
if iscellstr(str) || ischar(str)
    str = cellstr(str);
else
    error('regexpcmp:InvalidInput','Input must be a string or cell array of strings.');
end
if ~ischar(expr)
    error('regexpcmp:InvalidRegExp','Regular expression must be a string.');
end

%% Run comparison
TF = ~cellfun('isempty',feval(regfun,cellstr(str),expr,'match','once'));