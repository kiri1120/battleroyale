#==================#
# ■ レーダー処理  #
#==================#
sub READER {

    if ($item[$wk] !~ /R/) {&ERROR("不正なアクセスです。") ;}

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    open(DB,"$area_file");seek(DB,0,0); @arealist=<DB>;close(DB);

    ($ar,$hackflg,$a) = split(/,/, $arealist[1]);
    @ara = split(/,/, $arealist[4]);

    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);
        for ($j=0; $j<$#area+1; $j++) {
            if (($w_pls eq $j)&&($w_hit > 0)) {
                $mem[$j] += 1;last;
            }
        }
    }


    if ($item[$wk] =~ /<>R2/) {
        for ($j=0; $j<$#area+1; $j++) {
            if ($j == $pls) {
                $wk = $mem[$j];
                $mem[$j] = "<FONT color=\"#ff0000\"><b>$wk<b></FONT>";
            } elsif ($mem[$j] <= 0) {
                $mem[$j] = "　" ;
            }
        }
    } else {
        for ($j=0; $j<$#area+1; $j++) {
            if ($j == $pls) {
                $wk = $mem[$j];
                $mem[$j] = "<FONT color=\"#ff0000\"><b>$wk<b></FONT>";
            } else {
                $mem[$j] = "　" ;
            }
        }
    }
  if ($hackflg == 0) {
    for ($j=0; $j<$ar; $j++) {
        $mem[$ara[$j]] = "<FONT color=\"#ff0000\"><b>×<b></FONT>";
    }
  }

print <<"_HERE_";
<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">$place[$pls]（$area[$pls]）</FONT></B><BR></P>
<TABLE width="568">
<TR><TD><B><FONT color="#ff0000">
@links
</FONT></B></TD></TR>
</TABLE>
<TABLE width="568">
  <TBODY>
    <TR>
      <TD valign="top" width="279" height="311">
    <TABLE border="1" width="389" height="300">
        <TBODY align="center" valign="middle">
          <TR>
            <TD>　</TD>
            <TD>01</TD>
            <TD>02</TD>
            <TD>03</TD>
            <TD>04</TD>
            <TD>05</TD>
            <TD>06</TD>
            <TD>07</TD>
            <TD>08</TD>
            <TD>09</TD>
            <TD>10</TD>
          </TR>
          <TR>
            <TD>A</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>$mem[1]</TD>
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
            <TD>B</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>$mem[2]</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>C</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>$mem[3]</TD>
            <TD>$mem[4]</TD>
            <TD>$mem[5]</TD>
            <TD>$mem[6]</TD>
            <TD>　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>D</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>$mem[7]</TD>
            <TD>　</TD>
            <TD>$mem[0]</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>E</TD>
            <TD>　</TD>
            <TD>$mem[8]</TD>
            <TD>　</TD>
            <TD>$mem[9]</TD>
            <TD>$mem[10]</TD>
            <TD>　</TD>
            <TD>$mem[11]</TD>
            <TD>　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>F</TD>
            <TD>　</TD>
            <TD>$mem[12]</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>$mem[13]</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>G</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>$mem[14]</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>$mem[15]</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>H</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>$mem[16]</TD>
            <TD>　</TD>
            <TD>$mem[17]</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
          <TR>
            <TD>I</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>　</TD>
            <TD>$mem[18]</TD>
            <TD>$mem[19]</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>　</TD>
            <TD>$mem[20]</TD>
          </TR>
          <TR>
            <TD>J</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD>$mem[21]</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
            <TD bgcolor="#00ffff">　</TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" width="200" height="311">
      <TABLE border="1" cellspacing="0">
        <TBODY>
          <TR><TD align="center" width="250"><B>コマンド</B></TD>
          <TR>
            <TD align="left" valign="top" width="190" height="280">
            <FORM METHOD="POST">
            <INPUT TYPE="HIDDEN" NAME="mode" VALUE="command">
            <INPUT TYPE="HIDDEN" NAME="Id" VALUE="$id2">
            <INPUT TYPE="HIDDEN" NAME="Password" VALUE="$password2">
_HERE_

            &COMMAND;

print <<"_HERE_";
            </FORM>
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
    </TR>
    <TR>
      <TD colspan="2" valign="top" height="101">
      <TABLE border="1" cellspacing="0" height="150" cellpadding="0">
        <TBODY>
          <TR>
            <TD height="20" valign="top" width="600">レーダーを使用した。<BR><BR>数字：エリアにいる人数<BR>赤数字：自分がいるエリアの人数</TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
    </TR>
  </TBODY>
</TABLE>
_HERE_

$mflg="ON"; #ステータス非表示
}

1;
