Welcome back, and congratulations on making it up
to this point of the course.
I really hope that you're having an enjoyable learning
experience.
It has been a learning experience for me as well.
I'm not used to not seeing my students during the lectures,
but hopefully I'm getting the hang of it.
So today, we will talk about Constraint Satisfaction
Problems, also known CSPs.
CSPs are actually search problems
but specific search problems.
Recall from the previous lectures
that search algorithms care about finding
the sequence of actions that lead to the goal.
So we care about the sequence of actions about the goal,
but we also care about finding the least-cost solution,
for example, or finding the solutions in few steps.
We often use some search algorithms like BFS, DFS, et
cetera, and we use even some heuristics, or rule of thumbs,
to speed up the search and to find the optimal solution.
CSPs are search problems, too, in which we don't care much
about the path or the sequence of actions
that lead to the goal as we care about the goal itself.
So, specifically, remember from the previous lectures
we spoke about different representations of states.
So we talked about atomic representations
that is used in search problems in which we want
to go from point B to point C. And each state is,
in this case, a black box.
We don't have any representation details or presentation
of these states.
All we want to do is to reach the goal
and find the sequence of actions that lead to the goal.
In constraint satisfaction problems
the state is not just a black box.
The state has a more complex representation to it
that allows for smarter and deeper understanding
of the problem at hand in order to solve it.
More specifically, the state in a CSP
is defined by variables Xi with values from some domain Di.
Recall from the previous lecture that we called this a factored
representation in which we have some variables defining
the features of the state.
A goal test, in this case, is a set
of constraints specifying allowable combinations
of variable values.
Just to put things back in context,
CSP falls under the representations of variables,
so remember this axis about low intelligence
to high intelligence levels.
So we have seen search problems and adversarial games.
We also have seen several machining learning methodologies.
So, basically, CSPs fall under the variable representation model
in which we are going toward the high level of intelligence
systems.
So let's now define what is a CSP problem.
So a CSP problem consists of three elements.
And these are a set of variables, X,
that's equal to the set X1, X2, Xn, if you have n variables--
a set of domains for each variable, D1, D2, Dn--
and a set of constraints, C, that
specify allowable combinations of value.
So what kind of values can we combine together
to solve that CSP?
Solving the CSP causes, then, in finding the assignments that
actually satisfy all the constraints of the problem.
We learn different concepts in this lecture.
And these include how to formalize the problem,
how to do a backtracking search in CSPs,
how to check for arc consistency,
among other concepts.
Finally, we call the solution a consistent assignment.
Why consistent?
Because we try to find the assignment
that does not violate the constraint of the problem.
Let's take an example of CSP called Map coloring.
Map coloring is inspired by graph theory.
It's a famous problem in graph theory
in which you want to color a map and not use the same color
on any two adjacent regions.
So let's move now from North America
to Australia, in which we are given a map,
and this map has different regions of Australia,
seven regions specifically, right.
And you want to be able to color this message so
that we don't use the same color on two adjacent regions.
To formalize the problem as a CSP,
we are going to first define what are the variables.
And the variables in this case are
x equal to Western Australia, WA, Northern Territory, NT, et
cetera.
So we have seven variables in our problem.
The domain are the colors you are given to color the map.
And these are red, green, and blue,
which means that any variable in x
can take any of these three values.
And finally, the constraints are: adjacent regions
must have different colors.
So could spell this constraint as follows.
We could say, for example, we want WA to be different of NT,
or we could write it as a pair.
We want the pair WA, NT to belong to the set
either with green, or red blue, or blue green, et cetera.
So we're going to spell out all possible pairs
such as the first element of the pair
is different from the second element of the pair.
This is a typical CSP problem.
And the solution for this kind of CSP
is to find this assignment of colors to the regions.
Here's an example.
So an example of solutions to this
would be a possible solution is equal to what?
Give the color red to WA, the color
green to Northern Territory, red to Queensland, et cetera.
So note here that we could color Tasmania
in another color, any other color,
because it's not linked to any other area on the map.
So finding a solution for CSP is to find an assignment of colors
to the different variables in the problem.
Real-world problems of CSPs are numerous,
and this includes assignment problems.
For example, who teaches what class?
Timetabling problems such as which
class is offered when and where, hardware configurations,
spreadsheets, transportation scheduling,
factory scheduling, floor planning.
And notice that many real-world problems
involve real value variables rather than discrete variables
such as the color problem in the map coloring.
It's often useful to represent the CSP
as what we call the constraint graph, in which we have nodes
representing the variables and edges representing
the constraints between the nodes.
So, for example, in the Australia map,
we could represent each of these regions
as a node, and any constraint we have has actually an edge
between those nodes.
So, for example, we have the constraint
that WA should be different of NT.
A is represented by this node here.
We talk about binary CSPs when constraints relate at
most one pair of variables or two variables.
It's often CSP algorithms which leverage
that structure or that graph that represents the problem
to speed up the search.
For example, Tazmania is independent
of the other regions, and we can color it with whatever color
we want among the three colors, red, blue, and green.
So using this graph is very interesting
to speed up the search and come up
with better search algorithms to solve the problem.
We also have a variety of variables,
and this includes discrete variables
or continuous variables.
So in discrete variables we could have finite domain
or infinite domain.
And in finite domain, we assume that we have n variables
and each variable takes its value in d values,
then the number of complete assignments we can have
is on the order of d to the n.
Examples of this kind of variables
include map coloring, the 8-queen problem,
and so on and so forth.
If the domain is infinite, such as integers or strings,
but it's still discrete in the values,
then we need to use some constraint language.
The constraint language we define actually
how we spell out the constraint of the problem.
For job scheduling, for example, to express that time 2 needs
to start D after time 1, then we could
express that T1 plus D is less than or equal to T2.
If the variables are continuous, which
is common in operating research, then we
use some techniques like linear programming,
with linear and nonlinear equalities
to solve the problem.
We may also have a variety of constraints.
And this includes unary constraints which
involve only one variable.
For example, we could say that SA is different than green,
is the one variable different than a value?
We could have binary constraint, which is most common,
in which we have a constraint on pairs of variables such as SA
different than WA means that the color of SA
different than the color of WA.
We may also have what we call global constraints, that
involves three or more variables.
For example, and a famous one is Alldiff (All Different),
that specifies that all the variables
must have a different value.
Example of this kind of constraint
includes cryptoarithmetic puzzles,
which we will see in a second, and Sudoku problems.
We may also have more subtle kinds of constraints,
and this includes preferences.
For example, red is better than blue or professor A prefers
to teach in the morning.
So these are softer, we are going
to often represent that by cost for each variable assignment.
And this actually includes problems
such as constraint optimization problems,
in which we are going to include that kind of constraints.
Now let's revise again the 8-queen problem
seen a few weeks ago.
So remember we want to place 8 queens on an eight-
by-eight chess board so as no queen attacks another one.
And if a queen attacks another one,
if it's put on the same column as the other queen,
or on the same line, or on the same diagonal.
So we have seen this problem as a search problem in which we
were looking for the sequence of actions
putting a queen after a queen on the board
as we solve the problem.
So let's discuss this problem now in the CSP framework.
A first problem formalization could
be that we define one variable per queen.
So we have Q1, Q2, Q8, these are the variables.
These are the variables X. So X would
be equal to queen 1, queen 2, queen 8
where each variable would have a value between 1 and 64,
this is the size of the board.
So the first one would be put at cell one
and the last one would be at cell 64.
So you're going to start from the top-left corner
to the bottom-right corner.
A solution to that would be the position of the queen
or the assignment of the value between 1 and 64
to each of the variables, Q1 to Q8.
So a solution could be, queen 1 is 1, queen 2 is 13,
queen 3 is 24, and et cetera.
A second possibility to formalize the problem
is to use still eight variables, Q1, Q2, Q8, but in this case
a domain would be more restricted.
Each variable could have a value between 1 and 8,
considering the columns.
In other words, we're going to see
in what position in the column we're going to put the queen.
So the first one would be in position one.
In the second column we will use position 7.
And the third column is going to be positioned 5, et cetera.
So the domain now for each variable,
given that we're going column by column from left to right,
it's clear that we're going to just provide
the position of the line in that column.
So in this case we're going to use less possible values
to assign to the variables.
We might be tempted to do a brute force search.
In other words, can we simply generate and test
all possible configurations.
You know, just say whether-- check the constraint
on each possible configuration and pick the one that
satisfies all the constraints.
So this might look easy, especially
on a four-by-four chess board.
So suppose we have a four-queen problem.
So in the four-queen problem, if we
choose the second formalization of the problem in which case
we put one queen per column, so each variable,
each queen would have a value between 1 and 8,
then it may sound easy.
So this is a random generation of all possible queens
on the chess board, a four-by-four,
but actually we have to be careful
that these kinds of configurations are actually
deemed to be not successful.
So let's suppose that we are going
to put a queen on each column.
In this case, the first column could have four possibilities
to put the first queen, the second
would have another four possibilities
to put the second queen, the third one we have four
possibilities, and the fourth one we
have four possibilities, which will give us 4 to the 4,
which would be equal to 256.
So for a 4-queen problem it's easy to just generate
these 256 configurations and test all of them on a computer.
It's going to be very fast.
However, the question is, is this brute force search
scalable?
For example, if we move to an 8-queen problem,
we don't have any more a choice between four positions
on the column, we have eight.
So it's going to be 8 times 8 times 8, which
is 8 to the 8, which actually will grow really, really big
and up to something like 16.7 million
possible configurations.
The problem becomes very big, and it's
hard to really think about generating all possibilities
or all configurations and simply test the constraints to pick
a solution.
So think also about maybe 16-queen
in which we will have something like 10
to the 20 possible configurations of the boards.