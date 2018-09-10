#
# String T Length      String P Length           Sequential Time            Parallel Time    
#         18                   3               2.4068362902751606e-05     0.2083725811751123
#        1804                  3                0.00150317866492794       0.21360927346729203
#       43308                  3                0.03063574392574686       0.26678066318550614
#       182091                 5                0.10712901262458574       0.27296659712368476
#       640016                 3                 0.3737853226017607       0.38125709059441215
#       864216                 2                 0.4059577950316333       0.46231423144064854
#
#           For varrying T length, runtime will increase as the legnth of T increases.
#           For varrying P length, runtime will increase as the length of P increases, but not nearly as much as when T is increased.
#
#           For small values of P and T length, sequential is faster
#
#           When T length is large, parallel version is faster.


from multiprocessing import Process, Array
import ctypes
import multiprocessing as mp
from functools import partial
import timeit

def time_results() :
    """Write any code needed to compare the timing of the sequential and parallel versions
    with a variety of string lengths."""
    def parallelTimer(T, P):
        time = timeit.timeit(lambda:p_naive_string_matcher(T, P), number = 1)
        return time
    
    def sequentialTimer(T, P):
        time = timeit.timeit(lambda: naive_string_matcher(T, P), number = 1)
        return time

    def increaseLengthOfT(T, amount):
        newT = T
        for i in range(amount):
            newT += T + T + T + T
        return newT
    
    if __name__ == "__main__":

        pTimeA = parallelTimer(A, a)
        sTimeA = sequentialTimer(A, a)
        
        newB = increaseLengthOfT(B, 10)
        pTimeB = parallelTimer(newB, b)
        sTimeB = sequentialTimer(newB, b)
        
        newC = increaseLengthOfT(C, 100)
        pTimeC = parallelTimer(newC, c)
        sTimeC = sequentialTimer(newC, c)

        newD = increaseLengthOfT(D, 500)
        pTimeD = parallelTimer(newD, d)
        sTimeD = sequentialTimer(newD, d)

        newE = increaseLengthOfT(E, 10000)
        pTimeE = parallelTimer(newE, e)
        sTimeE = sequentialTimer(newE, e)

        newF = increaseLengthOfT(F, 1000)
        pTimeF = parallelTimer(newF, f)
        sTimeF = sequentialTimer(newF, f)
  
        print('{:^20} {:^20} {:^30} {:^20}'.format("String T Length", "String P Length", "Sequential Time", "Parallel Time"))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(A), len(a), sTimeA, pTimeA))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(newB), len(b), sTimeB, pTimeB))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(newC), len(c), sTimeC, pTimeC))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(newD), len(d), sTimeD, pTimeD))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(newE), len(e), sTimeE, pTimeE))
        print('{:^20} {:^20} {:^30} {:^10}'.format(len(newF), len(f), sTimeF, pTimeF))

def print_results(L) :
    """Prints the list of indices for the matches."""
    for i in range(len(L)):
        print("Pattern occurs at index: " + str(L[i]))

def naive_string_matcher(T, P) :
    """Naive string matcher algorithm from textbook page 988.

    Slight variation of the naive string matcher algorithm from
    textbook page 988.  Specifically, the textbook version prints the
    results.  This python function does not print the results.
    Instead, it generates and returns a list of the indices at the start
    of each match.  For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    n = len(T)
    m = len(P)
    
    for s in range(n - m + 1):
        for i in range(m):
            if T[s + i] != P[i]:
                break
        if i == (m - 1):
            indices.append(s)
    return indices

def p_naive_string_matcher(T, P) :
    """Parallel naive string matcher algorithm from Problem Set 4.

    This function implements the parallel naive string matcher algorithm that you specified in
    Problem Set 4.  You may assume in your implementation that there are 4 processor cores.
    If you want to write this more generally, you may add a parameter to the function for number
    of processes.  If you do, don't change the order of the existing parameters, and your new parameters
    must follow, and must have default values such that if the only parameters I pass are T and P, that
    you default to 4 processes.

    Like the sequential implementation from step 1 of assignment, this function should not
    print results.  Instead, have it return a list of the indices where the matches begin.
    For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    You must use Process objects from the multiprocessing module and not Threads from threading because
    in the next step of the assignment, you're going to investigate performance relative to the sequential
    implementation.

    You will need to decide how to distribute the work among the processes.
    One way (not the only way) is to give all of your processes T and P, and to give each process
    a range of starting indices to check, such that you give each approximately equal sized ranges.
    Another way is to give all processes the pattern string P, but only a substring of T (of approximately
    equal size).  In this case, you'd need to figure out how to map the indices back into the original.

    You will need to decide how to get the results back from the processes.
    One way (not the only way) is to give all processes a reference to a Queue object for the results.

    If you give all processes the full T and P, then if the size of the text T is large, the savings from
    multiprocessing may be outweighed by the cost of giving each its own independent copy of T.
    You might try using an Array object to use shared memory.  Here's how to do it.  Create an array of
    characters in shared memory with: a = Array(ctypes.c_wchar, "Hello World", lock=None)
    You'll need to import ctypes
    for this to work.  You can then access individual characters with a[0], a[1], etc.
    You might do this for both T and P.  None of the processes need to change them, so there is no risk
    of a race condition.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    n = len(T)
    m = len(P)
    char = [i for i in range(0, n - m + 1)]
    newPool = mp.Pool()
    function = partial(pHelp, T, P, m)
    match = [x for x in newPool.map(function, char) if x is not None]
    return match

def pHelp(T, P, m, i):
    if P == T[i:i + m]:
        return i

A = "abczzzzzzzzzzzzabc"
a = "abc"
    
B = "aaaaaaaaaaaaaaabyeaaaaaaabaaabyaaaaaaaabyeaa"
b = "bye"

C = "000000000000000000000000000000000000000010000000000000001101010000000000000000000000000000000000000000000010"
c = "101"

D = "asdfdfjasdfiemnasdfhelloasdfjdahgehelasdfjdewyuiwerjoeruaniodgnioawieroaladhadhiadjfdahello"
d = "hello"

E = "3212312131223123"
e = "123"

F = "----------------------------------------------RG-------------------------------RG----RG-----------------------RR---------------------------------RG------------------------------------------------------------------RG-"
f = "RG"

indices=[]
time_results()
