---
layout: page
title: Programming Dos and Don'ts
date: 2021-12-08 18:00:00
description: Basic rules for coding, best practices
---


## Python

Python is a beautiful programming language precisely because it emphasises **readability**. 

Besides being pythonic in our coding, we want to code not as if we're coding to make our program run(!). But: 

**The way we write code should be intended for someone less skilled than us to be able to read it, in two years time.** 

It's likely that this person will be one of your colleagues, it could be someone somewhere on the other side of the world, but most likely it is going to be your future self with a hangover. The motto is: **have mercy on your future self**. Any shortcuts you take now are going to mean hours of work when you have to revisit the code. And revisit the code you will - research isn't called **re**-search for nothing!


First step: do ```import this```
which returns:

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

Make sure you understand what is meant by each of these lines in the [Zen of Python, pep0020](https://www.python.org/dev/peps/pep-20/)


### Some further basic rules:

- never hardcode any numbers in your code. Values used in an analysis should propagate from function arguments and/or come from a .yml file containing the settings of your analysis or experiment.
- use [pep8](https://pep8.org). no discussion.
- the names of variables, classes, and functions/methods should be descriptive, unambiguous, and correct. The reader should immediately understand what your code does from the name's implications as to types of inputs, outputs, etc. 
- always use docstrings, following [pep257](https://www.python.org/dev/peps/pep-0257/). Keep them up to date. 
- use git, preferably in a [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)-type setup
- .....

### Software Design Principles

You are part of a software development team, whether you like it or not. This means that we all need to have a basic grasp of software design principles. Tomas has a folder of pdfs of books, several of which treat these principles. There are some valuable youtube resources too:

- [Arjan Codes](https://www.youtube.com/c/ArjanCodes) where, Arjan explains python software design principles
- [mCoding](https://www.youtube.com/c/mCodingWithJamesMurphy) where James Murphy explains the innards of python

### Test-driven developement

One of those things that we scientists can learn from programmers is test-driven developement, in which you first write the tests that your code should pass, and only then write the actual code. This is a good practice for several reasons; it forces you to think about what you're going to be coding, but it also makes your code more robust. Moreover, it gives you a lasting target for the performance of your code, which is essential for continuous integration. 


<hr/>

We will be expanding this document in the coming period. 
