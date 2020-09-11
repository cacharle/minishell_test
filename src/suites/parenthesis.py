# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    parenthesis.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:57 by charles           #+#    #+#              #
#    Updated: 2020/09/11 14:23:35 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from suite import suite

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
