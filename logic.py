import json

from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

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
    with open("askables.json") as f:
        askables = json.load(f)
    with open("cafes.json") as f2:
        cafes = json.load(f2)

    def read_input2(A, V, Y):
        if isinstance(Y, Variable):
            askable = str(A)
            ask_dict = askables[askable]
            shared_data["curr_question"] = {
                "id": askable,
                "text": ask_dict["text"],
                "type": ask_dict["type"],
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
                value_opt = next(opt for opt in ask_dict["options"] if opt["id"] == response[0])
                Y.unify(float(value_opt["value"]))
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
    shared_data["done"] = True
    rec_id = rec[0]['X'] if rec else None
    shared_data["rec"] = cafes[rec_id] if rec_id else None
    shared_data["rec_id"] = rec_id
    with open("rec.txt", 'w') as f:
        f.write(f"I recommend {rec_id}" if rec else "No recommendation.")
        f.write(str(list(prolog.query("known(A, V)"))))

#   
