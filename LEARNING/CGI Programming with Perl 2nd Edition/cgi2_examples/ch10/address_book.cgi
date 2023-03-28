#!/usr/bin/perl -wT

use strict;

use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

use vars qw($DBH $CGI $TABLE @FIELD_NAMES @FIELD_DESCRIPTIONS);

$DBH = DBI->connect("DBI:CSV:f_dir=/usr/local/apache/data/address")
      or die "Cannot connect: " . $DBI::errstr;

@FIELD_NAMES = ("fname", "lname", "phone",
                  "dept", "location");

@FIELD_DESCRIPTIONS = ("First Name", "Last Name", "Phone",
                       "Department", "Location");

$TABLE = "address";

$CGI = new CGI();

if ($CGI->param( "submit_do_maintenance" ) ) {
  displayMaintenanceChoices( $CGI );
}
elsif ( $CGI->param( "submit_update" ) ) {
  doUpdate( $CGI, $DBH );
}
elsif ( $CGI->param( "submit_delete" ) ) {
  doDelete( $CGI, $DBH );
}
elsif ( $CGI->param( "submit_add" ) ) {
  doAdd( $CGI, $DBH );
}
elsif ( $CGI->param( "submit_enter_query_for_delete" ) ) {
  displayDeleteQueryScreen( $CGI );
}
elsif ( $CGI->param( "submit_enter_query_for_update" ) ) {
  displayUpdateQueryScreen( $CGI );
}
elsif ( $CGI->param( "submit_query_for_delete" ) ) {
  displayDeleteQueryResults( $CGI, $DBH );
}
elsif ( $CGI->param( "submit_query_for_update" ) ) {
  displayUpdateQueryResults( $CGI, $DBH );
}
elsif ( $CGI->param( "submit_enter_new_address" ) ) {
  displayEnterNewAddressScreen( $CGI );
}
elsif ( $CGI->param( "submit_query" ) ) {
  displayQueryResults( $CGI, $DBH );
}
else {
  displayQueryScreen( $CGI );
}


sub displayQueryScreen {
  my $cgi = shift;

  print $cgi->header();

print qq`
<HTML>
<HEAD>
<TITLE>Address Book</TITLE>
</HEAD>

<BODY BGCOLOR = "FFFFFF" TEXT = "000000">

<CENTER>
<H1>Address Book</H1> 
</CENTER>
<HR>

<FORM METHOD=POST>

<H3><STRONG>Enter Search criteria: </STRONG></H3>
<TABLE>
<TR>
  <TD ALIGN="RIGHT">First Name:</TD>
  <TD><INPUT TYPE="text" NAME="fname"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Last Name:</TD>
  <TD><INPUT TYPE="text" NAME="lname"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Phone:</TD>
  <TD><INPUT TYPE="text" NAME="PHONE"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Department:</TD>
  <TD><INPUT TYPE="text" NAME="dept"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Location:</TD>
  <TD><INPUT TYPE="text" NAME="location"></TD>
</TR>
</TABLE>
<P>

<INPUT TYPE="checkbox" NAME="exactmatch">
  <STRONG> Perform Exact Match</STRONG> 
  (Default search is case sensitive against partial word matches)
 <P>
<INPUT TYPE="submit" name="submit_query" value="Do Search">
<INPUT TYPE="submit" name="submit_do_maintenance" value="Maintain Database">
<INPUT TYPE="reset" value="Clear Criteria Fields">
</FORM>

<P><HR>

</BODY></HTML>
`;

} # end of displayQueryScreen


sub displayMaintenanceChoices {
  my $cgi = shift;
  my $message = shift;

  if ($message) {
    $message = $message . "\n<HR>\n";
  }

  print $cgi->header();

  print qq`<HTML>
<HEAD><TITLE>Address Book Maintenance</TITLE></HEAD>
 
<BODY BGCOLOR="FFFFFF">
<CENTER>
<H1>Address Book Maintenance</H1>
<HR>
$message
<P>

<FORM METHOD=POST>

<INPUT TYPE="SUBMIT" NAME="submit_enter_new_address" VALUE="New Address">
<INPUT TYPE="SUBMIT" NAME="submit_enter_query_for_update" VALUE="Update Address">
<INPUT TYPE="SUBMIT" NAME="submit_enter_query_for_delete" VALUE="Delete Address">
<INPUT TYPE="SUBMIT" NAME="submit_nothing" VALUE="Search Address">

</FORM>
</CENTER>
<HR>
</BODY></HTML>`;

} # end of displayMaintenanceChoices

