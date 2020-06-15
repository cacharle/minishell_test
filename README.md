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

The reasons for this is are:
1. we're free to set the prompt to whatever we want
2. termcaps would be a nightmare to test

## Run

`> ./test.sh`

# Configuration

The default configuration can be changed in the `minishell\_test.config` file.
