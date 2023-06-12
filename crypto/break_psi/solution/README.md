# Solution

We have to pass incorrect intersection of sets given by server, but it must to pass correctness test.

This test contains:
 1. Comparing hashes of intersections sent to Alice and Bob
 2. Counting if every element occurs with corresponding 8 redundant elements

It means that:
 1. We have to send the same intersections to Alice and Bob
 2. If we want to remove an element, we must also remove corresponding redundant elements

In a properly written PSI we don't know which elements are redundant, because sets are shuffled, but here all of these are at the end. For example if the sets had 5 elements and there were 3 redundants to each element, they would look like this:

`1 2 3 4 5 1 1 1 2 2 2 3 3 3 4 4 4 5 5 5`

We can find one element that is in intersection and ignore rest of them (there always will be at least one, it can be proven with pigeonhole principle). Than we include redundant elements to pass correctness test and send it to both Alice and Bob. There is a risk that intersection will be correct, but the probability is very low, so it should work most of attempts.

Example solving script in python is in [solution.py](solution.py)