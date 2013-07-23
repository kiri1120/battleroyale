#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";


    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    open(DB,"$area_file");seek(DB,0,0); @arealist=<DB>;close(DB);
    ($ar,$a) = split(/,/, $arealist[1]);

    ($ar,$hackflg,$a) = split(/,/, $arealist[1]);
    ($ara[0],$ara[1],$ara[2],$ara[3],$ara[4],$ara[5],$ara[6],$ara[7],$ara[8],$ara[9],
        $ara[10],$ara[11],$ara[12],$ara[13],$ara[14],$ara[15],$ara[16],$ara[17],$ara[18],$ara[19],
        $ara[20],$ara[21]) = split(/,/, $arealist[4]);

    for ($j=0; $j<$#area+1; $j++) {
        $mem[$j] = "$place[$j]" ;
    }

    if ($hackflg == 0) {
        for ($j=0; $j<$ar; $j++) {
            $mem[$ara[$j]] = "<FONT color=\"#ff0000\">$place[$ara[$j]]</FONT>";
        }

        $mem[$ara[$j]] = "<FONT color=\"yellow\">$place[$ara[$j]]</FONT>";
        $mem[$ara[$j+1]] = "<FONT color=\"yellow\">$place[$ara[$j+1]]</FONT>";
        $mem[$ara[$j+2]] = "<FONT color=\"yellow\">$place[$ara[$j+2]]</FONT>";
    }

    &HEADER ;

print <<"_HERE_";

<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">会場簡易地図</FONT></B><BR></P>
<CENTER>

<TABLE border="1" height="550" cellspacing="0">
  <COL span="11" width="50">
  <TBODY>
    <TR bgcolor="#cccccc">
      <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000">　</FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０１</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０２</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０３</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０４</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０５</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０６</FONT></B></FONT></TD>
      <TD align="center" valign="middle" width="45"><FONT color="#000000"><B><FONT size="5">０７</FONT></B></FONT></TD>
      <TD align="center" valign="middle" width="47"><FONT color="#000000"><B><FONT size="5">０８</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">０９</FONT></B></FONT></TD>
      <TD align="center" valign="middle"><FONT color="#000000"><B><FONT size="5">１０</FONT></B></FONT></TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">A</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle"><B>$mem[1]</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff" width="45">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff" width="47">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5"><FONT size="5">B</FONT></FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[2]</B></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" width="45" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" width="47" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">C</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[3]</B></TD>
      <TD align="center" valign="middle"><B>$mem[4]</B></TD>
      <TD align="center" valign="middle"><B>$mem[5]</B></TD>
      <TD align="center" valign="middle"><B>$mem[6]</B></TD>
      <TD align="center" valign="middle" width="45">　</TD>
      <TD align="center" valign="middle" width="47" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">D</FONT></B></FONT></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[7]</B></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[0]</B></TD>
      <TD align="center" valign="middle" width="45">　</TD>
      <TD align="center" valign="middle" width="47">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">E</FONT></B></FONT></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[8]</B></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[9]</B></TD>
      <TD align="center" valign="middle"><B>$mem[10]</B></TD>
      <TD align="center" valign="middle"><B>$mem[10]</B></TD>
      <TD align="center" valign="middle" width="45"><B>$mem[11]</B></TD>
      <TD align="center" valign="middle" width="47">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">F</FONT></B></FONT></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[12]</B></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[10]</B></TD>
      <TD align="center" valign="middle"><B>$mem[10]</B></TD>
      <TD align="center" valign="middle" width="45"><B>$mem[10]</B></TD>
      <TD align="center" valign="middle" width="47">　</TD>
      <TD align="center" valign="middle"><B>$mem[13]</B></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">G</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[14]</B></TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD valign="middle" align="center"><B>$mem[15]</B></TD>
      <TD align="center" valign="middle" width="45">　</TD>
      <TD align="center" valign="middle" width="47">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">H</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[16]</B></TD>
      <TD align="center" valign="middle"><B>$mem[16]</B></TD>
      <TD align="center" valign="middle"><B>$mem[17]</B></TD>
      <TD align="center" valign="middle" width="45"><B>　</B></TD>
      <TD align="center" valign="middle" width="47">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">I</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[18]</B></TD>
      <TD align="center" valign="middle" width="45"><B>$mem[19]</B></TD>
      <TD align="center" valign="middle" width="47" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle">　</TD>
      <TD align="center" valign="middle"><B>$mem[20]</B></TD>
    </TR>
    <TR>
     <TD height="50" valign="middle" align="center" bgcolor="#cccccc"><FONT color="#000000"><B><FONT size="5">J</FONT></B></FONT></TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle"><B>$mem[21]</B></TD>
      <TD align="center" valign="middle" width="45" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff" width="47">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
      <TD align="center" valign="middle" bgcolor="#00ffff">　</TD>
    </TR>
  </TBODY>
</TABLE>
</CENTER>
_HERE_

    &FOOTER;
&UNLOCK;

exit;
