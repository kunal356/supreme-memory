# Trackbase Software Engineering Task

## Background

For this task, you're part of the team at Trackbase helping to maintain one of our products. The product includes some logic which calculates the total cost for a path through a network (a path is referred to as a "traversal" in the code). Each node in the network can have several different costs associated with it. One of your colleagues has identified a performance issue with the current implementation and has asked for your help to improve it.


## Task
**Support Ticket #2024-10-01.25**
### Notes
User(s) are reporting a degradation in performance at peak times and their API response times are failing our SLAs.

I think I've isolated the issue to a core piece of logic that is calculating traversal costs - seems a little greedy!

I extracted the raw logic into the method `logic_as_is` in `funcs.py` and added a crude profiling harness to help us out.

### Actions
1) Could you take a look and see if you can improve things with the logic?
2) We'll need to give the users test-access to this improved version outside our prod system, could you wrap it up as a simple REST API for me?

p.s. Sorry about the code quality, I'm in a bit of a rush!
 - I welcome any tidy-up/refactor suggestions you have to improve the profiling harness code - could be a helpful tool if we generalised it!?
