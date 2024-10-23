#!/usr/bin/env python
# coding: utf-8

'''
 Analisor léxico baseado em busca por regex
 Autor: Francisco Ferreira

 Finalmente executando o analisador léxico:
	python analyzer.py 
'''

import re
import tkinter as tk
from tkinter import filedialog

class Tokenizer:
    def __init__(self):
        # Lista de regexes
        self.regex_list = [
            ('LINE_COMMENT', r'//(.)*\n'),
            ('BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),
            ('STRING', r'\"([^\"\'])*\"'), # Exclui os caracteres (ASCII 34 aspas simples, ASCII 39 aspas simples) 
            ('CHARACTER', r'\'([^\"\'])\''), # Exclui os caracteres (ASCII 34 aspas simples, ASCII 39 aspas simples) 
            ('KEY_WORD', r'(variables|methods|constants|class|return|empty|main|if|then|else|while|for|read|write|integer|float|boolean|string|true|false|extends)'),
            ('IDENTIFIER', r'[a-zA-Z]+[a-zA-Z0-9_]*'),
            ('NUMBER', r'-?\d+(\.\d+)?'),
            ('OPERATOR', r'(\+\+)|(--)|(\+)|(-)|(\*)|(\/)|(==)|(>=)|(<=)|(>)|(<)|(=)|(!)|(&&)|(\|\|)|(!)'),
            ('DELIMITER', r';|,|\(|\)|\{|\}|\[|\]'),
            ('SYMBOL', r'[\x20-\x21\x23-\x26\x28-\x7E]'), # Usando range para excluir aspas simples e aspas duplas
            ('ERRO_LEXICO', r'.') # Regex para determinar erros léxicos (ou seja, match qualquer outra coisa fora do nosso dicionário)
        ]
        # Agrupa a a lista de regex em um único named capturing groups
        self.final_regex = '|'.join('(?P<%s>%s)' % p for p in self.regex_list)

    '''
        Dado um text, faz análise léxica e retorna:
        - results: lista de tokens e suas respectivas posições no arquivo de texto
        - stats: um dicionário com contadores de ocorrência para cada token
    '''
    def analyze(self, source_code_str):
        results = []
        stats = {}
        for item in self.regex_list: 
            stats[item[0]] = 0

        # Ref: https://docs.python.org/3/library/re.html#re.finditer
        # Faz match das regexes e retorna uma list de grupos encontrados
        for m in re.finditer(self.final_regex, source_code_str):
            lex_label = m.lastgroup
            lex_value = m.group(lex_label)
            counter = stats[lex_label]
            stats[lex_label] = counter + 1
            
            start = m.start()
            end = m.end()

            # Linha de início do lexema e seu offset
            start_line = source_code_str.count('\n', 0, start) + 1
            start_offset = start - source_code_str.rfind('\n', 0, start) - 1

            # Linha de término do lexema e seu offset
            end_line = source_code_str.count('\n', 0, end) + 1
            end_offset = end - source_code_str.rfind('\n', 0, end) - 1
            
            if (not lex_value.__eq__(" ")):
                results.append(dict(
                    #start_line=start_line, start_offset=start_offset, 
                    #end_line=end_line, end_offset=end_offset, 
                    label=lex_label, value=lex_value
                ))

        return results, stats

def main():
    file_path = 'func_code.txt'
    with open(file_path, "r") as file:
        content = file.read()
        analyzer = Tokenizer()
        results, stats = analyzer.analyze(content)
        print(results)

if __name__ == '__main__':
    main()    
