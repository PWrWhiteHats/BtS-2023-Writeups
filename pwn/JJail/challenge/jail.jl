function check_input(input)
    forbidden_words = ["@", "`", "eval", "cmd", "split"]
    for w in forbidden_words
        if occursin(w, input)
            return false
        end
    end
    return true
end

begin
    write(stdout, "Welcome to the JJail! Can you escape?\n")
    while true
        try
            input = readline(stdin, keep=true)
            if input == "" || input == nothing
                continue
            end
            if check_input(input)
                pipe = Pipe()
                writer = redirect_stdout(pipe) do
                    eval(Meta.parse(input))
                    close(Base.pipe_writer(pipe))
                end
                write(stdout, read(pipe, String) * "\n")
            else
                write(stdout, "Forbidden phrase found!\n")
            end
        catch e
            println(e)
        end
    end
end