%  Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

%Maria's market cafe
recommend(mmc):- wifi, computer(need_charge), noise_level(moderate), arrive_time(morning), lunch.
recommend(mmc):- wifi, computer(need_charge), noise_level(moderate), arrive_time(noon), lunch.
recommend(mmc):- wifi, computer(need_charge), noise_level(moderate), arrive_time(noon).
recommend(mmc):- computer(need_charge), noise_level(moderate), arrive_time(noon).


wifi:- work(meeting).
% Asking clauses
wifi:- ask(wifi, X).
noise_level(quiet):- wifi.
noise_level(X):- ask(noise_level, X). %noise_level can have values quiet, moderate, noisy
work(X):- ask(work, X). % work can have values meeting, no_meeting, none
computer(X):- ask(computer, X). % computer can have values need_charge
diet(X):- ask(diet, X). % diet can have values vegan, veg, gluten_free
arrive_time(X):- ask(arrive_time, X). % arrive_time can be very_early, morning, noon, evening, late_evening, night
breakfast:- ask(breakfast, X).
lunch:- ask(lunch, X).
dinner:- ask(dinner, X).
length_stay(X):- ask(length_stay, X).
travel_distance(X):- ask(travel_distance, X).

%% known(no, engine, turning_over).
%% known(no, lights, weak).
%% known(no, radio, weak).
%% known(yes, warning_light, oil).

ask(A, V):-
known(yes, A, V), % succeed if true
!.	% stop looking

ask(A, V):-
known(_, A, V), % fail if false
!, fail.

% If not multivalued, and already known to be something else, don't ask again for a different value.
ask(A, V):-
\+multivalued(A),
known(yes, A, V2),
V \== V2,
!, fail.

%% ask(A, V):-
%% read_py(A,V,Y), % get the answer
%% assertz(known(Y, A, V)), % remember it
%% Y == "yes". % succeed or fail

ask(A, V):-
read_categorical(A,V), % get the answer
assertz(known("yes", A, V)). % succeed