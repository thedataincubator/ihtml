# Copyright 2016 The Data Incubator
# ihtml is distributed under the terms of the BSD 3-Clause License
# https://github.com/thedataincubator/ihtml

from IPython.display import display_javascript
from .ihtmlmagic import IHtmlMagics


get_ipython().register_magics(IHtmlMagics)
display_javascript("""
function add_highlight_mode(mode, pattern) {
    var modes = Jupyter.CodeCell.options_default.highlight_modes;
    var mode_name = 'magic_' + mode;
    if (!modes[mode_name])
        modes[mode_name] = {};
    if (!modes[mode_name]['reg'])
        modes[mode_name]['reg'] = [];
    modes[mode_name]['reg'].push(pattern);
}
add_highlight_mode('html', /^%%ihtml/);
add_highlight_mode('javascript', /^%%jsdoc/);
add_highlight_mode('css', /^%%cssdoc/);
""", raw=True)
