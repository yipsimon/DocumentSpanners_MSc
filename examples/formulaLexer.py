# Generated from formula.g4 by ANTLR 4.5.1
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\16J\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write(u"\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t")
        buf.write(u"\r\4\16\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\4")
        buf.write(u"\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n")
        buf.write(u"\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3")
        buf.write(u"\17\6\17@\n\17\r\17\16\17A\3\20\6\20E\n\20\r\20\16\20")
        buf.write(u"F\3\20\3\20\2\2\21\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write(u"\23\13\25\2\27\2\31\2\33\f\35\r\37\16\3\2\6\3\2c|\3\2")
        buf.write(u"C\\\3\2\62;\5\2\13\f\17\17\"\"I\2\3\3\2\2\2\2\5\3\2\2")
        buf.write(u"\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2")
        buf.write(u"\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\33\3\2\2\2\2")
        buf.write(u"\35\3\2\2\2\2\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2\7%\3\2")
        buf.write(u"\2\2\t\'\3\2\2\2\13)\3\2\2\2\r+\3\2\2\2\17-\3\2\2\2\21")
        buf.write(u"/\3\2\2\2\23\61\3\2\2\2\25\63\3\2\2\2\27\65\3\2\2\2\31")
        buf.write(u"\67\3\2\2\2\339\3\2\2\2\35?\3\2\2\2\37D\3\2\2\2!\"\7")
        buf.write(u"*\2\2\"\4\3\2\2\2#$\7\60\2\2$\6\3\2\2\2%&\7+\2\2&\b\3")
        buf.write(u"\2\2\2\'(\7,\2\2(\n\3\2\2\2)*\7~\2\2*\f\3\2\2\2+,\7-")
        buf.write(u"\2\2,\16\3\2\2\2-.\7}\2\2.\20\3\2\2\2/\60\7<\2\2\60\22")
        buf.write(u"\3\2\2\2\61\62\7\177\2\2\62\24\3\2\2\2\63\64\t\2\2\2")
        buf.write(u"\64\26\3\2\2\2\65\66\t\3\2\2\66\30\3\2\2\2\678\t\4\2")
        buf.write(u"\28\32\3\2\2\29:\7\61\2\2:;\7g\2\2;<\7o\2\2<\34\3\2\2")
        buf.write(u"\2=@\5\25\13\2>@\5\27\f\2?=\3\2\2\2?>\3\2\2\2@A\3\2\2")
        buf.write(u"\2A?\3\2\2\2AB\3\2\2\2B\36\3\2\2\2CE\t\5\2\2DC\3\2\2")
        buf.write(u"\2EF\3\2\2\2FD\3\2\2\2FG\3\2\2\2GH\3\2\2\2HI\b\20\2\2")
        buf.write(u"I \3\2\2\2\6\2?AF\3\b\2\2")
        return buf.getvalue()


class formulaLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    EMPTY = 10
    LETTER = 11
    WS = 12

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'('", u"'.'", u"')'", u"'*'", u"'|'", u"'+'", u"'{'", u"':'", 
            u"'}'", u"'/em'" ]

    symbolicNames = [ u"<INVALID>",
            u"EMPTY", u"LETTER", u"WS" ]

    ruleNames = [ u"T__0", u"T__1", u"T__2", u"T__3", u"T__4", u"T__5", 
                  u"T__6", u"T__7", u"T__8", u"LOWERCASE", u"UPPERCASE", 
                  u"DIGIT", u"EMPTY", u"LETTER", u"WS" ]

    grammarFileName = u"formula.g4"

    def __init__(self, input=None):
        super(formulaLexer, self).__init__(input)
        self.checkVersion("4.5.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


