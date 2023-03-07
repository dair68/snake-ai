#module for holding the randElement function

import random

#obtains random element from a list
#@param elements - list of elements
#returns random element from elements
def randElement(elements):
    #checking if list is nonempty
    if len(elements) == 0:
        print("Error. Empty list inputted.")
        return None
    
    i = random.randrange(len(elements))
    return elements[i]