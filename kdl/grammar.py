#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu, leftrec, nomemo
from tatsu.parsing import leftrec, nomemo  # noqa
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class KdlBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(KdlBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class KdlParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=KdlBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(KdlParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa

        def block0():
            self._ws_()
        self._closure(block0)
        self._nodes_()
        self.name_last_node('@')

        def block2():
            self._ws_()
        self._closure(block2)
        self._check_eof()

    @tatsumasu()
    def _nodes_(self):  # noqa

        def block0():
            self._linespace_()
        self._closure(block0)

        def block1():
            self._node_()
            self.add_last_node_to_name('@')

            def block3():
                self._linespace_()
            self._closure(block3)
        self._closure(block1)

    @tatsumasu()
    def _node_(self):  # noqa
        with self._optional():
            self._token('/-')
            self.name_last_node('commented')

            def block1():
                self._ws_()
            self._closure(block1)
        self._identifier_()
        self.name_last_node('name')

        def block3():
            self._node_space_()
            self._node_props_and_args_()
            self.add_last_node_to_name('props_and_args')
        self._closure(block3)
        with self._optional():

            def block5():
                self._node_space_()
            self._closure(block5)
            self._node_children_()
            self.name_last_node('children')

            def block7():
                self._ws_()
            self._closure(block7)
        self._node_terminator_()
        self.ast._define(
            ['children', 'commented', 'name'],
            ['props_and_args']
        )

    @tatsumasu()
    def _node_props_and_args_(self):  # noqa
        with self._optional():
            self._token('/-')
            self.name_last_node('commented')

            def block1():
                self._ws_()
            self._closure(block1)
        with self._group():
            with self._choice():
                with self._option():
                    self._prop_()
                    self.name_last_node('prop')
                with self._option():
                    self._value_()
                    self.name_last_node('value')
                self._error('no available options')
        self.ast._define(
            ['commented', 'prop', 'value'],
            []
        )

    @tatsumasu()
    def _node_children_(self):  # noqa
        with self._optional():
            self._token('/-')
            self.name_last_node('commented')

            def block1():
                self._ws_()
            self._closure(block1)
        self._token('{')
        self._nodes_()
        self.name_last_node('children')
        self._token('}')
        self.ast._define(
            ['children', 'commented'],
            []
        )

    @tatsumasu()
    def _node_space_(self):  # noqa
        with self._choice():
            with self._option():
                with self._group():

                    def block0():
                        self._ws_()
                    self._closure(block0)
                    self._escline_()

                    def block1():
                        self._ws_()
                    self._closure(block1)
            with self._option():

                def block2():
                    self._ws_()
                self._positive_closure(block2)
            self._error('no available options')

    @tatsumasu()
    def _node_terminator_(self):  # noqa
        with self._choice():
            with self._option():
                self._single_line_comment_()
            with self._option():
                self._newline_()
            with self._option():
                self._token(';')
            with self._option():
                self._check_eof()
            self._error('no available options')

    @tatsumasu()
    def _identifier_(self):  # noqa
        with self._choice():
            with self._option():
                self._string_()
                self.name_last_node('string')
            with self._option():
                self._bare_identifier_()
                self.name_last_node('bare')
            self._error('no available options')
        self.ast._define(
            ['bare', 'string'],
            []
        )

    @tatsumasu()
    def _bare_identifier_(self):  # noqa
        with self._ifnot():
            self._digit_()
        self._first_identifier_char_()
        self.add_last_node_to_name('@')

        def block1():
            self._rest_identifier_char_()
            self.add_last_node_to_name('@')
        self._positive_closure(block1)

    @tatsumasu()
    def _digit_(self):  # noqa
        self._pattern('[0-9]')

    @tatsumasu()
    def _first_identifier_char_(self):  # noqa
        with self._ifnot():
            self._linespace_()
        with self._ifnot():
            self._pattern('[\\\\<{;\\[=,"]')
        self._pattern('.')

    @tatsumasu()
    def _rest_identifier_char_(self):  # noqa
        with self._ifnot():
            self._linespace_()
        with self._ifnot():
            self._pattern('[\\\\;=,"]')
        self._pattern('.')

    @tatsumasu()
    def _prop_(self):  # noqa
        self._identifier_()
        self.name_last_node('name')
        self._token('=')
        self._value_()
        self.name_last_node('value')
        self.ast._define(
            ['name', 'value'],
            []
        )

    @tatsumasu()
    def _value_(self):  # noqa
        with self._choice():
            with self._option():
                self._symbol_()
            with self._option():
                self._number_()
            with self._option():
                self._string_()
            with self._option():
                self._boolean_()
            with self._option():
                self._null_()
            self._error('no available options')

    @tatsumasu()
    def _string_(self):  # noqa
        with self._choice():
            with self._option():
                self._raw_string_()
            with self._option():
                self._escaped_string_()
            self._error('no available options')

    @tatsumasu()
    def _escaped_string_(self):  # noqa
        self._token('"')

        def block1():
            self._character_()
        self._closure(block1)
        self.name_last_node('escstring')
        self._token('"')
        self.ast._define(
            ['escstring'],
            []
        )

    @tatsumasu()
    def _character_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('\\')
                self._escape_()
                self.name_last_node('escape')
            with self._option():
                self._pattern('[^"]')
                self.name_last_node('char')
            self._error('no available options')
        self.ast._define(
            ['char', 'escape'],
            []
        )

    @tatsumasu()
    def _escape_(self):  # noqa
        with self._choice():
            with self._option():
                self._pattern('[\\\\\\/bfnrt]')
                self.name_last_node('named')
            with self._option():
                self._token('u{')
                self._pattern('[0-9a-fA-F]{1,6}')
                self.name_last_node('unichar')
                self._token('}')
            self._error('no available options')
        self.ast._define(
            ['named', 'unichar'],
            []
        )

    @tatsumasu()
    def _raw_string_(self):  # noqa
        self._token('r')
        self._raw_string_hash_()
        self.name_last_node('rawstring')
        self.ast._define(
            ['rawstring'],
            []
        )

    @tatsumasu()
    def _raw_string_hash_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('#')
                self._raw_string_hash_()
                self.name_last_node('@')
                self._token('#')
            with self._option():
                self._raw_string_quotes_()
                self.name_last_node('@')
            self._error('no available options')

    @tatsumasu()
    def _raw_string_quotes_(self):  # noqa
        self._token('"')
        self._pattern('[^"]*')
        self.name_last_node('@')
        self._token('"')

    @tatsumasu()
    def _symbol_(self):  # noqa
        self._token(':')
        self._identifier_()
        self.name_last_node('symbol')
        self.ast._define(
            ['symbol'],
            []
        )

    @tatsumasu()
    def _number_(self):  # noqa
        with self._choice():
            with self._option():
                self._hex_()
            with self._option():
                self._octal_()
            with self._option():
                self._binary_()
            with self._option():
                self._decimal_()
            self._error('no available options')

    @tatsumasu()
    def _decimal_(self):  # noqa
        self._pattern('[+\\-]?[0-9][0-9_]*(\\.[0-9][0-9_]*)?([eE][+-]?[0-9][0-9_]*)?')
        self.name_last_node('decimal')
        self.ast._define(
            ['decimal'],
            []
        )

    @tatsumasu()
    def _hex_(self):  # noqa
        self._pattern('[+\\-]?0x[0-9a-fA-F][0-9a-fA-F_]*')
        self.name_last_node('hex')
        self.ast._define(
            ['hex'],
            []
        )

    @tatsumasu()
    def _octal_(self):  # noqa
        self._pattern('[+\\-]?0o[0-7][0-7_]*')
        self.name_last_node('octal')
        self.ast._define(
            ['octal'],
            []
        )

    @tatsumasu()
    def _binary_(self):  # noqa
        self._pattern('[+\\-]?0b[01][01_]*')
        self.name_last_node('binary')
        self.ast._define(
            ['binary'],
            []
        )

    @tatsumasu()
    def _boolean_(self):  # noqa
        with self._group():
            with self._choice():
                with self._option():
                    self._token('true')
                with self._option():
                    self._token('false')
                self._error('no available options')
        self.name_last_node('boolean')
        self.ast._define(
            ['boolean'],
            []
        )

    @tatsumasu()
    def _null_(self):  # noqa
        with self._group():
            self._token('null')
        self.name_last_node('null')
        self.ast._define(
            ['null'],
            []
        )

    @tatsumasu()
    def _escline_(self):  # noqa
        self._token('\\')

        def block0():
            self._ws_()
        self._closure(block0)
        with self._group():
            with self._choice():
                with self._option():
                    self._single_line_comment_()
                with self._option():
                    self._newline_()
                self._error('no available options')

    @tatsumasu()
    def _linespace_(self):  # noqa
        with self._choice():
            with self._option():
                self._check_eof()
            with self._option():
                self._newline_()
            with self._option():
                self._ws_()
            with self._option():
                self._single_line_comment_()
            self._error('no available options')

    @tatsumasu()
    def _single_line_comment_(self):  # noqa
        self._token('//')

        def block0():
            self._newline_()
        self._skip_to(block0)

    @tatsumasu()
    def _multi_line_comment_(self):  # noqa
        self._token('/*')
        with self._group():
            with self._choice():
                with self._option():
                    self._commented_block_()
                with self._option():
                    self._multi_line_comment_()
                self._error('no available options')
        self._token('*/')

    @tatsumasu()
    def _commented_block_(self):  # noqa

        def block0():
            with self._choice():
                with self._option():
                    self._token('*')
                    self._pattern('[^\\/]')
                with self._option():
                    self._pattern('[^*]')
                self._error('no available options')
        self._closure(block0)

    @tatsumasu()
    def _newline_(self):  # noqa
        self._pattern('(\\r\\n|[\\r\\n\\u0085\\u000C\\u2028\\u2029])')

    @tatsumasu()
    def _ws_(self):  # noqa
        self._pattern('([\\t \\u00A0\\u1680\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u202F\\u205F\\u3000]|\\uFFEF)+')


class KdlSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def nodes(self, ast):  # noqa
        return ast

    def node(self, ast):  # noqa
        return ast

    def node_props_and_args(self, ast):  # noqa
        return ast

    def node_children(self, ast):  # noqa
        return ast

    def node_space(self, ast):  # noqa
        return ast

    def node_terminator(self, ast):  # noqa
        return ast

    def identifier(self, ast):  # noqa
        return ast

    def bare_identifier(self, ast):  # noqa
        return ast

    def digit(self, ast):  # noqa
        return ast

    def first_identifier_char(self, ast):  # noqa
        return ast

    def rest_identifier_char(self, ast):  # noqa
        return ast

    def prop(self, ast):  # noqa
        return ast

    def value(self, ast):  # noqa
        return ast

    def string(self, ast):  # noqa
        return ast

    def escaped_string(self, ast):  # noqa
        return ast

    def character(self, ast):  # noqa
        return ast

    def escape(self, ast):  # noqa
        return ast

    def raw_string(self, ast):  # noqa
        return ast

    def raw_string_hash(self, ast):  # noqa
        return ast

    def raw_string_quotes(self, ast):  # noqa
        return ast

    def symbol(self, ast):  # noqa
        return ast

    def number(self, ast):  # noqa
        return ast

    def decimal(self, ast):  # noqa
        return ast

    def hex(self, ast):  # noqa
        return ast

    def octal(self, ast):  # noqa
        return ast

    def binary(self, ast):  # noqa
        return ast

    def boolean(self, ast):  # noqa
        return ast

    def null(self, ast):  # noqa
        return ast

    def escline(self, ast):  # noqa
        return ast

    def linespace(self, ast):  # noqa
        return ast

    def single_line_comment(self, ast):  # noqa
        return ast

    def multi_line_comment(self, ast):  # noqa
        return ast

    def commented_block(self, ast):  # noqa
        return ast

    def newline(self, ast):  # noqa
        return ast

    def ws(self, ast):  # noqa
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'start'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = KdlParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, KdlParser, name='Kdl')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()