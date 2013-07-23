#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";


    @ara = split(/,/, $arealist[4]);

    for ($j=0; $j<$#area+1; $j++) {
        $mem[$j] = "$place[$j]" ;
    }

    if ($hackflg) {
        $areacolor = "#ffff00";
    } else {
        $areacolor = "#ff0000";
    }

    for ($j=0; $j<$ar; $j++) {
        $mem[$ara[$j]] = "<FONT color=\"$areacolor\">$place[$ara[$j]]</FONT>";
    }
    $mem[$ara[$j]] = "<FONT color=\"yellow\">$place[$ara[$j]]</FONT>";
    $mem[$ara[$j+1]] = "<FONT color=\"yellow\">$place[$ara[$j+1]]</FONT>";
    $mem[$ara[$j+2]] = "<FONT color=\"yellow\">$place[$ara[$j+2]]</FONT>";

    &HEADER ;

print <<"_HERE_";

<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">会場簡易地図</FONT></B><BR></P>
<CENTER>

<TABLE border="1" height="550" cellspacing="0">
  <COL span="11" width="50">
  <TBODY align="center" valign="middle">
    <TR bgcolor="#cccccc">
      <TD height="50" bgcolor="#cccccc">　</TD>
      <TD><FONT color="#000000" size="5"><B>０１</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０２</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０３</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０４</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０５</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０６</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０７</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０８</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>０９</B></FONT></TD>
      <TD><FONT color="#000000" size="5"><B>１０</B></FONT></TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>A</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD><B>$mem[1]</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>B</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD><B>$mem[2]</B></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>C</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD><B>$mem[3]</B></TD>
      <TD><B>$mem[4]</B></TD>
      <TD><B>$mem[5]</B></TD>
      <TD><B>$mem[6]</B></TD>
      <TD>　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>D</B></FONT></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD><B>$mem[7]</B></TD>
      <TD>　</TD>
      <TD><B>$mem[0]</B></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>E</B></FONT></TD>
      <TD>　</TD>
      <TD><B>$mem[8]</B></TD>
      <TD>　</TD>
      <TD><B>$mem[9]</B></TD>
      <TD><B>$mem[10]</B></TD>
      <TD><B>$mem[10]</B></TD>
      <TD><B>$mem[11]</B></TD>
      <TD>　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>F</B></FONT></TD>
      <TD>　</TD>
      <TD><B>$mem[12]</B></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD><B>$mem[10]</B></TD>
      <TD><B>$mem[10]</B></TD>
      <TD><B>$mem[10]</B></TD>
      <TD>　</TD>
      <TD><B>$mem[13]</B></TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>G</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD><B>$mem[14]</B></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD><B>$mem[15]</B></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>H</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD><B>$mem[16]</B></TD>
      <TD><B>$mem[16]</B></TD>
      <TD><B>$mem[17]</B></TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>I</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD>　</TD>
      <TD><B>$mem[18]</B></TD>
      <TD><B>$mem[19]</B></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD>　</TD>
      <TD><B>$mem[20]</B></TD>
    </TR>
    <TR>
     <TD height="50" bgcolor="#cccccc"><FONT color="#000000" size="5"><B>J</B></FONT></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD><B>$mem[21]</B></TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
      <TD bgcolor="#00ffff">　</TD>
    </TR>
  </TBODY>
</TABLE>
</CENTER>
_HERE_

    &FOOTER;
&UNLOCK;

exit;
