# Import necessary packages
from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

askables = {
    "work": ["meeting", "no_meeting", "none"],
    "wifi": ["strong", "normal", "none"],
    "noise_level": ["quiet", "moderate", "noisy"],
    "computer": ["need_charge", "no_need_charge"],
    "diet_restriction": ["vegan", "vegt", "gluten_free", "none"], # multiple possible
    "arrive_time": ["morning", "afternoon", "evening"], # multiple possible
    "breakfast": ["yes", "no"],
    "lunch": ["yes", "no"],
    "dinner": ["yes", "no"],
    "length_stay": float(),
    "travel_distance": float(),
    "budget_category": ["one", "two", "three"]
}

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

#print(list(prolog.query("known(A, V)")))
