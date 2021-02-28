# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    flow.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:52 by charles           #+#    #+#              #
#    Updated: 2021/02/27 20:35:46 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from minishell_test.config import Config
from minishell_test.suite.decorator import suite
from minishell_test.hooks import (
    error_line0,
    platform_status,
    discard,
    replace_double,
    error_eof_to_expected_token
)


@suite()
def suite_end(test):
    """ `;` tests """
    test("echo bonjour; echo je")
    test("echo bonjour ;echo je")
    test("echo bonjour ; echo je")
    test("echo bonjour;")
    test("echo; ")
    test("echo ; ")
    test("echo ;")
    test("; echo", hook=error_line0, hook_status=platform_status(2, 1))
    test(" ;echo", hook=error_line0, hook_status=platform_status(2, 1))
    test(" ; echo", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a; echo b; echo c; echo d; echo e; echo f; echo g; echo h; echo i;"
         "echo j; echo k; echo l; echo m; echo c; echo c; echo c; echo c; echo c;"
         "echo c; echo c; echo c; echo v; echo w; echo x; echo y; echo z")
    test("echo a ; echo b; echo c ;echo d     ;   echo e   ;echo f;        echo g  ;echo h; echo i;"
         "echo j  ; echo k; echo l; echo m; echo c    ; echo c; echo c    ; echo c; echo c;"
         "echo c; echo c   ; echo c; echo v   ; echo w;    echo x; echo y    ; echo z")
    test("ls doesnotexists ; echo bonjour")
    test("ls doesnotexists; echo bonjour")
    test("echo bonjour; ls doesnotexists")
    test("echo a ; ;", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a ; ;", hook=error_line0, hook_status=platform_status(2, 1))
    test(";", hook=error_line0, hook_status=platform_status(2, 1))
    test("; ;", hook=error_line0, hook_status=platform_status(2, 1))
    test("; ; ;", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a ; ; echo b", hook=error_line0, hook_status=platform_status(2, 1))
    test(";;", hook=[error_line0, replace_double(";")], hook_status=platform_status(2, 1))
    test(";;;", hook=[error_line0, replace_double(";")], hook_status=platform_status(2, 1))
    test(";;;;;", hook=[error_line0, replace_double(";")], hook_status=platform_status(2, 1))
    test("echo a ;; echo b", hook=[error_line0, replace_double(";")], hook_status=platform_status(2, 1))
    test("echo a ;;;;; echo b", hook=[error_line0, replace_double(";")], hook_status=platform_status(2, 1))
    test("ls " + 40 * " ; ls", setup="touch a b c")
    test("ls " + 80 * " ; ls", setup="touch a b c")
    test("ls " + 40 * " ; ls" + ";", setup="touch a b c")
    test("ls " + 80 * " ; ls" + ";", setup="touch a b c")


@suite()
def suite_pipe(test):
    """ `|` tests """
    test("cat /etc/shells | head -c 10")
    test("cat -e /etc/shells | head -c 10")
    test("cat -e /etc/shells | cat -e | head -c 10")
    test("cat -e /etc/shells | cat -e | cat -e | head -c 10")
    test("cat -e /dev/random | head -c 10", hook=discard)
    test("cat -e /dev/random | cat -e | head -c 10", hook=discard)
    test("cat -e /dev/random | cat -e | cat -e | head -c 10", hook=discard)
    test("echo bonjour | cat")
    test("echo bonjour | cat -e")
    test("echo bonjour | cat -e | cat -e | cat -e | cat -e | cat -e | cat -e | cat -e")
    test("ls | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat | cat | cat", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat -e | cat -e | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e < a", setup="touch a b c d; mkdir m1 m2 m3; echo bonjour > a")
    test("echo|", hook=discard, hook_status=platform_status(2, 1))
    test("echo |", hook=discard, hook_status=platform_status(2, 1))
    test("echo | ", hook=discard, hook_status=platform_status(2, 1))
    test("|cat", hook=error_line0, hook_status=platform_status(2, 1))
    test("| cat", hook=error_line0, hook_status=platform_status(2, 1))
    test(" | cat", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a | export A=a; echo $A")
    test("export A=a | cat; echo $A")
    test("echo bonjour | | cat -e", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo bonjour | asdf")
    test("asdf | echo bonjour")
    test("echo a ||| echo b", hook=error_line0, hook_status=platform_status(2, 1))
    test("ls " + 40 * " | ls", setup="touch a b c")
    test("ls " + 80 * " | ls", setup="touch a b c")
    test("echo bonjour " + 40 * " | cat -e")
    test("echo bonjour " + 80 * " | cat -e")
    test("ls asdfasdf | echo a")
    test("echo a | ls asdfasdf")
    test("ls asdfasdf | echo a; echo b")
    test("echo a | ls asdfasdf; echo b")
    test("echo a > foo | cat -e", files=["foo"])
    test("echo a >> foo | cat -e", files=["foo"])
    test("echo a | cat -e < foo", setup="echo b > foo")
    test("echo a > bar | cat -e < foo", setup="echo b > foo", files=["bar"])


@suite(bonus=True)
def suite_and(test):
    """ `&&` tests """
    test("echo bonjour&& echo je")
    test("echo bonjour &&echo je")
    test("echo bonjour && echo je")
    test("echo bonjour&&", hook=discard, hook_status=platform_status(2, 1))
    test("echo&& ", hook=discard, hook_status=platform_status(2, 1))
    test("echo && ", hook=discard, hook_status=platform_status(2, 1))
    test("echo &&", hook=discard, hook_status=platform_status(2, 1))
    test("&&echo", hook=error_line0, hook_status=platform_status(2, 1))
    test("&& echo", hook=error_line0, hook_status=platform_status(2, 1))
    test(" && echo", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a&& echo b&& echo c&& echo d&& echo e&& echo f&& echo g&& echo h&& echo i&&"
         "echo j&& echo k&& echo l&& echo m&& echo c&& echo c&& echo c&& echo c&& echo c&&"
         "echo c&& echo c&& echo c&& echo v&& echo w&& echo x&& echo y&& echo z")
    test("echo a && echo b&& echo c &&echo d     &&   echo e   &&echo f&&        echo g  &&echo h&& echo i&&"
         "echo j  && echo k&& echo l&& echo m&& echo c    && echo c&& echo c    && echo c&& echo c&&"
         "echo c&& echo c   && echo c&& echo v   && echo w&&    echo x&& echo y    && echo z")
    test("ls doesnotexists && echo bonjour")
    test("ls doesnotexists&& echo bonjour")
    test("echo bonjour&& ls doesnotexists")
    test("ls " + 40 * " && ls", setup="touch a b c")
    test("ls " + 80 * " && ls", setup="touch a b c")


@suite(bonus=True)
def suite_or(test):
    """ `||` tests """
    test("echo bonjour|| echo je")
    test("echo bonjour ||echo je")
    test("echo bonjour || echo je")
    test("echo bonjour||", hook=discard, hook_status=platform_status(2, 1))
    test("echo|| ", hook=discard, hook_status=platform_status(2, 1))
    test("echo || ", hook=discard, hook_status=platform_status(2, 1))
    test("echo ||", hook=discard, hook_status=platform_status(2, 1))
    test("||echo", hook=error_line0, hook_status=platform_status(2, 1))
    test("|| echo", hook=error_line0, hook_status=platform_status(2, 1))
    test(" || echo", hook=error_line0, hook_status=platform_status(2, 1))
    test("echo a|| echo b|| echo c|| echo d|| echo e|| echo f|| echo g|| echo h|| echo i||"
         "echo j|| echo k|| echo l|| echo m|| echo c|| echo c|| echo c|| echo c|| echo c||"
         "echo c|| echo c|| echo c|| echo v|| echo w|| echo x|| echo y|| echo z")
    test("echo a || echo b|| echo c ||echo d     ||   echo e   ||echo f||        echo g  ||echo h|| echo i||"
         "echo j  || echo k|| echo l|| echo m|| echo c    || echo c|| echo c    || echo c|| echo c||"
         "echo c|| echo c   || echo c|| echo v   || echo w||    echo x|| echo y    || echo z")
    test("ls doesnotexists || echo bonjour")
    test("ls doesnotexists|| echo bonjour")
    test("echo bonjour|| ls doesnotexists")
    test("ls asdf" + 40 * " || ls asdf", setup="touch a b c")
    test("ls asdf" + 80 * " || ls asdf", setup="touch a b c")


@suite(bonus=True)
def suite_parenthesis(test):
    """ `(`, `)` tests """
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
    test("(echo bonjour > f1 > f2 > f3)", files=["f1", "f2", "f3"])
    test("(echo bonjour > f1 > f2 > f3 > f4 > f5 > f6 > f7 > f8 > f9)",
         files=["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"])
    test("(echo bonjour) > f1", files=["f1"])
    test("(echo bonjour) > f1 > f2 > f3", files=["f1", "f2", "f3"])
    test("(echo bonjour) > f1 > f2 > f3 > f4 > f5 > f6 > f7 > f8 > f9",
         files=["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"])
    test("(cat -e < f1)", setup="echo bonjour > f1")
    test("(cat -e < f1 < f2 < f3)", setup="touch f1 f2 f3 f4; echo bonjour > f3")
    test("(cat -e < f1 < f2 < f3 < f4 < f5 < f6 < f7 < f8 < f9)",
         setup="touch f1 f2 f3 f4 f5 f6 f7 f8 f9; echo bonjour > f9")
    test("(cat -e) < f1", setup="echo bonjour > f1")
    test("(cat -e) < f1 < f2 < f3", setup="touch f1 f2 f3 f4; echo bonjour > f3")
    test("(cat -e) < f1 < f2 < f3 < f4 < f5 < f6 < f7 < f8 < f9",
         setup="touch f1 f2 f3 f4 f5 f6 f7 f8 f9; echo bonjour > f9")
    test("(echo bonjour > f1 > f2 > f3 > f4) > f5 > f6 > f7 > f8 > f9",
         files=["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"])
    test("(cat -e < f1 < f2 < f3 < f4) < f5 < f6 < f7 < f8 < f9",
         setup="touch f1 f2 f3 f4 f5 f6 f7 f8 f9; echo bonjour > f4")
    test("(echo bonjour > f1) > f2", files=["f1", "f2"])
    test("(cat -e > f1) < f2", setup="ls -l / > f2", files=["f1"])
    test("(exit); echo bonjour")
    test("(echo bonjour; exit; echo aurevoir)")
    test("(ls && ls)")
    test("(ls doesntexist || ls)")
    test("(ls doesntexist && ls)")
    test("(ls && ls) && echo $?")
    test("(echo a; echo b) | cat -e")
    test("echo bonjour | (cat -e; echo a)")
    test("echo bonjour | (echo a; cat -e)")
    test("(echo a) | (cat -e)")
    test("(echo a; echo b) | (cat -e)")
    test("(echo a) | (cat -e | cat -e)")
    test("(echo a; echo b) | (cat -e | cat -e)")
    test("(echo a; echo b) | cat -e | cat -e")
    test("(echo a); (echo b) | (cat -e) | (cat -e)")
    test("echo a | (cat -e | cat -e | cat -e)")
    test("echo a | (cat -e | cat -e | cat -e) | cat -e")
    test("(echo a) | (cat -e | cat -e | cat -e) | cat -e")
    test("(echo a) | (cat -e | cat -e | cat -e) | (cat -e)")
    test("(echo bonjour ; echo aurevoir) | (cat -e | cat -e) | cat -e")
    test("(    echo salut && echo bonjours )   ; echo comment ca va")
    test("(cd /; echo $PWD; pwd); echo $PWD; pwd")
    test("(export A=a; echo $A); echo $A")
    test("(cat /etc/shells) | (cat -e) | (cat -e) | (cat -e)")
    test("(cat /etc/shells) | (cat -e) | (cat -e) | (cat -e) | (cat -e) | (cat -e) | (cat -e) | (cat -e) | (cat -e)")
    test("(cat /etc/shells | (cat -e) | (cat -e) | (cat -e)",
         hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))
    test("(cat /etc/shells) | (cat -e) | (cat -e | (cat -e)",
         hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))


@suite()
def suite_syntax_error(test):
    """ separator syntax error test """
    test("< | a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("> | a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(">> | a", hook=error_line0, hook_status=platform_status(2, 1))
    test("< ; a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("> ; a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(">> ; a", hook=error_line0, hook_status=platform_status(2, 1))
    test("; | a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("; < a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("; > a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("; >> a", hook=error_line0, hook_status=platform_status(2, 1))
    test("| ; a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("| < a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("| > a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("| >> a", hook=error_line0, hook_status=platform_status(2, 1))
    test("> a ; a",  hook=error_line0)
    test("< a ; a",  hook=error_line0)
    test(">> a ; a", hook=error_line0)
    test(Config.lorem + " > >" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " < <" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " ; |" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " | ;" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))


@suite(bonus=True)
def suite_syntax_error_bonus(test):
    """ separator syntax error bonus test """
    test("< && a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("> && a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(">> && a", hook=error_line0, hook_status=platform_status(2, 1))
    test("< || a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("> || a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(">> || a", hook=error_line0, hook_status=platform_status(2, 1))
    test("< ( a",   hook=error_line0, hook_status=platform_status(2, 1))
    test("> ( a",   hook=error_line0, hook_status=platform_status(2, 1))
    test(">> ( a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("< ) a",   hook=error_line0, hook_status=platform_status(2, 1))
    test("> ) a",   hook=error_line0, hook_status=platform_status(2, 1))
    test(">> ) a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("&& < a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("&& > a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("&& >> a", hook=error_line0, hook_status=platform_status(2, 1))
    test("&& || a", hook=error_line0, hook_status=platform_status(2, 1))
    test("&& ( a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("&& ) a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("|| < a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("|| > a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("|| >> a", hook=error_line0, hook_status=platform_status(2, 1))
    test("|| && a", hook=error_line0, hook_status=platform_status(2, 1))
    test("|| ( a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("|| ) a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("( < a",   hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))
    test("( > a",   hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))
    test("( >> a",  hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))
    test(") < a",   hook=error_line0, hook_status=platform_status(2, 1))
    test(") > a",   hook=error_line0, hook_status=platform_status(2, 1))
    test(") >> a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("( && a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("( || a",  hook=error_line0, hook_status=platform_status(2, 1))
    test("( ) a",   hook=error_line0, hook_status=platform_status(2, 1))
    test(") && a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(") || a",  hook=error_line0, hook_status=platform_status(2, 1))
    test(") ( a",   hook=error_line0, hook_status=platform_status(2, 1))
    test("() a",    hook=error_line0, hook_status=platform_status(2, 1))
    test("( a",     hook=[error_line0, error_eof_to_expected_token], hook_status=platform_status(2, 1))
    test(") a",     hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " && &&" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " || ||" + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " ( ("   + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test(Config.lorem + " ) )"   + Config.lorem, hook=error_line0, hook_status=platform_status(2, 1))
    test("(); () ;() ;() ;() ;() ;() ;() ;() ;() ;a",    hook=error_line0, hook_status=platform_status(2, 1))
