// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R2
M=0

@R0
D=M
@END
D; JEQ

@R1
D=M
@END
D; JEQ

@sum // Initialize sum at 0
M=0

(LOOP)
@R0
D=M
@sum // Add num1 to sum
M=M+D

@R1
M = M-1
D = M

@LOOP
D; JGT // If D is greater than 0, repeat loop

@sum // Get answer
D=M

@R2 // Assign answer to R2
M=D


(END)
@END
0; JMP




