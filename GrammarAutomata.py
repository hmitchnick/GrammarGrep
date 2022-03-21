# import graphviz

import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'


class GrammarAutomata:
    class Group:
        def __init__(self, lineno, col_offset):
            self.lineno_begin = lineno
            self.lineno_end = float('-inf')
            self.col_offset_begin = col_offset
            self.col_offset_end = float('-inf')

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
                return codelines[lineno - 1].startswith(self.str, col_offset), [(lineno, col_offset + len(self.str))]
            elif self.type == "epsilon":
                return True, [(lineno, col_offset)]
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
        self.groups = []

    def add_group(self, group_index):
        self.groups.append((group_index, self.nodes[0], self.nodes[-1]))

    def get_groups_begin(self, node):
        return [group_index for (group_index, begin_node, _) in self.groups if begin_node == node]

    def get_groups_end(self, node):
        return [group_index for (group_index, _, end_node) in self.groups if end_node == node]

    @staticmethod
    def get_next_begin(codelines, lineno, col_offset):
        if col_offset + 1 < len(codelines[lineno - 1]):
            return lineno, col_offset + 1
        elif lineno < len(codelines):
            return lineno + 1, 0
        else:
            return -1, -1

    @staticmethod
    def update_groups(groups, groups_begin, groups_end, lineno, col_offset):
        for group_index in groups:
            if group_index in groups_end:
                group = groups[group_index]
                group.lineno_end = max(group.lineno_end, lineno)
                group.col_offset_end = max(group.col_offset_end, col_offset)
        for group_index in groups_begin:
            if group_index not in groups:
                group = GrammarAutomata.Group(lineno, col_offset)
                groups[group_index] = group

    @staticmethod
    def create_automata_matching(string):
        ga = GrammarAutomata()
        ga.add_node()
        ga.add_node()
        cond = GrammarAutomata.Cond("str", string)
        ga.add_edge(0, 1, cond)
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
    def create_automata_or(ga0, ga1):
        ga = GrammarAutomata()
        ga.nodes = ga0.nodes + ga1.nodes
        ga.add_edge(0, len(ga0.nodes), GrammarAutomata.Cond("epsilon"))
        ga.add_edge(len(ga0.nodes) - 1, len(ga.nodes) - 1, GrammarAutomata.Cond("epsilon"))
        ga.groups = ga0.groups + ga1.groups
        return ga

    @staticmethod
    def create_automata_star(ga0):
        ga = GrammarAutomata.create_automata_plus(ga0)
        ga = GrammarAutomata.create_automata_question(ga)
        ga.groups = ga0.groups
        return ga

    @staticmethod
    def create_automata_plus(ga0):
        ga = ga0
        ga.add_edge(len(ga.nodes) - 1, 0, GrammarAutomata.Cond("epsilon"))
        ga.groups = ga0.groups
        return ga

    @staticmethod
    def create_automata_question(ga0):
        ga = ga0
        ga.add_edge(0, len(ga.nodes) - 1, GrammarAutomata.Cond("epsilon"))
        ga.groups = ga0.groups
        return ga

    @staticmethod
    def create_automata_concat(ga0, ga1):
        if ga0 is None:
            return ga1
        ga = GrammarAutomata()
        ga.nodes = ga0.nodes + ga1.nodes
        ga.add_edge(len(ga0.nodes) - 1, len(ga0.nodes), GrammarAutomata.Cond("epsilon"))
        ga.groups = ga0.groups + ga1.groups
        return ga

    def add_node(self):
        self.nodes.append(GrammarAutomata.Node())

    def add_edge(self, id_src, id_dst, cond):
        self.nodes[id_src].add_edge(self.nodes[id_dst], cond)

    def print_graph(self):
        for node in self.nodes:
            print("NODE", hex(id(node)), ":")
            for edge in node.edges:
                print("EDGE TO", hex(id(edge[0])), "WITH COND TYPE:", edge[1].type, "STR:", edge[1].str)

    def display_graph(self):
        '''dot = graphviz.Digraph(comment='Automata')
        for i, node in enumerate(self.nodes):
            dot.node(hex(id(node)), str(i))
            for edge in node.edges:
                if edge[1].type == "str":
                    dot.edge(hex(id(node)), hex(id(edge[0])), edge[1].type + ":'" + edge[1].str + "'")
                else:
                    dot.edge(hex(id(node)), hex(id(edge[0])), edge[1].type)
        dot.render('doctest-output/automata.gv', view=True)'''
        pass

    def match_generator(self, codelines, labels):
        groups = {}
        lineno_begin = 1
        col_offset_begin = 0
        while lineno_begin != -1:
            stack = [(self.nodes[0], lineno_begin, col_offset_begin)]
            while len(stack) > 0:
                node, lineno, col_offset = stack[-1]
                stack.pop()
                groups_begin = self.get_groups_begin(node)
                groups_end = self.get_groups_end(node)
                self.update_groups(groups, groups_begin, groups_end, lineno, col_offset)
                for node_dst, cond in node.edges:
                    satisfied, listends = cond.check(codelines, labels, lineno, col_offset)
                    if satisfied:
                        if node_dst == self.nodes[-1]:
                            yield [((lineno_begin, col_offset_begin), listend) for listend in listends], groups
                        else:
                            for ends in listends:
                                stack.append((node_dst, ends[0], ends[1]))
            lineno_begin, col_offset_begin = self.get_next_begin(codelines, lineno_begin, col_offset_begin)

    def match_all(self, codelines, labels):
        return [m for (m, _) in self.match_generator(codelines, labels)]

    def match_first(self, codelines, labels):
        return next(self.match_generator(codelines, labels))[0]

    def replace_all(self, codelines: str, labels, replace_list):
        codelines_replaced = codelines
        for match, groups in self.match_generator(codelines, labels):
            line_beg, col_beg = match[0][0]
            line_end, col_end = match[0][1]
            codelines_replaced[line_beg-1] = codelines_replaced[line_beg-1][:col_beg]+replace_list[0]
        return codelines_replaced

    def replace_first(self, codelines, labels, replace_list):
        match, groups = next(self.match_generator(codelines, labels))[0]
        print(match, groups)
        return codelines
