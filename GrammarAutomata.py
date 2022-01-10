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
        def check(self, string: str, labels, idx):
            if self.type == "str":
                return string.startswith(self.str, idx), idx + len(self.str)
            else:
                return False, -1

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
        ga.add_edge(len(ga0.nodes)-1, len(ga.nodes)-1, GrammarAutomata.Cond("epsilon"))
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
        ga.add_edge(len(ga0.nodes)-1, len(ga0.nodes), GrammarAutomata.Cond("epsilon"))
        return ga

    def add_node(self):
        self.nodes.append(GrammarAutomata.Node())

    def add_edge(self, id_src, id_dst, cond):
        self.nodes[id_src].add_edge(self.nodes[id_dst], cond)

    def check(self, string, labels, idx_begin):
        stack = [(self.nodes[0], idx_begin)]
        while len(stack) > 0:
            node, idx = stack[0]
            stack.pop()
            for node_dst, cond in node.edges:
                satisfied, idx_edge = cond.check(string, labels, idx)
                if satisfied:
                    if node_dst == self.nodes[-1]:
                        return True, idx_edge
                    else:
                        stack.append((node_dst, idx_edge))
        return False, -1
