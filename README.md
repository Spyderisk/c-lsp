# C LSP

This is an experiment to assemble a [Language Server Protocol]() (LSP) server from existing components, targeting a well-known
language.

To measure success we need to see each of the following steps work:

* Creating an incremental parser from a known-good grammar
* Incorporating this parser into an LSP server-creation tool
* Connecting this LSP to an editor
* Testing that while editing, we get well-formed and descriptive errors, progressively at the speed of typing
* Testing that while editing, the errors are correctly localised to blocks, lines or characters as appropriate
* Repeating the above for a second, dissimilar editor

Our experimental setup is:

* the C language as a target. It is small, statically typed and there are many known-good grammars available
* the [tree-sitter incremental parser tool]() to emit a parser in the C language with Python bindings
* [the pygls LSP library]() to construct an LSP server in Python
* the $editor editor with an LSP configuration

## How to build

## How to configure and run

## Features

- Marking areas which failed to parse
