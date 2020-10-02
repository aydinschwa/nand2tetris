import sys
import os

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
    'and': 'C_ARITHMETIC',
    'or' : 'C_ARITHMETIC',
    'not': 'C_ARITHMETIC',
    'label': 'C_LABEL',
    'goto': 'C_GOTO',
    'if-goto': 'C_IF',
    'call': 'C_CALL',
    'return': 'C_RETURN',
    'function': 'C_FUNCTION'
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
    def __init__(self, file, file_name):
        self.outfile = open(file, 'w')
        self.file_name = file_name
        self.function = ""
        self.label = ""
        self.ret_addr = ""
        self.ret = 1
        self.eq = 0
        self.lt = 0
        self.gt = 0
        self.pointer = 0

    # Writes Sys.init code. Should only call Sys.init if reading from a directory
    def writeInit(self):

        if str(self.file_name).__contains__("_together"):
            self.outfile.writelines("// Initializing pointers\n")
            self.outfile.writelines("@256\nD=A\n@0\nM=D\n"  # Set RAM[0] (SP) to 256
                                    "@300\nD=A\n@1\nM=D\n"  # Set RAM[1] (LCL) to 300
                                    "@400\nD=A\n@2\nM=D\n")  # Set RAM[2] (ARG) to 400

            self.outfile.writelines("// Calling Sys.init\n\n")
            self.writeFunc("call Sys.init 0")


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
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@15\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@15\nD=D-M\n"
                                    f"@TRUE.EQ.{self.eq}\nD;JEQ\n@SP\nA=M\nM=0\n@FALSE.EQ.{self.eq}\n"
                                    f"0;JMP\n(TRUE.EQ.{self.eq})\n@SP\nA=M\nM=-1\n(FALSE.EQ.{self.eq})"
                                    f"\n@SP\nM=M+1\n")
            self.eq += 1
        if command == "lt":
            self.outfile.writelines("// less than\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@15\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@15\nD=D-M\n"
                                    f"@TRUE.LT.{self.lt}\nD;JLT\n@SP\nA=M\nM=0\n@FALSE.LT.{self.lt}\n"
                                    f"0;JMP\n(TRUE.LT.{self.lt})\n@SP\nA=M\nM=-1\n(FALSE.LT.{self.lt})"
                                    f"\n@SP\nM=M+1\n")
            self.lt += 1
        if command == "gt":
            self.outfile.writelines("// less than\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@15\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@15\nD=D-M\n"
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
                self.outfile.writelines(f"@{i}\nD=A\n@{symbol_dict[seg]}\nD=M+D\n@15\nM=D\n@SP\nM=M-1\nA=M\nD=M\n"
                                        f"@15\nA=M\nM=D\n")
        elif seg == 'temp':
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{int(symbol_dict[seg])+int(i)}\nD=M\n@SP\nA=M\nM=D\n@SP"
                                        f"\nM=M+1\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@{int(symbol_dict[seg])+int(i)}\nM=D\n")

        elif seg == 'static':
            file = self.function.split(".")[0]
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{file}.{int(i)}\nD=M\n@SP\nA=M\nM=D\n@SP"
                                        f"\nM=M+1\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@{file}.{int(i)}\nM=D\n")

        elif seg == 'pointer':
            if stack == 'push':
                self.outfile.writelines(f"// push {seg} {i}\n")
                self.outfile.writelines(f"@{i}\nD=A\n@POINTER.THIS.{self.pointer}\nD;JEQ\n@4\nD=M\n@SP"
                                        f"\nA=M\nM=D\n@SP\nM=M+1\n@POINTER.THAT.{self.pointer}\n0;JMP\n"
                                        f"(POINTER.THIS.{self.pointer})\n@3\nD=M\n@SP\nA=M\nM=D\n@SP\n"
                                        f"M=M+1\n(POINTER.THAT.{self.pointer})\n")
            else:
                self.outfile.writelines(f"// pop {seg} {i}\n")
                self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@15\nM=D\n@{i}\nD=A\n@POINTER.THIS.{self.pointer}"
                                        f"\nD;JEQ\n@15\nD=M\n@4\nM=D\n@POINTER.THAT.{self.pointer}\n0;JMP\n"
                                        f"(POINTER.THIS.{self.pointer})\n@15\nD=M\n@3\nM=D\n"
                                        f"(POINTER.THAT.{self.pointer})\n")
            self.pointer += 1

    # Writes assembly command that corresponds to the branching command that was issued
    def writeBranch(self, command):
        self.label = f"{self.function}${command.split(' ')[1]}"

        if command.__contains__('label'):
            self.outfile.writelines("// loop spot\n")
            self.outfile.writelines(f"({self.label})\n")

        if command.__contains__('if-goto'):
            self.outfile.writelines("// Initialize conditional goto statement\n")
            self.outfile.writelines(f"@SP\nM=M-1\nA=M\nD=M\n@{self.label}\nD;JNE\n")

        if command.__contains__('goto') and not command.__contains__('if'):
            self.outfile.writelines("// Initialize unconditional goto statement\n")
            self.outfile.writelines(f"@{self.label}\n0; JMP\n")

    def writeFunc(self, command):

        if command.__contains__("function"):
            f, fname, nvars = command.split(" ")
            self.function = fname  # Declares which function currently being parsed
            self.outfile.writelines("// Function definition\n")
            self.outfile.writelines(f"({fname})\n")  # Label function name
            [self.writePushPop("push constant 0") for num in range(int(nvars))]  # push 0 on stack nvars times

        if command.__contains__("return"):
            self.outfile.writelines("// Implementing return \n")

            # storing endframe in RAM[13]
            self.outfile.writelines(f"@1\nD=M\n@13\nM=D\n")

            # Getting return address from endframe, store in RAM[14]
            self.outfile.writelines(f"A=M\nA=A-1\nA=A-1\nA=A-1\nA=A-1\nA=A-1\nD=M\n@14\nM=D\n")

            # Put return value in ARG 0
            self.writePushPop("pop argument 0")

            # Putting stack pointer one after arg pointer
            self.outfile.writelines(f"@2\nD=M\n@0\nM=D+1\n")

            #Restoring memory segments
            self.outfile.writelines("// Restoring memory segments \n")
            self.outfile.writelines("@13\nA=M\nA=A-1\nD=M\n@4\nM=D\n")
            self.outfile.writelines("@13\nA=M\nA=A-1\nA=A-1\nD=M\n@3\nM=D\n")
            self.outfile.writelines("@13\nA=M\nA=A-1\nA=A-1\nA=A-1\nD=M\n@2\nM=D\n")
            self.outfile.writelines("@13\nA=M\nA=A-1\nA=A-1\nA=A-1\nA=A-1\nD=M\n@1\nM=D\n")

            self.outfile.writelines("// Jump to return label\n")
            self.outfile.writelines("@14\nA=M\n0;JMP\n")


        if command.__contains__("call"):
            call, fname, nargs = command.split(" ")
            self.outfile.writelines(f"// Calling {fname} {nargs}\n")
            self.outfile.writelines("// Pushing return address\n")
            self.ret_addr = f"{fname}$ret.{self.ret}"
            self.outfile.writelines(f"@{self.ret_addr}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

            for num in range(1, 5):
                self.outfile.writelines("// Push LCL, ARG, THIS, THAT onto stack\n")
                self.outfile.writelines(f"@{num}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            self.outfile.writelines("// Shifting ARG pointer\n")
            to_sub = 5+int(nargs)  # How many places to downshift stack pointer
            self.outfile.writelines(f"@SP\nD=M\n@2\nM=D\n@{to_sub}\nD=A\n@2\nM=M-D\n")
            self.outfile.writelines("// Shifting LCL pointer\n")
            self.outfile.writelines("@SP\nD=M\n@1\nM=D\n")
            self.outfile.writelines("// Jump to function\n")
            self.outfile.writelines(f"@{fname}\n0;JMP\n")
            self.outfile.writelines("// Define return label\n")
            self.outfile.writelines(f"({self.ret_addr})\n")
            self.ret += 1


    # Closes output file at end
    def close(self):
        self.outfile = self.outfile.close()



def main(base):
    # Trying to combine all files into one if I'm reading from a directory
    # Otherwise just read from the single vm file that was passed
    if os.path.isdir(f"{base}"):
        files = os.listdir(f"{base}")
        compiled = open(f"{base}_together.vm", "w")
        for file in files:
            if not file.__contains__("vm"):
                continue
            to_add = open(f"{base}/{file}", 'r')
            add_data = to_add.read()
            compiled.write(add_data)
        compiled.close()

        infile = f"{base}_together.vm"
    else:
        infile = base
        
    if os.path.isdir(f"{base}"):
        outfile = f'{base}/{base.replace(".vm", "")}.asm'

    else:
        outfile = f'{base.replace(".vm", "")}.asm'

    vmlines = Parser(infile)
    if infile.__contains__("together"):  # flag to tell CodeWriter if sysinit should be called
        asmlines = CodeWriter(outfile, f"{base}_together")
    else:
        asmlines = CodeWriter(outfile, base)

    asmlines.writeInit()
    while True:
        curr_line = vmlines.advance()
        if not curr_line:
            break
        type = vmlines.commandType()
        if type == 'C_ARITHMETIC':
            asmlines.writeArithmetic(curr_line)
        elif type in ('C_PUSH', 'C_POP'):
            asmlines.writePushPop(curr_line)
        elif type in ('C_LABEL, C_GOTO, C_IF'):
            asmlines.writeBranch(curr_line)
        elif type in ('C_FUNCTION', 'C_CALL', 'C_RETURN'):
            asmlines.writeFunc(curr_line)
    asmlines.close()

if __name__ == '__main__':
    main(sys.argv[1])
