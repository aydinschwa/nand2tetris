// Function definition
(SimpleFunction.test)
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@0
D=A
@1
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@1
D=A
@1
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
// not
@SP
M=M-1
A=M
D=M
M=!D
@SP
M=M+1
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
// Implementing return 
@1
D=M
@13
M=D
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@14
M=D
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
@2
D=M
@0
M=D+1
@13
A=M
A=A-1
D=M
@4
M=D
@13
A=M
A=A-1
A=A-1
D=M
@3
M=D
@13
A=M
A=A-1
A=A-1
A=A-1
D=M
@2
M=D
@13
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@1
M=D
@14
D=M
A=D
0;JMP