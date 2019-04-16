
class Alert:
    def __init__(self, code, obj=None, descr='', help=''):
        self.code = code
        self.descr = descr
        self.help = help
        self.url = 'https://psychopy.org/issues/{}.html'.format(self.code)
        self.obj = obj

    def __str__(self):
        return "{} ({})".format(self.descr, self.url)

    def __repr__(self):
        return ("Alert(code={}, obj={}, descr={}, help={})"\
                .format(self.code, self.obj, self.descr, self.help)
                )
