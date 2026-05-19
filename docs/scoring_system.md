# Scoring System
*March 16, 2026. 5 p.m.*
It is necessary to first define the scoring system in order to create a solid relational database model from the beginning.

How do you rate things? Well, you can either assign a value in a scale, any value that you find fitting to your own criteria (absolute rating), or you can further refine that value by comparing the new element with other elements previously rated.

Both ways have problems.

If you use absolute rating, you might find that you rated two elements with the maximum value, because both met all of your criteria, and you didn't find any reason to degrade any of them. However, you might then find that those two elements are at whole different level, and that it is not fair to treat them as equals.

And if you use relative ratings, you might find that your scale needs a total adjustment every time you do a discovery that changes your view and whole way of thinking.

In the absolute rating, a way to tackle its problem down is to switch into relative rating, but as exposed, relative ratings can be even more annoying.

Additionally, auxiliary rating systems are very common. Marking an element as favorite denotes its emotional relevance, and placing elements in tiers can further honor them without needing to adjust the primary system.

Also, it tends to be hard to abstractly think of a number while thinking on the element, and people might find themselves not completely comfortable with the values they assign. A way to solve that problem is to allow the user to visualize the entire scale at once, instead of just prompting for a value.

Whether ratings should be absolute or relative should turn into an irrelevant question. The rating system should be complete enough, yet simple, for the users to use it easily and quickly.

Another important constraint is that a neutral value should exist, so people are not forced to choose if something was good or bad if they don't feel in either way.

The previous statements summarize in the following conclusions:

1. The primary rating should consist on a discrete-eleven-valued scale from zero to ten
2. The entire scale should be visible at once in the UI
3. A tier system is necessary to encourage users to default into absolute ratings
4. The ability to mark something as a favorite is fundamental

As far as the data pipeline is concerned, that information is just enough.