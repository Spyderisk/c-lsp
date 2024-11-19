# Investigating a Tree-sitter based LSP

# Purpose

Spyderisk v2 likely has a need to be able to parse and perform analysis on arbitrary formal languages, particularly Domain
Specific Languages (DSLs). The DSLs might be a rule-based modelling language extended to know about ontologies, or N3 with more
capable branching logic, or something else again such as a derivative of Algebraeic Julia.

The potential use cases are at least:

* Validating and/or compiling our own Domain Specific Languages for rule-based modelling as part of model development
  workflow as well as for production modelling.

* An editor. We have written multiple editors over the years to handle our ontology-plus-more domain modelling language, 
  without lasting success. While perhaps we can return again to the idea of using something like Protégé, at the moment we are trying 
  out the concept of a [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) server for use with
  any LSP-compliant editor. And even if we did use Protégé, we might still need a
  [custom plugin](https://protegewiki.stanford.edu/wiki/Protege_Plugin_Library), which again will need
  some detailed knowledge of the language.

This investigation focusses on the second option, while doing a lot of work that is relevant to the first.

# Architectural view

## About Tree-Sitter

[Tree-sitter](https://tree-sitter.github.io/tree-sitter/) generates parsers for any language, given a grammar. Tree-sitter
parsers are emitted in C, and are very fast, incremental and fault-tolerant. Tree-sitter comes with grammars for [nearly 500
languages](https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers). Tree-sitter parsers are intended for use in
language editors and IDEs, where it is common for there to be many errors that change rapidly. A Tree-sitter parser can be 
called with every keystroke a developer types, with only the changes to the tree being parsed (incremental) and parsing
able to continue after many classes of error (fault-tolerant).

Many editors support tree-sitter directly to do things like keyword colouring and highlighting parse errors. But we want our
editors to have knowledge of the target language at a higher level, for example syntax highlighting. Syntax highlighting
requires a knowledge of scope, which the tree-sitter Abstract Syntax Tree (AST) does not have. Therefore, we investigated how
possible it would be to have an LSP that uses tree-sitter as its parser.

## About editors and LSP

- Most major editors support some form of LSP, however it seems limited to two types:
  - Large editors (e.g. VSCode, Eclipse, GUI-type editors) have difficult support for the maintainter, often requiring some form of plugin to be written, but end users have the simplest experience
  - Minimal (or non-GUI) editors (e.g. Nvim, Emacs) usually require heavy configuration from the end user to add support, and the editors are often less accessible, being more opinionated or difficult to use
- For development a environment with a minimal editor makes sense
- Unit testing tools exist for tree sitter and LSP
  - <https://pypi.org/project/pytest-lsp/>
- Debugging tools for LSP also exist
  - <https://lsp-devtools.readthedocs.io/en/latest/lsp-devtools/guide/getting-started.html>

# Tools used in this research

## NeoVim

- Neovim (A modern Vim-based editor, Vim being a fork of Vi) has good support for LSP, along with nice debugging tools
- Neovim LSPs are configured using a Lua based config system
  - Nvim has a core way to configure these, but most seem to use this abstraction library <https://github.com/neovim/nvim-lspconfig>. It also contains example configs for many common LSPs.
  - This has a dependency on LuaRocks, which I need to install

## lsp-tree-sitter
- Thought we could use this
[python library for building tree-sitter LSPs](https://lsp-tree-sitter.readthedocs.io/en/latest/)
to do most of the work
- was developed for simple Domain Specific Languages (DSLs)
- seems only applicable to configuration/serialization languages (JSON, TOML etc)
- we abandoned lsp-tree-sitter

## PYTHON-LSP insert-details-here XXX

- detail 1
- detail 2

# Technical details of tree-sitter

Since tree-sitter is the most significant part of our investigation we need to know what it does and does not do.

- Tree sitter is very useful for parsing our language, however it is not very smart.
  - No concept of scope, symbols etc.
  - See the online [tree-sitter playground](https://tree-sitter.github.io/tree-sitter/playground) to get a sense of what it can do
- For our lsp to implement "Smart" features, it requires additional knowledge about the language embedded within. This is
  something we need to code ourselves.
- We can implement basic features generic of our grammar, but a generic smart lsp is not possible with tree-sitter
  - Syntax errors can be implemented generically by taking errored tokens, and (in theory) using the grammar at runtime to find what could be there in place of the errored token
  - ```c
    // For example:
    #include <stdio.h>

    int main { // Fails after "main", so we can then infer that we need parenthesis and arguments afterwards
        printf("Hello world!\n");
        return 0;
    }
    ```
- We shall call the difference "grammar" and "language" level

# Features we are looking for in the editor

## Smart Completions/Missing Symbols
- This must be implemented at the language level
- We need to keep track of scope and known symbols, along maybe filtering results based on types (requires deep language level knowledge, such as parsing entire languages and projects)

## Semantic highlighting (Code colouring)

- Useful document talking about useful semantic highlighting, and how to design it <https://gist.github.com/swarn/fb37d9eefe1bc616c2a7e476c0bc0316>
- This is very different from tree-sitter based colouring, however it requires language level understanding of scope, symbols etc.
- Example of good highlighting, based off symbol scope, modifiers etc
  ![highlighting scopes](https://i.imgur.com/Gp1l2ZZ.png)

## Code lens (hover info)

- Requires language level implementation

## Debugging

- An idea was to implement some form of debugging for use with Kappa, our eventual target language.
- This would XXX

# Technical details of the LSP

- As of LSP version X.Y, all/some/XXX of the features we need are part of the protocol
- Not all implementations support all features
- At the LSP level, the features we need are: XXX, XXX, XXX
- XXX



