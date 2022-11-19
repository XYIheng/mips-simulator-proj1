import sys

SAMPLE_FILE = ""
PC = 64
REGISTER = []
DATA = []
DATA_BEGIN_ADDRESS = 64


class Instruction(object):
    def __init__(self, instruction):
        self.instruction = instruction

    def __str__(self):
        return ""
    def execute(self):
        global PC
        PC += 4

class J_Instruction(Instruction):
    jump_address = 0

    def __init__(self, instruction):

        self.instruction = instruction
        self.jump_address = int((self.instruction[-26:] + "00"), 2)

    def __str__(self) -> str:

        return "J #" + str(self.jump_address)

    def execute(self):
        global PC
        PC = self.jump_address


class JR_Instruction(Instruction):
    jump_register = 0

    def __init__(self, instruction):

        self.instruction = instruction
        self.jump_register = int(instruction[6:11], 2)

    def __str__(self):
        return "JR " + "R" + str(self.jump_register)

    def execute(self):
        global PC
        PC = REGISTER[self.jump_register]


class BEQ_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.jump_offset = int((self.instruction[-16:] + "00"), 2)

    def __str__(self) -> str:
        return (
            "BEQ "
            + "R"
            + str(self.rs)
            + ", R"
            + str(self.rt)
            + ", #"
            + str(self.jump_offset)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        if REGISTER[self.rs] == REGISTER[self.rt]:
            PC = PC + self.jump_offset


class BLTZ_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.jump_offset = int((self.instruction[-16:] + "00"), 2)

    def __str__(self) -> str:
        return "BLTZ " + "R" + str(self.rs) + ", #" + str(self.jump_offset)

    def execute(self):
        global PC
        PC = PC + 4
        if REGISTER[self.rs] < 0:
            PC = PC + self.jump_offset


class BGTZ_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.jump_offset = int((self.instruction[-16:] + "00"), 2)

    def __str__(self) -> str:
        return "BGTZ " + "R" + str(self.rs) + ", #" + str(self.jump_offset)

    def execute(self):
        global PC
        PC = PC + 4
        if REGISTER[self.rs] > 0:
            PC = PC + self.jump_offset


class BREAK_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction

    def __str__(self) -> str:
        return "BREAK"

    def execute(self):
        global PC
        PC = PC + 4


class SW_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.base = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        if int(instruction[-16]) == 0:
            self.offset = int((self.instruction[-16:]), 2)
        else:
            self.offset = int((self.instruction[-15:]), 2) - (1 <<15)

    def __str__(self) -> str:
        return (
            "SW "
            + "R"
            + str(self.rt)
            + ", "
            + str(self.offset)
            + "(R"
            + str(self.base)
            + ")"
        )

    def execute(self):
        global PC
        global DATA
        PC = PC + 4
        address = REGISTER[self.base] + self.offset
        DATA[int((address - DATA_BEGIN_ADDRESS) / 4)] = REGISTER[self.rt]


class LW_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.base = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        if int(instruction[-16]) == 0:
            self.offset = int((self.instruction[-16:]), 2)
        else:
            self.offset = int((self.instruction[-15:]), 2) - (1 << 15)

    def __str__(self) -> str:
        return (
            "LW "
            + "R"
            + str(self.rt)
            + ", "
            + str(self.offset)
            + "(R"
            + str(self.base)
            + ")"
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        address = REGISTER[self.base] + self.offset
        # print(self.offset)
        # print(self.offset)
        REGISTER[self.rt] = DATA[int((address - DATA_BEGIN_ADDRESS) / 4)]


class SLL_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)
        self.sa = int(instruction[21:26], 2)

    def __str__(self) -> str:
        return "SLL " + "R" + str(self.rd) + ", R" + str(self.rt) + ", #" + str(self.sa)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        mask = (2**32) - 1
        REGISTER[self.rd] = (REGISTER[self.rt] << self.sa) & mask


class SRL_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)
        self.sa = int(instruction[21:26], 2)

    def __str__(self) -> str:
        return "SRL " + "R" + str(self.rd) + ", R" + str(self.rt) + ", #" + str(self.sa)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rt] >> self.sa


class SRA_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)
        self.sa = int(instruction[21:26], 2)

    def __str__(self) -> str:
        return "SRA " + "R" + str(self.rd) + ", R" + str(self.rt) + ", #" + str(self.sa)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rt] >> self.sa


