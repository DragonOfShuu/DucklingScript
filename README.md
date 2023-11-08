# DUCKLINGSCRIPT

Welcome to ducklingscript, a language that compiles into Rubber Ducky Scripting Language 1.0! The main idea is to use this language with the Flipper Zero, however it may have other applications if necessary.

# Benefits to DucklingScript

There are many key points to using DucklingScript. Here are some key points.

## Type Safety

Because DucklingScript has to go through a compilation process, it means DucklingScript can validate your script will work on your hardware. It will tell you that there is an error, and it will tell you exactly where. For example, CTRL requires one character. DucklingScript will validate that this is true.

## Flow Control

Rubber Ducky Scripting Language 1.0 and even the Flipper's implementation don't add any kind of flow control. e.g. if statements, while/for loops, etc. DucklingScript gives you those capabilities, and more!

## Syntactical Speed

Normal Rubber Ducky Scripting 1.0 doesn't give much room for speed, and oftentimes leads you to repeating yourself in code. Not only does DucklingScript add commands to improve this, it also makes small syntactical changes. Such as:

### Rubber Ducky 1.0
```
STRINGLN Hello,
STRINGLN world,
STRINGLN it is I!
```
### DucklingScript
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
```
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

