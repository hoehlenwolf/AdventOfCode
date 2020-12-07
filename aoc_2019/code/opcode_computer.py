class OpcodeComputer:
    memory = []
    program = []

    def __init__(self, program : list):
        """Creates a new OpcodeComputer with a given program (list of integers)"""
        self.program = program.copy()
        self.memory = program.copy()

    def run(self):
        """Executes the given program"""
        pos = 0
        while pos < self.memory.__len__():
            opcode = self.memory[pos]
            if opcode == 1:  # ADD
                # Add values from 2 positions after the opcode together, store at position of 3rd argument
                result = self.get_value_at_addr_value(pos+1) + self.get_value_at_addr_value(pos+2)
                self.set_value_at_addr_value(pos+3, result)
            if opcode == 2:  # MULTIPLY
                # Multiply values from 2 positions after the opcode together, store at position of 3rd argument
                result = self.get_value_at_addr_value(pos + 1) * self.get_value_at_addr_value(pos + 2)
                self.set_value_at_addr_value(pos + 3, result)
            if opcode == 99:  # Immediately HALT
                return
            # Increment position by 4
            pos += 4

    def get_memory(self) -> list:
        return self.memory

    def set_value_at_addr_value(self, source_pos: int, value: int):
        """Sets the program at the position (value at source_pos) to value"""
        self.memory[self.memory[source_pos]] = value

    def get_value_at_addr_value(self, source_pos: int) -> int:
        """Gets the value at the position (value at source_pos)"""
        return self.memory[self.memory[source_pos]]

    def set_value_at_addr(self, source_pos: int, value: int):
        """Sets the program at the position (value at source_pos) to value"""
        self.memory[source_pos] = value

    def get_value_at_addr(self, source_pos: int) -> int:
        """Gets the value at the position (value at source_pos)"""
        return self.memory[source_pos]

    def reset(self):
        self.memory = self.program.copy()
