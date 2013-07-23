#==================#
# ■ メッセ 設定   #
#==================#

$listmax = 300;  # メッセージ保管数
$mesmax = 10;   # 最大表示メッセージ件数
$mes = 100;     # １件の最大メッセージ長

$mesall = 1;    # 全員宛メッセージ（off:0 / on:1）

$col_to   = "#ff0000";  # 受信メッセージの色
$col_from = "#00ffff";  # 発信メッセージの色
$col_all  = "#ffffff";  # 全員宛メッセージの色
$col_adm  = "#ffff00";  # 管理人宛メッセージの色
$col_grp  = "#00ff00";  # グループ宛メッセージの色

#==================#
# ■ メッセ メイン #
#==================#
sub MESMAIN {

    local($hitbarleng) = 0; if ($hit > 0) { $hitbarleng = int($hit / $mhit * 45); }
    local($hitbarlenr) = 45 - $hitbarleng;
    local($stabarleng) = int($sta / $maxsta * 45);
    local($stabarlenr) = 45 - $stabarleng;

    $up = ($level * $level) + ($level * $baseexp);

    $kega ="" ;
    if ($inf =~ /頭/) {$kega = ($kega . "頭部　") ;}
    if ($inf =~ /腕/) {$kega = ($kega . "腕　") ;}
    if ($inf =~ /腹/) {$kega = ($kega . "腹部　") ;}
    if ($inf =~ /足/) {$kega = ($kega . "足　") ;}
    if ($inf =~ /毒/) {$kega = ($kega . "毒　") ;}
    if ($inf =~ /狂/) {$kega = ($kega . "狂気　") ;}
    if ($kega eq "") { $kega = "　" ;}

    local($w_name,$w_kind) = split(/<>/, $wep);
    if (($we eq "B") && ($w_kind =~ /B/)) { $tactics2 = "棍"; }
    elsif (($we eq "P") && ($w_kind =~ /P/)) { $tactics2 = "殴"; }
    elsif (($we eq "A") && ($w_kind =~ /A/) && ($wtai > 0)) { $tactics2 = "弓"; }
    elsif (($we eq "G") && ($w_kind =~ /G/) && ($wtai > 0)) { $tactics2 = "銃"; }
    elsif (($we eq "N") && ($w_kind =~ /N/)) { $tactics2 = "斬"; }
    elsif (($we eq "S") && ($w_kind =~ /S/)) { $tactics2 = "刺"; }
    elsif (($we eq "D") && ($w_kind =~ /D/)) { $tactics2 = "爆"; }
    elsif (($we eq "C") && ($w_kind =~ /C/)) { $tactics2 = "投"; }
    else { $tactics2 = "指定無し"; }

    local($tension);
    if($feel == 300) {
        $tension = "<font color=\"red\">超越</font>";
    }elsif($feel > 240) {
        $tension = "<font color=\"orange\">超強気</font>";
    }elsif($feel > 180) {
        $tension = "<font color=\"yellow\">強気</font>";
    }elsif($feel > 120) {
        $tension = "<font color=\"lime\">普通</font>";
    }elsif($feel > 60) {
        $tension = "<font color=\"aqua\">弱気</font>";
    }elsif($feel > 0) {
        $tension = "<font color=\"blue\">鬱</font>";
    }else{
        $tension = "<font color=\"fuchsia\">混乱</font>";
    }

    $nowtime = sprintf("%04d年%02d月%02d日（%s）%02d:%02d:%02d",$year, $month, $mday, ('日','月','火','水','木','金','土') [$wday], $hour, $min, $sec);

    open(DB,"$MES_DIR/$mes_file");seek(DB,0,0); @mes_list=<DB>;close(DB);

    $chkmes ="OFF"; $mes_i = 0;
    foreach (0 .. $#mes_list) {
        ($to,$from,$message,$mestime) = split(/,/, $mes_list[$_]);
        ($how,$to_id) = split(/_/, $to);
        if ($how eq "id") {
            #受信
            if ($id eq $to_id) {
                $chkmes ="ON";
                push(@log,"<font color=\"$col_to\">$message</font> [$mestime]<br>\n");
                if ($mesmax <= $mes_i++) { last; }
            #送信
            } elsif ($id eq $from) {
                $chkmes ="ON";
                push(@log,"<font color=\"$col_from\">$message</font> [$mestime]<br>\n");
                if ($mesmax <= $mes_i++) { last; }
            }
        #グループ
        } elsif (($how eq "group") && ($group eq $to_id)) {
            $chkmes ="ON";
            push(@log,"<font color=\"$col_grp\">$message</font> [$mestime]<br>\n");
            if ($mesmax <= $mes_i++) { last; }
        #管理人
        } elsif (($how eq "admin") && (($id eq $from) || ($id eq "kiri1120") || ($id eq "adminid0"))) {
            $chkmes ="ON";
            push(@log,"<font color=\"$col_adm\">$message</font> [$mestime]<br>\n");
            if ($mesmax <= $mes_i++) { last; }
        #ＡＬＬ
        } elsif ($how eq "ALL") {
            $chkmes ="ON";
            push(@log,"<font color=\"$col_all\">$message</font> [$mestime]<br>\n");
            if ($mesmax <= $mes_i++) { last; }
        }
    }

    if ($chkmes eq "OFF") { push(@log,"<br><center><b>メッセージはありません</b></center>\n"); }

print <<"_HERE_";
<TABLE width="610">
  <TBODY>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">ＢＲメッセンジャー</FONT></B></TD>
    </TR>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000">@links</FONT></B></TD>
    </TR>
    <TR>
      <TD valign="top" width="400" height="311">
      <TABLE border="1" width="400" cellspacing="0" height="310">
        <TBODY>
          <TR>
            <TH colspan="5">$nowtime</TH>
          </TR>
          <TR>
            <TD ROWSPAN="4" width="17%" nowrap><IMG src="$imgurl$icon" width="70" height="70" border="0" align="middle"></TD>
            <TH width="16%" nowrap>氏 名</TH><TD nowrap colspan="3">$f_name $l_name ($cl $sex$no番)</TD>
          </TR>
          <TR>
            <TH nowrap>部 活</TH><TD nowrap>$club</TD>
            <TH nowrap>愛称</TH><TD nowrap>$a_name</TD>
          </TR>
          <TR>
            <TH nowrap>体 力</TH><TD nowrap><img src="$imgurl$bar_green" width=$hitbarleng height=10><img src="$imgurl$bar_red" width=$hitbarlenr height=10> $hit/$mhit</TD>
            <TH width="16%" nowrap>レベル</TH><TD width="16%" nowrap>$level($exp/$up)</TD>
          </TR>
          <TR>
            <TH nowrap>スタミナ</TH><TD nowrap><img src="$imgurl$bar_green" width=$stabarleng height=10><img src="$imgurl$bar_red" width=$stabarlenr height=10> $sta/$maxsta</TD>
            <TH nowrap>テンション</TH><TD nowrap>$tension</TD>
          </TR>
          <TR>
            <TH nowrap>負傷個所</TH><TD nowrap colspan="2">$kega</TD>
            <TH nowrap>殺害</TH><TD nowrap><font color="red"><b>$kill</b></font>人殺害</TD>
          </TR>
          <TR>
            <TH nowrap>方針</TH><TD nowrap colspan="2">$tactics(反撃：$tactics2)</TD>
            <TH nowrap>状態</TH><TD nowrap>$sts</TD>
          </TR>
          <TR>
            <TH nowrap>グループ</TH><TD nowrap colspan="4">$group($gpass)</TD>
          </TR>
          <TR height="210">
            <TD colspan="5" valign="top">
              <TABLE width="400" height="180">
                <TR align="center">
                  <TD width="20%" nowrap><B>表示文字色</B></TD>
                  <TD nowrap>
<font color="$col_to">受信</font>　
<font color="$col_from">発信</font>　
<font color="$col_all">全員への発言</font>　
<font color="$col_grp">グループ宛</font>　
<font color="$col_adm">管理人宛</font>　
                  </TD>
                </TR>
                <TR height="170">
                  <TD valign="top" colspan="2">
@log
                  </TD>
                </TR>
                <TR>
                  <TD colspan="2" nowrap align="right" valign="bottom"><B>Base script:<A href="http://kurisutof.hp.infoseek.co.jp/" target="_blank">ＢＲメッセンジャーVer1.03</A></B></TD>
                </TR>
              </TABLE>
            </TD>
          </TR>
        </TABLE>
      </TD>
      <TD valign="top" width="210" height="346">
      <TABLE border="1" cellspacing="0" height="346">
        <TBODY>
          <TR><TH width="210">コマンド</TH>
          <TR>
            <TD align="left" valign="top" width="210" height="335">
            <FORM METHOD="POST" name="f1">
            <INPUT TYPE="HIDDEN" NAME="mode" VALUE="command">
            <INPUT TYPE="HIDDEN" NAME="Id" VALUE="$id2">
            <INPUT TYPE="HIDDEN" NAME="Password" VALUE="$password2">
_HERE_

        print "誰にメッセージを送りますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "<option value=\"MAIN\" selected>戻る</option>\n";
        if ($sts eq "治療") {
            print "<option value=\"HEAL2\">治療</option>\n";
        } elsif ($sts eq "睡眠") {
            print "<option value=\"INN2\">睡眠</option>\n";
        } elsif ($sts eq "休憩") {
            print "<option value=\"KYUKEI2\">休憩</option>\n";
        }
        print "<option value=\"SENDMES_reload\">リロード</option>\n";
        for ($k=0; $k<=$#userlist; $k++) {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$k]);
            if (($id ne $w_id) && (($gpass eq $w_gpass) || ($gpass eq $w_gpass) || ($id eq "kiri1120") || ($id eq "adminid0")) && ($w_hit > 0) && ($w_inf !~ /NPC/)) {
                print "<option value=\"SENDMES_id_$w_id\_$k\">$w_f_name $w_l_name</option>\n";
            }
        }
        print "<option value=\"SENDMES_group_$group\">グループ全員</option>\n";
        print "<option value=\"SENDMES_ALL\">参加者全員</option>\n";
        print "<option value=\"SENDMES_admin\">管理人</option>\n";
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "メッセージを入力してください。<BR>（全角", $mes / 2, "文字まで）<BR><BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"speech\" maxlength=\"$mes\"><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";

print <<"_HERE_";
            </FORM>
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
    </TR>
    <TR>
      <TD valign="top" height="151">
      <TABLE border="1" cellspacing="0" height="150" cellpadding="0" width="410">
        <TBODY>
          <TR>
            <TH height="10">ログウィンドウ</TH>
          </TR>
          <TR>
            <TD height="140" valign="top">$log</TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" height="151">
      <TABLE border="1" cellspacing="0" height="150" cellpadding="0">
        <TBODY>
          <TR>
            <TH height="10" width="210" nowrap>グループメンバー</TH>
          </TR>
          <TR>
            <TD height="140" valign="top" width="210" nowrap>
_HERE_

            &GrpMem;

print <<"_HERE_";
            </TD>
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

#==================#
# ■ メッセ 送信   #
#==================#
sub SENDMES {

    local($a,$how,$mes_id,$k) = split(/_/, $Command);


    if (length($speech) > $mes) {
        $log = ($log . "メッセージが最大文字数（全角" . $mes / 2 . "文字）を越えています！<BR>");
    } elsif (($speech ne "") && ($how ne "reload")) {
        $to = "";
        if ($how eq "id") {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$k]);
            if (($w_id eq $mes_id) && ($w_id ne $id) && ($w_hit > 0) && ($w_inf !~ /NPC/)) {
                $to = "＞$w_f_name $w_l_name";
                $mes_id = "_" . $w_id;
            }
            if ($to eq "") { &ERROR("不正なアクセスです。"); }
        }
        elsif ($how eq "group") { $to = "＞$group"; $mes_id = "_" . $group; }
        elsif ($how eq "admin") { $to = "＞管理人"; $mes_id = ""; }
        elsif ($how eq "ALL") {   $to = ""; $mes_id = ""; }
        else { &ERROR("不正なアクセスです。"); }

        open(IN,"$MES_DIR/$mes_file");seek(IN,0,0); @meslist=<IN>;close(IN);

        local($nowtime) = sprintf("%02d/%02d (%02d:%02d)", $month, $mday, $hour, $min);
        $message = "$how$mes_id,$id,$f_name $l_name＞$speech$to,$nowtime,\n";
        unshift (@meslist, $message);
        if ($#meslist >= $listmax) { pop (@meslist); }

        open(OUT,">$MES_DIR/$mes_file"); seek(OUT,0,0); print OUT @meslist; close(OUT);

        $log = ($log . "メッセージを送信しました。<BR>");

    }

    &SAVE;

    &HEADER;
    &MESMAIN;
    &FOOTER;
}
1;
