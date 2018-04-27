# !/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

"""
Autocompletion example that displays the autocompletions like readline does by
binding a custom handler to the Tab key.
"""


from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.contrib.completers import WordCompleter,PathCompleter
import os

animal_completer = PathCompleter("C:\\")


def main():
    text = prompt('Give some animals: ', completer=animal_completer)
    print('You said: %s' % text)


if __name__ == '__main__':
    answer = confirm('Should we do that? (Y/n) ')
    print('You said: %s' % answer)