import ast
import RegExParser


class GrammarGrep:
    def __init__(self):
        self.code = None
        self.labels = None

    def match_all(self, regex):
        pass

    def match_first(self, regex):
        nfa = RegExParser.regex_to_nfa(regex)
        nfa.check(self.code, self.labels, idx)

    def load_code(self, code: str):
        labels = {}

        class LabelVisitor(ast.NodeVisitor):
            def generic_visit(self, node: ast.AST):
                if isinstance(node, ast.expr):
                    key = (node.lineno, node.col_offset)
                    value = ("expr", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.stmt):
                    key = (node.lineno, node.col_offset)
                    value = ("stmt", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Name):
                    key = (node.lineno, node.col_offset)
                    value = ("id", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Num):
                    key = (node.lineno, node.col_offset)
                    value = ("num", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Str):
                    key = (node.lineno, node.col_offset)
                    value = ("str", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                ast.NodeVisitor.generic_visit(self, node)

        self.code = code
        parsed_code = ast.parse(code)
        LabelVisitor().visit(parsed_code)
        self.labels = labels
