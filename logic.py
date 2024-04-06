# Import necessary packages
from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call

prolog = Prolog() # Global handle to interpreter

retractall = Functor("retractall")
known = Functor("known",3)

# Define foreign functions for getting user input and writing to the screen
def write_py(X):
    print(str(X))
    sys.stdout.flush()
    return True

def read_py(A, V, Y):
    # print(dir(A))
    if isinstance(Y, Variable):
        response = input(str(A) + " is " + str(V) + "? ")
        Y.unify(response)
        return True
    else:
        return False

def read_categorical(A, V):
    if isinstance(V, Variable):
        response = input(f"What is {A}?")
        V.unify(response)
        return True
    else:
        return False

write_py.arity = 1
read_py.arity = 3
read_categorical.arity = 2

registerForeign(read_py)
registerForeign(write_py)
registerForeign(read_categorical)

prolog.consult("expert.pl") # open the KB for consulting

call(retractall(known))
problem = [s for s in prolog.query("recommend(X)", maxresult=1)]
print("Recommend " + (problem[0]['X'] + "." if problem else "unknown."))

print(list(prolog.query("known(\"yes\", A, V)")))