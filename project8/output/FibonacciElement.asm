// Initializing pointers
@256
D=A
@0
M=D
@300
D=A
@1
M=D
@400
D=A
@2
M=D
// Calling Sys.init

// Calling Sys.init 0
// Pushing return address
@Sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// Shifting ARG pointer
@SP
D=M
@2
M=D
@5
D=A
@2
M=M-D
// Shifting LCL pointer
@SP
D=M
@1
M=D
// Jump to function
@Sys.init
0;JMP
// Define return label
(Sys.init$ret.1)
// Function definition
(Main.fibonacci)
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
// less than
@SP
M=M-1
A=M
D=M
@15
M=D
@SP
M=M-1
A=M
D=M
@15
D=D-M
@TRUE.LT.0
D;JLT
@SP
A=M
M=0
@FALSE.LT.0
0;JMP
(TRUE.LT.0)
@SP
A=M
M=-1
(FALSE.LT.0)
@SP
M=M+1
// Initialize conditional goto statement
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// Initialize unconditional goto statement
@Main.fibonacci$IF_FALSE
0; JMP
// loop spot
(Main.fibonacci$IF_TRUE)
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
@15
M=D
@SP
M=M-1
A=M
D=M
@15
A=M
M=D
@2
D=M
@0
M=D+1
// Restoring memory segments 
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
// Jump to return label
@14
A=M
0;JMP
// loop spot
(Main.fibonacci$IF_FALSE)
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
// Calling Main.fibonacci 1
// Pushing return address
@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// Shifting ARG pointer
@SP
D=M
@2
M=D
@6
D=A
@2
M=M-D
// Shifting LCL pointer
@SP
D=M
@1
M=D
// Jump to function
@Main.fibonacci
0;JMP
// Define return label
(Main.fibonacci$ret.2)
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
// Calling Main.fibonacci 1
// Pushing return address
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// Shifting ARG pointer
@SP
D=M
@2
M=D
@6
D=A
@2
M=M-D
// Shifting LCL pointer
@SP
D=M
@1
M=D
// Jump to function
@Main.fibonacci
0;JMP
// Define return label
(Main.fibonacci$ret.3)
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
@15
M=D
@SP
M=M-1
A=M
D=M
@15
A=M
M=D
@2
D=M
@0
M=D+1
// Restoring memory segments 
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
// Jump to return label
@14
A=M
0;JMP
// Function definition
(Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// Calling Main.fibonacci 1
// Pushing return address
@Main.fibonacci$ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push LCL, ARG, THIS, THAT onto stack
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// Shifting ARG pointer
@SP
D=M
@2
M=D
@6
D=A
@2
M=M-D
// Shifting LCL pointer
@SP
D=M
@1
M=D
// Jump to function
@Main.fibonacci
0;JMP
// Define return label
(Main.fibonacci$ret.4)
// loop spot
(Sys.init$WHILE)
// Initialize unconditional goto statement
@Sys.init$WHILE
0; JMP
