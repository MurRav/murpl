#!/usr/bin/perl -wT

#/----------------------------------------------------------------
# UserTracker Package
# 
# Inherits from HTML::Parser
# 
# 

package UserTracker;

push @ISA, "HTML::Parser";

use strict;
use URI;
use HTML::Parser;

my $GLOBAL_COUNT = 0;

1;


#/----------------------------------------------------------------
# Public methods
# 

sub new {
    my( $class, $path ) = @_;
    my $id;
    
    my $self = $class->SUPER::new();
    
    $self->base_path( $path ) if defined $path;
    
    return $self;
}

sub base_path {
    my( $self, $path ) = @_;
    my $id;
    
    if ( defined $path ) {
        $self->{base_path} = $path;
        if ( $ENV{PATH_INFO} ) {
            if ( $ENV{PATH_INFO} =~ s|^/$self->{base_path}/\.([a-zA-Z0-9_.-]*)/|/| ) {
                $id = $1;
            }
        }
        $id ||= $self->unique_id;
        $self->user_id( $id );
    }
    return defined( $self->{base_path} ) ? $self->{base_path} : "";
}

sub user_id {
    my( $self, $user_id ) = @_;
    $self->{user_id} = $user_id if defined $user_id;
    $self->{user_id} ||= $self->unique_id;
    
    return $self->{user_id};
}


#/----------------------------------------------------------------
# Internal (protected) methods
# 

sub unique_id {
    my $self = shift;
    # Use Apache's mod_unique_id if available
    return $ENV{UNIQUE_ID} || eval {
        require Digest::MD5;
        my $md5 = new Digest::MD5;
        my $semi_unique = defined( $$ ) ?
            $$ : $ENV{REMOTE_ADDR} . $ENV{REMOTE_PORT};
        my $id = $md5->md5_base64( time, $semi_unique, $GLOBAL_COUNT++ );
        $id =~ tr|+/=|-_.|;
        $id;
    } || die "Unable to generate unique identifier for cookie\n";
}

sub encode {
    my( $self, $url ) = @_;
    my $uri  = new URI( $url, "http" );
    my $id   = $self->user_id();
    my $base = $self->base_path;
    my $path = $uri->path;
    
    $path =~ s|^$base|$base/.$id|;
    $uri->path( $path );
    
    return $uri->as_string;
}


#/----------------------------------------------------------------
# Subs to implement HTML::Parser callbacks
# 

sub start {
    my( $self, $tag, $attr, $attrseq, $origtext ) = @_;
    my $new_text = $origtext;
    
    my %relevant_pairs = (
        frameset    => "src",
        a           => "href",
        area        => "href",
        form        => "action",
# Uncomment these lines if you want to track images too
#        img         => "src",
#        body        => "background",
    );
    
    while ( my( $rel_tag, $rel_attr ) = each %relevant_pairs ) {
        if ( $tag eq $rel_tag and $attr->{$rel_attr} ) {
            $attr->{$rel_attr} = $self->encode( $attr->{$rel_attr} );
            my @attribs = map { "$_=\"$attr->{$_}\"" } @$attrseq;
            $new_text = "<$tag @attribs>";
        }
    }
    
    # Meta refresh tags have a different format, handled separately
    if ( $tag eq "meta" and $attr->{"http-equiv"} eq "refresh" ) {
        my( $delay, $url ) = split ";URL=", $attr->{content}, 2;
        $attr->{content} = "$delay;URL=" . $self->encode( $url );
        my @attribs = map { "$_=\"$attr->{$_}\"" } @$attrseq;
        $new_text = "<$tag @attribs>";
    }
    
    print $new_text;
}

sub declaration {
    my( $self, $decl ) = @_;
    print $decl;
}

sub text {
    my( $self, $text ) = @_;
    print $text;
}

sub end {
    my( $self, $tag ) = @_;
    print "</$tag>";
}

sub comment {
    my( $self, $comment ) = @_;
    print "<!--$comment-->";
}
