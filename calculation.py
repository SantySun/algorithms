import unittest

class Calculation:
  @staticmethod
  def exec(expression):
    stack = [[0, '+']]
    for char in expression:
      if char == "(":
        stack.append([0, '+'])
      elif char == ")":
        # calculate the last 2 elements in the stack
        sub_result, _ = stack.pop()
        sub_result_2, sign = stack.pop()
        if sign == "+":
          stack.append([sub_result_2 + sub_result, '+'])
        elif sign == "-":
          stack.append([sub_result_2 - sub_result, '+'])
      elif char in "0123456789":
        if stack[-1][1] == '+':
          stack[-1][0] += int(char)
        elif stack[-1][1] == '-':
          stack[-1][0] -= int(char)
      elif char == "+":
        stack[-1][1] = '+'
      elif char == "-":
        stack[-1][1] = '-'
    
    while len(stack) > 1:
      last, _ = stack.pop()
      _, second_last_sign = stack[-1]
      if second_last_sign == "+":
        stack[-1][1] += last
      else:
        stack[-1][1] -= last
    return stack[0][0]
    



class CalculationTest(unittest.TestCase):
  def test_simple_calc(self):
    calc = Calculation()
    self.assertEqual(calc.exec('1+2+3+4'), 10)
    self.assertEqual(calc.exec('1+2-3+4'), 4)
    self.assertEqual(calc.exec('1+(2+4)-3'), 4)
    self.assertEqual(calc.exec('1-(2+3)+4'), 0)
    self.assertEqual(calc.exec('1-((2+3)-4)'), 0)
    self.assertEqual(calc.exec('-(1-((2+3)-4))+2'), 2)



if __name__ == "__main__":
  unittest.main()