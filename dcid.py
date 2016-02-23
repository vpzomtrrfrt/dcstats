import random

# thanks to Grom PE for figuring this out
theAlphabet = "36QtfkmuFds0UjlvCGIXZ125bEMhz48JSYgipwKn7OVHRBPoy9DLWaceqxANTr"

def decTo62(n):
  b = theAlphabet
  result = ''
  bLen = len(b)
  while (n != 0):
    q = n % bLen
    result = b[int(q)] + result
    n = (n - q) / bLen
  return result

def _62ToDec(n):
  n = str(n)
  b = theAlphabet
  cache_pos = {}
  bLen = len(b)
  result = 0
  pw = 1
  i = len(n)-1
  while(i >= 0):
    c = n[i]
    if not c in cache_pos:
      cache_pos[c] = b.find(c)
    result += pw * cache_pos[c]
    pw *= bLen
    i-=1
  return result

def scrambleID(num):
  return decTo62(int(num) + 3521614606208)[::-1]

def unscrambleID(s):
  return _62ToDec(s[::-1]) - 3521614606208

def randomID(mn, mx):
  return scrambleID(random.randrange(unscrambleID(mn), unscrambleID(mx)))
