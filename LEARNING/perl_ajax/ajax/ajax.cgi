#!/usr/bin/perl
# @(#) $Id: ajax.cgi 613 2006-01-24 19:31:08Z dom $
# User registration script.
use strict;
use warnings;
use CGI;
use CGI::Ajax;
my $cgi  = CGI->new();
my $ajax = CGI::Ajax->new( check_username => \&check_username );
$ajax->JSDEBUG(1);
print $ajax->build_html( $cgi, \&main );

sub check_username {
    my ( $user ) = @_;
    return unless -f '/tmp/users.txt';
    open my $fh, '<', '/tmp/users.txt'
      or return "open(/tmp/users.txt): $!";
    while (<$fh>) {
        chomp;
        return "Username '$user' taken!" if lc $_ eq lc $user;
    }
    return '';
}

sub save_username {
    my ( $user ) = @_;
    open my $fh, '>>', '/tmp/users.txt'
      or die "open(>>/tmp/users.txt): $!";
    print $fh "$user\n";
    close $fh;
    return;
}

sub main {
    my $html = <<HTML;
<html><head>
<title>Signup!</title>
<script type="text/javascript" src="binding.js"></script>
</head><body>
<h1>Signup!</h1>
HTML
    if ( my $user = $cgi->param('user') ) {
        my $err = check_username( $user );
        if ( $err ) {
            $html .= "<p class='problem'>$err</p>";
        } else {
            save_username( $user );
            $html .= "<p>Account <em>$user</em> created!</p>\n";
        }
    }
    my $url = $cgi->url(-relative => 1);
    $html .= <<HTML;
<form action="$url" method="post">
<p>Please fill in the details to create a new Account.</p>
<p>Username: <input type="text" name="user" id="user"/>
<em id="baduser"></em></p>
<p>Password: <input type="password" name="pass" id="pass"/></p>
<p><input type="submit" name="submit" value="SIGNUP"/></p>
</form></body></html>
HTML
    return $html;
}

exit 0;
__END__
