from converter import Automaton

afn = Automaton(4, {3})
afn.add_transition(0, '1', 1)
afn.add_transition(0, ('1','0'), 0)
afn.add_transition(1, '0', 2)
afn.add_transition(1, '', 2)
afn.add_transition(2, '1', 3)
afn.add_transition(3, '0', 3)
afn.add_transition(3, '1', 3)

afd = afn.convert_to_dfa()

# Imprimir o AFD resultante
afd.print_automaton()