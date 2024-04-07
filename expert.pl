%  Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

%Attendant Coffee Roasters - Shoreditch
recommend(acr):- \+wifi(strong),
	\+budget_category(one),
	noise_level(noisy),
	travel_distance(X), X >= 0.5,
	\+arrive_time(evening),
	\+arrive_time(late_evening),
	\+dinner,
	length_stay(X), X =< 2.

%Maria's market cafe
recommend(mmc):- noise_level(moderate), arrive_time(morning).
recommend(mmc):- noise_level(moderate), arrive_time(noon).

%The English Rose Café and Tea Shop
recommend(erc):- \+computer(need_charge), \+budget_category(one),
	noise_level(moderate),
	travel_distance(X), X >= 3.7,
	\+arrive_time(evening),
	\+arrive_time(late_evening),
	\+dinner,
	length_stay(X), X =< 1.

recommend(mola_cafe):- \+budget_category(one),
	noise_level(quiet),
	travel_distance(X), X >= 0.5,
	\+arrive_time(evening),
	\+arrive_time(late_evening),
	\+dinner,
	length_stay(X), X =< 2.


wifi(strong):- work(meeting).
wifi(strong):- ask(wifi, X), X == yes. % yes or no
noise_level(quiet):- wifi(strong).
noise_level(X):- ask(noise_level, X). %noise_level can have values quiet, moderate, noisy (or maybe dont_care for last option)
work(X):- ask(work, X). % work can have values meeting, no_meeting, none
computer(X):- ask(computer, X). % computer can have values need_charge
diet(X):- ask(diet, X). % diet can have values vegan, vegt, gluten_free. Should we
%recommend a vegan place to only vegans or anyone generally?
arrive_time(X):- ask(arrive_time, X). % arrive_time can be very_early, morning, noon, evening, late_evening, night
breakfast:- ask(breakfast, X), X \== no.
lunch:- ask(lunch, X), X \== no.
dinner:- ask(dinner, X), X \== no.
length_stay(X):- ask(length_stay, X).
travel_distance(X):- ask(travel_distance, X).
budget_category(X):- ask(budget_category, X).

ask(A, V):-
known(A, V), % succeed if true
!.	% stop looking

ask(A, V):-
known(A, X), % fail if something else
!, fail.

ask(A, V):-
read_categorical(A, V, Y), % in future, V is a list of multiple responses
assertz(known(A, Y)),
V = Y. % if V is not bound, succeed, else check if it is same as Y