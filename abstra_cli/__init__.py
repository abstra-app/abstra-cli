import fire


class CLI(object):

    def double(self, number):
        return 2 * number

    def hello(self, name="World"):
        return "Hello %s!" % name


def main():
    fire.Fire(CLI)
