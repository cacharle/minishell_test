# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    builtin.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juligonz <juligonz@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:43 by charles           #+#    #+#              #
#    Updated: 2020/09/11 17:53:52 by juligonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

import config
import hooks
from suite import suite

@suite()
def suite_echo(test):
    test("echo")
    test("echo bonjour")
    test("echo lalalala lalalalal alalalalal alalalala")
    test("echo lalalala                lalalalal      alalalalal alalalala")
    test("echo " + config.LOREM)

    test("echo -n")
    test("echo -n bonjour")
    test("echo -n lalalala lalalalal alalalalal alalalala")
    test("echo -n lalalala                lalalalal      alalalalal alalalala")
    test("echo -n " + config.LOREM)

    test("echo bonjour -n")
    test("echo -n bonjour -n")
    test("                        echo                     bonjour             je")
    test("                        echo       -n            bonjour             je")

    test("echo a '' b '' c '' d")
    test('echo a "" b "" c "" d')
    test("echo -n a '' b '' c '' d")
    test('echo -n a "" b "" c "" d')
    test("echo '' '' ''")

@suite()
def suite_export(test):
    test("export", hook=hooks.sort_lines)
    # test("export A=; env | grep A=; echo $A")
    # test("export A; env | grep A; echo $A")
    test("export A=a; echo $A")
    test("export A=a B=b C=c; echo $A$B$C")
    test("export A=a B=b C=c D=d E=e F=f G=g H=h I=i J=j K=k L=l" +
            "M=m N=n O=o P=p Q=q R=r S=s T=t U=u V=v W=w X=x Y=y Z=z" +
            "; echo $A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z")
    test("export BONJOURJESUIS=a; echo $BONJOURJESUIS")
    test("export bonjourjesuis=a; echo $bonjourjesuis")
    test("export bonjour_je_suis=a; echo $bonjour_je_suis")
    test("export BONJOURJESUIS1=a; echo $BONJOURJESUIS1")
    test("export bO_nJq123o__1ju_je3234sui__a=a; echo $bO_nJq123o__1ju_je3234sui__a")
    test("export a0123456789=a; echo $a0123456789")
    test("export abcdefghijklmnopqrstuvwxyz=a; echo $abcdefghijklmnopqrstuvwxyz")
    test("export ABCDEFGHIJKLMNOPQRSTUVWXYZ=a; echo $ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    test("export __________________________=a; echo $__________________________")
    test("export _bonjour_=a; echo $_bonjour_")
    test("export _=a; echo $_a")
    test("export 1=a")
    test("export BONJOURJESUIS =a")
    test("export BONJOURJESUIS= a")
    test(r"export BONJOUR\\JESUIS=a")
    test(r"export BONJOUR\'JESUIS=a")
    test(r'export BONJOUR\"JESUIS=a')
    test(r"export BONJOUR\$JESUIS=a")
    test(r"export BONJOUR\&JESUIS=a")
    test(r"export BONJOUR\|JESUIS=a")
    test(r"export BONJOUR\;JESUIS=a")
    test(r"export BONJOUR\_JESUIS=a")
    test(r"export BONJOUR\0JESUIS=a")
    test(r"export \B\O\N\ \ \ \ \ \ \ JOURJESUIS=a")
    test(r"export A=\B\O\N\ \ \ \ \ \ \ JOURJESUIS; echo $A")
    test(r"export A='bonjour je suis charles'; echo $A")
    test(r'export A="bonjour je suis charles"; echo $A')
    test(r"export A==a; echo $A")
    test(r"export A===a; echo $A")
    test(r"export A====a; echo $A")
    test(r"export A=====a; echo $A")
    test(r"export A======a; echo $A")
    test(r"export A=a=a=a=a=a; echo $A")
    test("export A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C; echo $A$B$C")
    test("export 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C; echo $A$B$C")
    test("export A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf '; echo $A$B$C")
    test("export A B C; echo $A$B$C")


    test("export 'AH@'=nop")
    test("export \"AH'\"=nop")
    test("export 'AH\"'=nop")
    test("export 'AH$'=nop")
    test("export 'AH!'=nop")
    test("export 'AH|'=nop")
    test("export 'AH;'=nop")
    test("export 'AH&'=nop")
    test("export 'AH\\'=nop")

    test("export $TEST", exports={"TEST": "A=a"})

@suite()
def suite_cd(test):
    test("cd .; pwd; echo $PWD");
    test("cd ..; pwd; echo $PWD");
    test("cd ../..; pwd; echo $PWD");
    test("cd ../../..; pwd; echo $PWD");
    test("cd ../../../..; pwd; echo $PWD");
    test("cd ../../../../..; pwd; echo $PWD");
    test("cd ../../../../../..; pwd; echo $PWD");
    test("cd /; pwd; echo $PWD");
    test("cd /etc; pwd; echo $PWD");
    test("cd ''; pwd; echo $PWD");
    test("cd '' ''; pwd; echo $PWD");
    test("cd '' '' ''; pwd; echo $PWD");
    test("cd ' '; pwd; echo $PWD");
    # test("cd '\t'; pwd; echo $PWD");
    # test("cd '\t   \t\t\t    '; pwd; echo $PWD");
    test("cd d ''; pwd; echo $PWD", setup="mkdir d")
    test("cd d d; pwd; echo $PWD", setup="mkdir d")
    test("cd d ' '; pwd; echo $PWD", setup="mkdir d")
    test("cd $HOME; pwd; echo $PWD");
    test("cd $HOME; pwd; echo $PWD", exports={"HOME": os.getenv("HOME")});
    # test("cd ~; pwd; echo $PWD"); # do we have to handle ~ ?
    # test("cd ~/..; pwd; echo $PWD");
    # test("cd ~/../..; pwd; echo $PWD");
    test("cd /; pwd; echo $PWD");
    test("cd /.; pwd; echo $PWD");
    test("cd /./; pwd; echo $PWD");
    test("cd /././././; pwd; echo $PWD");
    test("cd //; pwd; echo $PWD");
    test("cd ///; pwd; echo $PWD");
    test("cd ////; pwd; echo $PWD");
    test("cd //////////////////////////////////////////////////////; pwd; echo $PWD");
    test("cd")

    test("cd ' /'; pwd; echo $PWD")
    test("cd ' / '; pwd; echo $PWD")
    test("cd '                  /'; pwd; echo $PWD")
    test("cd '                  /              '; pwd; echo $PWD")
    test("cd ' // '; pwd; echo $PWD")

    test("cd //home; pwd; echo $PWD")
    test("cd ' //home'; pwd; echo $PWD")
    test("cd '     //home    '; pwd; echo $PWD")

    test("cd d", setup="mkdir -m 000 d")
    test("cd d", setup="mkdir -m 001 d")
    test("cd d", setup="mkdir -m 002 d")
    test("cd d", setup="mkdir -m 003 d")
    test("cd d", setup="mkdir -m 004 d")
    test("cd d", setup="mkdir -m 005 d")
    test("cd d", setup="mkdir -m 006 d")
    test("cd d", setup="mkdir -m 007 d")
    test("cd d", setup="mkdir -m 010 d")
    test("cd d", setup="mkdir -m 020 d")
    test("cd d", setup="mkdir -m 030 d")
    test("cd d", setup="mkdir -m 040 d")
    test("cd d", setup="mkdir -m 050 d")
    test("cd d", setup="mkdir -m 060 d")
    test("cd d", setup="mkdir -m 070 d")
    test("cd d", setup="mkdir -m 100 d")
    test("cd d", setup="mkdir -m 200 d")
    test("cd d", setup="mkdir -m 300 d")
    test("cd d", setup="mkdir -m 400 d")
    test("cd d", setup="mkdir -m 500 d")
    test("cd d", setup="mkdir -m 600 d")
    test("cd d", setup="mkdir -m 700 d")

    test("cd d", setup="mkdir -m 755 d")
    test("cd d", setup="mkdir -m 644 d")
    test("cd d", setup="mkdir -m 311 d")
    test("cd d", setup="mkdir -m 111 d")
    test("cd d", setup="mkdir -m 222 d")
    test("cd d", setup="mkdir -m 333 d")

    test("cd d", setup="mkdir -m 0777 d")
    test("cd d", setup="mkdir -m 1000 d")
    test("cd d", setup="mkdir -m 2000 d")
    test("cd d", setup="mkdir -m 3000 d")
    test("cd d", setup="mkdir -m 4000 d")
    test("cd d", setup="mkdir -m 5000 d")
    test("cd d", setup="mkdir -m 6000 d")
    test("cd d", setup="mkdir -m 7000 d")
    test("cd d", setup="mkdir -m 1777 d")
    test("cd d", setup="mkdir -m 2777 d")
    test("cd d", setup="mkdir -m 3777 d")
    test("cd d", setup="mkdir -m 4777 d")
    test("cd d", setup="mkdir -m 5777 d")
    test("cd d", setup="mkdir -m 6777 d")
    test("cd d", setup="mkdir -m 7777 d")
    test("cd d", setup="mkdir -m 0000 d")

@suite()
def suite_unset(test):
    test("unset")
    test("unset A; echo $A", setup="export A=a")
    test("unset 'A '; echo $A", setup="export A=a")
    test("unset 'A='; echo $A", setup="export A=a")
    test("unset A B C; echo $A$B$C", setup="export A=a B=b C=c")
    test("unset A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C; echo $A$B$C",
            setup="export A=a B=b C=c")
    test("unset 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C; echo $A$B$C",
            setup="export A=a B=b C=c")
    test("unset A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf '; echo $A$B$C",
            setup="export A=a B=b C=c")
    test("unset A; echo $A$B$C", setup="export A=a B=b C=c")
    test("unset C; echo $A$B$C", setup="export A=a B=b C=c")

    test("unset A B C", setup="export A=a B=b C=c")
    test("unset A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C",
            setup="export A=a B=b C=c")
    test("unset 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf ' C",
            setup="export A=a B=b C=c")
    test("unset A 'asdf ' B ' asdf asdf asd f' ' asdf ' '' 'asdf '",
            setup="export A=a B=b C=c")
    test("unset A", setup="export A=a B=b C=c")

@suite()
def suite_pwd(test):
    test("pwd")
    test("pwd", setup="cd ..")
    test("pwd", setup="cd ../..")
    test("pwd", setup="cd ../../..")
    test("pwd", setup="cd /")
    test("pwd", setup="cd $HOME")
    test("pwd | cat -e")
    test("cd lnk; rmdir ../d; pwd", setup="mkdir d; ln -s d lnk")

@suite()
def suite_env(test):
    test("env", hook=hooks.sort_lines)
    test("env", setup="export A=a", hook=hooks.sort_lines)
    test("env", setup="export A=a B=b C=c", hook=hooks.sort_lines)
    test("env | cat -e", setup="export A=a B=b C=c", hook=hooks.sort_lines)

@suite()
def suite_exit(test):
    test("exit")
    test("exit 1")
    test("exit 2")
    test("exit 3")
    test("exit ' 3'")
    test("exit '\t3'")
    test("exit '\t\f\r 3'")
    test("exit '3 '")
    test("exit '3\t'")
    test("exit '3\r'")
    test("exit '3\t\f\r '")
    test("exit '3     a'")
    test("exit '3\t\t\ta'")
    test("exit 0")
    test("exit -0")
    test("exit -1")
    test("exit 255")
    test("exit 256")
    test("exit 2000000")
    test("exit -2000000")
    test("exit 2147483647")
    test("exit -2147483648")
    test("exit 2147483648")
    test("exit -2147483649")
    test("exit 3147483648")
    test("exit -3147483649")
    test("exit 4294967295")
    test("exit 4294967296")
    test("exit -9223372036854775808")
    test("exit 9223372036854775807")
    test("exit -9223372036854775809")
    test("exit 9223372036854775808")
    test("exit 18446744073709551615")
    test("exit 18446744073709551616")

    test("exit +1")
    test("exit +2")
    test("exit +3")
    test("exit +0")
    test("exit +255")
    test("exit +256")
    test("exit +2000000")
    test("exit +2147483647")

    test("exit ++1")
    test("exit ++2")
    test("exit ++3")
    test("exit ++0")
    test("exit ++255")
    test("exit ++256")
    test("exit ++2000000")
    test("exit ++2147483647")

    test("exit --1")
    test("exit --2")
    test("exit --3")
    test("exit --0")
    test("exit --255")
    test("exit --256")
    test("exit --2000000")
    test("exit --2147483647")

    test("exit bonjour")
    test("exit 0_")
    test("exit _0")
    test("exit 0123456789")
    test("exit -0123456789")
    test("exit 00000000000000000000000000000000000000000000001")
    test("exit 00000000000000000000000000000000000000000000000" +
            "00000000000000000000000000000000000000000000001")
    test("exit 00000000000000000000000000000000000000000000000" +
            "00000000000000000000000000000000000000000000000")
    test("exit -00000000000000000000000000000000000000000000000" +
            "00000000000000000000000000000000000000000000001")
    test("exit -99999999999999999999999999999999999999999999" +
            "99999999999999999999999999999999999999999999")
    test("exit 99999999999999999999999999999999999999999999" +
            "99999999999999999999999999999999999999999999")

    test("exit 0 bonjour")
    test("exit bonjour 0")
    test("exit 0 1")
    test("exit 0 1 2 3 4 5 6 7 8 9")

    test("exit " + config.LOREM)
