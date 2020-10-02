// push argument 1
@1
D=A
@2
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@13
M=D
@1
D=A
@POINTER.THIS.0
D;JEQ
@13
D=M
@4
M=D
@POINTER.THAT.0
0;JMP
(POINTER.THIS.0)
@13
D=M
@3
M=D
(POINTER.THAT.0)
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@0
D=A
@4
D=M+D
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@1
D=A
@4
D=M+D
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push argument 0
@0
D=A
@2
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// subtract
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=D
@SP
M=M+1
// pop argument 0
@0
D=A
@2
D=M+D
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Initialize loop spot
(MAIN_LOOP_START)
// push argument 0
@0
D=A
@2
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// Initialize conditional goto statement
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
// Initialize unconditional goto statement
@END_PROGRAM
0; JMP
// Initialize loop spot
(COMPUTE_ELEMENT)
// push that 0
@0
D=A
@4
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@1
D=A
@4
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M+D
M=D
@SP
M=M+1
// pop that 2
@2
D=A
@4
D=M+D
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push pointer 1
@1
D=A
@POINTER.THIS.1
D;JEQ
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@POINTER.THAT.1
0;JMP
(POINTER.THIS.1)
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
(POINTER.THAT.1)
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M+D
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@13
M=D
@1
D=A
@POINTER.THIS.2
D;JEQ
@13
D=M
@4
M=D
@POINTER.THAT.2
0;JMP
(POINTER.THIS.2)
@13
D=M
@3
M=D
(POINTER.THAT.2)
// push argument 0
@0
D=A
@2
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// subtract
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=D
@SP
M=M+1
// pop argument 0
@0
D=A
@2
D=M+D
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Initialize unconditional goto statement
@MAIN_LOOP_START
0; JMP
// Initialize loop spot
(END_PROGRAM)
(END)
@END
0;JMP
