from GrammarGrep import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    regex = 'if len(;id) > 0:'

    code = '''def f(z: set):
        x = []
        y = "hello world"
        for i in range(32):
            if len(x) > 0:
                return 0
            if len(y) > 0:
                x += 1
                return 1
    '''

    grammerGrep = GrammarGrep()
    grammerGrep.load_code(code)
    grammerGrep.match(regex)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
