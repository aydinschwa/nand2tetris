// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.



(PRELOOP)
@KBD
D=M
@old
D=M-D
@LOOP
D; JNE

(LOOP)

@SCREEN
D=A
@array //pointer to the index where SCREEN starts
M=D

@8192     //pointer to the length of SCREEN map
D=A
@n
M=D

@i     //reset increment
M=0

@KBD
D=M
@old
M=D
@BLACK
D; JNE

(WHITE)
@array //get index from pointer
D=M
@i
A=M+D //will sequentially pull elements from the array
M=0   //sets each register to 0
@i
M=M+1
@n
M=M-1
D=M
@WHITE
D; JNE //if n>0, repeat
@PRELOOP
0; JMP //else, jump back to top



(BLACK)
@array //get index from pointer
D=M
@i
A=M+D //will sequentially pull elements from the array
M=-1  //sets each register to -1
@i    //increments i
M=M+1
@n
M=M-1 //decreases n for every operation
D=M   //once n hits 0, the loop will break
@BLACK
D; JNE //if n>0, repeat
@PRELOOP
0; JMP //else, jump back to top







