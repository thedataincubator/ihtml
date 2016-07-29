# Copyright 2016 The Data Incubator
# ihtml is distributed under the terms of the BSD 3-Clause License
# https://github.com/thedataincubator/ihtml

from IPython.display import IFrame, display_javascript, display_html
from IPython.core.magic import Magics, magics_class, cell_magic
import base64
import re
import json


@magics_class
class IHtmlMagics(Magics):

    var_re = re.compile(r'{{\s*(\w+)\s*(?:\|\s*(\w+)\s*)?}}')

    def __init__(self, shell):
        super(IHtmlMagics, self).__init__(shell)
        self.js = {}
        self.css = {}

    def var_replace(self, match):
        as_json = (match.group(2) == 'json')
        if not match.group(2) or as_json:
            if match.group(1) in self.shell.user_ns:
                val = self.shell.user_ns[match.group(1)]
                if as_json:
                    try:
                        return val.to_json()
                    except AttributeError:
                        try:
                            return json.dumps(val)
                        except TypeError as e:
                            return json.dumps(str(e))  # Make sure it's quoted, so it's valid JS
                else:
                    return str(val)
        elif match.group(2) == 'jsdoc' and match.group(1) in self.js:
            return "<script>%s</script>" % self.js[match.group(1)]
        elif match.group(2) == 'cssdoc' and match.group(1) in self.css:
            return "<style>%s</style>" % self.css[match.group(1)]

        return match.group(0)

    @cell_magic
    def ihtml(self, line, cell):
        height = int(line or 400)
        url = "data:text/html;base64," + base64.b64encode(self.var_re.sub(self.var_replace, cell))
        display_html(IFrame(url, "100%", height))

    def save_doc(self, type_, name, value):
        name = name.strip()
        if name:
            getattr(self, type_)[name] = self.var_re.sub(self.var_replace, value)
        else:
            display_html("<div class='js-error'>Error: Must specify name for %s document" % type_
                         + " (<tt>%%%%%sdoc <i>name</i></tt>).</div>" % type_, raw=True)

    @cell_magic
    def jsdoc(self, line, cell):
        self.save_doc('js', line, cell)

    @cell_magic
    def cssdoc(self, line, cell):
        self.save_doc('css', line, cell)


ip = get_ipython()
ip.register_magics(IHtmlMagics)
display_javascript("""
function add_highlight_mode(mode, pattern) {
    var modes = IPython.CodeCell.config_defaults.highlight_modes;
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
