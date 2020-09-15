# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    path.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/09 15:12:58 by charles           #+#    #+#              #
#    Updated: 2020/09/15 14:10:37 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from suite import suite


@suite()
def suite_path(test):
    mode_fmt = "mkdir path && cp /bin/whoami ./path/a && chmod {} ./path/a"
    test("a", setup=mode_fmt.format("000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("001"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("002"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("003"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("004"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("005"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("006"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("007"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("010"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("020"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("030"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("040"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("050"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("060"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("070"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("100"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("200"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("300"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("400"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("500"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("600"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("700"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("755"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("644"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("311"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("111"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("222"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("333"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("0777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("1000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("2000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("3000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("4000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("5000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("6000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("7000"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("1777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("2777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("3777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("4777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("5777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("6777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("7777"), exports={"PATH": "path"})
    test("a", setup=mode_fmt.format("0000"), exports={"PATH": "path"})
    test("b", setup="mkdir path && cp /bin/whoami ./path/a && ln -s ./path/a ./path/b", exports={"PATH": "path"})
    test("b", setup="mkdir path && ln -s /bin/whoami ./path/b", exports={"PATH": "path"})
    test("a", setup="mkdir path && mkfifo path/a")
    test("a", setup="mkdir path && mkfifo path/a && chmod 777 path/a")
    test("a", setup="mkdir path1 path2 && cp /bin/whoami path1/a"
         "&& cp /bin/whoami path2/a && chmod 000 path1/a", exports={"PATH": "path1:path2"})
    test("a", setup="mkdir path1 path2 && cp /bin/whoami path1/a"
         "&& cp /bin/whoami path2/a && chmod 000 path1/a", exports={"PATH": "path2:path1"})


@suite()
def suites_path_variable(test):
    test("echo $PATH", exports={"PATH": "doesnotexits"})
    test("echo $PATH", exports={"PATH": "doesnotexits:asdfasdfas"})
    test("echo $PATH", exports={"PATH": "a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z"})
    test("echo $PATH", exports={"PATH": "________"})
    test("echo $PATH", exports={"PATH": "        "})
    test("echo $PATH", exports={"PATH": "   :    "})
    test("echo $PATH", exports={"PATH": "     /bin      "})
    test("echo $PATH", exports={"PATH": "     /sbin      "})
    test("echo $PATH", exports={"PATH": "/bin:/bin:/bin:/bin"})
    test("echo $PATH", exports={"PATH": "/sbin:/sbin:/sbin:/sbin"})
    test("echo $PATH", exports={"PATH": ""})
    test("echo $PATH", exports={"PATH": ":"})
    test("echo $PATH", exports={"PATH": ":::::::::::::::::::"})
    test("echo $PATH", exports={"PATH": "/asdfasdf"})
    test("echo $PATH", exports={"PATH": "/usr/asdf:/usr/lib/asdfasdf"})
    test("whoami", exports={"PATH": "doesnotexits"})
    test("whoami", exports={"PATH": "doesnotexits:asdfasdfas"})
    test("whoami", exports={"PATH": "a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z"})
    test("whoami", exports={"PATH": "________"})
    test("whoami", exports={"PATH": "        "})
    test("whoami", exports={"PATH": "   :    "})
    test("whoami", exports={"PATH": "     /bin      "})
    test("whoami", exports={"PATH": "/bin:/bin:/bin:/bin"})
    test("whoami", exports={"PATH": "     /sbin      "})
    test("whoami", exports={"PATH": "/sbin:/sbin:/sbin:/sbin"})
    test("whoami", exports={"PATH": ""})
    test("whoami", exports={"PATH": ":"})
    test("whoami", exports={"PATH": ":::::::::::::::::::"})
    test("whoami", exports={"PATH": "/asdfasdf"})
    test("whoami", exports={"PATH": "/usr/asdf:/usr/lib/asdfasdf"})
    test("whoami", setup="unset PATH")
    create_cmd_setup = "echo '#!/bin/sh\necho bonjour' > somecmd; chmod +x somecmd"
    test("somecmd", setup=create_cmd_setup, exports={"PATH": ""})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": ":"})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": "::::::::"})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": "/asdfasdf"})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": "/usr/asdf:/usr/lib/asdfasdf"})
    test("somecmd", setup=create_cmd_setup + "; unset PATH")
    test("somecmd", setup=create_cmd_setup, exports={"PATH": "/bin:"})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": ":/bin"})
    test("somecmd", setup=create_cmd_setup, exports={"PATH": ":/bin:"})
