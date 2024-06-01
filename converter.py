class Automaton:
    def __init__(self, num_states, accepting_states):
        self.num_states = num_states
        self.transitions = [{} for _ in range(num_states)]
        self.accepting_states = accepting_states

    def add_transition(self, start_state, characters, end_state): # Adiciona uma transição do start_state para o end_state usando um ou mais caracteres
        if isinstance(characters, tuple):
            for character in characters:
                if character not in self.transitions[start_state]:
                    self.transitions[start_state][character] = set()
                self.transitions[start_state][character].add(end_state)
        else:
            if characters not in self.transitions[start_state]:
                self.transitions[start_state][characters] = set()
            self.transitions[start_state][characters].add(end_state)

    def _epsilon_closure(self, states): # Calcula o fechamento epsilon para um conjunto de estados
        stack = list(states)
        closure = set(states)
        
        while stack:
            state = stack.pop()
            if '' in self.transitions[state]:
                for next_state in self.transitions[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def convert_to_dfa(self): # Converte o AFN atual em um AFD
        initial_state = frozenset(self._epsilon_closure({0}))  
        dfa_states = {initial_state: 0} 
        dfa_accepting_states = set()  
        dfa_transitions = [{}]  
        new_states = [initial_state] 
        state_counter = 1 

        while new_states:
            current = new_states.pop() 
            current_state_id = dfa_states[current] 

            if any(state in self.accepting_states for state in current):
                dfa_accepting_states.add(current_state_id) 

            all_symbols = set()
            for state in current:
                all_symbols.update(self.transitions[state].keys()) 

            all_symbols.discard('') 

            for symbol in sorted(all_symbols):
                next_state = set()
                for sub_state in current:
                    if symbol in self.transitions[sub_state]:
                        next_state.update(self.transitions[sub_state][symbol]) 
                next_state_closure = frozenset(self._epsilon_closure(next_state))  

                if next_state_closure not in dfa_states:
                    dfa_states[next_state_closure] = state_counter 
                    new_states.append(next_state_closure)  
                    dfa_transitions.append({}) 
                    state_counter += 1

                dfa_transitions[current_state_id][symbol] = dfa_states[next_state_closure] 

        dfa = Automaton(len(dfa_states), dfa_accepting_states) 
        dfa.transitions = dfa_transitions 
        return dfa

    def print_automaton(self):
        print("States and transitions:")
        for i, state_transitions in enumerate(self.transitions):
            for symbol, next_state in state_transitions.items():
                print(f"State {i} --{symbol}--> State {next_state}") 
        print(f"Accepting states: {self.accepting_states}")