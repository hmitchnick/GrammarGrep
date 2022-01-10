from GrammarAutomata import GrammarAutomata

'''
Production Rules:
    r = ;(s;)
    r = st
    r = s;|t
    r = s;*
    r = s;+
    r = s;?
    r = ;id
    r = ;stmt
    r = ;expr
    r = ;str
    r = ;num

Examples:
    1. if len(;id) > ;num and ;expr:
    2. \(assertEquals(;expr, ;expr)\) | \(assert(;expr)\)
    3. ;id = ;str\?
    4. ;id = ;id ** ;num
    5. ;id = 1\(0\)\*
'''


def get_closing_paren(regex: str, paren_open_idx):
    i = regex.find(";", paren_open_idx)
    counter = 1
    while True:
        if regex[i + 1] == "(":
            counter += 1
        elif regex[i + 1] == ")":
            counter -= 1
        if counter == 0:
            return i
        i = regex.find(";", i+1)


def regex_to_nfa(regex: str):
    nfa = None
    idx_begin = 0
    while idx_begin < len(regex):
        meta_idx = regex.find(";", idx_begin)
        if meta_idx == -1:
            nfa_step = GrammarAutomata.create_automata_matching(regex)
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            return nfa

        if meta_idx > idx_begin:
            nfa_step = GrammarAutomata.create_automata_matching(regex[idx_begin:meta_idx])
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)

        if regex[meta_idx + 1] == "(":
            idx_close = get_closing_paren(regex, meta_idx+1)
            nfa_step = regex_to_nfa(regex[meta_idx+2:idx_close])
            idx_begin = idx_close + 2
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
        elif regex[meta_idx + 1] == "|":
            nfa_l = nfa
            nfa_r = regex_to_nfa(regex[meta_idx + 2:])
            nfa = GrammarAutomata.create_automata_or(nfa_l, nfa_r)
            return nfa
        elif regex[meta_idx + 1] == "*":
            nfa_inner = regex_to_nfa(regex[idx_begin:meta_idx])
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_inner)
            nfa = GrammarAutomata.create_automata_star(nfa)
            idx_begin = meta_idx + 2
        elif regex[meta_idx + 1] == "+":
            nfa_inner = regex_to_nfa(regex[idx_begin:meta_idx])
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_inner)
            nfa = GrammarAutomata.create_automata_plus(nfa)
            idx_begin = meta_idx + 2
        elif regex[meta_idx + 1] == "?":
            nfa_inner = regex_to_nfa(regex[idx_begin:meta_idx])
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_inner)
            nfa = GrammarAutomata.create_automata_question(nfa)
            idx_begin = meta_idx + 2
        elif regex[meta_idx + 1:].startswith("id"):
            nfa_step = GrammarAutomata.create_automata_meta("type_id")
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            idx_begin = meta_idx + 1 + 2
        elif regex[meta_idx + 1:].startswith("stmt"):
            nfa_step = GrammarAutomata.create_automata_meta("type_stmt")
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            idx_begin = meta_idx + 1 + 4
        elif regex[meta_idx + 1:].startswith("expr"):
            nfa_step = GrammarAutomata.create_automata_meta("type_expr")
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            idx_begin = meta_idx + 1 + 4
        elif regex[meta_idx + 1:].startswith("str"):
            nfa_step = GrammarAutomata.create_automata_meta("type_str")
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            idx_begin = meta_idx + 1 + 3
        elif regex[meta_idx + 1:].startswith("num"):
            nfa_step = GrammarAutomata.create_automata_meta("type_num")
            nfa = GrammarAutomata.create_automata_concat(nfa, nfa_step)
            idx_begin = meta_idx + 1 + 3
        else:
            print("Error!")
            return None
    return nfa