# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    operation.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:52 by charles           #+#    #+#              #
#    Updated: 2020/09/11 17:05:35 by charles          ###   ########.fr        #
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
    test("echo a; echo b; echo c; echo d; echo e; echo f; echo g; echo h; echo i;" +
         "echo j; echo k; echo l; echo m; echo c; echo c; echo c; echo c; echo c;" +
         "echo c; echo c; echo c; echo v; echo w; echo x; echo y; echo z")
    test("echo a ; echo b; echo c ;echo d     ;   echo e   ;echo f;        echo g  ;echo h; echo i;" +
         "echo j  ; echo k; echo l; echo m; echo c    ; echo c; echo c    ; echo c; echo c;" +
         "echo c; echo c   ; echo c; echo v   ; echo w;    echo x; echo y    ; echo z")

    test("ls doesnotexists ; echo bonjour")
    test("ls doesnotexists; echo bonjour")
    test("echo bonjour; ls doesnotexists")

@suite()
def suite_pipe(test):
    test("echo bonjour | cat")
    test("echo bonjour | cat -e")
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
    test("echo a&& echo b&& echo c&& echo d&& echo e&& echo f&& echo g&& echo h&& echo i&&" +
         "echo j&& echo k&& echo l&& echo m&& echo c&& echo c&& echo c&& echo c&& echo c&&" +
         "echo c&& echo c&& echo c&& echo v&& echo w&& echo x&& echo y&& echo z")
    test("echo a && echo b&& echo c &&echo d     &&   echo e   &&echo f&&        echo g  &&echo h&& echo i&&" +
         "echo j  && echo k&& echo l&& echo m&& echo c    && echo c&& echo c    && echo c&& echo c&&" +
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
    test("echo a|| echo b|| echo c|| echo d|| echo e|| echo f|| echo g|| echo h|| echo i||" +
         "echo j|| echo k|| echo l|| echo m|| echo c|| echo c|| echo c|| echo c|| echo c||" +
         "echo c|| echo c|| echo c|| echo v|| echo w|| echo x|| echo y|| echo z")
    test("echo a || echo b|| echo c ||echo d     ||   echo e   ||echo f||        echo g  ||echo h|| echo i||" +
         "echo j  || echo k|| echo l|| echo m|| echo c    || echo c|| echo c    || echo c|| echo c||" +
         "echo c|| echo c   || echo c|| echo v   || echo w||    echo x|| echo y    || echo z")

    test("ls doesnotexists || echo bonjour")
    test("ls doesnotexists|| echo bonjour")
    test("echo bonjour|| ls doesnotexists")
