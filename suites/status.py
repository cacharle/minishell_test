from suite import suite

@suite
def suite_status(test):
    test("echo $?")
    test("echo; echo $?")
    test("notfound; echo $?")
    test("cat < doesntexist; echo $?")
    test("cat < noperm; echo $?", setup="echo bonjour > noperm; chmod 000 noperm")
    test("(ls && ls) && echo $?")

    test("echo")
    test("notfound")
    test("cat < doesntexist")
    test("cat < noperm", setup="echo bonjour > noperm; chmod 000 noperm")
    test("(ls && ls)")
    test("(ls doesntexist || ls)")
    test("(ls doesntexist && ls)")
