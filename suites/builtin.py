# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    builtin.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:43 by charles           #+#    #+#              #
#    Updated: 2020/07/17 13:42:15 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config
from suite import suite

@suite
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

@suite
def suite_export(test):
    test("export")
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

    test("export $TEST", exports={"TEST": "A=a"})

@suite
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
    test("cd $HOME; pwd; echo $PWD");
    test("cd ~; pwd; echo $PWD");
    test("cd ~/..; pwd; echo $PWD");
    test("cd ~/../..; pwd; echo $PWD");
    test("cd /; pwd; echo $PWD");
    test("cd /.; pwd; echo $PWD");
    test("cd /./; pwd; echo $PWD");
    test("cd /././././; pwd; echo $PWD");
    test("cd //; pwd; echo $PWD");
    test("cd")

@suite
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

@suite
def suite_pwd(test):
    test("pwd")
    test("pwd", setup="cd ..")
    test("pwd", setup="cd ../..")
    test("pwd", setup="cd ../../..")
    test("pwd", setup="cd /")
    test("pwd", setup="cd $HOME")
    test("pwd | cat -e")

@suite
def suite_env(test):
    test("env")
    test("env", setup="export A=a")
    test("env", setup="export A=a B=b C=c")
    test("env | cat -e", setup="export A=a B=b C=c")

@suite
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
