def regexRangeDigits(start,stop):
  if start == stop:
    return str(start)
  return '[%d-%d]' % (start,stop)

# generate list of regular expressions for the number range [start,end]
def genRangeRegex(start, end):
  if start <= 0:
    raise ValueError('only ranges of positive numbers supported')

  if start >= end:
    return []

  digitsStart = str(start)
  digitsEnd   = str(end)
  lastDigitStart = start%10

  if start//10 == (end-1)//10: # integer division
    lastDigitStop = (end-1)%10
    regexAll = digitsStart[:-1] + regexRangeDigits(lastDigitStart,lastDigitStop)
    return [regexAll]

  regexListStart = [] # at most one regular expression for going up to first multiple of 10
  if lastDigitStart != 0:
    regexStart = digitsStart[:-1] + regexRangeDigits(lastDigitStart,9)
    regexListStart.append(regexStart)

  regexListEnd = [] # at most one regular expression for going up from last multiple of 10
  lastDigitEnd = end%10
  if lastDigitEnd != 0:
    regexEnd = digitsEnd[:-1] + regexRangeDigits(0,lastDigitEnd-1)
    regexListEnd.append(regexEnd)

  regexListMidTrunc = genRangeRegex((start+9)//10, end//10)
  regexListMid = [r+'[0-9]' for r in regexListMidTrunc]

  return regexListStart + regexListMid + regexListEnd
  
f = open("as-numbers-ripe.txt","r")
lines = f.read().splitlines()
f.close()

for items in lines:
	if "-" in items:
		range1=int(items.split("-")[0])
		range2=int(items.split("-")[1])+1
		as_path_list = genRangeRegex(range1,range2)
		for items in as_path_list: 
			print ("ip as-path access-list RIPE_ALL_AS permit ^"+str(items)+"_*")
	else:
		print("ip as-path access-list RIPE_ALL_AS permit ^"+str(items)+"_*")
