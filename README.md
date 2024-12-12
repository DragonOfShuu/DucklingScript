![DucklingScript Header](https://github.com/DragonOfShuu/DucklingScript/blob/main/git_docs/DucklingScriptHeader.png?raw=true)

![PyPI - Downloads](https://img.shields.io/pypi/dm/ducklingscript)

Welcome to DucklingScript, a language that compiles into Rubber Ducky Scripting Language 1.0! DucklingScript is the best language to use for BadUSB on the Flipper Zero. Although this is the main idea, there are many other applications as well!

All documentation, contributing guides, are found [here](https://ducklingscript.dragonofshuu.dev/docs/guides/why-ducklingscript)!

Issues and PR's are welcome!

# Documentation

We got you covered! Docs are hosted on a separate website found [here](https://ducklingscript.dragonofshuu.dev/docs/guides/why-ducklingscript)!

# VSCode Support

DucklingScript has a public VSCode extension that supports syntax highlighting. 

[DucklingScript VSCode Extension ->](https://marketplace.visualstudio.com/items?itemName=DragonofShuu.ducklingscript-language-support)

![DucklingScript VSCode Extension Screenshot](https://github.com/DragonOfShuu/DucklingScript/blob/main/git_docs/DucklingScriptExtension.png?raw=true)

# Why DucklingScript?

There are many key points to using DucklingScript, such as Type Safety, Flow Control, Syntactical Speed, and Forward Compatibility.

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
