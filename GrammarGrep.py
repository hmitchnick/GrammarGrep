import ast


class GrammarGrep:
    def __init__(self):
        self.code = None
        self.parsed_code = None

    def load_code(self, code: str):
        self.code = code
        self.parsed_code = ast.parse(code)

    def match(self, expr: str):
        return []
