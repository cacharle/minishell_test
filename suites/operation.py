from suite import suite

@suite
def suite_end(test):
    test("echo bonjour; echo je")
    test("echo bonjour ;echo je")
    test("echo bonjour ; echo je")
    test("echo bonjour;")
    test("echo; ")
    test("echo ; ")
    test("echo ;")
    test("echo a; echo b; echo c; echo d; echo e; echo f; echo g; echo h; echo i;" +
         "echo j; echo k; echo l; echo m; echo c; echo c; echo c; echo c; echo c;" +
         "echo c; echo c; echo c; echo v; echo w; echo x; echo y; echo z")
    test("echo a ; echo b; echo c ;echo d     ;   echo e   ;echo f;        echo g  ;echo h; echo i;" +
         "echo j  ; echo k; echo l; echo m; echo c    ; echo c; echo c    ; echo c; echo c;" +
         "echo c; echo c   ; echo c; echo v   ; echo w;    echo x; echo y    ; echo z")

    test("ls doesnotexists ; echo bonjour")
    test("ls doesnotexists; echo bonjour")
    test("echo bonjour; ls doesnotexists")

@suite
def suite_and(test):
    test("echo bonjour&& echo je")
    test("echo bonjour &&echo je")
    test("echo bonjour && echo je")
    test("echo bonjour&&")
    test("echo&& ")
    test("echo && ")
    test("echo &&")
    test("echo a&& echo b&& echo c&& echo d&& echo e&& echo f&& echo g&& echo h&& echo i&&" +
         "echo j&& echo k&& echo l&& echo m&& echo c&& echo c&& echo c&& echo c&& echo c&&" +
         "echo c&& echo c&& echo c&& echo v&& echo w&& echo x&& echo y&& echo z")
    test("echo a && echo b&& echo c &&echo d     &&   echo e   &&echo f&&        echo g  &&echo h&& echo i&&" +
         "echo j  && echo k&& echo l&& echo m&& echo c    && echo c&& echo c    && echo c&& echo c&&" +
         "echo c&& echo c   && echo c&& echo v   && echo w&&    echo x&& echo y    && echo z")

    test("ls doesnotexists && echo bonjour")
    test("ls doesnotexists&& echo bonjour")
    test("echo bonjour&& ls doesnotexists")

@suite
def suite_or(test):
    test("echo bonjour|| echo je")
    test("echo bonjour ||echo je")
    test("echo bonjour || echo je")
    test("echo bonjour||")
    test("echo|| ")
    test("echo || ")
    test("echo ||")
    test("echo a|| echo b|| echo c|| echo d|| echo e|| echo f|| echo g|| echo h|| echo i||" +
         "echo j|| echo k|| echo l|| echo m|| echo c|| echo c|| echo c|| echo c|| echo c||" +
         "echo c|| echo c|| echo c|| echo v|| echo w|| echo x|| echo y|| echo z")
    test("echo a || echo b|| echo c ||echo d     ||   echo e   ||echo f||        echo g  ||echo h|| echo i||" +
         "echo j  || echo k|| echo l|| echo m|| echo c    || echo c|| echo c    || echo c|| echo c||" +
         "echo c|| echo c   || echo c|| echo v   || echo w||    echo x|| echo y    || echo z")

    test("ls doesnotexists || echo bonjour")
    test("ls doesnotexists|| echo bonjour")
    test("echo bonjour|| ls doesnotexists")

@suite
def suite_pipe(test):
    test("echo bonjour | cat")
    test("echo bonjour | cat -e")
    test("ls | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat | cat | cat", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat -e | cat -e | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e < a", setup="touch a b c d; mkdir m1 m2 m3; echo bonjour > a")
