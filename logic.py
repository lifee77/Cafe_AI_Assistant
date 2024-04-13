import json

from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom


def run_expert_system(shared_data):
    prolog = Prolog()  # Global handle to interpreter
    retractall = Functor("retractall")
    # Functor representing the 'known' predicate used in Prolog
    known = Functor("known", 2)
    # Load 'askables' data from a JSON file
    with open("askables.json") as f:
        askables = json.load(f)
    # Load 'cafes' data from a JSON file containing the names and Google Maps links
    with open("cafes.json") as f2:
        cafes = json.load(f2)
    
    # Function that interfaces with Prolog to handle user inputs
    def read_input(A, V, Y):
         # Check if the third argument is a variable
        if isinstance(Y, Variable):
            askable = str(A)
            # Retrieve the question data from the 'askables'
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
            # Retrieve the response
            response = shared_data[f"{askable}_response"]  # a list
            if askable in ["diet_restrictions", "arrive_times"]:
                 # For list-based responses, we need to convert each item to a Prolog atom and unify
                Y.unify(list(map(Atom, response)))
            elif askable in ["travel_distance", "length_stay"]:
                # For numeric responses, we need to find the corresponding numeric value and unify
                value_opt = next(
                    opt for opt in ask_dict["options"] if opt["id"] == response[0]
                )
                Y.unify(float(value_opt["value"]))
            else:
                # For single-choice responses
                Y.unify(Atom(response[0]))
            return True
        else:
            return False
    # Set the arity of the read_input function, which is the number of arguments it accepts
    read_input.arity = 3

    registerForeign(read_input)
    
    # Load the Prolog knowledge base
    prolog.consult("expert.pl")
    
    # Reset the 'known' predicate in the KB to delete any prior user responses
    call(retractall(known))
    
    rec: list = [s for s in prolog.query("recommend(X)", maxresult=1)]
    shared_data["done"] = True
    # Extract the recommendation from the query result
    rec_id = rec[0]["X"] if rec else None
    shared_data["rec"] = cafes[rec_id] if rec_id else None
    shared_data["rec_id"] = rec_id

