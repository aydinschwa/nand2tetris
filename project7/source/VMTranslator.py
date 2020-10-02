import sys
# Trying to be a real OOP guy, so writing this implementation using classes.
# Parser: strips whitespace, breaks commands into their lexical components
# CodeWriter: takes output from Parser and writes code
# Main: Initiates the process

symbol_dict = {
    'SP': '0',
    'local': '1',
    'argument': '2',
    'this': '3',
    'that': '4',
    'temp': '5',
    'static': '16',
    'R0': '0',
    'R1': '1',
    'R2': '2',
    'R3': '3',
    'R4': '4',
    'R5': '5',
    'R6': '6',
    'R7': '7',
    'R8': '8',
    'R9': '9',
    'R10': '10',
    'R11': '11',
    'R12': '12',
    'R13': '13',
    'R14': '14',
    'R15': '15',
    'SCREEN': '16384',
    'KBD': '24576',
}

command_dict = {

    'add': 'C_ARITHMETIC',
    'sub': 'C_ARITHMETIC',
    'neg': 'C_ARITHMETIC',
    'eq' : 'C_ARITHMETIC',
    'gt' : 'C_ARITHMETIC',
    'lt' : 'C_ARITHMETIC',
    'push': 'C_PUSH',
    'pop':  'C_POP',
    'and': 'C_ARITHMETIC',  # ?
    'or' : 'C_ARITHMETIC',  # ?
    'not': 'C_ARITHMETIC'   # ?
}


class Parser:
    def __init__(self, file):
        self.file_old = open(file, 'r').readlines()
        self.file = self._clean()
        self.current_command = ""

    # Private method to clean up the input file
    def _clean(self):
        self.file_old = [line.partition("//") for line in self.file_old]
        self.file_old = [line[0].replace("\n", "") for line in self.file_old]
        self.file_old = [line.strip() for line in self.file_old if line]
        return self.file_old

    # Returns true as long as the command list is not empty
    def hasMoreCommands(self):
        return len(self.file) > 0

    # Pops and returns the next command in the command list
    def advance(self):
        if self.hasMoreCommands():
            self.current_command = self.file.pop(0)
            return self.current_command
        else:
            return False

    def commandType(self):
        if len(self.current_command) == 1:
            return command_dict[self.current_command]
        else:
            command = self.current_command.split(" ")
            return command_dict[command[0]]

    # Returns the first argument in the command list
    def arg1(self):
        args = self.current_command.split(" ")
        return args[0]

    # Returns the second argument in the command list
    # Only called if the command is C_PUSH or C_POP
    def arg2(self):
        args = self.current_command.split(" ")
        return args[0]


