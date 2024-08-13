def get_int(output="Not a num: ", num="a", first_out=1, vaid_range=None, range_out="Not in range: "):
  '''
  This is a funtion to get integers with a output, and a optional number.
  This fition will contiueasly loop asking the user for an input in till it gets a number
  then it will return the input as an ingiger 
  you can also set a range being 2 numbers in a list that the input must be in 
    Note: the lowist number of the range is a valid number and the highest is not 
      Meaning a range of [1,5] 1 is a valid number but 5 is not

  output: str
    the output that will be printed when the user gets an invalid input
  num: str
    a number that will be cheeked so you can iput a string that will be cheeked
  first_out: str
    the first output that will be printed when the user gets an invalid input if not changed it will only use output
  vaid_range: list
    a list of 2 numbers that the input must be in the rules of wich are difined above if not changed or and invalid range like [1,3,5] or "1, 5" there will be no range
  range_out: str
    the output that will be printed when the user gets an valid input that is not in the range if not changed it will be 'Not in range: '
  '''
  if type(first_out) == str:
    num = input(first_out)
  
  if type(vaid_range) == list and len(vaid_range) == 2:
    while True:
      if num.isdigit():
        if int(num) in range(vaid_range[0], vaid_range[1]):
          return int(num)
        else:
          num = input(range_out)
      else:
        num = input(output)
      
  while num.isdigit() == False:
      num = input(output)
  return int(num)

#___________________________________________________

def _is_float(num):
  '''
  A fintion in the get_float to return True if the input can be converted to a float
  elce returning False so the loop can repeat it till it gets a float
  '''
  try:
    float(num)
    return True
  except ValueError:
    return False

#_____________________

def get_float(output="Not a flout: ", num='a', first_out=1 ,vaid_range=None, range_out="Not in range: "):
  '''
  This funtion will take a output to be displyed and an option al number 
  it will contiueasly loop asking the user for an input in till it gets a number
  this nuumber can also be a float (number with a decimal)
  it will then return the number as a float
  you can also set a range being 2 numbers in a list that the input must be in 
    Note: the lowist and highist number of the range is a valid number
      Meaning a range of [1,5] 1 and 5 arevalid numbers and nothing above or below are exepted

  output: str
    the output that will be printed when the user gets an invalid input
  num: str
    a number that will be cheeked so you can iput a string that will be cheeked
  first_out: str
    the first output that will be printed when the user gets an invalid input if not changed it will only use output
  vaid_range: list
    a list of 2 numbers that the input must be in the rules of wich are difined above if not changed or and invalid range like [1,3,5] or "1, 5" there will be no range
  range_out: str
    the output that will be printed when the user gets an valid input that is not in the range if not changed it will be 'Not in range: '
  '''

  if type(first_out) == str:
    num = input(first_out)

  if type(vaid_range) == list and len(vaid_range) == 2:

    while True:
      if _is_float(num):
        num = float(num)
        if num >= vaid_range[0] and num <= vaid_range[1]:
          return float(num)
        else:
          num = input(range_out)
      else:
        num = input(output)
      
  while _is_float(num) == False:
      num = input(output)
  return float(num)

#___________________________________________________

def get_val_str(output="Do you want to continue (y/n): ", acceptable=["y", "n"], invalid="Not Valid", inp="___ ", want_lower=True):
  """
  This funtion takes an out put and a list of acceptable inputs
  if the input is not in the list it will contiue to ask the user for a input
  if the input is in the list it will return the input
  
  praramiters 
        output: what will be displyed each time the user is asked for a input
        acceptable: a list of acceptable inputs
          defalt: = y, n
        inp: the inputed string so if you want the fisert time to be unice you can have your own input and have this to cheek it and display somthing else as other inputs if it was wrrong 
        want_lower: if true it will make the inputed string lower case so it is not case sensative
  """
  inp = input(output).strip().upper()
  while inp not in acceptable:
    print(invalid)
    inp = input(output).strip()
    if want_lower:
      inp = inp.upper()
  return inp[0]

def get_accept(output="Do you want to continue (y/n): ", inp="___ ", conform=["y"], deny=["n"], want_lower=True):
  """
  This funtion takes 2 list's of acceptable and not acceptable inputs and will return a Ture if it is in the list of acceptable inputs and a False if it is in the list of not acceptable inputs
  
  all inputs will be sriped of spaces at thier founts and ends and be lower case if want_lower is True
  
  this is so that the user dosen't have to worry about spaces as that can make inputing tedias and confusing 
  
  unlike want_lower there is no way to stop the input being striped of spaces at the ends and starts
  the conform and deny lists will also have there spaces striped of them so all elments of the list can be acssed by the user 
  
  praramiters:
  if in nithere it will contiue to ask the user for a input
  output: str
    what will be displyed each time the user is asked for a input
  conform: list
    list of acceptable inputs that if the user inputs one of these it will return True
  deny: list
    list of not acceptable inputs that if the user inputs one of these it will return False
  want_lower: bool
    if ture all inpts will be lower case so it is not case sensative
      Note: if True the conform and deny lists will be converted to lower case
  """
  if want_lower:
    conform = [i.strip().lower() for i in conform]
    deny = [i.strip().lower() for i in deny]
  else:
    conform = [i.strip() for i in conform]
    deny = [i.strip() for i in deny]

  inp = inp.strip()
  while inp not in conform and inp not in deny:
    inp = input(output).strip()
    if want_lower:
      inp = inp.lower()
  return (inp in conform)