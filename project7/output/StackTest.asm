// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// equality
@SP
M=M-1
A=M
D=M
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.EQ.0
D;JEQ
@SP
A=M
M=0
@FALSE.EQ.0
0;JMP
(TRUE.EQ.0)
@SP
A=M
M=-1
(FALSE.EQ.0)
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// equality
@SP
M=M-1
A=M
D=M
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.EQ.1
D;JEQ
@SP
A=M
M=0
@FALSE.EQ.1
0;JMP
(TRUE.EQ.1)
@SP
A=M
M=-1
(FALSE.EQ.1)
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// equality
@SP
M=M-1
A=M
D=M
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.EQ.2
D;JEQ
@SP
A=M
M=0
@FALSE.EQ.2
0;JMP
(TRUE.EQ.2)
@SP
A=M
M=-1
(FALSE.EQ.2)
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
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
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.LT.1
D;JLT
@SP
A=M
M=0
@FALSE.LT.1
0;JMP
(TRUE.LT.1)
@SP
A=M
M=-1
(FALSE.LT.1)
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.LT.2
D;JLT
@SP
A=M
M=0
@FALSE.LT.2
0;JMP
(TRUE.LT.2)
@SP
A=M
M=-1
(FALSE.LT.2)
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.GT.0
D;JGT
@SP
A=M
M=0
@FALSE.GT.0
0;JMP
(TRUE.GT.0)
@SP
A=M
M=-1
(FALSE.GT.0)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.GT.1
D;JGT
@SP
A=M
M=0
@FALSE.GT.1
0;JMP
(TRUE.GT.1)
@SP
A=M
M=-1
(FALSE.GT.1)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
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
@5
M=D
@SP
M=M-1
A=M
D=M
@5
D=D-M
@TRUE.GT.2
D;JGT
@SP
A=M
M=0
@FALSE.GT.2
0;JMP
(TRUE.GT.2)
@SP
A=M
M=-1
(FALSE.GT.2)
@SP
M=M+1
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
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
// push constant 112
@112
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
// neg
@SP
M=M-1
A=M
D=M
D=-D
M=D
@SP
M=M+1
// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M&D
M=D
@SP
M=M+1
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M|D
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
(END)
@END
0;JMP
