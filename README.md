# timings
Yet another time logging utility...

## Why another one?
All those utilities I have found so far do not work the way I want. At least not exactly. 

Most of them were too much for me: I only want to create projects, start and stop working and see the summary. That's it.

I do not need any graphical evaluation and I do not want the SW to have more maintenance code than to add entries of work periods.

Instead I want to have a siiimple text file which can be manipulated easily.

And another reason: that should be fairly easy and fun to implement. Indeed, it was.

## How it works

Add a new project you want to bill time on:

```
$ timings add my-new-project
```

Start working on this project:

```
$ timings start my-new-project
```

When you are done:

```
$ timings stop my-new-project
```

That's it.

The result is stored in `~/.timings.txt`. After the above it look's like this:
```
{
    "my-new-project": [
        [
            "2019.02.25 17:07:00 .. 2019.02.25 19:45:22",
            158
        ]
    ]
}
```

BTW: The string is just a comment. In case it makes sense to you, you can replace it by any other string. Only the _int_ is used to sum up.
