from IPython.display import IFrame, display_javascript, display_html
from IPython.core.magic import Magics, magics_class, cell_magic
import base64
import re
import json


@magics_class
class IHtmlMagics(Magics):

    var_re = re.compile(r'%%(\w+)(\|\w+)?%%')
    
    def __init__(self, shell):
        super(IHtmlMagics, self).__init__(shell)
        self.js = {}
        self.css = {}

    def var_replace(self, match):
        if match.group(2) == '|jsdoc':
            return "<script>%s</script>" % self.js.get(match.group(1), '')
        if match.group(2) == '|cssdoc':
            return "<style>%s</style>" % self.css.get(match.group(1), '')
        
        if match.group(1) not in self.shell.user_ns:
            return match.group(0)

        val = self.shell.user_ns[match.group(1)]
        if match.group(2) == '|json':
            try:
                return json.dumps(val)
            except TypeError as e:
                return json.dumps(str(e))  # Make sure it's quoted, so it's valid JS

        return str(val)

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
