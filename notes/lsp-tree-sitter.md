# Investigating a Tree-sitter based LSP

[Tree-sitter](https://tree-sitter.github.io/tree-sitter/)
is a very fast, incremental parser that can do error recovery. It supports
[nearly 500 languages](https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers),
and is intended for use in language editors and IDEs.
We wanted to learn how feasible it is to have an LSP with tree-sitter behind it,
rather than the editor/IDE supporting tree-sitter directly (which many editors also do.)
This is interesting because LSP adds many higher-level features in a standard way,
such as syntax highlighting.


## Research

### lsp-tree-sitter
- Thought we could use this
[python library for building tree-sitter LSPs](https://lsp-tree-sitter.readthedocs.io/en/latest/)
to do most of the work
- was developed for simple Domain Specific Languages (DSLs)
- seems only applicable to configuration/serialization languages (JSON, TOML etc)

## Implementation

### Ecosystem

- Most major editors support some form of LSP, however it seems limited to two types:
  - Large editors (e.g. VSCode, Eclipse, GUI-type editors) have difficult support for the maintainter, often requiring some form of plugin to be written, but end users have the simplest experience
  - Minimal editors (e.g. Nvim, Emacs) usually require heavy configuration from the end user to add support, and the editors are often less accessible, being more opinionated or difficult to use
- For development a environment with a minimal editor makes sense
- Unit testing tools exist for tree sitter and LSP
  - <https://pypi.org/project/pytest-lsp/>
- Debugging tools for LSP also exist
  - <https://lsp-devtools.readthedocs.io/en/latest/lsp-devtools/guide/getting-started.html>

### Tree Sitter

- Tree sitter is very useful for parsing our language, however it is not very smart.
  - No concept of scope, symbols etc
    [tree-sitter playground](https://tree-sitter.github.io/tree-sitter/playground)
- For our lsp to implement "Smart" features, it requires additional knowledge about the language embedded within.
- We can implement basic features generic of our grammar, but a generic smart lsp is not possible
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

### Features

#### Smart Completions/Missing Symbols
- This must be implemented at the language level
- We need to keep track of scope and known symbols, along maybe filtering results based on types (requires deep language level knowledge, such as parsing entire languages and projects)

#### Semantic highlighting (Code colouring)

- Useful document talking about useful semantic highlighting, and how to design it <https://gist.github.com/swarn/fb37d9eefe1bc616c2a7e476c0bc0316>
- This is very different from tree-sitter based colouring, however it requires language level understanding of scope, symbols etc.
- Example of good highlighting, based off symbol scope, modifiers etc
  ![highlighting scopes](https://i.imgur.com/Gp1l2ZZ.png)

#### Code lens (hover info)

- Requires language level implementation

#### Debugging

- An idea was to implement some form of debugging for use with Kappa, our eventual target language.
- This would 
