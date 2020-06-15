# minishell test

Test for the minishell project of school 42.

# Usage

## Test compatibility

Your executable **must** support the `-c` option which allow to pass command as string.

example:

```
> bash -c 'echo bonjour je suis'
bonjour je suis
> ./minishell -c 'echo bonjour je suis'
bonjour je suis

> bash -c 'ls'
README.md test.sh
> ./minishell -c 'ls'
README.md test.sh
```

The reasons for this:
1. You're free to set the prompt to whatever you want
2. Termcaps would be a nightmare to test

## Run

`> ./main.py`

# Configuration

The default configuration can be changed in <config.py>
