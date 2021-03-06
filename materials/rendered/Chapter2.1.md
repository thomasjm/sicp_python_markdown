
[[table-of-contents]]

# 2.1 Introduction

We concentrated in Chapter 1 on computational processes and on the role of functions in program design. We saw how to use primitive data (numbers) and primitive operations (arithmetic operations), how to form compound functions through composition and control, and how to create functional abstractions by giving names to processes. We also saw that higher-order functions enhance the power of our language by enabling us to manipulate, and thereby to reason, in terms of general methods of computation. This is much of the essence of programming.

This chapter focuses on data. Data allow us to represent and manipulate information about the world using the computational tools we have acquired so far. Programs without data structures may suffice for exploring mathematical properties. But real-world phenomena, such as documents, relationships, cities, and weather patterns, all have complex structure that is best represented using *compound data types*. With structured data, programs can simulate and reason about virtually any domain of human knowledge and experience. Thanks to the explosive growth of the Internet, a vast amount of structured information about the world is freely available to us all online.

## 2.1.1 The Object Metaphor

In the beginning of this course, we distinguished between functions and data: functions performed operations and data were operated upon. When we included function values among our data, we acknowledged that data too can have behavior. Functions could be operated upon like data, but could also be called to perform computation.

In this course, *objects* will serve as our central programming metaphor for data values that also have behavior. Objects represent information, but also *behave* like the abstract concepts that they represent. The logic of how an object interacts with other objects is bundled along with the information that encodes the object's value. When an object is printed, it knows how to spell itself out in letters and numbers. If an object is composed of parts, it knows how to reveal those parts on demand. Objects are both information and processes, bundled together to represent the properties, interactions, and behaviors of complex things.

The object metaphor is implemented in Python through specialized object syntax and associated terminology, which we can introduce by example. A date is a kind of simple object.

``` {.python}
from datetime import date
```

The name `date` is bound to a *class*. A class represents a kind of object. Individual dates are called *instances* of that class, and they can be *constructed* by calling the class as a function on arguments that characterize the instance.

``` {.python}
today = date(2011, 9, 12)
```

While `today` was constructed from primitive numbers, it behaves like a date. For instance, subtracting it from another date will give a time difference, which we can display as a line of text by calling `str`.

``` {.python}
str(date(2011, 12, 2) - today)
```
<html><div class="codeparent python"><pre class="stdout"><code>'81 days, 0:00:00'</code></pre></div></html>

Objects have *attributes*, which are named values that are part of the object. In Python, we use dot notation to designated an attribute of an object.

> &lt;expression&gt; . &lt;name&gt;

Above, the `<expression>` evaluates to an object, and `<name>` is the name of an attribute for that object.

Unlike the names that we have considered so far, these attribute names are not available in the general environment. Instead, attribute names are particular to the object instance preceding the dot.

``` {.python}
today.year
```
<html><div class="codeparent python"><pre class="stdout"><code>2011</code></pre></div></html>

Objects also have *methods*, which are function-valued attributes. Metaphorically, the object "knows" how to carry out those methods. Methods compute their results from both their arguments and their object. For example, The `strftime` method of `today` takes a single argument that specifies how to display a date (e.g., `%A` means that the day of the week should be spelled out in full).

``` {.python}
today.strftime('%A, %B %d')
```
<html><div class="codeparent python"><pre class="stdout"><code>'Monday, September 12'</code></pre></div></html>

Computing the return value of `strftime` requires two inputs: the string that describes the format of the output and the date information bundled into `today`. Date-specific logic is applied within this method to yield this result. We never stated that the 12th of September, 2011, was a Monday, but knowing one's weekday is part of what it means to be a date. By bundling behavior and information together, this Python object offers us a convincing, self-contained abstraction of a date.

Dot notation provides another form of combined expression in Python. Dot notation also has a well-defined evaluation procedure. However, developing a precise account of how dot notation is evaluated will have to wait until we introduce the full paradigm of object-oriented programming over the next several sections.

Even though we haven't described precisely how objects work yet, it is time to start thinking about data as objects now, because in Python every value is an object.

## 2.1.2 Native Data Types

Every object in Python has a *type*. The `type` function allows us to inspect the type of an object.

``` {.python}
type(today)
```
<html><div class="codeparent python"><pre class="stdout"><code><class 'datetime.date'></code></pre></div></html>

So far, the only kinds of objects we have studied are numbers, functions, Booleans, and now dates. We also briefly encountered sets and strings, but we will need to study those in more depth. There are many other kinds of objects --- sounds, images, locations, data connections, etc. --- most of which can be defined by the means of combination and abstraction that we develop in this chapter. Python has only a handful of primitive or *native* data types built into the language.

Native data types have the following properties:

1.  There are primitive expressions that evaluate to objects of these types, called *literals*.
2.  There are built-in functions, operators, and methods to manipulate these objects.

As we have seen, numbers are native; numeric literals evaluate to numbers, and mathematical operators manipulate number objects.

``` {.python}
12 + 3000000000000000000000000
```
<html><div class="codeparent python"><pre class="stdout"><code>3000000000000000000000012</code></pre></div></html>

In fact, Python includes three native numeric types: integers (`int`), real numbers (`float`), and complex numbers (`complex`).

``` {.python}
type(2)
```
<html><div class="codeparent python"><pre class="stdout"><code><class 'int'></code></pre></div></html>

``` {.python}
type(1.5)
```
<html><div class="codeparent python"><pre class="stdout"><code><class 'float'></code></pre></div></html>

``` {.python}
type(1+1j)
```
<html><div class="codeparent python"><pre class="stdout"><code><class 'complex'></code></pre></div></html>

The name `float` comes from the way in which real numbers are represented in Python: a "floating point" representation. While the details of how numbers are represented is not a topic for this course, some high-level differences between `int` and `float` objects are important to know. In particular, `int` objects can only represent integers, but they represent them exactly, without any approximation. On the other hand, `float` objects can represent a wide range of fractional numbers, but not all rational numbers are representable. Nonetheless, float objects are often used to represent real and rational numbers approximately, up to some number of significant figures.

**Further reading.** The following sections introduce more of Python's native data types, focusing on the role they play in creating useful data abstractions. A chapter on [native data types](http://diveintopython3.ep.io/native-datatypes.html) in Dive Into Python 3 gives a pragmatic overview of all Python's native data types and how to use them effectively, including numerous usage examples and practical tips. You needn't read that chapter now, but consider it a valuable reference.

