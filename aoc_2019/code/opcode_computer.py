# maximum number of parameters per instruction
import time

_MAX_PARAMETERS = 4


def parse_instruction(instruction: int) -> (int, int):
    instr = str(instruction)
    opcode = int(instr[-2:])
    mode_arr = [int(c) for c in instr[:-2]]
    mode_arr.reverse()
    while mode_arr.__len__() < _MAX_PARAMETERS:
        mode_arr.append(0)
    return opcode, mode_arr


class OpcodeComputer:
    memory = []
    program = []
    inputs = []
    outputs = []

    def __init__(self, program: list, inputs: list = []):
        """Creates a new OpcodeComputer with a given program (list of integers)"""
        self.program = program.copy()
        self.memory = program.copy()
        self.inputs = inputs.copy()
        self.outputs = []

    def run(self):
        """Executes the given program"""
        pos = 0
        while pos < self.memory.__len__():
            opcode, modes = parse_instruction(self.memory[pos])
            if opcode == 1:  # ADD
                # Add values from 2 positions after the opcode together, store at position of 3rd argument
                result = self.get_value(pos + 1, modes[0]) + self.get_value(pos + 2, modes[1])
                self.set_value(pos + 3, result, modes[2])
            if opcode == 2:  # MULTIPLY
                # Multiply values from 2 positions after the opcode together, store at position of 3rd argument
                result = self.get_value(pos + 1, modes[0]) * self.get_value(pos + 2, modes[1])
                self.set_value(pos + 3, result, modes[2])
            if opcode == 99:  # Immediately HALT
                return
            if opcode == 3:  # INPUT
                # if there are no inputs left
                if self.inputs.__len__() < 1:
                    # "throw" error
                    print("Missing inputs!")
                    exit(-1)
                # get next input value
                input_value = self.inputs[0]
                # store the input value to the given position respecting modes
                self.set_value(pos+1, input_value, modes[0])
                # "consume" the input value
                self.inputs = self.inputs[1:]
            if opcode == 4:  # OUTPUT
                # adds value of position in parameter to outputs respecting modes
                self.outputs.append(self.get_value(pos+1, modes[0]))
            if opcode == 5:  # JUMP-IF-TRUE
                to_check = self.get_value(pos+1, modes[0])
                new_ip = self.get_value(pos+2, modes[1])
                if to_check != 0:
                    pos = new_ip
                else:
                    pos += 3  # increment if IP hasn't been modified
            if opcode == 6:  # JUMP-IF-FALSE
                to_check = self.get_value(pos+1, modes[0])
                new_ip = self.get_value(pos+2, modes[1])
                if to_check == 0:
                    pos = new_ip
                else:
                    pos += 3  # increment if IP hasn't been modified
            if opcode == 7:  # LESS_THAN
                first = self.get_value(pos+1, modes[0])
                second = self.get_value(pos + 2, modes[1])
                store_at = self.get_value(pos + 3, 1)
                if first < second:
                    self.set_value(store_at, 1, 1)
                else:
                    self.set_value(store_at, 0, 1)
            if opcode == 8:  # EQUALS
                first = self.get_value(pos+1, modes[0])
                second = self.get_value(pos + 2, modes[1])
                store_at = self.get_value(pos + 3, 1)
                if first == second:
                    self.set_value(store_at, 1, 1)
                else:
                    self.set_value(store_at, 0, 1)
            # Increment position by 4 for ADD and MULTIPLY
            if opcode in [1, 2, 7, 8]:
                pos += 4
            # Increment position by 2 for INPUT and OUTPUT
            elif opcode in [3, 4]:
                pos += 2

    def get_memory(self) -> list:
        return self.memory

    def set_value(self, source_pos: int, value: int, mode: int):
        """Sets the program at the position (interpreted dependently from mode) to value"""
        if mode == 0:
            self.memory[self.memory[source_pos]] = value
        elif mode == 1:
            self.memory[source_pos] = value

    def get_value(self, source_pos: int, mode : int) -> int:
        """Gets the value at the position (interpreted dependently from mode)"""
        if mode == 0:
            return self.memory[self.memory[source_pos]]
        elif mode == 1:
            return self.memory[source_pos]


    def get_outputs(self) -> list:
        return self.outputs

    def reset(self):
        self.memory = self.program.copy()
