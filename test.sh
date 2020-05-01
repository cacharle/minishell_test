#!/bin/sh

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.sh                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/05/01 10:54:53 by charles           #+#    #+#              #
#    Updated: 2020/05/01 10:54:53 by charles          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

case $# in
    0) config_file=minishell_test.config;;
    1) config_file=$1;;
    *) echo "Usage: $0 [config file]"; exit 1;;
esac

config_extract() {
    grep $1 $config_file | cut -d '=' -f 2
}

minishell_path=`config_extract minishell_path`
minishell_exec=`config_extract minishell_exec`
minishell_exec_path=$minishell_path/$minishell_exec
reference_shell_path=`config_extract reference_shell_path`
lorem_path=`config_extract lorem_path`
lorem=`cat $lorem_path`
pass_marker=`config_extract pass_marker`
fail_marker=`config_extract fail_marker`
log_file=`config_extract log_file`

# echo $minishell_path
# echo $minishell_exec
# echo $minishell_exec_path
# echo $lorem

if [ ! -f $minishell_exec_path ]; then
    echo "Error: $minishell_exec_path does not exist"
    exit 1
fi

red()              { echo -n "`tput setaf 1`$1`tput sgr 0`"; }
green()            { echo -n "`tput setaf 2`$1`tput sgr 0`"; }
put_pass_marker () { green $pass_marker; }
put_fail_marker () { red $fail_marker;   }

append_fail () {
    tested=$1
    expected=$2
    expected_status=$3
    actual=$4
    actual_status=$5
    echo "for $1"
}

expect() {
    expected=`$referecence_shell_path -c $1`
    expected_status=$?
    actual=`$minishell_exec_path -c $1`
    actual_status=$?
    ([ $expected = $actual ] && [ $expected_status -eq $actual_status ] && put_pass_marker)
        || (put_fail_marker &&
    echo <<EOF
for $1:
expected: $expected
actual:   $actual
status: expected: $expected_status actual: $actual_status

EOF
}

###############################################################################
# Builtin
###############################################################################

expect 'echo bonjour'
expect 'echo bonjour je suis'
expect "echo $lorem"
expect "echo $lorem $lorem $lorem $lorem"

