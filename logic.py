# Import necessary packages
from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

prolog = Prolog() # Global handle to interpreter

retractall = Functor("retractall")
known = Functor("known",2)

def read_input(A, V, Y):
    if isinstance(Y, Variable):
        response = input(f"What is {A}? ")
        if str(A) in ["travel_distance", "length_stay"]:
            Y.unify(float(response))
        else:
            Y.unify(Atom(response))
        return True
    else:
        return False


read_input.arity = 3

registerForeign(read_input)

prolog.consult("expert.pl") # open the KB for consulting

call(retractall(known))
rec = [s for s in prolog.query("recommend(X)", maxresult=1)]
print(" I recommend " + (rec[0]['X'] + "." if rec else "unknown."))

print(list(prolog.query("known(A, V)")))