sub displayAllQueryResults {
  my $cgi = shift;
  my $dbh = shift;
  my $op  = shift;

  my $ra_query_results = getQueryResults($cgi, $dbh);

  print $cgi->header();

  my $title;
  my $extra_column = "";
  my $form = "";
  my $center = "";
  if ($op eq "SEARCH") {
    $title = "AddressBook Query Results";
    $center = "<CENTER>";
  } elsif ($op eq "UPDATE") {
    $title = "AddressBook Query Results For Update";
    $extra_column = "<TH>Update</TH>";
    $form = qq`<FORM METHOD="POST">`;
  } else {
    $title = "AddressBook Query Results For Delete";
    $extra_column = "<TH>Delete</TH>";
    $form = qq`<FORM METHOD="POST">`;
  }

  print qq`<HTML>
<HEAD><TITLE>$title</TITLE></HEAD>
<BODY BGCOLOR="WHITE">
$center
<H1>Query Results</H1>
<HR>
$form
<TABLE BORDER=1>
`;

  print "<TR>$extra_column" 
        . join("\n", map("<TH>" . $_ . "</TH>", @FIELD_DESCRIPTIONS))
        . "</TR>\n";

  
  my $row;
  foreach $row (@$ra_query_results) { 
    print "<TR>";
    if ($op eq "SEARCH") {
      print join("\n", map("<TD>" . $_ . "</TD>", @$row));
    } elsif ($op eq "UPDATE") {
      print qq`\n<TD ALIGN="CENTER">
            <INPUT TYPE="radio" NAME="update_criteria" VALUE="` .
            join("|", @$row) . qq`"></TD>\n`;
      print join("\n", map("<TD>" . $_ . "</TD>", @$row));
    } else { # delete
      print qq`\n<TD ALIGN="CENTER">
            <INPUT TYPE="radio" NAME="delete_criteria" VALUE="` .
            join("|", @$row) . qq`"></TD>\n`;
      print join("\n", map("<TD>" . $_ . "</TD>", @$row));
    }
    print "</TR>\n";
  }

  print qq"</TABLE>\n";

  if ($op eq "UPDATE") {
    my $address_table = getAddressTableHTML();

    print qq`$address_table
      <INPUT TYPE="submit" NAME="submit_update" VALUE="Update Selected Row">
      <INPUT TYPE="submit" NAME="submit_do_maintenance" VALUE="Maintain Database">
      </FORM>
      `;
  } elsif ($op eq "DELETE") {
    print qq`<P>
      <INPUT TYPE="submit" NAME="submit_delete" VALUE="Delete Selected Row">
      <INPUT TYPE="submit" NAME="submit_do_maintenance" VALUE="Maintain Database">
      </FORM>
      `;
  } else {
    print "</CENTER>";
  }

  print "</BODY></HTML>\n";

}

sub getQueryResults {
  my $cgi = shift;
  my $dbh = shift;

  my @query_results;
  my $field_list = join(",", @FIELD_NAMES);
  my $sql = "SELECT $field_list FROM $TABLE";

  my %criteria = ();

  my $field;  
  foreach $field (@FIELD_NAMES) {
    if ($cgi->param($field)) {
      $criteria{$field} = $cgi->param($field);
    }
  }

  # build up where clause
  my $where_clause;
  if ($cgi->param('exactmatch')) {
    $where_clause = join(" and ", 
                    map ($_ 
                         . " = \"" 
                         . $criteria{$_} . "\"", (keys %criteria)));
  } else {
    $where_clause = join(" and ", 
                    map ($_ 
                         . " like \"%"
                         . $criteria{$_} . "%\"", (keys %criteria)));

  }
  $where_clause =~ /(.*)/;
  $where_clause = $1;

  $sql = $sql . " where " . $where_clause if ($where_clause);
  
  my $sth = $dbh->prepare($sql) 
           or die "Cannot prepare: " . $dbh->errstr();
  $sth->execute() or die "Cannot execute: " . $sth->errstr();

  my @row;
  while (@row = $sth->fetchrow_array()) {
    my @record = @row;
    push(@query_results, \@record);    
  }
  $sth->finish();

  return \@query_results;

} # end of getQueryResults

