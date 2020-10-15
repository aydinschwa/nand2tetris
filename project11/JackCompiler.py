# Jack compiler (project 10)

import sys
import os
import re

keywords = ["class", "constructor", "function", "method",
            "field", "static", "var", "int", "char",
            "boolean", "void", "true", "false", "null",
            "this", "let", "do", "if", "else", "while",
            "return"]
symbols = ["{", "}", "(", ")", ";", "=", ".", "[", "]",
           ",", ";", "+", "-", "*", "/", "&", "|", "<",
           ">", "~", "&lt;", "&gt;", "&amp;"]
constants = ("integerConstant", "stringConstant", "keyword")
xml = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
op = ["<", ">", "+", "-", "=", "|", "&", "*", "/", "&lt;", "&gt;", "&amp;", "~"]
op_dict = {"+": "add", "-": "sub", "=": "eq", "&gt;": "gt",
           "&lt;": "lt", "&amp;": "and", "|": "or", "~": "not", "*": "call Math.multiply 2",
           "/": "call Math.divide 2"}


class JackTokenizer:

    def __init__(self, data, directory):
        if directory:
            self.data_orig = open(f"{directory}/{data}", 'r').readlines()
        else:
            self.data_orig = open(data, 'r').readlines()
        self.current_token = ""
        self.data_nocomment = self.__stripComments()
        self.data_tokens = self.__tokenize()
        self.data_xml = self.__toXML()
        # self.out = open(f"output/{data.replace('.jack', '')}T.xml", 'w')
        # [self.out.write(x) for x in self.data_xml]
        # self.out.close()

    def write(self):
        return [x for x in self.data_xml]

    def __stripComments(self):
        data_clean = []
        data = self.data_orig
        block = False
        for line in data:
            line = line.strip().replace("\n", "")
            if line.__contains__("//"):
                keep, toss, toss = line.partition("//")
                if keep:
                    data_clean.append(keep)
                continue
            if line.__contains__("/**"):
                block = True
            if line.__contains__("*/"):
                block = False
                continue
            if (not block) and line:
                data_clean.append(line)
        return data_clean

    def __tokenize(self):
        data_clean = []
        data = self.data_nocomment
        for line in data:
            word = ""
            quote = 0
            for letter in line:
                if letter == '"':
                    quote += 1
                    word += '"'
                if letter.isalnum() | (quote > 0 and letter == " "):
                    word += letter
                elif letter in symbols and quote != 1:
                    if letter in xml:
                        letter = xml[letter]
                    data_clean.append(word)
                    data_clean.append(letter)
                    word = ""
                elif quote == 1:
                    word += letter
                elif letter == " " and word and (quote == 0 or quote == 2):
                    if word.__contains__('"'):
                        word += '"'
                    data_clean.append(word)
                    word = ""
        data_clean = [data for data in data_clean if data]
        return data_clean

    def __toXML(self):
        data_clean = []
        # data_clean.append("<tokens>\n")
        while self.advance():
            left_tag = f"<{self.tokenType()}>"
            right_tag = f"</{self.tokenType()}>"
            key = self.current_token
            data_clean.append(f"{left_tag} {key} {right_tag}\n".replace('"', ''))
        # data_clean.append("</tokens>\n")
        return data_clean

    def advance(self):
        try:
            self.current_token = self.data_tokens.pop(0)
            return self.current_token
        except IndexError:
            return False

    def tokenType(self):
        if self.current_token in keywords:
            return "keyword"
        elif self.current_token in symbols:
            return "symbol"
        elif re.search("^[A-Za-z_][A-Za-z0-9_]*", self.current_token):
            return "identifier"
        elif self.current_token.isnumeric() and int(self.current_token) <= 32767:
            return "integerConstant"
        elif self.current_token.__contains__('"'):
            return "stringConstant"
        else:
            raise Exception(f"Cannot determine type of {self.current_token}")


