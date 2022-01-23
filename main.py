from GrammarGrep import *

if __name__ == '__main__':

    regex = 'if len(;id) > 0:;|;(return ;id;)'

    code = '''def f(z: set):
        x = []
        y = "hello world"
        for i in range(32):
            if len(x) > 0:
                return 0
            if len(y) > 0:
                x += 1
                return x
    '''

    grammerGrep = GrammarGrep()
    grammerGrep.load_code(code)
    print(grammerGrep.match(regex))
    print(grammerGrep.replace(regex, ["yield 3"]))
