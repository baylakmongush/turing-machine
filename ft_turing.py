import json
import sys

def find_transition(state, symbol, transitions):
    return next((t for t in transitions[state] if t["read"] == symbol), None)

def apply_transition(tape, head, transition):
    tape[head] = transition["write"]
    new_head = head + 1 if transition["action"] == "RIGHT" else head - 1
    return new_head, transition["to_state"]

def run_turing_machine(machine_description, input_string):
    states = machine_description["states"]
    initial_state = machine_description["initial"]
    final_states = set(machine_description["finals"])
    transitions = machine_description["transitions"]
    blank = machine_description["blank"]

    tape = list(input_string) + [blank]
    head = 0
    state = initial_state

    while state not in final_states:
        symbol = tape[head]
        transition = find_transition(state, symbol, transitions)
        if transition is None:
            raise ValueError(f"No transition found for state '{state}' and symbol '{symbol}'.")

        head, state = apply_transition(tape, head, transition)
        print_tape(tape, head, state)

    print("\nFinal state reached.")

def print_tape(tape, head, state):
    tape_str = ''.join([f'[{s}]' if i == head else s for i, s in enumerate(tape)])
    print(f"{tape_str} (Current state: {state})")

def main():
    if len(sys.argv) != 3:
        print("usage: ft_turing jsonfile input")
        sys.exit(1)

    json_file, input_string = sys.argv[1], sys.argv[2]
    try:
        with open(json_file, 'r') as file:
            machine_description = json.load(file)
        run_turing_machine(machine_description, input_string)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