class CompilationEngine:

    def __init__(self, tokens, name, dirname):
        self.class_name = name.replace('.jack', '')
        self.tokens = tokens
        self.current_token = self.advance()
        self.word = re.search("> (.+) <", self.current_token).groups()[0]
        self.tag = re.search("<([a-z]+)>", self.current_token).groups()[0]
        self.data = []
        self.VM_out = VMWriter(dirname, self.class_name)
        # Declare class and subroutine symbol tables
        self.class_symbols = SymbolTable()
        self.sub_symbols = SymbolTable()

        self.n_args = 0
        self.if_count = 0
        self.while_count = 0

        self.compileClass()
        # self.XML_out = open(f"{dirname}/{name.replace('.jack', '')}.xml", 'w')
        # [self.XML_out.write(x) for x in self.data]
        # self.VM_out.close()

    def advance(self):
        try:
            self.current_token = self.tokens.pop(0)
            self.word = re.search("> (.+) <", self.current_token).groups()[0]
            self.tag = re.search("<([a-zA-Z]+)>", self.current_token).groups()[0]
            return self.current_token

        except IndexError:
            return False

    def eat(self, string):
        if self.word != string:
            raise Exception(f"{self.word} should be {string}")
        else:
            self.data.append(self.current_token)
            self.advance()

    def compileClass(self):
        self.data.append("<class>\n")

        # 'class'
        self.eat("class")

        # ClassName
        if self.current_token.__contains__("identifier"):
            self.data.append(self.current_token)
            self.advance()
        else:
            raise Exception(f"{self.tag} is not identifier")

        # '{'
        self.eat("{")

        # classVarDec*
        while True:
            if self.word not in ("static", "field"):
                break
            self.compileClassVarDec()

        # subroutineDec*
        while True:
            if self.word not in ("constructor", "function", "method"):
                break
            self.compileSubroutine()

        # '}'
        self.eat("}")

        self.data.append("</class>\n")

    def compileClassVarDec(self):
        self.data.append("<classVarDec>\n")

        # ('static'|'field')
        if self.word in ("static", "field"):
            self.class_symbols.current_kind = self.word
            self.data.append(self.current_token)
            self.advance()
        else:
            raise Exception(f"{self.word} is not static or field")

        # type. Weird because of ClassName issue. Feel like I have to allow any alnum
        if self.word.isalnum():
            self.class_symbols.current_type = self.word
            self.data.append(self.current_token)
            self.advance()
        else:
            raise Exception(f"{self.word} is not an allowed type")

        # varName(',' varName)*
        while True:
            # Append the first varName since that's always there
            self.class_symbols.current_name = self.word
            self.data.append(self.current_token)
            self.advance()
            self.class_symbols.Define(self.class_symbols.current_name,
                                      self.class_symbols.current_type,
                                      self.class_symbols.current_kind)

            if self.word != ",":
                break
            else:
                self.data.append(self.current_token)
                self.advance()

        self.eat(';')
        self.data.append("</classVarDec>\n")

    def compileSubroutine(self):
        # Declare symbol table for subroutine
        self.sub_symbols = SymbolTable()
        self.data.append("<subroutineDec>\n")
        method = False

        # ('constructor'|'function'|'method')
        if self.word in ("constructor", "function", "method"):
            self.data.append(self.current_token)
        else:
            raise Exception(f"{self.word} is not constructor, function, or method")

        # ('void'|type) subroutineName
        if self.word == "constructor":
            self.advance()
            if self.word == "void":
                raise Exception("constructor cannot return void")
            else:
                obj_size = self.class_symbols.VarCount("FIELD")

                # anchor the base address of the object
                self.VM_out.writeFunction(f"{self.class_name}.new", 0)
                self.VM_out.writePush(["push", "constant", obj_size])
                self.VM_out.writeCall("Memory.alloc", 1)
                self.VM_out.writePop(["pop", "pointer", "0"])

                self.data.append(self.current_token)
                self.advance()
        else:
            # add 'this' to subroutine symbol table
            if self.word == "method":
                method = True
                self.sub_symbols.Define("this", self.class_name, "argument")
                self.data.append(self.current_token)
                self.advance()
                self.advance()
            elif self.word == "function":
                self.advance()
                self.advance()

        # function/method name
        fm_name = self.word
        self.data.append(self.current_token)
        self.advance()

        # '('
        self.eat('(')

        # parameterList
        self.compileParameterList()

        # ')'
        self.eat(')')

        # subroutineBody
        self.data.append("<subroutineBody>\n")
        # '{'
        self.eat('{')

        # varDec*
        pre = self.sub_symbols.size()
        while True:
            if self.word not in "var":
                break
            else:
                self.compileVarDec()

        post = self.sub_symbols.size()
        locals = post - pre

        if method:
            # anchor base of 'this' segment
            self.VM_out.writeFunction(f"{self.class_name}.{fm_name}", locals)
            self.VM_out.writePush(["push", "argument", "0"])
            self.VM_out.writePop(["pop", "pointer", "0"])
        elif fm_name != "new":
            self.VM_out.writeFunction(f"{self.class_name}.{fm_name}", locals)

        # statements
        self.compileStatements()

        # '}'
        self.eat('}')
        self.data.append("</subroutineBody>\n")

        self.data.append("</subroutineDec>\n")

    def compileParameterList(self):
        # Every item in a parameterList is an argument
        self.sub_symbols.current_kind = "argument"
        self.data.append("<parameterList>\n")

        if self.word.isalnum():
            # type
            self.sub_symbols.current_type = self.word
            self.data.append(self.current_token)
            self.advance()
            # varName
            self.sub_symbols.current_name = self.word
            self.data.append(self.current_token)
            self.advance()
            # Add to subroutine symbol table
            self.sub_symbols.Define(self.sub_symbols.current_name,
                                    self.sub_symbols.current_type,
                                    self.sub_symbols.current_kind)
            while True:
                if self.word != ",":
                    break
                else:
                    self.eat(",")
                    # type
                    self.sub_symbols.current_type = self.word
                    self.data.append(self.current_token)
                    self.advance()
                    # varName
                    self.sub_symbols.current_name = self.word
                    self.data.append(self.current_token)
                    self.advance()
                    # add to subroutine symbol table
                    self.sub_symbols.Define(self.sub_symbols.current_name,
                                            self.sub_symbols.current_type,
                                            self.sub_symbols.current_kind)
        self.data.append("</parameterList>\n")

    def compileVarDec(self):
        self.sub_symbols.current_kind = "var"
        self.data.append("<varDec>\n")
        # 'var'
        self.eat('var')

        # type
        self.sub_symbols.current_type = self.word
        self.data.append(self.current_token)
        self.advance()

        # varName
        while True:
            # Append the first varName since that's always there
            self.sub_symbols.current_name = self.word
            self.data.append(self.current_token)
            self.advance()
            self.sub_symbols.Define(self.sub_symbols.current_name,
                                    self.sub_symbols.current_type,
                                    self.sub_symbols.current_kind)
            if self.word != ",":
                break
            else:
                self.data.append(self.current_token)
                self.advance()

        self.eat(';')
        self.data.append("</varDec>\n")

    def compileStatements(self):
        self.data.append("<statements>\n")
        # statement*
        while True:
            if self.word not in ("if", "let", "while", "do", "return"):
                break

            # letStatement|ifStatement|whileStatement|doStatement|returnStatement
            if self.word == "if":
                self.compileIf()

            if self.word == "let":
                self.compileLet()

            if self.word == "while":
                self.compileWhile()

            if self.word == "do":
                self.compileDo()

            if self.word == "return":
                self.compileReturn()

        self.data.append("</statements>\n")

    def compileDo(self):
        self.data.append("<doStatement>\n")

        # 'do'
        self.data.append(self.current_token)
        self.advance()

        # subroutineCall
        self.compileExpression()

        # pop the temp segment
        self.VM_out.writePop(["pop", "temp", "0"])

        # ';'
        self.eat(';')

        self.data.append("</doStatement>\n")

    def compileLet(self):
        self.data.append("<letStatement>\n")
        # 'let'
        self.data.append(self.current_token)
        self.advance()

        # varName
        var_name = self.word
        arr = False
        self.data.append(self.current_token)

        # ('['expression']')?
        if self.tokens[0].__contains__("["):
            arr = True
            self.compileExpression()
        else:
            self.advance()

            # '='
            self.eat('=')

        # expression
        self.compileExpression()

        if arr:
            self.VM_out.writePop(["pop", "temp", "0"])
            self.VM_out.writePop(["pop", "pointer", "1"])
            self.VM_out.writePush(["push", "temp", "0"])
            self.VM_out.writePop(["pop", "that", "0"])
        else:
            try:
                self.VM_out.writePop(self.sub_symbols.symbols[var_name])
            except KeyError:
                self.VM_out.writePop(self.class_symbols.symbols[var_name])

        # ';'
        self.eat(';')

        self.data.append("</letStatement>\n")

    def compileWhile(self):
        self.data.append("<whileStatement>\n")
        l1 = 0 + self.while_count
        l2 = 1 + self.while_count
        self.while_count += 2

        # 'while'
        self.data.append(self.current_token)
        self.advance()

        self.VM_out.writeLabel(f"{self.class_name}.WHILE.{l1}")

        # '('
        self.eat('(')

        # expression
        self.compileExpression()
        self.VM_out.writeArithmetic(op_dict["~"])
        self.VM_out.writeIf(f"{self.class_name}.WHILE.{l2}")

        # ')'
        self.eat(')')
        # '{'
        self.eat('{')

        # statements
        self.compileStatements()
        self.VM_out.writeGoto(f"{self.class_name}.WHILE.{l1}")
        self.VM_out.writeLabel(f"{self.class_name}.WHILE.{l2}")

        # '}'
        self.eat('}')

        self.data.append("</whileStatement>\n")

    def compileReturn(self):
        self.data.append("<returnStatement>\n")

        # 'return'
        self.data.append(self.current_token)
        self.advance()

        # this?
        if self.word == "this":
            self.advance()
            self.VM_out.writePush(["push", "pointer", "0"])

        # expression?
        elif self.word != ';':
            self.compileExpression()
        else:
            self.VM_out.writePush(["push", "constant", "0"])

        # ';'
        self.eat(';')

        self.VM_out.writeReturn()
        self.data.append("</returnStatement>\n")

    def compileIf(self):
        l1 = 0 + self.if_count
        l2 = 1 + self.if_count
        l3 = 2 + self.if_count
        self.if_count += 3
        self.data.append("<ifStatement>\n")

        # 'if'
        self.eat('if')

        # '('
        self.eat('(')

        # expression
        self.compileExpression()
        self.VM_out.writeIf(f"{self.class_name}.IF.{l1}")
        self.VM_out.writeGoto(f"{self.class_name}.IF.{l2}")
        self.VM_out.writeLabel(f"{self.class_name}.IF.{l1}")
        # ')'
        self.eat(')')

        # '{'
        self.eat('{')

        # statements

        self.compileStatements()
        # '}'
        self.eat('}')

        # ('else' '{'statements'}')?
        if self.word == "else":
            self.VM_out.writeGoto(f"{self.class_name}.IF.{l3}")
            self.eat('else')
            self.eat('{')
            self.VM_out.writeLabel(f"{self.class_name}.IF.{l2}")
            self.compileStatements()
            self.VM_out.writeLabel(f"{self.class_name}.IF.{l3}")
            self.eat('}')
        else:
            self.VM_out.writeLabel(f"{self.class_name}.IF.{l2}")

        self.data.append("</ifStatement>\n")

    def compileExpression(self):
        self.data.append("<expression>\n")

        # term
        self.compileTerm()

        while True:

            # op
            if self.word in op:
                operator = self.word
                self.data.append(self.current_token)
                self.advance()

                # term
                self.compileTerm()
                self.VM_out.writeArithmetic(op_dict[operator])
            else:
                break

        self.data.append("</expression>\n")

    def compileTerm(self):
        self.data.append("<term>\n")

        # integerConstant, stringConstant, keyword
        if self.tag in constants:
            if self.word == "true":
                self.VM_out.writePush(["int", "constant", "0"])
                self.VM_out.writeArithmetic(op_dict["~"])
            if self.word == "false":
                self.VM_out.writePush(["int", "constant", "0"])
            if self.word == "null":
                self.VM_out.writePush(["int", "constant", "0"])
            if self.tag == "integerConstant":
                self.VM_out.writePush(["int", "constant", self.word])
            if self.word == "this":
                self.VM_out.writePush(["push", "pointer", "0"])
            if self.tag == "stringConstant":
                self.VM_out.writePush(["push", "constant", len(self.word)])
                self.VM_out.writeCall("String.new", "1")
                for i in range(len(self.word)):
                    self.VM_out.writePush(["push", "constant", ord(self.word[i])])
                    self.VM_out.writeCall("String.appendChar", 2)
            self.data.append(self.current_token)
            self.advance()
            self.data.append("</term>\n")
            return

        # varName[expression]
        if self.word.isalnum() and self.tokens[0].__contains__("["):
            self.data.append(self.current_token)
            try:
                self.VM_out.writePush(self.sub_symbols.symbols[self.word])
            except KeyError:
                self.VM_out.writePush(self.class_symbols.symbols[self.word])
            self.advance()
            self.eat("[")
            self.compileExpression()
            self.VM_out.writeArithmetic("add")
            self.eat("]")
            if self.word == "=":
                self.eat("=")
            else:
                self.VM_out.writePop(["pop", "pointer", "1"])
                self.VM_out.writePush(["push", "that", "0"])
            self.data.append("</term>\n")
            return

        # subroutineCall(expression)
        if self.word.isalnum() and self.tokens[0].__contains__("."):
            class_name = self.word
            if class_name[0].islower():
                try:
                    self.VM_out.writePush(self.sub_symbols.symbols[self.word])
                except KeyError:
                    self.VM_out.writePush(self.class_symbols.symbols[self.word])
            self.data.append(self.current_token)
            self.advance()
            self.eat(".")
            # call self.class_name.method
            method_name = self.word
            self.data.append(self.current_token)  # method
            self.advance()
            self.eat("(")
            self.compileExpressionList()
            self.eat(")")
            self.data.append("</term>\n")

            if class_name[0].islower():
                self.n_args += 1
                try:
                    self.VM_out.writeCall(f"{self.sub_symbols.TypeOf(class_name)}.{method_name}", self.n_args)
                except KeyError:
                    self.VM_out.writeCall(f"{self.class_symbols.TypeOf(class_name)}.{method_name}", self.n_args)
            else:
                self.VM_out.writeCall(f"{class_name}.{method_name}", self.n_args)
            return

        # unaryOp term
        if self.word == "(" and self.tokens[0].__contains__("-"):
            self.eat("(")
            self.compileExpression()
            self.eat(")")
            self.data.append("</term>\n")
            return

        if self.word == "-":
            self.eat("-")
            self.compileTerm()
            self.VM_out.writeArithmetic("neg")
            self.data.append("</term>\n")
            return

        if self.word == "~":
            self.eat("~")
            self.compileTerm()
            self.VM_out.writeArithmetic(op_dict["~"])
            self.data.append("</term>\n")
            return

        # (expression)
        if self.word == "(":
            self.eat("(")
            self.compileExpression()
            self.eat(")")
            self.data.append("</term>\n")
            return

        if self.word.isalnum() and self.tokens[0].__contains__("("):
            method_name = self.word
            self.advance()
            self.eat("(")
            self.VM_out.writePush(["push", "pointer", "0"])
            self.compileExpressionList()
            self.eat(")")
            self.VM_out.writeCall(f"{self.class_name}.{method_name}", self.n_args + 1)

        # varName
        if self.word.isalnum():
            try:
                self.VM_out.writePush(self.sub_symbols.symbols[self.word])
            except KeyError:
                self.VM_out.writePush(self.class_symbols.symbols[self.word])
            self.data.append(self.current_token)
            self.advance()
            self.data.append("</term>\n")
            return

    def compileExpressionList(self):
        self.data.append("<expressionList>\n")
        self.n_args = 0

        # ('['expression']')?

        # Empty statement body
        if self.word == ')':
            self.data.append("</expressionList>\n")
            return

        # List body
        while True:
            self.n_args += 1
            self.compileExpression()
            if self.word != ',':
                break
            self.eat(',')

        self.data.append("</expressionList>\n")


