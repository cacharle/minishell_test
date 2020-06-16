import config
from utils import suite, test

@suite
def suite_quote():
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
def suite_echo():
    test("echo bonjour")
    test("echo lalalala lalalalal alalalalal alalalala")
    test("echo lalalala                lalalalal      alalalalal alalalala")
    test("echo " + config.LOREM)

    test("echo -n bonjour")
    test("echo -n lalalala lalalalal alalalalal alalalala")
    test("echo -n lalalala                lalalalal      alalalalal alalalala")
    test("echo -n " + config.LOREM)

@suite
def suite_redirection():
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


@suite
def suite_edgecases():
    test('echo "\\"" >>a"b""c"  ', files=["abc"])
