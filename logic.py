import json

from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom


def run_expert_system(shared_data):
    prolog = Prolog()  # Global handle to interpreter
    retractall = Functor("retractall")
    known = Functor("known", 2)
    with open("askables.json") as f:
        askables = json.load(f)
    with open("cafes.json") as f2:
        cafes = json.load(f2)

    def read_input(A, V, Y):
        if isinstance(Y, Variable):
            askable = str(A)
            ask_dict = askables[askable]
            shared_data["curr_question"] = {
                "id": askable,
                "text": ask_dict["text"],
                "type": ask_dict["type"],
                "options": ask_dict["options"],
                "default": ask_dict["default"],
            }
            # wait for response
            while f"{askable}_response" not in shared_data:
                pass
            response = shared_data[f"{askable}_response"]  # a list
            if askable in ["diet_restrictions", "arrive_times"]:
                Y.unify(list(map(Atom, response)))
            elif askable in ["travel_distance", "length_stay"]:
                value_opt = next(
                    opt for opt in ask_dict["options"] if opt["id"] == response[0]
                )
                Y.unify(float(value_opt["value"]))
            else:
                Y.unify(Atom(response[0]))
            return True
        else:
            return False

    read_input.arity = 3

    registerForeign(read_input)

    prolog.consult("expert.pl")  # open the KB for consulting
    call(retractall(known))
    rec: list = [s for s in prolog.query("recommend(X)", maxresult=1)]
    shared_data["done"] = True
    rec_id = rec[0]["X"] if rec else None
    shared_data["rec"] = cafes[rec_id] if rec_id else None
    shared_data["rec_id"] = rec_id
    with open("rec.txt", "w") as f:
        f.write(f"I recommend {rec_id}" if rec else "No recommendation.")
        f.write(str(list(prolog.query("known(A, V)"))))


#
