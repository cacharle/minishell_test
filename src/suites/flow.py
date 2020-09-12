# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    flow.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:52 by charles           #+#    #+#              #
#    Updated: 2020/09/12 15:30:37 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from suite import suite
import hooks


@suite()
def suite_end(test):
    test("echo bonjour; echo je")
    test("echo bonjour ;echo je")
    test("echo bonjour ; echo je")
    test("echo bonjour;")
    test("echo; ")
    test("echo ; ")
    test("echo ;")
    test("; echo", hook=hooks.error_line0)
    test(" ;echo", hook=hooks.error_line0)
    test(" ; echo", hook=hooks.error_line0)
    test("echo a; echo b; echo c; echo d; echo e; echo f; echo g; echo h; echo i;"
         "echo j; echo k; echo l; echo m; echo c; echo c; echo c; echo c; echo c;"
         "echo c; echo c; echo c; echo v; echo w; echo x; echo y; echo z")
    test("echo a ; echo b; echo c ;echo d     ;   echo e   ;echo f;        echo g  ;echo h; echo i;"
         "echo j  ; echo k; echo l; echo m; echo c    ; echo c; echo c    ; echo c; echo c;"
         "echo c; echo c   ; echo c; echo v   ; echo w;    echo x; echo y    ; echo z")
    test("ls doesnotexists ; echo bonjour")
    test("ls doesnotexists; echo bonjour")
    test("echo bonjour; ls doesnotexists")


@suite()
def suite_pipe(test):
    test("cat /etc/shells | head -c 10")
    test("cat -e /etc/shells | head -c 10")
    test("cat -e /etc/shells | cat -e | head -c 10")
    test("cat -e /etc/shells | cat -e | cat -e | head -c 10")
    test("echo bonjour | cat")
    test("echo bonjour | cat -e")
    test("echo bonjour | cat -e | cat -e | cat -e | cat -e | cat -e | cat -e | cat -e")
    test("ls | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat | cat | cat", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e | cat -e | cat -e | cat -e", setup="touch a b c d; mkdir m1 m2 m3")
    test("ls -l | cat -e < a", setup="touch a b c d; mkdir m1 m2 m3; echo bonjour > a")
    test("echo|", hook=hooks.discard)
    test("echo |", hook=hooks.discard)
    test("echo | ", hook=hooks.discard)
    test("|cat", hook=hooks.error_line0)
    test("| cat", hook=hooks.error_line0)
    test(" | cat", hook=hooks.error_line0)
    test("echo a | export A=a; echo $A")
    test("export A=a | cat; echo $A")
    # test("echo a | A=a; echo $A")
    # test("A=a | cat; echo $A")


@suite(bonus=True)
def suite_and(test):
    test("echo bonjour&& echo je")
    test("echo bonjour &&echo je")
    test("echo bonjour && echo je")
    test("echo bonjour&&", hook=hooks.discard)
    test("echo&& ", hook=hooks.discard)
    test("echo && ", hook=hooks.discard)
    test("echo &&", hook=hooks.discard)
    test("&&echo", hook=hooks.error_line0)
    test("&& echo", hook=hooks.error_line0)
    test(" && echo", hook=hooks.error_line0)
    test("echo a&& echo b&& echo c&& echo d&& echo e&& echo f&& echo g&& echo h&& echo i&&"
         "echo j&& echo k&& echo l&& echo m&& echo c&& echo c&& echo c&& echo c&& echo c&&"
         "echo c&& echo c&& echo c&& echo v&& echo w&& echo x&& echo y&& echo z")
    test("echo a && echo b&& echo c &&echo d     &&   echo e   &&echo f&&        echo g  &&echo h&& echo i&&"
         "echo j  && echo k&& echo l&& echo m&& echo c    && echo c&& echo c    && echo c&& echo c&&"
         "echo c&& echo c   && echo c&& echo v   && echo w&&    echo x&& echo y    && echo z")
    test("ls doesnotexists && echo bonjour")
    test("ls doesnotexists&& echo bonjour")
    test("echo bonjour&& ls doesnotexists")


@suite(bonus=True)
def suite_or(test):
    test("echo bonjour|| echo je")
    test("echo bonjour ||echo je")
    test("echo bonjour || echo je")
    test("echo bonjour||", hook=hooks.discard)
    test("echo|| ", hook=hooks.discard)
    test("echo || ", hook=hooks.discard)
    test("echo ||", hook=hooks.discard)
    test("||echo", hook=hooks.error_line0)
    test("|| echo", hook=hooks.error_line0)
    test(" || echo", hook=hooks.error_line0)
    test("echo a|| echo b|| echo c|| echo d|| echo e|| echo f|| echo g|| echo h|| echo i||"
         "echo j|| echo k|| echo l|| echo m|| echo c|| echo c|| echo c|| echo c|| echo c||"
         "echo c|| echo c|| echo c|| echo v|| echo w|| echo x|| echo y|| echo z")
    test("echo a || echo b|| echo c ||echo d     ||   echo e   ||echo f||        echo g  ||echo h|| echo i||"
         "echo j  || echo k|| echo l|| echo m|| echo c    || echo c|| echo c    || echo c|| echo c||"
         "echo c|| echo c   || echo c|| echo v   || echo w||    echo x|| echo y    || echo z")
    test("ls doesnotexists || echo bonjour")
    test("ls doesnotexists|| echo bonjour")
    test("echo bonjour|| ls doesnotexists")


@suite(bonus=True)
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
