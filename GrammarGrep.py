import ast
import RegExParser


class GrammarGrep:
    def __init__(self):
        self.code = None
        self.labels = None

    def match_all(self, regex):
        nfa = RegExParser.regex_to_nfa(regex)
        return nfa.check_all(self.code, self.labels)

    def match_first(self, regex):
        nfa = RegExParser.regex_to_nfa(regex)
        return nfa.check_first(self.code, self.labels)

    def load_code(self, code: str):
        labels = {}

        class LabelVisitor(ast.NodeVisitor):
            def generic_visit(self, node: ast.AST):
                if isinstance(node, ast.expr):
                    key = (node.lineno, node.col_offset)
                    value = ("expr_type", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.stmt):
                    key = (node.lineno, node.col_offset)
                    value = ("stmt_type", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Name):
                    key = (node.lineno, node.col_offset)
                    value = ("id_type", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Num):
                    key = (node.lineno, node.col_offset)
                    value = ("num_type", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                if isinstance(node, ast.Str):
                    key = (node.lineno, node.col_offset)
                    value = ("str_type", node.end_lineno, node.end_col_offset)
                    labels.setdefault(key, [])
                    labels[key].append(value)
                ast.NodeVisitor.generic_visit(self, node)

        self.code = code.splitlines()
        parsed_code = ast.parse(code)
        LabelVisitor().visit(parsed_code)
        self.labels = labels
