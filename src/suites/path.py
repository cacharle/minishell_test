# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    path.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/09 15:12:58 by charles           #+#    #+#              #
#    Updated: 2020/09/09 15:39:17 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config
from suite import suite

@suite
def suite_path(test):
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 001 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 002 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 003 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 004 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 005 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 006 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 007 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 010 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 020 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 030 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 040 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 050 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 060 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 070 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 100 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 200 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 300 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 400 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 500 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 600 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 700 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 755 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 644 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 311 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 111 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 222 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 333 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 0777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 1000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 2000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 3000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 4000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 5000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 6000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 7000 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 1777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 2777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 3777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 4777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 5777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 6777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 7777 ./path/a", exports={"PATH": "path"})
    test("a", setup="mkdir path && cp /bin/ls ./path/a && chmod 0000 ./path/a", exports={"PATH": "path"})

    test("b", setup="mkdir path && cp /bin/ls ./path/a && ln -s ./path/a ./path/b", exports={"PATH": "path"})

    test("ls", exports={"PATH": "doesnotexits"})
    test("ls", exports={"PATH": "doesnotexits:asdfasdfas"})
    test("ls", exports={"PATH": "a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z"})
    test("ls", exports={"PATH": "________"})
    test("ls", exports={"PATH": "        "})
    test("ls", exports={"PATH": "   :    "})
    test("ls", exports={"PATH": "     /bin      "})