class NOP_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction

    def __str__(self) -> str:
        return "NOP"

    def execute(self):
        global PC
        PC = PC + 4


class ADD_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "ADD " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rs] + REGISTER[self.rt]


class ADDI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "ADD "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = REGISTER[self.rs] + self.immediate


class SUB_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "SUB " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rs] - REGISTER[self.rt]


class SUBI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "SUB "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = REGISTER[self.rs] - self.immediate


class MUL_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "MUL " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rs] * REGISTER[self.rt]


class MULI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "SUB "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = REGISTER[self.rs] * self.immediate


class AND_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "AND " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = REGISTER[self.rs] & REGISTER[self.rt]


class ANDI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "AND "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = REGISTER[self.rs] & self.immediate


class NOR_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "NOR " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = ~(REGISTER[self.rs] | REGISTER[self.rt])


class NORI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "NOR "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = ~(REGISTER[self.rs] | self.immediate)


class SLT_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.rd = int(instruction[16:21], 2)

    def __str__(self) -> str:
        return "SLT " + "R" + str(self.rd) + ", R" + str(self.rs) + ", R" + str(self.rt)

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rd] = True if REGISTER[self.rs] < REGISTER[self.rt] else False


class SLTI_Instruction(Instruction):
    def __init__(self, instruction):

        self.instruction = instruction
        self.rs = int(instruction[6:11], 2)
        self.rt = int(instruction[11:16], 2)
        self.immediate = int(instruction[-16:], 2)

    def __str__(self) -> str:
        return (
            "SLT "
            + "R"
            + str(self.rt)
            + ", R"
            + str(self.rs)
            + ", #"
            + str(self.immediate)
        )

    def execute(self):
        global PC
        global REGISTER
        PC = PC + 4
        REGISTER[self.rt] = True if REGISTER[self.rs] < self.immediate else False


def parse_instruction(instruction):
    if instruction[0:6] == "000000":
        if instruction[-6:] == "000000":
            if int(instruction, 2) == 0:
                return NOP_Instruction(instruction)
            return SLL_Instruction(instruction)
        if instruction[-6:] == "000010":
            return SRL_Instruction(instruction)
        if instruction[-6:] == "000011":
            return SRA_Instruction(instruction)
        if instruction[-6:] == "100000":
            return ADD_Instruction(instruction)
        elif instruction[-6:] == "100010":
            return SUB_Instruction(instruction)
        elif instruction[-6:] == "100100":
            return AND_Instruction(instruction)
        elif instruction[-6:] == "100111":
            return NOR_Instruction(instruction)
        elif instruction[-6:] == "101010":
            return SLT_Instruction(instruction)
        elif instruction[-6:] == "001000":
            return JR_Instruction(instruction)
        elif instruction[-6:] == "001101":
            return BREAK_Instruction(instruction)
    elif instruction[0:6] == "011100" and instruction[-6:] == "000010":
        return MUL_Instruction(instruction)
    elif instruction[0:6] == "000010":
        return J_Instruction(instruction)
    elif instruction[0:6] == "000100":
        return BEQ_Instruction(instruction)
    elif instruction[0:6] == "000001":
        return BLTZ_Instruction(instruction)
    elif instruction[0:6] == "000111":
        return BGTZ_Instruction(instruction)
    elif instruction[0:6] == "101011":
        return SW_Instruction(instruction)
    elif instruction[0:6] == "100011":
        return LW_Instruction(instruction)
    elif instruction[0:6] == "110000":
        return ADDI_Instruction(instruction)
    elif instruction[0:6] == "110001":
        return SUBI_Instruction(instruction)
    elif instruction[0:6] == "100001":
        return MULI_Instruction(instruction)
    elif instruction[0:6] == "110010":
        return ANDI_Instruction(instruction)
    elif instruction[0:6] == "110011":
        return NORI_Instruction(instruction)
    elif instruction[0:6] == "110101":
        return SLTI_Instruction(instruction)
    return Instruction(instruction)


def get_instruction(file):
    instructions = []
    with open(file, "r") as fin:
        for line in fin:
            instructions.append(line.strip())
    return instructions


def output_dis(file, instance):
    instruction = instance.instruction
    file.write(
        str(instruction[0:6])
        + " "
        + str(instruction[6:11])
        + " "
        + str(instruction[11:16])
        + " "
        + str(instruction[16:21])
        + " "
        + str(instruction[21:26])
        + " "
        + str(instruction[26:32])
        + "\t"
        + str(PC)
        + "\t"
        + instance.__str__()
        + "\n"
    )
    if isinstance(instance, BREAK_Instruction):
        # print("false")
        return False
    return True


