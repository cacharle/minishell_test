# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    status.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:40 by charles           #+#    #+#              #
#    Updated: 2020/07/15 18:24:40 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

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
