
class Issue:
    def __init__(self, code, descr, help):
        self.code = code
        self.descr = descr
        self.help = help
        self.url = 'https://psychopy.org/issues/{}.html'.format(self.code)

    def __str__(self):
        return "{} ({})".format(self.descr, self.url)

    def __repr__(self):
        return "Issue({}, {}, {})".format(self.code, self.descr, self.help)
