#module for holding the randElement function
import random

#obtains random element from a list
#@param elements - collection object
#returns random element from elements
def randElement(elements):
    return random.sample(elements, 1)[0]