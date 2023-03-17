#module with functions for common bitmask operations

#obtains the ith bit of a particular mask
#@param i - nonnegative integer representing bit index
#@param mask - nonnegative integer representing subset
#returns the ith digit in binary representation of mask. 
#   far right digit is 0th bit, 1 digit from right is 1st bit,
#   2 digits from right is 2nd bit, etc.
def bit(i, mask):
    assert i >= 0
    assert mask >= 0
    binNum = bin(mask)
    return int(binNum[-i-1])

#finds number nonzero bits within a bit string
#@param mask - nonnegative integer representing subset
#returns number of 1's in binary representation of mask
def count(mask):
    assert mask >= 0
    binNum = bin(mask)
    return binNum.count("1")

#finds position of first nonzero bit in mask
#@param mask - nonnegative integer representing subset
#returns index of first 1 found in binary representation of mask
#   far right digit is 0th bit, 1 digit from right is 1st bit,
#   2 digits from right is 2nd bit, etc. If no 1's present, returns -1.
def first(mask):
    assert mask >= 0
    binNum = bin(mask)
    reversedNum = binNum[::-1]
    #print(reversedNum)
    return reversedNum.find("1")

#sets certain bit within mask to a certain value
#@param i - nonnegative index specifying bit in mask
#@param mask - nonnegative integer representing subset. not changed by function
#@param value - 1 or 0
#returns new number with ith digit of mask's binary representation set to value
#   far right digit is 0th bit, 1 digit from right is 1st bit,
#   2 digits from right is 2nd bit, etc.
def setBit(i, mask, value):
    assert i >= 0
    assert mask >= 0
    value == 1 or value == 0
    binNum = bin(mask)
    index = len(binNum)-i-1
    newNum = binNum[0:index] + str(value) + binNum[index+1:]
    return int(newNum, 2)