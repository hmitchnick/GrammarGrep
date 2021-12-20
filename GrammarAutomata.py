class GrammarAutomata:
    class Node:
        def __init__(self, is_accept, is_initial):
            self.edges = []
            self.is_accept = is_accept
            self.is_initial = is_initial

        def add_edge(self, node_dst, cond):
            self.edges += (cond, node_dst)

    def __init__(self):
        self.nodes = []
        self.compiled = False

    def add_node(self, id_node, is_accept=False, is_initial=False):
        self.nodes[id_node] += GrammarAutomata.Node(is_accept, is_initial)

    def add_edge(self, id_src, id_dst, cond):
        self.nodes[id_src].add_edge(self.nodes[id_dst], cond)