# Solution

This is Julia prompt and forbidden phrases are: `@`, `` ` ``, `eval`, `cmd`, `split`

But wi still can use:
`run(Cmd(convert(Vector{String}, command)))`

example solution:

`println(run(Cmd(convert(Vector{String}, ["ls", "-al"]))))`

`println(run(Cmd(convert(Vector{String}, ["ls", "..", "-al"]))))`

`println(run(Cmd(convert(Vector{String}, ["cat", "../.flag"]))))`
