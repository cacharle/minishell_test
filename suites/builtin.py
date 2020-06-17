import config
from suite import suite

@suite
def suite_echo(test):
    test("echo bonjour")
    test("echo lalalala lalalalal alalalalal alalalala")
    test("echo lalalala                lalalalal      alalalalal alalalala")
    test("echo " + config.LOREM)

    test("echo -n bonjour")
    test("echo -n lalalala lalalalal alalalalal alalalala")
    test("echo -n lalalala                lalalalal      alalalalal alalalala")
    test("echo -n " + config.LOREM)

@suite
def suite_export(test):
    test("export A=a")
    test("export A=a B=b C=c")
    test("export A=a B=b C=c D=d E=e F=f G=g H=h I=i J=j K=k L=l" +
            "M=m N=n O=o P=p Q=q R=r S=s T=t U=u V=v W=w X=x Y=y Z=z")
    test("export BONJOURJESUIS=a")
    test("export bonjourjesuis=a")
    test("export bonjour_je_suis=a")
    test("export BONJOURJESUIS1=a")
    test("export bO_nJq123o__1ju_je3234sui__a=a")
    test("export a0123456789=a")
    test("export abcdefghijklmnopqrstuvwxyz=a")
    test("export ABCDEFGHIJKLMNOPQRSTUVWXYZ=a")
    test("export __________________________=a")
    test("export _bonjour_=a")
    test("export _=a")
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
    test(r"export A=\B\O\N\ \ \ \ \ \ \ JOURJESUIS")
    test(r"export A='bonjour je suis charles'")
    test(r'export A="bonjour je suis charles"')
    test(r"export A==a")
    test(r"export A===a")
    test(r"export A====a")
    test(r"export A=====a")
    test(r"export A======a")
    test(r"export A=a=a=a=a=a")

@suite
def suite_cd(test):
    test("cd .");
    test("cd ..");
    test("cd ../..");
    test("cd ../../..");
    test("cd ../../../..");
    test("cd ../../../../..");
    test("cd ../../../../../..");
    test("cd /");
    test("cd /etc");
    test("cd $HOME");
    test("cd ~");

@suite
def suite_unset(test):
    test("unset A", setup="export A=a")

@suite
def suite_pwd(test):
    test("pwd")
    test("pwd", setup="cd ..")
    test("pwd", setup="cd ../..")
    test("pwd", setup="cd ../../..")
    test("pwd", setup="cd /")
    test("pwd", setup="cd $HOME")

@suite
def suite_env(test):
    test("env")
    test("env", setup="export A=a")
    test("env", setup="export A=a B=b C=c")

@suite
def suite_exit(test):
    test("exit")
    test("exit 1")
    test("exit 2")
    test("exit 3")
