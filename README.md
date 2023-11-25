![DucklingScript Header](git_docs/DucklingScriptHeader.png)

<!-- # DUCKLINGSCRIPT -->
![GitHub search hit counter](https://img.shields.io/github/search/DragonOfShuu/DucklingScript/flat)
![GitHub all releases](https://img.shields.io/github/downloads/DragonOfShuu/DucklingScript/total)



Welcome to DucklingScript, a language that compiles into Rubber Ducky Scripting Language 1.0! DucklingScript is the best language to use for BadUSB on the Flipper Zero. Although this is the main idea, there are many other applications as well!

# Why DucklingScript?

There are many key points to using DucklingScript. Here are some of those now.

## Type Safety

Because DucklingScript has to go through a compilation process, it means DucklingScript can validate your script will work on your hardware. It will tell you that there is an error, and it will tell you exactly where. For example, CTRL requires one character. DucklingScript will validate that this is true.

## Flow Control

Rubber Ducky Scripting Language 1.0 and even the Flipper's implementation don't add any kind of flow control. e.g. if statements, while/for loops, etc. DucklingScript gives you those capabilities, and more!

## Syntactical Speed

Normal Rubber Ducky Scripting 1.0 doesn't give much room for speed, and oftentimes leads you to repeating yourself in code. Not only does DucklingScript add commands to improve this, it also makes small syntactical changes. Such as:

Rubber Ducky 1.0
```
STRINGLN Hello,
STRINGLN world,
STRINGLN it is I!
```
DucklingScript
```
STRINGLN 
    Hello,
    world,
    it is I!
```

## Forward Compatibility

If you use a command that does not exist in Rubber Ducky 1.0, DucklingScript will simply warn you that this is the case (these warnings can even be supressed using a flag on compilation, or editing the config file). However, it does not stop you from doing so. This allows you to use future commands!

# Language Basics

First off, DucklingScript allows for all syntax of [Rubber Ducky Scripting Language 1.0](https://web.archive.org/web/20220816200129/http://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript), as well as the [Flipper Zero's BadUsb ducky extension](https://docs.flipper.net/bad-usb).

> Note on Flipper Compatibility
> --
> If you are not using a device that can parse flipper commands, then you cannot use them. Please make sure to disable flipper commands if this is the case through the config file.

# DucklingScript: "Crash Course"

First, make sure to check the [Language Basics](#language-basics), and look through the documentation there to learn Rubber Ducky 1.0 and the Flipper commands.

## File Creation

DucklingScript files use the `.txt` file extension. This will be important for when we import external files later.

## Simple Commands

Simple commands can be characterized by a command that is a command and no argument, or a command with arguments, and no trailing code blocks. All Rubber Ducky 1.0 and Flipper Commands are Simple Commands.

However, in DucklingScript they have extended syntax.

### Command Skip

Using indentation, you don't have to repeat yourself. You can simply make an indentation after the command, and write all arguments for the command. This may seem a bit confusing, so here's an example:

DucklingScript
```
STRING 
    Hello World!
    I enjoy DucklingScript!
```
Compiles into:
```bash
STRING Hello World!
STRING I enjoy DucklingScript!
```

This is a powerful feature, allowing you to type out everything you need all at once, instead of repeatedly typing `STRING`.

However, if you start using indents inside of those indents, you might encounter an error. You may need these extra indents if you are for example having your injection device write code. In that case, simply use three quotation marks like so:

```
STRINGLN
    """
    print("Starting Hacking Software...")
    for i in range(10):
        print(f"Hacking your pc in {i} second(s)")
        if i < 4:
            print("This is your final warning!")
    """
```

### Dollar Sign Operator

All simple commands that don't already evaluate their arguments can use the dollar sign operator. This turns the argument into an expression that can be evaluated.

This allows you to write mathematical expressions, or use variables.

> Note
> --
> All Strings when using the dollar sign operator are
> required to be incased in quotations like this:
> "Hello World"

### Examples

DucklingScript:
```
$CTRL 1+1
```
Compiled:
```bash
CTRL 2
```

DucklingScript:
```
$STRING "Hello " + "world!"
```
Compiled:
```bash
STRING Hello world!
```

This becomes more relevant and more important when we introduce variables.

## Block Commands

All Block commands will be commands that require an argument, and then a code block after. As of writing, all block commands are added by DucklingScript.

### Examples

DucklingScript
```
REM Command with arg
REPEAT 10
    REM Command's code block
    STRING foo
    STRING bar
```

*More info on REPEAT [here](#for-loops)

## Data Typles, Variables and Functions

### Data Types

A string is a data type containing characters. It must be wrapped in quotation marks.
```
"Hello World"
```

A number is a data type containing, well, a number
```
100
```
A boolean is either a TRUE or FALSE value. When using these keywords in DucklingScript, make sure to keep them as all caps.
```
TRUE
FALSE
```

### Variables
A variable can be understood as a sort of "drawer" that has a label, and contains some form of data of specific type (either a string, number, or a boolean)

### Examples
```
VAR counter 0
REM a variable named "counter" now equals 0
```

```
VAR switch TRUE
REM a variable named "switch" is now TRUE
REM (Make sure that TRUE is in all caps)
```

### Functions

Functions allow you to run the same piece of code as many times as you want, where ever you want, plus the ability to control the variables inside.

To make a function, use the command named either `FUNC` or `FUNCTION`. After that, give the name, then following the name include all variable names separated by a comma.

To run a function, use the `RUN` command, followed by the name of the function to run, and then the value for all variables separated by comma in order as they were declared on function creation.

DucklingScript
```
FUNC hello
    STRING Hello World!

RUN hello
STRING In the middle
RUN hello
```
Compiled
```
STRING Hello World!
STRING In the middle
STRING Hello World!
```

DucklingScript
```
FUNC hello phrase,number
    $STRING "The number given was: "+number
    $STRING phrase

RUN hello "Foo/Bar",10
```
Compiled
```
STRING The number given was: 10
STRING Foo/Bar
```

It is also possible to leave a function early if you wish. Using the `RETURN` command, you can exit a function early.

DucklingScript
```
FUNC hello 
    STRING Hello!
    RETURN
    REM This does not run.
    STRING Goodbye!

RUN hello
```
Compiled
```
STRING Hello!
```

> ## Note
> The return command can also be used outside of a function to exit
> out of your program early

## Flow Control

These are commands that manage how your injection is ran. These are conditionals and loops.

### Conditional Statements

Conditional Statements allow you to run code, only if a certain condition is met. In DucklingScript, we use the commands `IF`, `ELIF`, and `ELSE` to evaluate conditionals.

`ELIF` can only come after an `IF`, and `ELSE` can only come after an `ELIF` or `IF`. If any `IF` or `ELIF` are true, then all subsequent `ELIF`s and `ELSE`s are ignored. After that, you can create a new `IF` statement by using the `IF` command once again.

### Examples

DucklingScript
```
VAR a 10

REM if a is equal to 10
IF a == 10
    REM this code is ran
    STRINGLN Hello World

REM if a is not equal to 10
ELSE 
    STRINGLN Hello World Not Found :/
```

Compiled
```
STRINGLN Hello World
```

DucklingScript
```
VAR a 10

IF a > 10
    STRING a is greater than 10
ELIF a < 10
    STRING a is less than 10
ELSE
    STRING a is 10
```

Compiled
```
STRING a is 10
```

### For Loops

Rubber Ducky 1.0 actually includes a sort of "for" loop already. To do this, write `REPEAT` (DucklingScript also accepts `FOR`, and it does the same things) directly after the command you want to repeat. 

Please note that although possible in DucklingScript, DucklingScript does not support the ability to check if you have compiled code BEFORE the repeat statement, and therefore cannot fix any syntax issues in doing so.

DucklingScript/Rubber Ducky 1.0
```
STRINGLN Hello World!
REPEAT 4
```

End Result
```
STRINGLN Hello World!
STRINGLN Hello World!
STRINGLN Hello World!
STRINGLN Hello World!
```

This is great, but unfortunately this will only work for one line of code. DucklingScript resolves this by including added syntax using indentation!

DucklingScript
```
REPEAT 3
    STRING Not only can I repeat...
    STRING ...but so can I!
```

Compiled
```
STRING Not only can I repeat...
STRING ...but so can I!
STRING Not only can I repeat...
STRING ...but so can I!
STRING Not only can I repeat...
STRING ...but so can I!
```

Not only that, but DucklingScript also includes the ability to count the amount of repeats that have occurred in a variable!

Please note that the first iteration is considered to be `0`.

The syntax for this is: `<variable name>, <iteration count>`.

DucklingScript
```
REPEAT i,3
    $STRING "this is iteration number "+i+"!" 
```
Compiled
```
STRING this is iteration number 0!
STRING this is iteration number 1!
STRING this is iteration number 2!
```

### While Loops

While loops are loops that continue to loop whilst a condition is true. 

> Note
> --
> Please note that there is a limit to while loops; while loops will eventually error if they run too many times.

DucklingScript
```
VAR a 10
WHILE a!=15
    VAR a a+1
    $STRING a
```
Compiled
```
STRING 11
STRING 12
STRING 13
STRING 14
STRING 15
```

DucklingScript
```
VAR a ""
WHILE a!="eee":
    VAR a a+"e"
    $STRING a
```
Compiled
```
STRING e
STRING ee
STRING eee
```

Just like the for loop, the while loop also allows you to implement a variable that stores the number of iterations completed.

DucklingScript
```
VAR a ""
WHILE count,a!="eee"
    VAR a a+"e"
    $STRING a + " [iteration: "+count+"]" 
```
Compiled
```
STRING e [iteration: 0]
STRING ee [iteration: 1]
STRING eee [iteration: 2]
```

### Loop Controls

DucklingScript offers to additional commands to assist with loop usage. These two commands help extend the usage of both kinds of loops.

#### BREAKLOOP

`BREAKLOOP`/`BREAK_LOOP` allows you to *break out* of a loop. This is especially useful if under a certain circumstance you need to leave a loop early.

DucklingScript
```
REPEAT i,10
    $STRING "iteration "+i
    IF i==2
        BREAKLOOP
```
Compiled
```
STRING iteration 0
STRING iteration 1
STRING iteration 2
```

As you can see, we left the while loop early because `i` was equal to two.

#### CONTINUELOOP

`CONTINUELOOP`/`CONTINUE_LOOP`/`CONTINUE` allows you to *continue* through the loop.

DucklingScript
```
REPEAT i,5
    IF i==3
        CONTINUELOOP
    $STRING "I like the number "+i+"!" 
```
Compiled
```
STRING I like the number 0!
STRING I like the number 1!
STRING I like the number 2!
STRING I like the number 4!
```

As you can see, the number 3 is missing from the compiled, because `CONTINUE` continued the loop, ignoring the resulting code after it.

## Multi-File Projects

DuckingScript supports multi-file projects using the `START`, `STARTENV`, `STARTCODE` commands.

All `START` commands start with the same general syntax, and they allow you to compile the code from another file into the output file. For this to work however, make sure to use the `.txt` extension on all files.

To start another file, simply use the `START` command, and for the argument put the file name. As long as both files are in the same folder, this will work flawlessly.

File Structure
```
Project
|-main.txt
|-startme.txt
```
DucklingScript - startme.txt
```
STRING "startme" says hello!
```
DucklingScript - main.txt
```
START startme
STRING ran startme file.
```
Compiled
```
STRING "startme" says hello!
STRING ran startme file.
```

This is great and all, but would if you want to access a file that is inside a folder? Or maybe the file is one level up. In this case comes the dot operator. To go inside a folder, give the name of the folder, then put a dot after. After that dot put the name of the file.

Similarly, if you want to go a level up, put a dot at the very beginning of the argument.

File Structure
```
Project
|-above.txt
|-middle
  |-main.txt
  |-below
    |-below.txt
```
DucklingScript - above.txt
```
STRING Hello from above!
```
DucklingScript - below.txt
```
STRING Hello from below!
```
DucklingScript - main.txt
```
REM Using the dot operator at the beginning, we can go up a folder
REM Using the dot operator in the middle allows use to go into a folder
START
    .above
    below.below
```
Compiled
```
STRING Hello from above!
STRING Hello from below!
```

## Debugging Commands

Because DucklingScript ramps up the complexity of your programs, discovering exactly what is happening might become difficult. This is why DucklingScript adds more commands for debugging!

First is `PRINT`, which allows you to send text to the console when you ocmpile your injection.

DucklingScript
```
PRINT Hello World!
```
Console output
```
--> Captured STD:OUT
example.txt - 1 > Hello World!
---
```

The next one is `NOTEXIST`/`NOT_EXIST`, which allows you to raise an error if the given variable exists.

DucklingScript
```
VAR a "hello world"
NOTEXIST a
```
Compiled
```
---
In file 'X:\test.txt', on line 2
> NOTEXIST a
GeneralError: 'a' does exist.
---
```

The next up is the opposite of `NOTEXIST`, which is `EXIST`. This raises an error if the given variable doesn't exist.

DucklingScript
```
EXIST a
```
Compiled
```
---
In file 'X:\test.txt', on line 1
> EXIST a
GeneralError: 'a' does not exist.
---
```

Finally, we have `PASS`, which allows you to fill in the block space for a block command without actually doing anything. Although a comment works too, `PASS` is cleaner, and allows you to find what hasn't been completed yet in a language specific way.

DucklingScript
```
FUNC a
    PASS
```

## Expression Evaluation

DucklingScript allows mathematical/logical/conditional expressions. Assuming you already have a basic understanding of 'normal' programming, you should understand ***most*** of this already.

### Mathematics

DucklingScript will follow the rules of PEMDAS (please note that addition/subtraction, and multiplication/division are evaluated left to right. However, multiplation/division is evaluated before addition/subtraction).

Here are all of the operators that DucklingScript accepts:

Exponents:
```
10^2
```
Result is 100

Addition/subtraction
```
5+5
5-5
```
Result is 10, and 0

Multiplication/division
```
5*5
5/5
```
Result is 25, and 1

Floor Division
```
3//2
```
Result is 1 (the decimal is essentially truncated, meaning removed)

