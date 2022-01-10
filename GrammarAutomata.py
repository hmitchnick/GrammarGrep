class GrammarAutomata:
    class Node:
        def __init__(self):
            self.edges = []

        def add_edge(self, node_dst, cond):
            self.edges.append((node_dst, cond))

    class Cond:
        # types are str, type_id, type_stmt, type_expr, type_str, type_num, epsilon
        def __init__(self, type, str=""):
            self.type = type
            self.str = str

        # returns if satisfied and index after passing
        def check(self, codelines, labels: dict, lineno, col_offset):
            if self.type == "str":
                return codelines[lineno].startswith(self.str, col_offset), [(lineno, col_offset + len(self.str))]
            else:
                matchs = []
                if (lineno, col_offset) in labels:
                    list_types = labels[(lineno, col_offset)]
                    for (type, end_lineno, end_col_offset) in list_types:
                        if type == self.type:
                            matchs.append((end_lineno, end_col_offset))
                if len(matchs) > 0:
                    return True, matchs
                else:
                    return False, []

    def __init__(self):
        self.nodes = []

    @staticmethod
    def create_automata_matching(string):
        ga = GrammarAutomata()
        ga.add_node()
        ga.add_node()
        cond = GrammarAutomata.Cond("str", string)
        ga.add_edge(0, 1, cond)
        return ga

    @staticmethod
    def create_automata_or(ga0, ga1):
        ga = GrammarAutomata()
        ga.nodes = ga0.nodes + ga1.nodes
        ga.add_edge(0, len(ga0.nodes), GrammarAutomata.Cond("epsilon"))
        ga.add_edge(len(ga0.nodes) - 1, len(ga.nodes) - 1, GrammarAutomata.Cond("epsilon"))
        return ga

    @staticmethod
    def create_automata_star(ga0):
        ga = GrammarAutomata.create_automata_plus(ga0)
        ga = GrammarAutomata.create_automata_question(ga)
        return ga

    @staticmethod
    def create_automata_plus(ga0):
        ga = ga0
        ga.add_edge(len(ga.nodes) - 1, 0, GrammarAutomata.Cond("epsilon"))
        return ga

    @staticmethod
    def create_automata_question(ga0):
        ga = ga0
        ga.add_edge(0, len(ga.nodes) - 1, GrammarAutomata.Cond("epsilon"))
        return ga

    @staticmethod
    def create_automata_meta(meta_type):
        ga = GrammarAutomata()
        ga.add_node()
        ga.add_node()
        cond = GrammarAutomata.Cond(meta_type)
        ga.add_edge(0, 1, cond)
        return ga

    @staticmethod
    def create_automata_concat(ga0, ga1):
        if ga0 is None:
            return ga1
        ga = GrammarAutomata()
        ga.nodes = ga0.nodes + ga1.nodes
        ga.add_edge(len(ga0.nodes) - 1, len(ga0.nodes), GrammarAutomata.Cond("epsilon"))
        return ga

    def add_node(self):
        self.nodes.append(GrammarAutomata.Node())

    def add_edge(self, id_src, id_dst, cond):
        self.nodes[id_src].add_edge(self.nodes[id_dst], cond)

    def check_all(self, codelines, labels):
        matchs = []
        stack = [(self.nodes[0], 0, 0)]
        while len(stack) > 0:
            node, lineno, col_offset = stack[0]
            stack.pop()
            for node_dst, cond in node.edges:
                satisfied, listends = cond.check(codelines, labels, lineno, col_offset)
                if satisfied:
                    if node_dst == self.nodes[-1]:
                        matchs += listends
                    else:
                        for ends in listends:
                            stack.append((node_dst, ends[0], ends[1]))
        return matchs

    def check_first(self, codelines, labels):
        stack = [(self.nodes[0], 0, 0)]
        while len(stack) > 0:
            node, lineno, col_offset = stack[0]
            stack.pop()
            for node_dst, cond in node.edges:
                satisfied, listends = cond.check(codelines, labels, lineno, col_offset)
                if satisfied:
                    if node_dst == self.nodes[-1]:
                        return listends[0]
                    else:
                        for ends in listends:
                            stack.append((node_dst, ends[0], ends[1]))
        return None