class SymbolTable:

    def __init__(self):
        self.symbols = {}
        self.static = 0
        self.field = 0
        self.arg = 0
        self.var = 0  # var is local segment
        self.current_name = ""
        self.current_type = ""
        self.current_kind = ""

    # Call when a new subroutine is compiled
    def startSubroutine(self):
        self.symbols = {}
        self.arg = 0
        self.var = 0

    def size(self):
        return len(self.symbols)

    def Define(self, name, type, kind):
        if kind == "static":
            index = self.static
            self.static += 1
        elif kind == "field":
            index = self.field
            self.field += 1
        elif kind == "argument":
            index = self.arg
            self.arg += 1
        elif kind == "var":
            index = self.var
            self.var += 1
        else:
            raise Exception("kind is not static, field, arg, or var!")

        self.symbols[name] = [type, kind, index]

    def VarCount(self, kind):
        if kind == "STATIC":
            return self.static
        if kind == "FIELD":
            return self.field
        if kind == "ARG":
            return self.arg
        if kind == "VAR":
            return self.var

    def KindOf(self, name):
        return self.symbols[name][1]

    def TypeOf(self, name):
        return self.symbols[name][0]

    def IndexOf(self, name):
        return self.symbols[name][2]


class VMWriter:

    def __init__(self, dirname, class_name):
        self.outfile = open(f"{dirname}/{class_name}.vm", "w")
        # self.outfile = open(f"/Users/Aydin/Desktop/Mine/{class_name}.vm", "w")

    def writePush(self, segment):
        # push kind index
        segment[1] = segment[1].replace('var', 'local').replace('field', 'this')
        self.outfile.write(f"push {segment[1]} {segment[2]}\n")

    def writePop(self, segment):
        # pop kind index
        segment[1] = segment[1].replace('var', 'local').replace('field', 'this')
        self.outfile.write(f"pop {segment[1]} {segment[2]}\n")

    def writeArithmetic(self, command):
        self.outfile.write(f"{command}\n")

    def writeLabel(self, label):
        self.outfile.write(f"label {label}\n")

    def writeGoto(self, label):
        self.outfile.write(f"goto {label}\n")

    def writeIf(self, label):
        self.outfile.write(f"if-goto {label}\n")

    def writeCall(self, name, n_args):
        self.outfile.write(f"call {name} {n_args}\n")

    def writeFunction(self, name, n_locals):
        self.outfile.write(f"function {name} {n_locals}\n")

    def writeReturn(self):
        self.outfile.write("return\n")

    def close(self):
        self.outfile.close()


class JackCompiler:

    def __init__(self, data):
        if os.path.isdir(data):
            files = os.listdir(data)
            for file in files:
                if not file.__contains__(".jack"):
                    continue
                tokens = JackTokenizer(file, data).write()
                CompilationEngine(tokens, file, data)
        else:
            tokens = JackTokenizer(data, False).write()
            CompilationEngine(tokens, data, False)


# Driver code
if __name__ == "__main__":
    JackCompiler(sys.argv[1])
