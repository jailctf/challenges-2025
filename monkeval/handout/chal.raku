#!/usr/bin/raku

$*OUT.out-buffer = False;
$*ERR.out-buffer = False;

# 🙈🙈🙈
sub MONKEY-SEE-NO-EVAL { 1 }

constant @allowed-charset = '()0123456789+-*/^~<=>$_ '.comb;

loop {
    my $input = prompt 'Enter a math expression: ';

    exit if $input eq 'exit';

    if $input.comb ⊈ @allowed-charset {
        say 'Invalid expression!';
        next;
    }

    $_ = EVAL($input);
    say $_;
}
