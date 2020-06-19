from suite import suite

@suite
def suite_parenthesis(test):
    test("(echo bonjour)")
    test("(echo bonjour )")
    test("( echo bonjour )")

    test("(echo a && echo b) && echo c")
    test("(echo a || echo b) || echo c")
    test("(ls doesnotexist || echo b) || echo c")
    test("(echo a || ls doesnotexist) || echo c")
    test("echo aa && (echo b && echo c)")
    test("ls doesnotexist || (echo b && echo c)")

    test("(echo bonjour > f1)", files=["f1"])
    test("(echo bonjour > f1) > f2", files=["f1", "f2"])
    test("(cat -e > f1) < f2", setup="ls -l / > f2", files=["f1"])
