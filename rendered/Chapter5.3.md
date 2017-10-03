
[[table-of-contents]]

# 5.3 Coroutines

Much of this text has focused on techniques for decomposing complex programs into small, modular components. When the logic for a function with complex behavior is divided into several self-contained steps that are themselves functions, these functions are called helper functions or *subroutines*. Subroutines are called by a main function that is responsible for coordinating the use of several subroutines.

![](img/subroutine.png)

In this section, we introduce a different way of decomposing complex computations using *coroutines*, an approach that is particularly applicable to the task of processing sequential data. Like a subroutine, a coroutine computes a single step of a complex computation. However, when using coroutines, there is no main function to coordinate results. Instead coroutines themselves link together to form a pipeline. There may be a coroutine for consuming the incoming data and sending it to other coroutines. There may be coroutines that each do simple processing steps on data sent to them, and there may finally be another coroutine that outputs a final result.

![](img/coroutine.png)

The difference between coroutines and subroutines is conceptual: subroutines slot into an overarching function to which they are subordinate, whereas coroutines are all colleagues, they cooperate to form a pipeline without any supervising function responsible for calling them in a particular order.

In this section, we will learn how Python supports building coroutines with the `yield` and `send()` statements. Then, we will look at different roles that coroutines can play in a pipeline, and how coroutines can support multitasking.

## 5.3.1 Python Coroutines

In the previous section, we introduced generator functions, which use `yield` to return values. Python generator functions can also consume values using a `(yield)` statement. In addition two new methods on generator objects, `send()` and `close()`, create a framework for objects that *consume* and produce values. Generator functions that define these objects are coroutines.

Coroutines consume values using a `(yield)` statement as follows:

```
value = (yield)
```

With this syntax, execution pauses at this statement until the object's `send` method is invoked with an argument:

```
coroutine.send(data)
```

Then, execution resumes, with `value` being assigned to the value of `data`. To signal the end of a computation, we shut down a coroutine using the `close()` method. This raises a `GeneratorExit` exception inside the coroutine, which we can catch with a `try/except` clause.

The example below illustrates these concepts. It is a coroutine that prints strings that match a provided pattern.

``` {.python}
def match(pattern):
    print('Looking for ' + pattern)
    try:
        while True:
            s = (yield)
            if pattern in s:
                print(s)
    except GeneratorExit:
        print("=== Done ===")
```

We initialize it with a pattern, and call `__next__()` to start execution:

``` {.python}
m = match("Jabberwock")
m.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Looking for Jabberwock</code></pre></div></html>

The call to `__next__()` causes the body of the function to be executed, so the line "Looking for jabberwock" gets printed out. Execution continues until the statement `line = (yield)` is encountered. Then, execution pauses, and waits for a value to be sent to `m`. We can send values to it using `send`.

``` {.python}
m.send("the Jabberwock with eyes of flame")
```
<html><div class="codeparent python"><pre class="stdout"><code>the Jabberwock with eyes of flame</code></pre></div></html>

``` {.python}
m.send("came whiffling through the tulgey wood")
m.send("and burbled as it came")
m.close()
```
<html><div class="codeparent python"><pre class="stdout"><code>=== Done ===</code></pre></div></html>

When we call `m.send` with a value, evaluation resumes inside the coroutine `m` at the statement `line = (yield)`, where the sent value is assigned to the variable `line`. Evaluation continues inside `m`, printing out the line if it matches, going through the loop until it encounters `line = (yield)` again. Then, evaluation pauses inside `m` and resumes where `m.send` was called.

We can chain functions that `send()` and functions that `yield` together achieve complex behaviors. For example, the function below splits a string named `text` into words and sends each word to another coroutine.

``` {.python}
def read(text, next_coroutine):
    for line in text.split():
        next_coroutine.send(line)
    next_coroutine.close()
```

Each word is sent to the coroutine bound to `next_coroutine`, causing `next_coroutine` to start executing, and this function to pause and wait. It waits until `next_coroutine` pauses, at which point the function resumes by sending the next word or completing.

If we chain this function together with `match` defined above, we can create a program that prints out only the words that match a particular word.

``` {.python}
text = 'Commending spending is offending to people pending lending!'
matcher = match('ending')
matcher.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Looking for ending</code></pre></div></html>

``` {.python}
read(text, matcher)
```
<html><div class="codeparent python"><pre class="stdout"><code>Commending
spending
offending
pending
lending!
=== Done ===
</code></pre></div></html>