sub displayQueryResults {
  my $cgi = shift;
  my $dbh = shift;

  displayAllQueryResults($cgi,$dbh,"SEARCH");

} # end of displayQueryResults

sub displayUpdateQueryResults {
  my $cgi = shift;
  my $dbh = shift;

  displayAllQueryResults($cgi,$dbh,"UPDATE");

} # end of displayUpdateQueryResults 

sub displayDeleteQueryResults {
  my $cgi = shift;
  my $dbh = shift;

  displayAllQueryResults($cgi, $dbh, "DELETE");

} # end of displayDeleteQueryResults

sub doAdd {
  my $cgi = shift;
  my $dbh = shift;

  my @value_array = ();
  my @missing_fields = ();

  my $field;
  foreach $field (@FIELD_NAMES){
    my $value = $cgi->param($field);
    if ($value) {
      push(@value_array, "'" . $value . "'");
    } else {
      push(@missing_fields, $field);
    }
  }

  my $value_list = "(" . join(",", @value_array) . ")";
  $value_list =~ /(.*)/;
  $value_list = $1;
  my $field_list = "(" . join(",", @FIELD_NAMES) . ")";

  if (@missing_fields > 0) {
    my $error_message = 
      qq`<STRONG> Some Fields (` . join(",", @missing_fields) .
      qq`) Were Not
            Entered!
            Address Not Inserted.
         </STRONG>`;
    displayErrorMessage($cgi, $error_message);

  } else {

    my $sql = qq`INSERT INTO $TABLE $field_list VALUES $value_list`;
    my $sth = $dbh->prepare($sql) 
           or die "Cannot prepare: " . $dbh->errstr();
    $sth->execute() or die "Cannot execute: " . $sth->errstr();
    $sth->finish();
    
    displayMaintenanceChoices($cgi,"Add Was Successful!");    

  }

} # end of doAdd

sub doDelete {
  my $cgi = shift;
  my $dbh = shift;

  my $delete_criteria = $cgi->param("delete_criteria");
  if (!$delete_criteria) {
    my $error_message = 
      "<STRONG>You didn't select a record to delete!</STRONG>";
    displayErrorMessage($cgi, $error_message);
  } else {

    my %criteria = ();

    my @field_values = split(/\|/, $delete_criteria);  
    for (1..@FIELD_NAMES) {
      $criteria{$FIELD_NAMES[$_ - 1]} = 
        $field_values[$_ - 1];
    }

    # build up where clause
    my $where_clause;
    $where_clause = join(" and ", 
                    map ($_ 
                         . " = \"" 
                         . $criteria{$_} . "\"", (keys %criteria)));
    $where_clause =~ /(.*)/;
    $where_clause = $1;


    my $sql = qq`DELETE FROM $TABLE WHERE $where_clause`;
    my $sth = $dbh->prepare($sql) 
           or die "Cannot prepare: " . $dbh->errstr();
    $sth->execute() or die "Cannot execute: " . $sth->errstr();
    $sth->finish();
    
    displayMaintenanceChoices($cgi,"Delete Was Successful!");    

  }

} # end of doDelete

sub doUpdate {
  my $cgi = shift;
  my $dbh = shift;

  my $update_criteria = $cgi->param("update_criteria");
  if (!$update_criteria) {
    my $error_message = 
      "<STRONG>You didn't select a record to update!</STRONG>";
    displayErrorMessage($cgi, $error_message);
  } else {

    # build up set logic
    my $set_logic = "";
    my %set_fields = ();
    my $field;
    foreach $field (@FIELD_NAMES) {
      my $value = $cgi->param($field);
      if ($value) {
        $set_fields{$field} = $value;
      }
    }
    $set_logic = join(", ", 
                 map ($_ . " = \"" . $set_fields{$_} . "\"",
                 (keys %set_fields)));
    $set_logic = " SET $set_logic" if ($set_logic);
    $set_logic =~ /(.*)/;
    $set_logic = $1;

    my %criteria = ();

    my @field_values = split(/\|/, $update_criteria);  
    for (1..@FIELD_NAMES) {
      $criteria{$FIELD_NAMES[$_ - 1]} = 
        $field_values[$_ - 1];
    }

    # build up where clause
    my $where_clause;
    $where_clause = join(" and ", 
                    map ($_ 
                         . " = \"" 
                         . $criteria{$_} . "\"", (keys %criteria)));
    $where_clause =~ /(.*)/;
    $where_clause = $1;


    my $sql = qq`UPDATE $TABLE $set_logic` .
                  qq` WHERE $where_clause`;

    my $sth = $dbh->prepare($sql) 
           or die "Cannot prepare: " . $dbh->errstr();
    $sth->execute() or die "Cannot execute: " . $sth->errstr();
    $sth->finish();
    
    displayMaintenanceChoices($cgi,"Update Was Successful!");    

  }

} # end of doUpdate

