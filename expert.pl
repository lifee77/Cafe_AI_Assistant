%  Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

%Attendant Coffee Roasters - Shoreditch
%closes at 5pm
recommend(acr):- \+wifi(strong),
	\+budget_category(one),
	noise_level(noisy),
	diet(none),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >= 0.8.
	

%Maria's market cafe
recommend(mmc):- noise_level(moderate),
	diet(none),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 16,
	\+breakfast,
	\+dinner,
	travel_distance(X), X >= 2.8.
	

%The English Rose Café and Tea Shop
recommend(erc):- \+computer(need_charge), \+budget_category(one),
	noise_level(moderate),
	\+diet(vegt), \+diet(gluten_free),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+lunch,
	\+dinner,
	travel_distance(X), X >= 3.7.
	

recommend(mola_cafe):- noise_level(quiet),
	\+diet(vegt), \+diet(gluten_free),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 16,
	\+dinner,
	travel_distance(X), X >= 0.5.
	

%Gecko Coffeehouse
recommend(gecko):- \+budget_category(one),
	noise_level(quiet),
	\+diet(vegt), \+diet(gluten_free),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >=1.3.

%a pinch of salt
recommend(pinch):- wifi(none),
	\+computer(need_charge),
	\+budget_category(one),
	noise_level(noisy),
	\+diet(vegt), \+diet(gluten_free),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 15,
	\+lunch,
	\+dinner,
	travel_distance(X), X >= 0.5.
	

%WatchHouse Bishopsgate
recommend(whb):- \+computer(need_charge),
	\+budget_category(one),
	noise_level(noisy),
	\+diet(vegan), \+diet(gluten_free),
	\+arrive_time(evening),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >= 1.2.

%Pret A Manager
recommend(pret_a):- noise_level(noisy),
	\+diet(vegan), \+diet(gluten_free),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 20.5,
	\+dinner,
	travel_distance(X), X >= 0.4.

wifi(strong):- work(meeting), assertz(known(wifi, strong)).
wifi(X):- ask(wifi, X). % strong, normal, none
noise_level(quiet):- wifi(strong).
noise_level(X):- ask(noise_level, X). %noise_level can have values quiet, moderate, noisy (or maybe dont_care for last option)
work(X):- ask(work, X). % work can have values meeting, no_meeting, none
computer(X):- ask(computer, X). % computer can have values need_charge, no_need_charge
diet(X):- ask(diet, X). % diet can have values vegan, vegt, gluten_free, none.

arrive_time(X):- ask(arrive_time, X). % arrive_time can be morning, afternoon, evening.
arrive_mean_time(9.5):- arrive_time(morning).
arrive_mean_time(14):- arrive_time(afternoon).
arrive_mean_time(18.5):- arrive_time(evening).

breakfast:- ask(breakfast, X), X \== no.
lunch:- ask(lunch, X), X \== no.
dinner:- ask(dinner, X), X \== no.
length_stay(X):- ask(length_stay, X).
travel_distance(X):- ask(travel_distance, X).
budget_category(X):- ask(budget_category, X). % one: 0-10, two: 10-20, three: 20+


ask(A, V):-
known(A, V), % succeed if true
!.	% stop looking

ask(A, V):-
known(A, X), % fail if something else
!, fail.

ask(A, V):-
read_input(A, V, Y), % in future, V is a list of multiple responses
assertz(known(A, Y)),
V = Y. % if V is not bound, succeed, else check if it is same as Y