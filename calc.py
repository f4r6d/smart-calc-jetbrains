from collections import deque
digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
operands = {'-': 1, '+': 1, '*': 2, '/': 2, '(': 0, ')': 0}
variables = {}

def variable_checker(var):
    if var.isalpha():
        return var
    else:
        return 'Invalid identifier'

def value_checker(val):
    if variable_checker(val) != 'Invalid identifier': 
        return return_value(val)
    else:
        try:
            value = int(val)
        except ValueError:
            return 'Invalid assignment'
        else:
            return value

def return_value(var):
    if variable_checker(var) != 'Invalid identifier':
        if variable_checker(var) in variables:
            value = variables[variable_checker(var)]
            return value
        else:
            return 'Unknown variable'
    return 'Invalid identifier'
        
def assign(str_list):
    if len(str_list) > 3:
        print('Invalid assignment')
    elif variable_checker(str_list[0]) == 'Invalid identifier':
        print('Invalid identifier')
    elif value_checker(str_list[2]) == 'Unknown variable':
        print('Unknown variable')
    elif value_checker(str_list[2]) == 'Invalid assignment':
        print('Invalid assignment')
    else:
        var = variable_checker(str_list[0])
        value = value_checker(str_list[2])
        variables[var] = value

def func_detector(str_list):
    if '=' in str_list:
        return assign(str_list)
    elif len(str_list) == 1 and not str_list[0].startswith('/'):
        print(return_value(str_list[0]))
    else:
        return calc(postfix(infix(''.join(str_list))))

def command_check(command):
    if command.startswith('/'):
        if command[1:] not in ('exit', 'help'):
            return True
            
def Braces_checker(string):
    opening = 0
    closing = 0
    for i in inp:
        if i == '(':
            opening += 1
        if i == ')':
            closing += 1
        if closing > opening:
            break
    if opening == closing:
        return True
    else:
        return False

def infix(string):
    if '**' in string or '//' in string:
        return False
    else:
        while '--' in string:
            string = string.replace('--', '+')
        while '++' in string:
            string = string.replace('++', '+')
        string = string.replace('+-', ' - ')
        string = string.replace('-', ' - ')
        string = string.replace('+', ' + ')
        string = string.replace('*', ' * ')
        string = string.replace('/', ' / ')
        string = string.replace('(', ' ( ')
        string = string.replace(')', ' ) ')
        string = string.replace('=', ' = ')
        return string
          
def postfix(infixx):
    infix = infixx.split()
    postfix = deque()
    stack = deque()
    for i in infix:
        if i not in operands:
            postfix.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            while stack[len(stack) - 1] != '(':
                postfix.append(stack.pop())
            stack.pop()    
        else:   
            if not stack:
                stack.append(i)
            elif operands[i] > operands[stack[len(stack) - 1]]:
                stack.append(i)
            else:
                while operands[i] <= operands[stack[len(stack) - 1]]:
                    postfix.append(stack.pop())
                    if len(stack) == 0:
                        break
                stack.append(i)
    while stack:
        postfix.append(stack.pop())
    return postfix
    
def calc(postfixx):
    postfix = deque()
    for i in postfixx:
        if i in variables:
            postfix.append(variables[i])
        elif i in operands:
            postfix.append(i)
        else:
            postfix.append(int(i))           
    stack = deque()
    for i in postfix:
        if i not in operands:
            stack.append(i)
        else:
            right_operand = stack.pop()
            left_operand = stack.pop()
            if i == '+':
                result = left_operand + right_operand
            elif i == '-':
                result = left_operand - right_operand
            elif i == '*':
                result = left_operand * right_operand
            elif i == '/':
                try:
                    result = left_operand / right_operand
                except ZeroDivisionError:
                    print('ZeroDivisionError')
                else:
                    result = result
            stack.append(result)
    answer = stack.pop()
    print(answer)
                 
while True:
    inp = input()
    if inp == '':
        continue
    if command_check(inp):
        print('Unknown command')
        continue    
    if inp == "/exit":
        print('Bye!')
        break
    if inp == '/help':
        print('The program calculates the sum of numbers')
        continue
    if not Braces_checker(inp):
        print('Invalid expression')
        continue
    if not infix(inp):
        print('Invalid expression')
        continue
    else:    
        num_list = infix(inp).split()    
        action = func_detector(num_list)