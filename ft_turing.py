import json
import sys


def find_transition(state, symbol, transitions):
    for transition in transitions[state]:
        if transition["read"] == symbol:
            return transition
    return None


def apply_transition(tape, head, transition):
    tape[head] = transition["write"]
    new_head = head + 1 if transition["action"] == "RIGHT" else head - 1
    return new_head, transition["to_state"]


def run_turing_machine(machine_description, input_string):
    # Initializing the machine based on the description
    initial_state = machine_description["initial"]
    final_states = set(machine_description["finals"])
    transitions = machine_description["transitions"]
    blank = machine_description["blank"]

    # Preparing the tape
    tape = [char for char in input_string]
    tape.append(blank)  # Adding the blank symbol at the end

    # Setting the initial position of the head and state
    head = 0
    current_state = initial_state

    # Running the machine
    while current_state not in final_states:
        current_symbol = tape[head] if head < len(tape) else blank

        # Finding the transition for the current state and symbol
        transition = None
        if current_state in transitions:
            for trans in transitions[current_state]:
                if trans["read"] == current_symbol:
                    transition = trans
                    break

        if transition is None:
            raise ValueError(f"No transition found for state '{current_state}' and symbol '{current_symbol}'.")

        # Applying the transition
        tape[head] = transition["write"]
        head = head + 1 if transition["action"] == "RIGHT" else head - 1
        current_state = transition["to_state"]

        # Printing the current state of the tape
        print_tape(tape, head, current_state)

    print("\nFinal state reached.")


def print_tape(tape, head, state):
    tape_str = ''
    for i, s in enumerate(tape):
        if i == head:
            # Using ANSI escape code for a bright color (e.g., bright red)
            tape_str += f'\033[91m[{s}]\033[0m'  # Highlighting the symbol at the head position
        else:
            tape_str += s  # Adding the symbol to the string as is

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