The `read` function sends each word to the coroutine `matcher`, which prints out any input that matches its `pattern`. Within the `matcher` coroutine, the line `s = (yield)` waits for each sent word, and it transfers control back to `read` when it is reached.

![](img/read-match-coroutine.png)

## 5.3.2 Produce, Filter, and Consume

Coroutines can have different roles depending on how they use `yield` and `send()`:

![](img/produce-filter-consume.png)

-   A **Producer** creates items in a series and uses send(), but not `(yield)`
-   A **Filter** uses `(yield)` to consume items and `send()` to send result to a next step.
-   A **Consumer** uses `(yield)` to consume items, but does not send.

The function `read` above is an example of a *producer*. It does not use `(yield)`, but uses `send` to produce data items. The function `match` is an example of a consumer. It does not `send` anything, but consumes data with `(yield)`.We can break up `match` into a filter and a consumer. The filter would be a coroutine that only sends on strings that match its pattern.

``` {.python}
def match_filter(pattern, next_coroutine):
    print('Looking for ' + pattern)
    try:
        while True:
            s = (yield)
            if pattern in s:
                next_coroutine.send(s)
    except GeneratorExit:
        next_coroutine.close()
```

And the consumer would be a function that printed out lines sent to it.

``` {.python}
def print_consumer():
    print('Preparing to print')
    try:
        while True:
            line = (yield)
            print(line)
    except GeneratorExit:
        print("=== Done ===")
```

When a filter or consumer is constructed, its `__next__` method must be invoked to start its execution.

``` {.python}
printer = print_consumer()
printer.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Preparing to print</code></pre></div></html>

``` {.python}
matcher = match_filter('pend', printer)
matcher.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Looking for pend</code></pre></div></html>

``` {.python}
read(text, matcher)
```
<html><div class="codeparent python"><pre class="stdout"><code>spending
pending
=== Done ===
</code></pre></div></html>

Even though the name *filter* implies removing items, filters can transform items as well. The function below is an example of a filter that transforms items. It consumes strings and sends along a dictionary of the number of times different letters occur in the string.

``` {.python}
def count_letters(next_coroutine):
    try:
        while True:
            s = (yield)
            counts = {letter:s.count(letter) for letter in set(s)}
            next_coroutine.send(counts)
    except GeneratorExit as e:
        next_coroutine.close()
```

We can use it to count the most frequently-used letters in text using a consumer that adds up dictionaries and finds the most frequent key.

``` {.python}
def sum_dictionaries():
    total = {}
    try:
        while True:
            counts = (yield)
            for letter, count in counts.items():
                total[letter] = count + total.get(letter, 0)
    except GeneratorExit:
        max_letter = max(total.items(), key=lambda t: t[1])[0]
        print("Most frequent letter: " + max_letter)
```

To run this pipeline on a file, we must first read the lines of a file one-by-one. Then, we send the results through `count_letters` and finally to `sum_dictionaries`. We can re-use the `read` coroutine to read the lines of a file.

``` {.python}
s = sum_dictionaries()
s.__next__()
c = count_letters(s)
c.__next__()
read(text, c)
```
<html><div class="codeparent python"><pre class="stdout"><code>Most frequent letter: n</code></pre></div></html>

## 5.3.3 Multitasking

A producer or filter does not have to be restricted to just one next step. It can have multiple coroutines downstream of it, and `send()` data to all of them. For example, here is a version of `read` that sends the words in a string to multiple next steps.

``` {.python}
def read_to_many(text, coroutines):
    for word in text.split():
        for coroutine in coroutines:
            coroutine.send(word)
    for coroutine in coroutines:
        coroutine.close()
```

We can use it to examine the same text for multiple words:

``` {.python}
m = match("mend")
m.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Looking for mend</code></pre></div></html>

``` {.python}
p = match("pe")
p.__next__()
```
<html><div class="codeparent python"><pre class="stdout"><code>Looking for pe</code></pre></div></html>

``` {.python}
read_to_many(text, [m, p])
```
<html><div class="codeparent python"><pre class="stdout"><code>Commending
spending
people
pending
=== Done ===
=== Done ===
</code></pre></div></html>

First, `read_to_many` calls `send(word)` on `m`. The coroutine, which is waiting at `text = (yield)` runs through its loop, prints out a match if found, and resumes waiting for the next `send`. Execution then returns to `read_to_many`, which proceeds to send the same line to `p`. Thus, the words of `text` are printed in order.