sub displayEnterNewAddressScreen {
  my $cgi = shift;

  displayNewDeleteUpdateScreen($cgi, "ADD");

} # end of displayEnterNewAddressScreen

sub displayUpdateQueryScreen {
  my $cgi = shift;
 
  displayNewDeleteUpdateScreen($cgi, "UPDATE");

} # end of displayUpdateQueryScreen

sub displayDeleteQueryScreen {
  my $cgi = shift;

  displayNewDeleteUpdateScreen($cgi, "DELETE");

} # end of displayDeleteQueryScreen

sub displayNewDeleteUpdateScreen {
  my $cgi       = shift;
  my $operation = shift;

  my $address_op = "Enter New Address";
  $address_op = "Enter Search Criteria For Deletion" if ($operation eq "DELETE");
  $address_op = "Enter Search Criterio For Updates" if ($operation eq "UPDATE");

  print $cgi->header();

# Prints out the header
print qq`
<HTML><HEAD>
<TITLE>Address Book Maintenance</TITLE>
</HEAD>
 
<BODY BGCOLOR="FFFFFF">
 
<H1>$address_op</H1>

<HR>
<P>
<FORM METHOD=POST>
`;

if ($operation eq "ADD") {
  print "Enter The New Information In The Form Below\n";
} elsif ($operation eq "UPDATE") {
  print "Enter Criteria To Query On In The Form Below.<P>\nYou will then be 
  able to choose entries to modify from the resulting list.\n";
} else {
  print "Enter Criteria To Query On In The Form Below.<P>\nYou will then be 
  able to choose entries to delete from the resulting list.\n"
}

my $address_table = getAddressTableHTML();
print qq`
<HR>
<P>

$address_table
`;

if ($operation eq "ADD") {
      print qq`
      <P>
      <INPUT TYPE="submit" NAME="submit_add" 
      VALUE="Add This New Address"><P>
      `; 
} elsif ($operation eq "UPDATE") {
      print qq`      <INPUT TYPE="checkbox" NAME="exactsearch">
      <STRONG>Perform Exact Search</STRONG>
      <P>
      <INPUT TYPE="submit" NAME="submit_query_for_update"
      VALUE="Query For Modification">
      <P>
      `;
} else {
      print qq`
      <INPUT TYPE="checkbox" NAME="exactsearch">
      <STRONG>Perform Exact Search</STRONG>
      <P>
      <INPUT TYPE="submit" NAME="submit_query_for_delete"
      VALUE="Query For List To Delete">
      <P>
      `;
}

# print the HTML footer.

print qq`
<INPUT TYPE="reset" VALUE="Clear Form">
</FORM>
</BODY></HTML> 
`;

} # end of displayNewUpdateDeleteScreen
sub displayErrorMessage {
  my $cgi = shift;
  my $error_message = shift;


  print $cgi->header();

  print qq`
<HTML>
<HEAD><TITLE>Error Message</TITLE></HEAD>
<BODY BGCOLOR="WHITE">
<H1>Error Occurred</H1>
<HR>
$error_message
<HR>
</BODY>
</HTML>
`;

} # end of displayErrorMessage

sub getAddressTableHTML {

return qq`
<TABLE>
<TR>
  <TD ALIGN="RIGHT">First Name:</TD>
  <TD><INPUT TYPE="text" NAME="fname"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Last Name:</TD>
  <TD><INPUT TYPE="text" NAME="lname"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Phone:</TD>
  <TD><INPUT TYPE="text" NAME="phone"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Department:</TD>
  <TD><INPUT TYPE="text" NAME="dept"></TD>
</TR>
<TR>
  <TD ALIGN="RIGHT">Location:</TD>
  <TD><INPUT TYPE="text" NAME="location"></TD>
</TR>
</TABLE>
`;

} # end of getAddressTableHTML
