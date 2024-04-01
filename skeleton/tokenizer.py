#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для синтаксичного розбору виразу по частинах.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
Вираз може містити:
    - змінні - ідентифікатори
    - константи - дійсні або цілі числа без знаку
    - знаки операцій: +, -, *, /
    - дужки: (, )

Функція `get_tokens` за заданим виразом має повертати послідовність 
лексем -- токенів.

Кожний токен (див. class Token) -- це пара: (<тип токену>, <значення токену>)
"""

# типи токенів
TOKEN_TYPE = (
    "variable",
    "constant",
    "operation",
    "equal",
    "left_paren",
    "right_paren",
    "other", 
)


# словник фіксованих токенів, що складаються з одного символа
TOKEN_TYPES = {
    "+": "operation",
    "-": "operation",
    "*": "operation",
    "/": "operation",
    "(": "left_paren",
    ")": "right_paren",
    "=": "equal",
}


class Token: 

    def __init__(self, type, value): 
        assert type in TOKEN_TYPE, 'недопустимий тип токена'
        self.type = type
        self.value = value 

    def __eq__(self, __value: object) -> bool:
        return self.type == __value.type and self.value == __value.value

    def __repr__(self): 
        return f"Token(type='{self.type}', value='{self.value}')"


def get_tokens(string):
    """Функція за рядком повертає список токенів типу Token.
    
    :param string: рядок
    :return: список токенів
    """
    tokens = []
    string = string.replace(" ", "")
    while string:
        token, string = _get_next_token(string)
        if token:
            tokens.append(token)
    return tokens


def _get_next_token(string):
    token, string_ = _get_token(string)
    if token:
        return token, string_
    else:
        return _get_other(string)


def _get_token(string):
    """Функція повертає наступний токен та залишок рядка.

    :param string: рядок
    :return: 
        next_token: наступний токен, якщо є, або None
        string: залишок рядка
    """
    for _get in [_get_par, 
                 _get_variable,
                 _get_equal,
                 _get_operator, 
                 _get_constant]:
        token, _string = _get(string)
        if token:
            return token, _string
    return None, string


def _get_par(string): 
    """Функція за рядком повертає дужку (якщо є) та залишок рядка. 

    :param string: рядок 
    :return: 
        next_token: дужка типу Token('left_paren', '(')
        string: залишок рядка
    """
    ch = string[0]
    if ch in ["(", ")"]:
        return Token(TOKEN_TYPES[ch], ch), string[1:]
    return None, string


def _get_operator(string):
    """Функція за рядком повертає оператор (якщо є) та залишок рядка.

    :param string: рядок
    :return: 
        next_token: оператор типу Token('operation', ...)
        string: залишок рядка
    """
    ch = string[0]
    if ch in ["+", "-", "*", "/"]:
        return Token(TOKEN_TYPES[ch], ch), string[1:]
    return None, string



def _get_equal(string): 
    """Функція за рядком повертає присвоєння '=' (якщо є) та залишок рядка.

    :param string: рядок
    :return: 
        next_token: оператор типу Token('equal', ...)
        string: залишок рядка
    """
    ch = string[0]
    if ch == "=":
        return Token(TOKEN_TYPES[ch], ch), string[1:]
    return None, string

    

def _get_constant(string):
    """Функція за рядком повертає константу (якщо є) та залишок рядка.

    :param string: рядок
    :return: 
        next_token: константа типу Token('constant', ...) або None
        string: залишок рядка
    """
    constant = ""
    dot = False
    end = 0
    for ch in string:
        if ch.isnumeric() or (constant != "" and not dot and ch == "."):
            if ch == ".":
                dot = True
            constant += ch
        else:
            break
        end += 1
    if constant != "":
        return Token("constant", constant), string[end:]
    else:
        return None, string
    


def _get_variable(string):
    """Функція за рядком повертає змінну (якщо є) та залишок рядка.

    :param string: рядок
    :return: 
        next_token: змінна типу Token('variable', ...)
        string: залишок рядка
    """
    var = "" 
    end = 0
    for ch in string:
        if ch.isalpha() or (ch == "_") or (var != "" and ch.isnumeric()):
            var += ch
        else:
            break
        end += 1
    if var != "":
        return Token("variable", var), string[end:]
    else:
        return None, str 



def _get_other(string):
    """Функція за рядком повертає символи, які не є відомим токеном.

    :param string: рядок
    :return: 
        next_token: змінна типу Token('other', ...)
        string: залишок рядка
    """
    token, string_ = _get_token(string)
    if token:
        return None, string
    else:
        return Token("other", string[0]), string[1:]
 


if __name__ == "__main__":
    needed = [
        Token(type='left_paren', value='('),
        Token(type='left_paren', value='('),
        Token(type='left_paren', value='('),
        Token(type='variable', value='ab1_'),
        Token(type='operation', value='-'),
        Token(type='constant', value='345.56'),
        Token(type='right_paren', value=')'),
        Token(type='left_paren', value='('),
        Token(type='operation', value='*'),
        Token(type='operation', value='/'),
        Token(type='other', value='.'),
        Token(type='constant', value='2'),
        Token(type='other', value='{'),
        Token(type='variable', value='_cde23')
    ]

    success = (x := get_tokens("(((ab1_ - 345.56)(*/.2{_cde23")) == needed 
    if not success: 
        if len(x) != len(needed): 
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x): 
            if exp != real: 
                print(f'Expected: {exp}, got {real}')

    needed = [
        Token(type='variable', value='x'),
        Token(type='equal', value='='),
        Token(type='left_paren', value='('),
        Token(type='variable', value='a'),
        Token(type='operation', value='+'),
        Token(type='variable', value='b'),
        Token(type='right_paren', value=')')
    ]

    success = success and (x := get_tokens("x = (a + b)")) == needed
    if not success: 
        if len(x) != len(needed): 
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x): 
            if exp != real: 
                print(f'Expected: {exp}, got {real}')        

    needed = [
        Token(type='variable', value='x'), 
        Token(type='equal', value='='), 
        Token(type='left_paren', value='('), 
        Token(type='variable', value='_a_s12'), 
        Token(type='operation', value='+'), 
        Token(type='constant', value='12.12321'), 
        Token(type='right_paren', value=')'), 
        Token(type='operation', value='*'), 
        Token(type='left_paren', value='('), 
        Token(type='constant', value='123'), 
        Token(type='variable', value='_asd'),
        Token(type='other', value='.'), 
        Token(type='operation', value='-'), 
        Token(type='constant', value='3.'), 
        Token(type='right_paren', value=')'),
    ]

    success = success and (x := get_tokens("x = (_a_s12 + 12.12321)*(123 _asd. - 3.)")) == needed
    if not success: 
        if len(x) != len(needed): 
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x): 
            if exp != real: 
                print(f'Expected: {exp}, got {real}')        

    print("Success =", success)