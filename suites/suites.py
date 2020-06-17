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

@suite
def suite_redirection(test):
    test("echo bonjour > test", setup="", files=["test"])
    test("echo > test bonjour", setup="", files=["test"])
    test("> test echo bonjour", setup="", files=["test"])
    test("echo bonjour >> test", setup="", files=["test"])
    test("echo >> test bonjour", setup="", files=["test"])
    test(">> test echo bonjour", setup="", files=["test"])
    test("cat < test", setup="echo bonjour > test")
    test("echo bonjour > test", setup="", files=["test"])

    test("echo > test'sticked' bonjour", setup="", files=["teststicked"])
    test("> test'sticked' echo bonjour", setup="", files=["teststicked"])
    test("echo bonjour >> test'sticked'", setup="", files=["teststicked"])
    test("echo >> test'sticked' bonjour", setup="", files=["teststicked"])
    test(">> test'sticked' echo bonjour", setup="", files=["teststicked"])
    test("cat < test'sticked'", setup="echo bonjour > test'sticked'")
    test("< test'sticked' cat", setup="echo bonjour > test'sticked'")

    test("echo > test\"sticked\" bonjour", setup="", files=["teststicked"])
    test("> test\"sticked\" echo bonjour", setup="", files=["teststicked"])
    test("echo bonjour >> test\"sticked\"", setup="", files=["teststicked"])
    test("echo >> test\"sticked\" bonjour", setup="", files=["teststicked"])
    test(">> test\"sticked\" echo bonjour", setup="", files=["teststicked"])
    test("cat < test\"sticked\"", setup="echo bonjour > test\"sticked\"")
    test("< test\"sticked\" cat", setup="echo bonjour > test\"sticked\"")

    test("echo > test'yo'\"sticked\" bonjour", setup="", files=["testyosticked"])
    test("> test'yo'\"sticked\" echo bonjour", setup="", files=["testyosticked"])
    test("echo bonjour >> test'yo'\"sticked\"", setup="", files=["testyosticked"])
    test("echo >> test'yo'\"sticked\" bonjour", setup="", files=["testyosticked"])
    test(">> test'yo'\"sticked\" echo bonjour", setup="", files=["testyosticked"])
    test("cat < test'yo'\"sticked\"", setup="echo bonjour > test'yo'\"sticked\"")
    test("< test'yo'\"sticked\" cat", setup="echo bonjour > test'yo'\"sticked\"")

    test("echo bonjour > test > je > suis", setup="", files=["test", "je", "suis"])
    test("echo > test > je bonjour > suis", setup="", files=["test", "je", "suis"])
    test("> test echo bonjour > je > suis", setup="", files=["test", "je", "suis"])
    test("echo bonjour >> test > je >> suis", setup="", files=["test", "je", "suis"])
    test("echo >> test bonjour > je > suis", setup="", files=["test", "je", "suis"])
    test(">> test echo > je bonjour > suis", setup="", files=["test", "je", "suis"])
    test("cat < test < je", setup="echo bonjour > test; echo salut > je")

    test("echo bonjour>test>je>suis", setup="", files=["test", "je", "suis"])
    test(">test echo bonjour>je>suis", setup="", files=["test", "je", "suis"])
    test("echo bonjour>>test>je>>suis", setup="", files=["test", "je", "suis"])
    test("cat<test<je", setup="echo bonjour > test; echo salut > je")

    test("echo bonjour > a'b'c'd'e'f'g'h'i'j'k'l'm'n'o'p'q'r's't'u'v'w'x'y'z'",
            files=["abcdefghijklmnopqrstuvwxyz"])
    test('echo bonjour > a"b"c"d"e"f"g"h"i"j"k"l"m"n"o"p"q"r"s"t"u"v"w"x"y"z"',
            files=["abcdefghijklmnopqrstuvwxyz"])
    test('echo bonjour > a\'b\'c"d"e\'f\'g"h"i\'j\'k"l"m\'n\'o"p\'q\'r"s\'t\'u"v"w"x"y\'z\'',
            files=["abcdefghijklmnopqrstuvwxyz"])

@suite
def suite_edgecases(test):
    test('echo "\\"" >>a"b""c"  ', files=["abc"])
    test("echo " + ''.join([chr(i) for i in range(1, 127) if chr(i) not in '\n`"\'()|&><']))

@suite
def suite_cmd_error(test):
    test(">")
    test(">>")
    test("<")
    test("echo >")
    test("echo >>")
    test("echo <")

    test("> test", files=["test"])
    test(">> test", files=["test"])
    test("< test", setup="touch test")

    test("echo foo >>> bar")
    test("echo foo >>>> bar")
    test("echo foo >>>>> bar")

    test("cat <<< bar", setup="echo bonjour > bar")
    test("cat <<<< bar", setup="echo bonjour > bar")
    test("cat <<<<< bar", setup="echo bonjour > bar")

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
