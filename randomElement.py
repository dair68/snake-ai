#module for holding the randElement function
import random

#obtains random element from a list
#@param elements - nonempty collection object
#returns random element from elements
def randElement(elements):
    assert len(elements) > 0
    return random.sample(elements, 1)[0]