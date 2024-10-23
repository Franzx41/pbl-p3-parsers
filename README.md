# pbl-p3-parsers

Fragmento de código de entrada:
```
function string example(integer x, integer y) {
  variables { 
  }
}
```

Saída do analisador léxico:
```
[{'label': 'IDENTIFIER', 'value': 'function'}, {'label': 'KEY_WORD', 'value': 'string'}, {'label': 'IDENTIFIER', 'value': 'example'}, {'label': 'DELIMITER', 'value': '('}, {'label': 'KEY_WORD', 'value': 'integer'}, {'label': 'IDENTIFIER', 'value': 'x'}, {'label': 'DELIMITER', 'value': ','}, {'label': 'KEY_WORD', 'value': 'integer'}, {'label': 'IDENTIFIER', 'value': 'y'}, {'label': 'DELIMITER', 'value': ')'}, {'label': 'DELIMITER', 'value': '{'}, {'label': 'KEY_WORD', 'value': 'variables'}, {'label': 'DELIMITER', 'value': '{'}, {'label': 'DELIMITER', 'value': '}'}, {'label': 'DELIMITER', 'value': '}'}]
```

Saída do parser preditivo:
```
{
 "prod": "function",
 "children": [
  {
   "label": "IDENTIFIER",
   "value": "function"
  },
  {
   "label": "KEY_WORD",
   "value": "string"
  },
  {
   "label": "IDENTIFIER",
   "value": "example"
  },
  {
   "prod": "parameters",
   "children": [
    {
     "label": "DELIMITER",
     "value": "("
    },
    {
     "prod": "parameter",
     "children": [
      {
       "label": "KEY_WORD",
       "value": "integer"
      },
      {
       "label": "IDENTIFIER",
       "value": "x"
      },
      {
       "prod": "parse_parameter_list",
       "children": [
        {
         "label": "DELIMITER",
         "value": ","
        },
        {
         "prod": "parameter",
         "children": [
          {
           "label": "KEY_WORD",
           "value": "integer"
          },
          {
           "label": "IDENTIFIER",
           "value": "y"
          },
          {
           "prod": "parse_parameter_list",
           "children": [
            {
             "label": "DELIMITER",
             "value": ")"
            }
           ]
          }
         ]
        }
       ]
      }
     ]
    }
   ]
  },
  {
   "label": "DELIMITER",
   "value": "{"
  },
  {
   "prod": "parse_statements",
   "children": [
    {
     "prod": "parse_variables",
     "children": [
      {
       "label": "KEY_WORD",
       "value": "variables"
      },
      {
       "label": "DELIMITER",
       "value": "{"
      },
      {
       "prod": "parse_variables_tail",
       "children": [
        {
         "label": "DELIMITER",
         "value": "}"
        }
       ]
      }
     ]
    }
   ]
  },
  {
   "label": "DELIMITER",
   "value": "}"
  }
 ]
}
```
