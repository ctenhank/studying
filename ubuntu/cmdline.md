# Difference between `-`(single hyphen) and `--`(double hyphen)
It is simply that by convention.

`-` means that the following flags are single-character only, and generally means that more than one flag can be passed.
Example
```
ls -la
grep -inr "asd"
```

`--` means a single positional flag/argument(multiple character) to a command line tool.
Example
```
ls -all
```
