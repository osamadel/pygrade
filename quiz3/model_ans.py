def gcdIter(a, b):
    '''
    a, b: positive integers
    
    returns: a positive integer, the greatest common divisor of a & b.
    '''
    # Your code here
    lowest = min(a,b)
    while lowest > 1:
        if a%lowest == 0 and b%lowest == 0: return lowest
        else: lowest -= 1
    return lowest