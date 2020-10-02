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
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@15
M=D
@0
D=A
@POINTER.THIS.0
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.0
0;JMP
(POINTER.THIS.0)
@15
D=M
@3
M=D
(POINTER.THAT.0)
// push constant 5000
@5000
D=A
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
@15
M=D
@1
D=A
@POINTER.THIS.1
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.1
0;JMP
(POINTER.THIS.1)
@15
D=M
@3
M=D
(POINTER.THAT.1)
// Calling Sys.main 0
// Pushing return address
@Sys.main$ret.2
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
@Sys.main
0;JMP
// Define return label
(Sys.main$ret.2)
// pop temp 1
@SP
M=M-1
A=M
D=M
@6
M=D
// loop spot
(Sys.init$LOOP)
// Initialize unconditional goto statement
@Sys.init$LOOP
0; JMP
// Function definition
(Sys.main)
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
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@15
M=D
@0
D=A
@POINTER.THIS.2
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.2
0;JMP
(POINTER.THIS.2)
@15
D=M
@3
M=D
(POINTER.THAT.2)
// push constant 5001
@5001
D=A
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
@15
M=D
@1
D=A
@POINTER.THIS.3
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.3
0;JMP
(POINTER.THIS.3)
@15
D=M
@3
M=D
(POINTER.THAT.3)
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@1
D=A
@1
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@2
D=A
@1
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@3
D=A
@1
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
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// Calling Sys.add12 1
// Pushing return address
@Sys.add12$ret.3
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
@Sys.add12
0;JMP
// Define return label
(Sys.add12$ret.3)
// pop temp 0
@SP
M=M-1
A=M
D=M
@5
M=D
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
// push local 2
@2
D=A
@1
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 3
@3
D=A
@1
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 4
@4
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
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@15
M=D
@0
D=A
@POINTER.THIS.4
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.4
0;JMP
(POINTER.THIS.4)
@15
D=M
@3
M=D
(POINTER.THAT.4)
// push constant 5002
@5002
D=A
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
@15
M=D
@1
D=A
@POINTER.THIS.5
D;JEQ
@15
D=M
@4
M=D
@POINTER.THAT.5
0;JMP
(POINTER.THIS.5)
@15
D=M
@3
M=D
(POINTER.THAT.5)
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
// push constant 12
@12
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
