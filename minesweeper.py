import random

def minesweeper():
  rows, cols = (8, 8)
  arr = [[0 for i in range(cols)] for j in range(rows)]

  xcount = 0
  while xcount < 8: #fill the grid with 8 bombs
    bombrow = random.randint(0, rows-1)
    bombcol = random.randint(0, cols-1)
    if arr[bombrow][bombcol] != 'X':
      arr[bombrow][bombcol] = 'X'

      #update adjacent squares to show the right number
      try:
        if bombrow > 0 and bombcol > 0:
          arr[bombrow-1][bombcol-1] += 1
      except:
        pass
      try:
        if bombcol > 0:
          arr[bombrow][bombcol-1] += 1
      except:
        pass
      try:
        if bombrow < rows-1 and bombcol > 0:
          arr[bombrow+1][bombcol-1] += 1
      except:
        pass
      try:
        if bombrow > 0:
          arr[bombrow-1][bombcol] += 1
      except:
        pass
      try:
        if bombrow < rows-1:
          arr[bombrow+1][bombcol] += 1
      except:
        pass
      try:
        if bombrow > 0 and bombcol < cols-1:
          arr[bombrow-1][bombcol+1] += 1
      except:
        pass
      try:
        if bombcol < cols-1:
          arr[bombrow][bombcol+1] += 1
      except:
        pass
      try:
        if bombrow < rows-1 and bombcol < cols-1:
          arr[bombrow+1][bombcol+1] += 1
      except:
        print("Exception!")
        pass
      xcount += 1

  #convert grid to string
  msg = ""
  for row in range(rows):
    for col in range(cols):
      if arr[row][col] == 0:
        msg += "||⬜|| "
      elif arr[row][col] == 'X':
        msg += "||💣|| "
      elif arr[row][col] == 1:
        msg += "||1️⃣|| "
      elif arr[row][col] == 2:
        msg += "||2️⃣|| "
      elif arr[row][col] == 3:
        msg += "||3️⃣|| "
      elif arr[row][col] == 4:
        msg += "||4️⃣|| "
      elif arr[row][col] == 5:
        msg += "||5️⃣|| "
      elif arr[row][col] == 6:
        msg += "||6️⃣|| "
      elif arr[row][col] == 7:
        msg += "||7️⃣|| "
      elif arr[row][col] == 8:
        msg += "||8️⃣|| "
      else:
        msg += str(arr[row][col])
    msg += "\n"
  return msg