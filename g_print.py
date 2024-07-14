import sys, time


def g_print_str(words="", step=0.01, sepr="", front=""):
  """
  print's words with a delay between each character 
  parameters: 
      words: string to print
      step: time between each character
          default: 0.1
      sepr: string to print between words
          default: ""
      front: string to print before words
          default: ""
          also inles you give it a \n it will be on the same line as letters
  """
  sys.stdout.write(front)
  sys.stdout.flush()

  for l in words:
    sys.stdout.write(l + sepr)
    sys.stdout.flush()
    time.sleep(step)
  print()


def g_print_lis(lis=[],
                step=0.0,
                sepr=", ",
                front="",
                item_indentashon=0,
                self_indentashon=0,
                sorting=False,
                one_line=True,
                upper=True):
  """
  print's items of a list with a delay between each item 
  paramiters: 
      lis: list to print
      step: time between each character
          defalt: 0.1
      sepr: string to print between words
          defalt: ", "
      front: string to print before words
          defalt: ""
          also inles you give it a \n it will be on the same line as the list items
  """

  indent = " " * item_indentashon
  all_indent = " " * self_indentashon
  sys.stdout.write(front)
  sys.stdout.flush()

  for value in range(len(lis)):
    type_val = type(lis[value])
    if type_val == dict:
      g_print_dict(lis[value], "", step, item_indentashon,
                   self_indentashon + item_indentashon, sorting, False)

    elif type_val == list or type_val == tuple or type_val == set:
      g_print_lis(lis[value], step, sepr, "\n", item_indentashon,
                  self_indentashon, sorting, one_line, False)

    else:
      if not one_line:
        sys.stdout.write("\n")
        sys.stdout.flush()

      sys.stdout.write(f"{all_indent}{indent}{lis[value]}")
      sys.stdout.flush()
      if value == len(lis) - 1 and upper:
        print()
      else:
        sys.stdout.write(sepr)
        sys.stdout.flush()
      time.sleep(step)


def g_print_dict(dicton={},
                 front=None,
                 step=0.0,
                 item_indentashon=4,
                 self_indentashon=0,
                 sorting=False,
                 up=True):
  """
  print's items of a dictionary with a no delay between each item
  paramiters: 
      dicton: dictionary to print
      front: string to print before words
          defalt: ""
      step: time between each character
          defalt: 0
      item_indentashon: indentashon of each charictor
          defalt: 4
      sorting: if true, sorts the dictionary
          defalt: False
  """
  if type(front) == str:
    print(front)

  if sorting:
    dicton = dict(sorted(dicton.items()))

  indent = " " * item_indentashon
  all_indent = " " * self_indentashon
  for k, v in dicton.items():

    if type(v) == dict:
      sys.stdout.write(f"\n{all_indent}{k}: ")
      sys.stdout.flush()
      for value in v.items():
        if type(value[1]) == dict:
          g_print_dict({value[0]: value[1]}, "", step, item_indentashon,
                       self_indentashon + item_indentashon, sorting, False)

        else:
          sys.stdout.write(f"\n{all_indent}{indent}{value[0]}:  {value[1]}")
          sys.stdout.flush()
          time.sleep(step)

    elif type(v) == list or type(v) == tuple or type(v) == set:
      sys.stdout.write(f"\n{all_indent}{k}: ")
      g_print_lis(v, step, "", "", item_indentashon,
                  self_indentashon + item_indentashon, sorting, False, False)

    else:
      sys.stdout.write(f"\n{all_indent}{k}:  {v}")
      sys.stdout.flush()
      time.sleep(step)
  if up:
    print()
