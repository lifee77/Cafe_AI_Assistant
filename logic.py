import json

from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

askables = {
    "init_tui": {
        "text": "Init",
        "options": [],
        "default": "Init",
        "type": "single_choice"
    },
    "work": {
        "text": "Do you wish to work at the cafe?",
        "options": [
            "meeting",
            "no_meeting",
            "none"
        ],
        "default": "none",
        "type": "single_choice"
    },
    "wifi": {
        "text": "What strength of wifi do you need (if any)?",
        "options": [
            "strong",
            "normal",
            "none"
        ],
        "default": "none",
        "type": "single_choice"
    },
    "noise_level": {
        "text": "What is the maximum noise level you can tolerate?",
        "options": [
            "quiet",
            "moderate",
            "noisy"
        ],
        "default": "quiet",
        "type": "single_choice"
    },
    "computer": {
        "text": "Are you the responsible type or type to forget to charge your computer before going out?",
        "options": [
            "need_charge",
            "no_need_charge"
        ],
        "default": "need_charge",
        "type": "single_choice"
    },
    "diet_restrictions": {
        "text": "What dietary restrictions do you have?",
        "options": [
            "vegan",
            "vegt",
            "gluten_free",
            "none"
        ],
        "default": "none",
        "type": "multi_choice"
    },
    "arrive_times": {
        "text": "At what times do you want to go to the cafe?",
        "options": [
            "morning",
            "afternoon",
            "evening"
        ],
        "default": "afternoon",
        "type": "multi_choice"
    },
    "breakfast": {
        "text": "Do you want to have breakfast at the cafe?",
        "options": [
            "yes",
            "no"
        ],
        "default": "no",
        "type": "single_choice"
    },
    "lunch": {
        "text": "Do you want to have lunch at the cafe?",
        "options": [
            "yes",
            "no"
        ],
        "default": "no",
        "type": "single_choice"
    },
    "dinner": {
        "text": "Do you want to have dinner at the cafe?",
        "options": [
            "yes",
            "no"
        ],
        "default": "no",
        "type": "single_choice"
    },
    "length_stay": {
        "text": "How long do you plan to stay in a cafe?",
        "options": [
            "1.0"
        ],
        "default": "1.0",
        "type": "single_choice"
    },
    "travel_distance": {
        "text": "How far are you willing to travel from the residence hall (maximum)?",
        "options": [
            "10.0"
        ],
        "default": "10.0",
        "type": "single_choice"
    },
    "budget_category": {
        "text": "What is your budget for a visit to the cafe?",
        "options": [
            "one",
            "two",
            "three"
        ],
        "default": "two",
        "type": "single_choice"
    }
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
    # with open("askables.json") as f:
    #     askables = json.load(f)

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
