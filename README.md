# Building FastAPI web apps
> A journal of random stuff I got in touch with while implementing a couple of FastAPI web apps

## Next

~~1. Think about the data model for the dizziness tracker.~~
1. Create a fake data layer simulating what a db would do.

    Start with the Journal Entry and and LevelSymptoms, we'll get to episode identification afterwards.

1. Replicate the examples for moviedb
1. Create a FastAPI guide - do not copy code, but link to examples instead.
1. Review docs
1. Commit and go to next chapter


## Tooling

For this project I've decided to give a try to the the [Astral](https://github.com/astral-sh) tooling.

This means:

+ I've installed `uv` for project and tool management.
+ I'm using `ruff` as the linter and formatter.

I installed `ruff` as a tool managed by `uv` so that it shows when you do:

```bash
$ uv tool list
```

Also, you can easily upgrade `ruff` doing:

```bash
$ uv tool upgrade ruff
```


The `ruff` configuration for VSCode is a bit tricky.

Apart from installing the extension and modifying the settings.json as recommended in the extension README.md, I removed all references to pylint, black, pycodestyle.

Then I had to disable the corresponding pylint and black extensions.

Then I prepared the configuration for ruff on the `pyproject.toml`. As I am no Python expert I don't have an opinion on the rules that I should be enabling, and therefore, I've decided to enable them all, and then disable the ones that don't look right for my projects.

You can see all the available rules in: https://docs.astral.sh/ruff/rules/


`uv` configuration was much simpler, just install it and it works.

Then you can add the FastAPI library by typing:

```bash
uv add fastapi --extra standard
```
