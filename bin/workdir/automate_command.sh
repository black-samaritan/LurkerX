#!/usr/bin/expect -f

set command [lindex $argv 0]
set value [lindex $argv 1]
set expect [lindex $argv 2]
set timeout -1

spawn {*}$command

expect $expect
send "$value\r"

expect eof