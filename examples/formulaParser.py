# Generated from formula.g4 by ANTLR 4.5.1
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\16=\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write(u"\4\b\t\b\3\2\6\2\22\n\2\r\2\16\2\23\3\2\3\2\3\3\3\3\3")
        buf.write(u"\3\3\3\3\3\3\3\3\3\5\3\37\n\3\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write(u"\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7")
        buf.write(u"\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\2\2\t\2\4\6")
        buf.write(u"\b\n\f\16\2\2<\2\21\3\2\2\2\4\36\3\2\2\2\6 \3\2\2\2\b")
        buf.write(u"&\3\2\2\2\n+\3\2\2\2\f\61\3\2\2\2\16\66\3\2\2\2\20\22")
        buf.write(u"\5\4\3\2\21\20\3\2\2\2\22\23\3\2\2\2\23\21\3\2\2\2\23")
        buf.write(u"\24\3\2\2\2\24\25\3\2\2\2\25\26\7\2\2\3\26\3\3\2\2\2")
        buf.write(u"\27\37\7\f\2\2\30\37\7\r\2\2\31\37\5\6\4\2\32\37\5\b")
        buf.write(u"\5\2\33\37\5\n\6\2\34\37\5\f\7\2\35\37\5\16\b\2\36\27")
        buf.write(u"\3\2\2\2\36\30\3\2\2\2\36\31\3\2\2\2\36\32\3\2\2\2\36")
        buf.write(u"\33\3\2\2\2\36\34\3\2\2\2\36\35\3\2\2\2\37\5\3\2\2\2")
        buf.write(u" !\7\3\2\2!\"\5\4\3\2\"#\7\4\2\2#$\5\4\3\2$%\7\5\2\2")
        buf.write(u"%\7\3\2\2\2&\'\7\3\2\2\'(\5\4\3\2()\7\5\2\2)*\7\6\2\2")
        buf.write(u"*\t\3\2\2\2+,\7\3\2\2,-\5\4\3\2-.\7\7\2\2./\5\4\3\2/")
        buf.write(u"\60\7\5\2\2\60\13\3\2\2\2\61\62\7\3\2\2\62\63\5\4\3\2")
        buf.write(u"\63\64\7\5\2\2\64\65\7\b\2\2\65\r\3\2\2\2\66\67\7\t\2")
        buf.write(u"\2\678\7\r\2\289\7\n\2\29:\5\4\3\2:;\7\13\2\2;\17\3\2")
        buf.write(u"\2\2\4\23\36")
        return buf.getvalue()


class formulaParser ( Parser ):

    grammarFileName = "formula.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'('", u"'.'", u"')'", u"'*'", u"'|'", 
                     u"'+'", u"'{'", u"':'", u"'}'", u"'/em'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"EMPTY", u"LETTER", u"WS" ]

    RULE_formula = 0
    RULE_regex = 1
    RULE_concat = 2
    RULE_star = 3
    RULE_union = 4
    RULE_plus = 5
    RULE_varconf = 6

    ruleNames =  [ u"formula", u"regex", u"concat", u"star", u"union", u"plus", 
                   u"varconf" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    EMPTY=10
    LETTER=11
    WS=12

    def __init__(self, input):
        super(formulaParser, self).__init__(input)
        self.checkVersion("4.5.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class FormulaContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.FormulaContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(formulaParser.EOF, 0)

        def regex(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(formulaParser.RegexContext)
            else:
                return self.getTypedRuleContext(formulaParser.RegexContext,i)


        def getRuleIndex(self):
            return formulaParser.RULE_formula

        def enterRule(self, listener):
            if hasattr(listener, "enterFormula"):
                listener.enterFormula(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFormula"):
                listener.exitFormula(self)




    def formula(self):

        localctx = formulaParser.FormulaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_formula)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 14
                self.regex()
                self.state = 17 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << formulaParser.T__0) | (1 << formulaParser.T__6) | (1 << formulaParser.EMPTY) | (1 << formulaParser.LETTER))) != 0)):
                    break

            self.state = 19
            self.match(formulaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RegexContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.RegexContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EMPTY(self):
            return self.getToken(formulaParser.EMPTY, 0)

        def LETTER(self):
            return self.getToken(formulaParser.LETTER, 0)

        def concat(self):
            return self.getTypedRuleContext(formulaParser.ConcatContext,0)


        def star(self):
            return self.getTypedRuleContext(formulaParser.StarContext,0)


        def union(self):
            return self.getTypedRuleContext(formulaParser.UnionContext,0)


        def plus(self):
            return self.getTypedRuleContext(formulaParser.PlusContext,0)


        def varconf(self):
            return self.getTypedRuleContext(formulaParser.VarconfContext,0)


        def getRuleIndex(self):
            return formulaParser.RULE_regex

        def enterRule(self, listener):
            if hasattr(listener, "enterRegex"):
                listener.enterRegex(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitRegex"):
                listener.exitRegex(self)




    def regex(self):

        localctx = formulaParser.RegexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_regex)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 21
                self.match(formulaParser.EMPTY)
                pass

            elif la_ == 2:
                self.state = 22
                self.match(formulaParser.LETTER)
                pass

            elif la_ == 3:
                self.state = 23
                self.concat()
                pass

            elif la_ == 4:
                self.state = 24
                self.star()
                pass

            elif la_ == 5:
                self.state = 25
                self.union()
                pass

            elif la_ == 6:
                self.state = 26
                self.plus()
                pass

            elif la_ == 7:
                self.state = 27
                self.varconf()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConcatContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.ConcatContext, self).__init__(parent, invokingState)
            self.parser = parser

        def regex(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(formulaParser.RegexContext)
            else:
                return self.getTypedRuleContext(formulaParser.RegexContext,i)


        def getRuleIndex(self):
            return formulaParser.RULE_concat

        def enterRule(self, listener):
            if hasattr(listener, "enterConcat"):
                listener.enterConcat(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitConcat"):
                listener.exitConcat(self)




    def concat(self):

        localctx = formulaParser.ConcatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_concat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(formulaParser.T__0)
            self.state = 31
            self.regex()
            self.state = 32
            self.match(formulaParser.T__1)
            self.state = 33
            self.regex()
            self.state = 34
            self.match(formulaParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StarContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.StarContext, self).__init__(parent, invokingState)
            self.parser = parser

        def regex(self):
            return self.getTypedRuleContext(formulaParser.RegexContext,0)


        def getRuleIndex(self):
            return formulaParser.RULE_star

        def enterRule(self, listener):
            if hasattr(listener, "enterStar"):
                listener.enterStar(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitStar"):
                listener.exitStar(self)




    def star(self):

        localctx = formulaParser.StarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_star)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(formulaParser.T__0)
            self.state = 37
            self.regex()
            self.state = 38
            self.match(formulaParser.T__2)
            self.state = 39
            self.match(formulaParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class UnionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.UnionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def regex(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(formulaParser.RegexContext)
            else:
                return self.getTypedRuleContext(formulaParser.RegexContext,i)


        def getRuleIndex(self):
            return formulaParser.RULE_union

        def enterRule(self, listener):
            if hasattr(listener, "enterUnion"):
                listener.enterUnion(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitUnion"):
                listener.exitUnion(self)




    def union(self):

        localctx = formulaParser.UnionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_union)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(formulaParser.T__0)
            self.state = 42
            self.regex()
            self.state = 43
            self.match(formulaParser.T__4)
            self.state = 44
            self.regex()
            self.state = 45
            self.match(formulaParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PlusContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.PlusContext, self).__init__(parent, invokingState)
            self.parser = parser

        def regex(self):
            return self.getTypedRuleContext(formulaParser.RegexContext,0)


        def getRuleIndex(self):
            return formulaParser.RULE_plus

        def enterRule(self, listener):
            if hasattr(listener, "enterPlus"):
                listener.enterPlus(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitPlus"):
                listener.exitPlus(self)




    def plus(self):

        localctx = formulaParser.PlusContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_plus)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(formulaParser.T__0)
            self.state = 48
            self.regex()
            self.state = 49
            self.match(formulaParser.T__2)
            self.state = 50
            self.match(formulaParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class VarconfContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(formulaParser.VarconfContext, self).__init__(parent, invokingState)
            self.parser = parser

        def LETTER(self):
            return self.getToken(formulaParser.LETTER, 0)

        def regex(self):
            return self.getTypedRuleContext(formulaParser.RegexContext,0)


        def getRuleIndex(self):
            return formulaParser.RULE_varconf

        def enterRule(self, listener):
            if hasattr(listener, "enterVarconf"):
                listener.enterVarconf(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVarconf"):
                listener.exitVarconf(self)




    def varconf(self):

        localctx = formulaParser.VarconfContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_varconf)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(formulaParser.T__6)
            self.state = 53
            self.match(formulaParser.LETTER)
            self.state = 54
            self.match(formulaParser.T__7)
            self.state = 55
            self.regex()
            self.state = 56
            self.match(formulaParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





