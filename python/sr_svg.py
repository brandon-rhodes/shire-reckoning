class SVG(object):
    def __init__(self, f, width, height, extra=''):
        self.f = f                 # f should be a file open for write
        self.f.write("""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN"
 "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg
 id="svg1"
 xmlns="http://www.w3.org/2000/svg"
 width="%dpx"
 height="%dpx" %s>""" % (width, height, extra))

    def write(self, *args):
        self.f.write(''.join(args))

    def close(self):
        self.write('</svg>\n')

    def element(self, name, content=None, **kargs):
        attributes = ''.join([ ' %s="%s"' % (n.replace('_', '-'), v)
                               for n, v in kargs.items() ])
        if not content:
            self.write('<', name, attributes, '/>')
        else:
            self.write('<', name, attributes, '>', content, '</', name, '>')

    def group(self, **kargs):
        attributes = ''.join([ ' %s="%s"' % (n.replace('_', '-'), v)
                               for n, v in kargs.items() ])
        self.write('<g', attributes, '>')

    def endgroup(self):
        self.write('</g>')
