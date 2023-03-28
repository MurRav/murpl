#!/usr/bin/perl -wT

package News;
use strict;

use Fcntl qw( :flock );

my $NEWS_DIR = "/usr/local/apache/data/news";

1;


sub get_stories {
    my @stories = ();
    local( *DIR, *STORY );
    
    opendir DIR, $NEWS_DIR or die "Cannot open $NEWS_DIR: $!";
    while ( defined( my $file = readdir DIR ) ) {
        next if $file =~ /^\./;       # skip . and ..
        open STORY, "$NEWS_DIR/$file" or next;
        flock STORY, LOCK_SH;
        my $headline = <STORY>;
        close STORY;
        chomp $headline;
        push @stories, [ $file, $headline, get_date( $file ) ];
    }
    closedir DIR;
    return sort { $a->[0] <=> $b->[0] } @stories;
}


# Returns standard Unix timestamp without the time, just the date
sub get_date {
    my $filename = shift;
    ( my $date = localtime $filename ) =~ s/ +\d+:\d+:\d+/,/;
    return $date;
}


sub get_story {
    my( $filename ) = shift() =~ /^(\d+)$/;
    my( $headline, $article );
    
    unless ( defined( $filename ) and -T "$NEWS_DIR/$filename" ) {
        return "Story Not Found", <<END_NOT_FOUND, get_time( time );
<P>Oops, the story you requested was not found.</P>
<P>If a link on our What's New page brought you here, please
notify the <A HREF="mailto:$ENV{SERVER_ADMIN}">webmaster</A>.</P>
END_NOT_FOUND
    }
    
    open STORY, "$NEWS_DIR/$filename" or
      die "Cannot open $NEWS_DIR/$filename: $!";
    flock STORY, LOCK_SH;
    $headline = <STORY>;
    chomp $headline;
    local $/ = undef;
    $article = <STORY>;
    
    return $headline, $article, get_date( $filename );
}


sub save_story {
    my( $story, $headline, $article ) = @_;
    local *STORY;
    
    $story ||= time;                        # name new files based on time in secs
    $article =~ s/\015\012|\015|\012/\n/g;  # make line endings consistent
    $headline =~ tr/\015\012//d;            # delete any line endings just in case
    
    my( $file ) = $story =~ /^(\d+)$/ or die "Illegal filename: '$story'";
    
    open STORY, "> $NEWS_DIR/$file";
    flock STORY, LOCK_EX;
    print STORY $headline, "\n", $article;
    close STORY;
}


sub delete_story {
    my $story = shift;
    
    my( $file ) = $story =~ /^(\d+)$/ or die "Illegal filename: '$story'";
    unlink "$NEWS_DIR/$file" or die "Cannot remove story $NEWS_DIR/$file: $!";
}