def output_dis_data(file, instance):
    instruction = instance.instruction
    data = 0
    if instruction[0] == "0":
        data = int(instruction, 2)
    else:
        data = int(instruction, 2) - (1 << 32)
    DATA[int((PC - 64) / 4)] = data
    file.write(str(instruction) + "\t" + str(PC) + "\t" + str(data) + "\n")


def output_sim(file, instance, cycle,break_index):
    
    file.write("--------------------" + "\n")
    if isinstance(instance, BREAK_Instruction):
        file.write("Cycle:"+ str(cycle)+ "\t"+ str(PC)+ "\t"+ instance.__str__()+ "\n")
    else:
        file.write("Cycle:"+ str(cycle)+ "\t"+ str(PC)+ "\t"+ instance.__str__().split(" ",1)[0]+"\t"+ instance.__str__().split(" ",1)[1]+ "\n")
    instance.execute()
    file.write("\n")
    file.write("Registers")
    file.write("\n")
    file.write(
        "R00:"
        + "\t"
        + str(REGISTER[0])
        + "\t"
        + str(REGISTER[1])
        + "\t"
        + str(REGISTER[2])
        + "\t"
        + str(REGISTER[3])
        + "\t"
        + str(REGISTER[4])
        + "\t"
        + str(REGISTER[5])
        + "\t"
        + str(REGISTER[6])
        + "\t"
        + str(REGISTER[7])
        + "\t"
        + str(REGISTER[8])
        + "\t"
        + str(REGISTER[9])
        + "\t"
        + str(REGISTER[10])
        + "\t"
        + str(REGISTER[11])
        + "\t"
        + str(REGISTER[12])
        + "\t"
        + str(REGISTER[13])
        + "\t"
        + str(REGISTER[14])
        + "\t"
        + str(REGISTER[15])
        + "\n"
    )
    file.write(
        "R16:"
        + "\t"
        + str(REGISTER[16])
        + "\t"
        + str(REGISTER[17])
        + "\t"
        + str(REGISTER[18])
        + "\t"
        + str(REGISTER[19])
        + "\t"
        + str(REGISTER[20])
        + "\t"
        + str(REGISTER[21])
        + "\t"
        + str(REGISTER[22])
        + "\t"
        + str(REGISTER[23])
        + "\t"
        + str(REGISTER[24])
        + "\t"
        + str(REGISTER[25])
        + "\t"
        + str(REGISTER[26])
        + "\t"
        + str(REGISTER[27])
        + "\t"
        + str(REGISTER[28])
        + "\t"
        + str(REGISTER[29])
        + "\t"
        + str(REGISTER[30])
        + "\t"
        + str(REGISTER[31])
        + "\n"
    )
    file.write("\n")
    
    file.write("Data")
    file.write("\n")
    for i in range(0,int((len(DATA)-break_index)/8)):
        data_address = break_index+i*8
        line = str(data_address*4+64)+":"
        for j in range(0,8):
            if data_address+j==len(DATA):
                break
            #print(data_address+j)
            line+=("\t"+str(DATA[data_address+j])) 
        file.write(line+"\n")
    file.write("\n")
    if isinstance(instance, BREAK_Instruction):
        # print("false")
        return False
    return True

def main():
    global REGISTER
    global PC
    global DATA
    REGISTER = [0] * 32
    input_file = sys.argv[1]
    output_disassembly = open("disassembly.txt", "w")
    output_simulation = open("simulation.txt", "w")
    instructions = get_instruction(input_file)
    PC = 64
    instruction_instances = []

    for instruction in instructions:
        instruction_instances.append(parse_instruction(instruction))

    DATA = [0] * len(instructions)

    for instance in instruction_instances:
        if not output_dis(output_disassembly, instance):
            PC += 4
            break
        PC += 4
    break_index = int((PC - 64) / 4)

    for instance in instruction_instances[break_index:]:
        output_dis_data(output_disassembly, instance)
        PC += 4
    # for i in range(0,len(DATA)):
    #     print(str(i)+","+str(DATA[i]))
    PC = 64
    
    cycle = 1
    while True:
        instance = instruction_instances[int((PC - 64) / 4)]
        if not output_sim(output_simulation, instance, cycle,break_index):
            break
        cycle+=1


if __name__ == "__main__":
    main()
