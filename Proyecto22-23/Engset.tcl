#!/usr/bin/tclsh
set tcl_precision 17

proc Engset {N m alpha} {
    set a [expr $alpha + 0.0]
    for {set i 1; set B 1.0} {$i <= $m} {incr i} {
	set B [expr 1 + $i/($a*($N-$i))*$B]
    }
    set B [expr 1/$B]
    return $B
}


proc uso {} { 
    global argv0
    puts "Uso: $argv0 N m α"
    puts "Salida: B"
    puts "N,m  ℤ   α  ℝ"
}

if {$argc != 3} {
    uso
    exit 2
}

foreach {N m alpha} $argv {}
if {! [string is integer $N] || ! [string is integer $m] ||  ![string is double $alpha]} {
    uso
    exit 3
}

set B [Engset $N $m $alpha]

puts "$B"
