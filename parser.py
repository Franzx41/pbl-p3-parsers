import json
from lex_analyzer import Tokenizer 

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  
        self.pos = 0          

    def lookahead(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return dict(label=None, value=None)

    def match_label(self, token_label):
        current_token = self.lookahead()
        if current_token['label'] == token_label:
            self.pos += 1 # Move to the next token
            return current_token
        else:
            raise SyntaxError(f"Expected token label {token_label} but got {self.lookahead()}")

    def match_value(self, token_value):
        current_token = self.lookahead()
        if current_token['value'] == token_value:
            self.pos += 1 # Move to the next token
            return current_token
        else:
            raise SyntaxError(f"Expected token label {token_value} but got {self.lookahead()}")

    def create_node(self, name):
        return  {"prod": name, "children": []}

    def parse_function(self):
        if self.lookahead()['value'] == "function":
            node = self.create_node("function")
            node["children"].append(self.match_value("function"))
            node["children"].append(self.match_label("KEY_WORD"))
            node["children"].append(self.match_label("IDENTIFIER"))
            node["children"].append(self.parse_parameters())
            node["children"].append(self.match_value("{"))
            node["children"].append(self.parse_statements())
            node["children"].append(self.match_value("}"))
            return node
        else:
            raise SyntaxError(f"Expected 'function' token but got {self.lookahead()}") 

    def parse_parameters(self):
        if self.lookahead()['value'] == "(":
            node = self.create_node("parameters")
            node["children"].append(self.match_value("("))
            node["children"].append(self.parse_parameter())
            return node
        else:
            raise SyntaxError(f"Expected '(' token but got {self.lookahead()}")

    def parse_parameter(self):
        if self.lookahead()['label'] == "KEY_WORD":
            node = self.create_node("parameter")
            node["children"].append(self.match_label("KEY_WORD"))
            node["children"].append(self.match_label("IDENTIFIER"))
            node["children"].append(self.parse_parameter_list())
            return node
        elif self.lookahead()['value'] == ")":
            node = {"type": "parameter", "children": []}
            node["children"].append(self.match_value(")"))
            return node
        else:
            raise SyntaxError(f"Expected KEY_WORD or ')' token but got {self.lookahead()}")      

    def parse_parameter_list(self):
        if self.lookahead()['value'] == ",":
            node = self.create_node("parse_parameter_list")
            node["children"].append(self.match_value(","))
            node["children"].append(self.parse_parameter())
            return node
        elif self.lookahead()['value'] == ")":
            node = self.create_node("parse_parameter_list")
            node["children"].append(self.match_value(")"))
            return node
        else:
            raise SyntaxError(f"Expected ',' or ')' token but got {self.lookahead()}") 

    def parse_statements(self):
        node = self.create_node("parse_statements") 
        node["children"].append(self.parse_variables())
        #node["children"].append(self.parse_body()) # TODO
        return node 

    def parse_variables(self):
        if self.lookahead()['value'] == "variables":
            node = self.create_node("parse_variables") 
            node["children"].append(self.match_value("variables"))
            node["children"].append(self.match_value("{"))
            node["children"].append(self.parse_variables_tail())
            return node
        else:
            raise SyntaxError(f"Expected 'variables' token but got {self.lookahead()}") 

    def parse_variables_tail(self):
        if self.lookahead()['value'] == "}":
            node = self.create_node("parse_variables_tail")
            node["children"].append(self.match_value("}"))
            return node
        
        raise SyntaxError(f"Expected '}}' token but got {self.lookahead()}") 
        '''
        else:
            node = self.create_node("parse_variables_tail")
            node["children"].append(self.parse_expression_variables())
            node["children"].append(self.match_value("}"))
            return node
        '''

    def parse_body(self): # TODO
        pass                            

def main():
    file_path = 'func_code.txt'
    with open(file_path, "r") as file:
        content = file.read()
        analyzer = Tokenizer()
        tokens, stats = analyzer.analyze(content)
        #print(json.dumps(tokens, indent=1))

        parser = Parser(tokens)
        tree = parser.parse_function()
        print(json.dumps(tree, indent=1))

if __name__ == '__main__':
    main()  
