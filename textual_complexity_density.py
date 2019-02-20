import math

def measure_textual_complexity(in_string,case_sens):
    '''Attempts to measure textual complexity/density of a string'''
    '''Based on ratio a!/l where a is length of alphabet (unique chars) and l is total string length'''
    '''@LawrenceA_UK'''
    if case_sens == True:
        in_string = in_string.lower()
    in_string = in_string.replace(" ", "")
    alphabet=set(list(in_string))  
    result = float(math.factorial(len(alphabet))) / float(len(in_string))
    result = round (result,2)
    return result
    
    
print measure_textual_complexity(in_string = "testing",case_sens=True)