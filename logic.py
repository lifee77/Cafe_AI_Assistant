# Import necessary packages
from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

askables = {
    "work": {"options": ["meeting", "no_meeting", "none"], "default": "none"},
    "wifi": {"options": ["strong", "normal", "none"], "default": "none"},
    "noise_level": {"options": ["quiet", "moderate", "noisy"], "default": "quiet"},
    "computer": {"options": ["need_charge", "no_need_charge"], "default": "need_charge"},
    "diet_restrictions": {"options": ["vegan", "vegt", "gluten_free", "none"], "default": "none"}, # multiple possible
    "arrive_times": {"options": ["morning", "afternoon", "evening"], "default": "afternoon"}, # multiple possible
    "breakfast": {"options": ["yes", "no"], "default": "no"},
    "lunch": {"options": ["yes", "no"], "default": "no"},
    "dinner": {"options": ["yes", "no"], "default": "no"},
    "length_stay": {"options": ["1.0"], "default": "1.0"},
    "travel_distance": {"options": ["10.0"], "default": "10.0"},
    "budget_category": {"options": ["one", "two", "three"],  "default": "two"},
}

def read_input(A, V, Y):
    """A is the askable, V is the value prolog wants to find out
    about (unused here but needed), Y is the return variable to prolog"""
    if isinstance(Y, Variable):
        response = input(f"What is {A}? ").split()
        if str(A) in ["diet_restriction", "arrive_time"]:
            Y.unify(list(map(Atom, response)))
        elif str(A) in ["travel_distance", "length_stay"]:
            Y.unify(float(response[0]))
        else:
            Y.unify(Atom(response[0]))
        return True
    else:
        return False
read_input.arity = 3



def run_expert_system(shared_data):
    prolog = Prolog() # Global handle to interpreter
    retractall = Functor("retractall")
    known = Functor("known",2)

    def read_input2(A, V, Y):
        if isinstance(Y, Variable):
            askable = str(A)
            ask_dict = askables[askable]
            shared_data["curr_question"] = {
                "text": askable,
                "type": "single_choice",
                "options": ask_dict["options"],
                "default": ask_dict["default"]
            }
            # wait for response
            while f"{askable}_response" not in shared_data:
                pass
            response = shared_data[f"{askable}_response"] # a list
            if askable in ["diet_restrictions", "arrive_times"]:
                Y.unify(list(map(Atom, response)))
            elif askable in ["travel_distance", "length_stay"]:
                Y.unify(float(response[0]))
            else:
                Y.unify(Atom(response[0]))
            return True
        else:
            return False
    read_input2.arity = 3

    registerForeign(read_input2)

    prolog.consult("expert.pl") # open the KB for consulting
    call(retractall(known))
    rec = [s for s in prolog.query("recommend(X)", maxresult=1)]
    with open("rec.txt", 'w') as f:
        f.write(f"I recommend {rec[0]['X']}" if rec else "No recommendation.")
        f.write(str(list(prolog.query("known(A, V)"))))

#   
