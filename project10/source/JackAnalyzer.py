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
xml = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
op = ["<", ">", "+", "-", "=", "|", "&", "*", "/", "&lt;", "&gt;", "&amp;", "~"]


# This class passes all the comparison tests and is well-behaving.
# Outputs XML files labeled xxxT.xml
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
        self.tokens = tokens
        self.current_token = self.advance()
        self.word = re.search("> (.+) <", self.current_token).groups()[0]
        self.tag = re.search("<([a-z]+)>", self.current_token).groups()[0]
        self.vars = []
        self.data = []
        self.compileClass()
        self.XML_out = open(f"{dirname}/{name.replace('.jack', '')}.xml", 'w')
        [self.XML_out.write(x) for x in self.data]

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
            [print(x) for x in self.data]
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
            self.data.append(self.current_token)
            self.advance()
        else:
            raise Exception(f"{self.word} is not static or field")

        # type. Weird because of ClassName issue. Feel like I have to allow any alnum
        if self.word.isalnum():
            self.data.append(self.current_token)
            self.advance()
        else:
            raise Exception(f"{self.word} is not an allowed type")

        # varName(',' varName)*
        while True:
            # Append the first varName since that's always there
            self.data.append(self.current_token)
            self.vars.append(self.word)
            self.advance()
            if self.word != ",":
                break
            else:
                self.data.append(self.current_token)
                self.advance()

        self.eat(';')
        self.data.append("</classVarDec>\n")

    def compileSubroutine(self):
        self.data.append("<subroutineDec>\n")

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
                self.data.append(self.current_token)
                self.advance()
        else:
            self.advance()
            self.data.append(self.current_token)
            self.advance()

        # function/method name
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
        while True:
            if self.word not in "var":
                break
            else:
                self.compileVarDec()

        # statements
        self.compileStatements()

        # '}'
        self.eat('}')
        self.data.append("</subroutineBody>\n")

        self.data.append("</subroutineDec>\n")

    def compileParameterList(self):
        self.data.append("<parameterList>\n")

        if self.word.isalnum():
            # type
            self.data.append(self.current_token)
            self.advance()
            # varName
            self.data.append(self.current_token)
            self.advance()
            while True:
                if self.word != ",":
                    break
                else:
                    self.eat(",")
                    # type
                    self.data.append(self.current_token)
                    self.advance()
                    # varName
                    self.data.append(self.current_token)
                    self.advance()

        self.data.append("</parameterList>\n")

    def compileVarDec(self):
        self.data.append("<varDec>\n")
        # 'var'
        self.eat('var')

        # type
        self.data.append(self.current_token)
        self.advance()

        # varName
        while True:
            # Append the first varName since that's always there
            self.data.append(self.current_token)
            self.vars.append(self.word)
            self.advance()
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
        self.data.append(self.current_token)  # class
        self.advance()

        if self.word == ".":
            self.eat(".")
            self.data.append(self.current_token)  # method
            self.advance()

        # '('
        self.eat("(")

        #
        self.compileExpressionList()

        # ')'
        self.eat(")")

        # ';'
        self.eat(';')

        self.data.append("</doStatement>\n")

    def compileLet(self):
        self.data.append("<letStatement>\n")
        # 'let'
        self.data.append(self.current_token)
        self.advance()

        # varName
        self.data.append(self.current_token)
        self.advance()

        # ('['expression']')?
        if self.word == "[":
            self.eat("[")
            self.compileExpression()
            self.eat("]")

        # '='
        self.eat('=')

        # expression
        self.compileExpression()

        # ';'
        self.eat(';')

        self.data.append("</letStatement>\n")

    def compileWhile(self):
        self.data.append("<whileStatement>\n")
        # 'while'
        self.data.append(self.current_token)
        self.advance()

        # '('
        self.eat('(')

        # expression
        self.compileExpression()

        # ')'
        self.eat(')')
        # '{'
        self.eat('{')

        # statements
        self.compileStatements()

        # '}'
        self.eat('}')

        self.data.append("</whileStatement>\n")

    def compileReturn(self):
        self.data.append("<returnStatement>\n")

        # 'return'
        self.data.append(self.current_token)
        self.advance()

        # expression?
        if self.word != ';':
            self.compileExpression()

        # ';'
        self.eat(';')

        self.data.append("</returnStatement>\n")

    def compileIf(self):
        self.data.append("<ifStatement>\n")

        # 'if'
        self.eat('if')

        # '('
        self.eat('(')

        # expression
        self.compileExpression()

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
            self.eat('else')
            self.eat('{')
            self.compileStatements()
            self.eat('}')

        self.data.append("</ifStatement>\n")

    def compileExpression(self):
        self.data.append("<expression>\n")

        # term
        self.compileTerm()

        while True:
            # op
            if self.word in op:
                self.data.append(self.current_token)
                self.advance()

                # term
                self.compileTerm()
            else:
                break

        self.data.append("</expression>\n")

    def compileTerm(self):
        constants = ("integerConstant", "stringConstant", "keywordConstant")
        self.data.append("<term>\n")

        # integerConstant, stringConstant, keywordConstant
        if self.tag in constants:
            self.data.append(self.current_token)
            self.advance()
            self.data.append("</term>\n")
            return

        # varName[expression]
        if self.word.isalnum() and self.tokens[0].__contains__("["):
            self.data.append(self.current_token)
            self.advance()
            self.eat("[")
            self.compileExpression()
            self.eat("]")
            self.data.append("</term>\n")
            return

        # subroutineCall(expression)
        if self.word.isalnum() and self.tokens[0].__contains__("."):
            self.data.append(self.current_token)
            self.advance()
            self.eat(".")
            self.data.append(self.current_token)  # method
            self.advance()
            self.eat("(")
            self.compileExpressionList()
            self.eat(")")
            self.data.append("</term>\n")
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
            self.data.append("</term>\n")
            return

        if self.word == "~":
            self.eat("~")
            self.compileTerm()
            self.data.append("</term>\n")
            return

        # (expression)
        if self.word == "(":
            self.eat("(")
            self.compileExpression()
            self.eat(")")
            self.data.append("</term>\n")
            return

        # varName
        if self.word.isalnum():
            self.data.append(self.current_token)
            self.advance()
            self.data.append("</term>\n")
            return

    def compileExpressionList(self):
        self.data.append("<expressionList>\n")

        # ('['expression']')?

        # Empty statement body
        if self.word == ')':
            self.data.append("</expressionList>\n")
            return

        # List body
        while True:
            self.compileExpression()
            if self.word != ',':
                break
            self.eat(',')

        self.data.append("</expressionList>\n")


class JackAnalyzer:

    def __init__(self, data):
        if os.path.isdir(data):
            files = os.listdir(data)
            for file in files:
                if file == ".DS_Store" or file.__contains__("xml"):
                    continue
                tokens = JackTokenizer(file, data).write()
                CompilationEngine(tokens, file, data)
        else:
            tokens = JackTokenizer(data, False).write()
            CompilationEngine(tokens, data, False)


# Driver code
if __name__ == "__main__":
    JackAnalyzer(sys.argv[1])
    #JackAnalyzer("ExpressionLessSquare")
