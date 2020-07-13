import config
from suite import suite

@suite
def suite_quote(test):
    test("'echo' 'bonjour'")
    test("'echo' 'je' 'suis' 'charles'")

    test('"echo" "bonjour"')
    test('"echo" "je" "suis" "charles"')

    test('echo je\'suis\'"charles"')
    test('echo "je"suis\'charles\'')
    test('echo \'je\'"suis"charles')

    test('echo "\\""')
    test('echo "\\$"')
    test('echo "\\\\"')

    test('ls ""')
    test("ls ''")

    test('ls "" "" "" \'\' """"')
    test("ls '' '' '''' ''")

@suite
def suite_interpolation(test):
    test("echo $TEST", exports={"TEST": "bonjour"})
    test("echo $TES", exports={"TEST": "bonjour"})
    test("echo $TEST_", exports={"TEST": "bonjour"})

    test('echo "|$TEST|"', exports={"TEST": "bonjour"})
    test('echo "|$TES|"', exports={"TEST": "bonjour"})
    test('echo "|$TEST_|"', exports={"TEST": "bonjour"})

    test("echo '|$TEST|'", exports={"TEST": "bonjour"})
    test("echo '|$TES|'", exports={"TEST": "bonjour"})
    test("echo '|$TEST_|'", exports={"TEST": "bonjour"})

    test("echo $A$B$C", exports={"A": "foo", "B": "bar", "C": "baz"})
    test('echo "$A$B$C"', exports={"A": "foo", "B": "bar", "C": "baz"})
    test("echo '$A$B$C'", exports={"A": "foo", "B": "bar", "C": "baz"})

    test("echo $A,$B,$C", exports={"A": "foo", "B": "bar", "C": "baz"})
    test('echo "$A,$B,$C"', exports={"A": "foo", "B": "bar", "C": "baz"})
    test("echo '$A,$B,$C'", exports={"A": "foo", "B": "bar", "C": "baz"})

    test('echo $A"$B"$C"A"$B"$C"', exports={"A": "foo", "B": "bar", "C": "baz"})
    test("echo $A'$B'$C'A'$B'$C'", exports={"A": "foo", "B": "bar", "C": "baz"})

    test("echo $A",   exports={"A": "'" + config.LOREM + "'"})
    test('echo "$A"', exports={"A": "'" + config.LOREM + "'"})
    test("echo '$A'", exports={"A": "'" + config.LOREM + "'"})

    test("$ECHO $ECHO", exports={"ECHO": "echo"})
    test("$A$B bonjour", exports={"A": "ec", "B": "ho"})

    test("echo $")

@suite
def suite_glob(test):
    test("echo *")
    test("echo *", setup="touch a b c")
    test("echo *.c", setup="touch a b c foo.c bar.c")
    test("echo src/*.c", setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c")
    test("echo */*.c", setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c")
    test("echo */*.c",
            setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.c inc/bar.c")
    test("echo */*.h",
            setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")
    test("echo l1/*/l3/*/*",
            setup="mkdir -p l1/l2_1/l3; mkdir -p l1/l2_2; cd l1/l2_1/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h;\
                   cd ../../..; cd l1/l2_2; touch bonjour je suis")

    test("echo */*/*/*/*.c",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")
    test("echo */*/*/*/*.h",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")

    test("echo */*/*/*.c",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")
    test("echo */*/*/*.h",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")

    test("echo */*/*/*/*/*.c",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")
    test("echo */*/*/*/*/*.h",
            setup="mkdir -p l1/l2/l3; cd l1/l2/l3;\
                   mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.h inc/bar.h")

    test("echo /*")
    test("echo /etc/*")
    test("echo /usr/include/*.h")
    test("echo /*/*")

    test("echo *nothing")
    test("echo nothing*")
    test("echo *nothing*")

    test("echo **")
    test("echo **", setup="touch a b c")
    test("echo **", setup="mkdir d; touch d/a d/b d/c")
    test("echo */*", setup="mkdir d; touch d/a d/b d/c")
    test("echo */a", setup="mkdir d; touch d/a d/b d/c")
    test("echo d/*", setup="mkdir d; touch d/a d/b d/c")

@suite
def suite_escape(test):
    test(r"echo \a")
    test(r"\e\c\h\o bonjour")
    test(r"echo charles\ ")
    test(r"echo \ \ jesuis\ \ charles")
    test(r"echo \ \ \ \ \ \ \ \ ")
    test(r"echo \ \ \ \ \ \ \ \               \ \ \ \ \ \ ")
    test(r"echo \$PATH")
    test(r"echo \$\P\A\T\H")
    test(r"echo\ bonjour")

@suite
def suite_preprocess(test):
    test(r"echo \*", setup="touch a b c")
    test(r"echo \*\*", setup="touch a b c")
    test(r"echo \ *", setup="touch a b c")
    test(r"echo *\.c", setup="touch a.c b.c c.c")
    test(r"echo *.\c", setup="touch a.c b.c c.c")
    test(r"echo *.c\ ", setup="touch a.c b.c c.c")
    test("echo $A$B",
            setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.c inc/bar.c",
            exports={"A": "*", "B": "/*.c"})
    test("echo $A$B",
            setup="mkdir src; touch src/a src/b src/c src/foo.c src/bar.c;\
                   mkdir inc; touch inc/a inc/b inc/c inc/foo.c inc/bar.c",
            exports={"A": "*/.", "B": "*.c"})