class CodeWriter:
    def __init__(self, file):
        self.outfile = open(file, 'w')
        self.eq = 0
        self.lt = 0
        self.gt = 0
        self.pointer = 0

    def setFileName(self):
        pass

    # Writes assembly command that corresponds to the arithmetic command that was issued
    def writeArithmetic(self, command):

        # Arithmetic Commands
        if command == "add":
            self.outfile.writelines("// add\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M+D\nM=D\n@SP\nM=M+1\n")
        if command == "sub":
            self.outfile.writelines("// subtract\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\nM=D\n@SP\nM=M+1\n")
        if command == "neg":
            self.outfile.writelines("// neg\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\nD=-D\nM=D\n@SP\nM=M+1\n")

        # Comparison Operators
        if command == "eq":
            self.outfile.writelines("// equality\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nD=D-M\n"
                                    f"@TRUE.EQ.{self.eq}\nD;JEQ\n@SP\nA=M\nM=0\n@FALSE.EQ.{self.eq}\n"
                                    f"0;JMP\n(TRUE.EQ.{self.eq})\n@SP\nA=M\nM=-1\n(FALSE.EQ.{self.eq})"
                                    f"\n@SP\nM=M+1\n")
            self.eq += 1
        if command == "lt":
            self.outfile.writelines("// less than\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nD=D-M\n"
                                    f"@TRUE.LT.{self.lt}\nD;JLT\n@SP\nA=M\nM=0\n@FALSE.LT.{self.lt}\n"
                                    f"0;JMP\n(TRUE.LT.{self.lt})\n@SP\nA=M\nM=-1\n(FALSE.LT.{self.lt})"
                                    f"\n@SP\nM=M+1\n")
            self.lt += 1
        if command == "gt":
            self.outfile.writelines("// less than\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nD=D-M\n"
                                    f"@TRUE.GT.{self.gt}\nD;JGT\n@SP\nA=M\nM=0\n@FALSE.GT.{self.gt}\n"
                                    f"0;JMP\n(TRUE.GT.{self.gt})\n@SP\nA=M\nM=-1\n(FALSE.GT.{self.gt})\n"
                                    f"@SP\nM=M+1\n")
            self.gt += 1
        # Logic statements
        if command == "and":
            self.outfile.writelines("// and\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M&D\nM=D\n@SP\nM=M+1\n")
        if command == "or":
            self.outfile.writelines("// or\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M|D\nM=D\n@SP\nM=M+1\n")
        if command == "not":
            self.outfile.writelines("// not\n")
            self.outfile.writelines("@SP\nM=M-1\nA=M\nD=M\nM=!D\n@SP\nM=M+1\n")

    # Writes assembly command that corresponds to the push/pop command that was issued
    def writePushPop(self, command):
        stack, seg, i = command.split(" ")
        if seg == 'constant':
            if stack == 'push':
                self.outfile.writelines(f"// push constant {i}\n")
                self.outfile.writelines(f"@{i}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif seg in ('local', 'argument', 'this', 'that'):
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{i}\nD=A\n@{symbol_dict[seg]}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@{i}\nD=A\n@{symbol_dict[seg]}\nD=M+D\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n"
                                        f"@13\nA=M\nM=D\n")
        elif seg in ('temp', 'static'):
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{int(symbol_dict[seg])+int(i)}\nD=M\n@SP\nA=M\nM=D\n@SP"
                                        f"\nM=M+1\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@{int(symbol_dict[seg])+int(i)}\nM=D")

        elif seg == 'pointer':
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{i}\nD=A\n@POINTER.THIS.{self.pointer}\nD;JEQ\n@4\nD=M\n@SP"
                                        f"\nA=M\nM=D\n@SP\nM=M+1\n@POINTER.THAT.{self.pointer}\n0;JMP\n"
                                        f"(POINTER.THIS.{self.pointer})\n@3\nD=M\n@SP\nA=M\nM=D\n@SP\n"
                                        f"M=M+1\n(POINTER.THAT.{self.pointer})\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@13\nM=D\n@{i}\nD=A\n@POINTER.THIS.{self.pointer}"
                                        f"\nD;JEQ\n@13\nD=M\n@4\nM=D\n@POINTER.THAT.{self.pointer}\n0;JMP\n"
                                        f"(POINTER.THIS.{self.pointer})\n@13\nD=M\n@3\nM=D\n"
                                        f"(POINTER.THAT.{self.pointer})\n")
            self.pointer += 1

    # Closes output file at end
    def close(self):
        self.outfile = self.outfile.close()


# Driver code
def main(base):

    infile = base
    #outfile = f'/Users/Aydin/Desktop/nand2Tetris/projects/07/out/{base}.asm'
    outfile = f'{base.replace("vm", "")}asm'

    vmlines = Parser(infile)
    asmlines = CodeWriter(outfile)
    while True:
        curr_line = vmlines.advance()
        if not curr_line:
            break
        type = vmlines.commandType()
        if type == 'C_ARITHMETIC':
            asmlines.writeArithmetic(curr_line)
        else:
            asmlines.writePushPop(curr_line)
    asmlines.outfile.writelines("(END)\n@END\n0;JMP\n")
    asmlines.close()

if __name__ == '__main__':
    main(sys.argv[1])