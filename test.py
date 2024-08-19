from operator import add, sub, mul, truediv
operations = {
                    '+': add,
                    '−': sub,
                    '×': mul,
                    '/': truediv
                }
temp = '23.2 + '
entry = '32.63'
a = float(temp[:-3])
b = float(entry)
c = operations[temp[-2:-1]](a, b)

print('a:', a)
print('b:', b)
print('c:', c)