%  Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

%Attendant Coffee Roasters - Shoreditch
%closes at 5pm
recommend(acr):-
	init_tui,
	\+wifi(strong),
	\+budget_category(one),
	noise_level(noisy),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >= 0.8.
	

%Maria's market cafe
recommend(mmc):- noise_level(moderate),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 16,
	\+breakfast,
	\+dinner,
	travel_distance(X), X >= 2.8.
	

%The English Rose Café and Tea Shop
recommend(erc):- \+computer(need_charge), \+budget_category(one),
	noise_level(moderate),
	diet_ok(vegan),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+lunch,
	\+dinner,
	travel_distance(X), X >= 3.7.
	

recommend(mola_cafe):- noise_level(quiet),
	diet_ok(vegan),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 16,
	\+dinner,
	travel_distance(X), X >= 0.5.
	

%Gecko Coffeehouse
recommend(gecko):- \+budget_category(one),
	noise_level(quiet),
	diet_ok(gluten_free),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >=1.3.

%a pinch of salt
recommend(pinch):- wifi(none),
	\+computer(need_charge),
	\+budget_category(one),
	noise_level(noisy),
	diet_ok(vegan),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 15,
	\+lunch,
	\+dinner,
	travel_distance(X), X >= 0.5.
	

%WatchHouse Bishopsgate
recommend(whb):- \+computer(need_charge),
	\+budget_category(one),
	noise_level(noisy),
	diet_ok(vegt),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 17,
	\+dinner,
	travel_distance(X), X >= 1.2.

%Pret A Manager
recommend(pret_a):- noise_level(noisy),
	diet_ok(vegt),
	arrive_mean_time(Y), length_stay(Z), Y + Z =< 20.5,
	\+dinner,
	travel_distance(X), X >= 0.4.

init_tui:- ask(init_tui, _). %This is just an initialising dummy for the tui to startup

wifi(strong):- work(meeting), assertz(known(wifi, strong)).
wifi(X):- ask(wifi, X). % strong, normal, none
work(X):- ask(work, X). % work can have values meeting, no_meeting, none

noise_level(quiet):- wifi(strong).
noise_level(X):- ask(noise_level, X). %noise_level can have values quiet, moderate, noisy (or maybe dont_care for last option)
computer(X):- ask(computer, X). % computer can have values need_charge, no_need_charge
diet_restrictions(X):- ask(diet_restrictions, X). % diet_restrictions is a list of values vegan, vegt, gluten_free, none.
%represents diet restrictions that the user is okay with
%[vegan, gluten_free] means that the user is fine with vegan or gluten_free or both
%[none] indicates the user is okay with any diet
diet_ok(_):- diet_restrictions([X]), X == none.
diet_ok(vegan):- diet_restrictions(X), member(vegan, X).
diet_ok(gluten_free):- diet_restrictions(X), member(gluten_free, X).
diet_ok(vegt):- diet_restrictions(X), member(vegt, X).

arrive_times(X):- ask(arrive_times, X). % arrive_times is a list of values morning: 7am-12pm, afternoon:12-4pm, evening:4-9pm.
%represents the possible arrival times by the user

can_arrive(morning):- arrive_times(X), member(morning, X). %can_arrive is one of those values
can_arrive(afternoon):- arrive_times(X), member(afternoon, X).
can_arrive(evening):- arrive_times(X), member(evening, X).
arrive_mean_time(9.5):- can_arrive(morning). %mean time within the arrive_time range
arrive_mean_time(14):- can_arrive(afternoon).
arrive_mean_time(18.5):- can_arrive(evening).

breakfast:- ask(breakfast, X), X \== no.
lunch:- ask(lunch, X), X \== no.
dinner:- ask(dinner, X), X \== no.
length_stay(X):- ask(length_stay, X).
travel_distance(X):- ask(travel_distance, X).
budget_category(X):- ask(budget_category, X). % one: 0-10, two: 10-20, three: 20+


ask(A, V):-
known(A, V), % succeed if true
!.	% stop looking

ask(A, _):-
known(A, _), % fail if something else
!, fail.

ask(A, V):-
read_input(A, V, Y), % in future, V is a list of multiple responses
assertz(known(A, Y)),
V = Y. % if V is not bound, succeed, else check if it is same as Y