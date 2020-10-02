#Project 10: Compiler 1: Syntax Analysis

From the nand2tetris website:


Background:

The Jack compiler, like those of Java and C#, is two-tiered: the compiler's front-end translates from the high-level language to an intermediate VM language; the compiler's back-end translates further from the VM language to the native code of the host platform. In projects 7-8 we've built the compiler's back-end (the VM translator); we now turn to building the compiler's front-end. This development will span two projects: syntax analysis (this project), and code generation (next project). Welcome to syntax analysis.


Objective:

In this project we build a syntax analyzer that parses Jack programs according to the Jack grammar, producing an XML file that renders the program's structure using marked-up text. In the next project, the logic that generates the XML output will be morphed into logic that generates VM code.