# minishell\_test

[![PyPI - Python Version](https://img.shields.io/pypi/v/minishell-test)](https://pypi.org/project/minishell-test/)
[![Documentation](https://readthedocs.org/projects/minishell-test/badge/?version=latest)](https://minishell-test.readthedocs.io)
[![Build Status](https://api.travis-ci.com/cacharle/minishell_test.svg?branch=master)](https://travis-ci.com/cacharle/minishell_test)

![preview](https://i.imgur.com/98xh2xY.gif)

## Documentation

The full documentation for this project is available at
[minishell-test.readthedocs.io](https://minishell-test.readthedocs.io).

## Getting Started

### Installation

``` 
$ pip3 install minishell-test
$ pip3 install --user minishell-test  # if you don't have root access
```

### Compatibility

Your executable **must** support the `-c` option which allow to pass
command as an argument.

``` 
$ bash -c 'echo bonjour je suis | cat -e'
bonjour je suis$
$ ./minishell -c 'echo bonjour je suis | cat -e'
bonjour je suis$
```

<div class="note">

<div class="title">


</div>

With this setup `argv[2]` is what you would usually get in `line` from
`get_next_line`.

</div>

### Usage

Run all the predefined tests:

``` 
$ cd <MINISHELL>
$ minishell_test
```

<div class="warning">

<div class="title">


</div>

If you get `command not found`, do either of those things:

-   Add `~/.local/bin` to your `PATH` environment variable.
-   Run `$ python3 -m minishell_test` instead of `$ minishell_test`

</div>
