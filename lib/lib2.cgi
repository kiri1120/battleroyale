# 汎用サブルーチン集

#==================#
# ■ IDチェック処理#
#==================#
sub IDCHK {

    $mem=0; $perlv=0; $perlv2=0;
    $chksts = "NG"; $hostchk = "OK";
    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
        if ($w_id eq $id2) {    #ID一致？
            if ($w_password eq $password2) {    #パスワード正常？
                if ($w_hit > 0) {
                    $chksts = "OK"; $Index=$i; $mem++; $perlv+=$w_level; $perlv2++; $plsmem[$w_pls]++;
                    ($id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$ho2,$os2) = split(/,/, $userlist[$i]);
                    &CSAVE;

                    if($mode eq "main") {
                        $rogindat = "$now,$year/$month/$mday $hour:$min:$sec,$id,$password,$f_name$l_name,$host,\n";
                        open(DB,">>$ADM_DIR/succeed$pgday.log"); seek(DB,0,0); print DB $rogindat; close(DB);
                    }

                    #銃声ログ読込
                    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);

                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[0]) ;
                    if (($now < ($guntime+(15))) && ($wid ne $id) && ($wid2 ne $id)) {   #銃使用から15秒以内？
                        $jyulog = "<font color=\"yellow\"><b>$gunpls の方で、銃声が聞こえた・・・。</b></font><br>" ;
                    } else { $jyulog = "" ; }
                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[1]) ;
                    if (($now < ($guntime+(15))) && ($wid ne $id) && ($wid2 ne $id) && ($place[$pls] eq $gunpls)) {  #殺害から15秒以内？
                        $jyulog2 = "<font color=\"yellow\"><b>近くで悲鳴が？誰か、殺されたのか・・・？</b></font><br>" ;
                    } else { $jyulog2 = "" ; }
                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[2]) ;
                    if (($now < ($guntime+(30)))) { #スピーカ使用から30秒以内？
                        $jyulog3 = "<font color=\"yellow\"><b>$gunpls の方から$widの声が聞こえる・・・</b></font><br><font color=\"lime\"><b>『$wid2』</b></font><br>" ;
                    } else { $jyulog3 = "" ; }
                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[3]) ;
                    if (($now < ($guntime+(15))) && ($wid ne $id) && ($wid2 ne $id)) {   #爆発から15秒以内？
                        $jyulog4 = "<font color=\"yellow\"><b>$gunpls の方で、爆音が聞こえた・・・。</b></font><br>" ;
                    } else { $jyulog4 = "" ; }
                } else {
                    &CDELETE;
                    &ERROR("既に死亡しています。<BR><BR>死因：$w_death<BR><BR><font color=\"lime\"><b>$w_msg</b></font><br><br>■戦闘ログ■<br>$w_log") ;
                }
            } else {
                $rogindat = "$now,$year/$month/$mday $hour:$min:$sec,$id2,$password2,passerror,$host,\n";
                open(DB,">>$ADM_DIR/faired$pgday.log"); seek(DB,0,0); print DB $rogindat; close(DB);
                &ERROR("パスワードが一致しません。") ;
            }
        } else {
            if ($w_hit > 0) {
                $plsmem[$w_pls]++ ;
                if ($w_inf !~ /NPC0/) { $mem ++ ; }
                if ($w_inf !~ /NPC/) {
                    $perlv+=$w_level; $perlv2++;
                    if ($host eq $w_host) { $hostchk = "NG"; }
                }
            }
        }
    }

    if ($chksts eq "NG") {
        $rogindat = "$now,$year/$month/$mday $hour:$min:$sec,$id2,$password2,iderror,$host,\n";
        open(DB,">>$ADM_DIR/faired$pgday.log"); seek(DB,0,0); print DB $rogindat; close(DB);
        &ERROR("ＩＤが見つかりません。") ;
    }

    if ($IP_deny && $hostchk eq "NG" && $inf !~ /NPC/) {
        $rogindat = "$now,$year/$month/$mday $hour:$min:$sec,$id2,$password2,hosterror,$host,\n";
        open(DB,">>$ADM_DIR/faired$pgday.log"); seek(DB,0,0); print DB $rogindat; close(DB);
        &ERROR("一つのIPで接続できるキャラは一人だけです。") ;
    }

    local($b_limit) = ($battle_limit * 3) + 1;
    if ((($mem == 1) && ($inf =~ /勝/) && ($ar > $b_limit))||(($mem == 1) && ($ar > $b_limit))) {    #優勝？
        if($fl !~ /終了/){
            &LOGSAVE("WINEND1");
        }
        require "$LIB_DIR/ending.cgi";
        &ENDING;
    }elsif ($inf =~ /解/){
        require "$LIB_DIR/ending.cgi";
        &ENDING;
    }elsif ($fl =~ /解除/){
        require "$LIB_DIR/ending.cgi";
        &ENDING;
    } else {
        if ($log ne '') {$wlog = $log ;$log="";&SAVE;$log=$wlog;}
        $bid = "" ;
    }
}

#==================#
# ■ ステータス部  #
#==================#
sub STS {

    local($watt_2) = 0 ;

    if (($Command ne "INN2")&&($Command ne "HEAL2")&&($Command ne "KYUKEI2")) {
        $up = ($now - $endtime) / $kaifuku_time;
        if ($inf =~ /腹/) { $up = $up / 2 ; }
        if ($sts eq "睡眠") {
            if ($club eq "サバイバル部") { $up = $up * 1.5; }
            $maxp = $maxsta - $sta ;    #最大値までいくつ
            $up = int($up);
            if ($up > $maxp) { $up = $maxp ; }
            $sta += $up ;
            if ($sta > $maxsta) { $sta = $maxsta ; }
            $log = ($log . "睡眠の結果、スタミナが $up 回復した。<BR>") ;
            $sts = "正常"; $endtime = 0 ;
            &SAVE ;
        } elsif ($sts eq "治療") {
            if ($kaifuku_rate == 0) { $kaifuku_rate = 1; }
            if ($club eq "保健委員") { $up = $up * 1.5; }
            $up = int($up / $kaifuku_rate) ;
            $maxp = $mhit - $hit ;  #最大値までいくつ
            if ($up > $maxp) { $up = $maxp ; }
            $hit += $up ;
            if ($hit > $mhit) { $hit = $mhit ; }
            $log = ($log . "治療の結果、体力が $up 回復した。<BR>") ;
            $sts = "正常"; $endtime = 0 ;
            &SAVE ;
        }
    }

    local($w_name,$w_kind) = split(/<>/, $wep);
    local($b_name,$b_kind) = split(/<>/, $bou);
    local($b_name_h,$b_kind_h) = split(/<>/, $bou_h);
    local($b_name_f,$b_kind_f) = split(/<>/, $bou_f);
    local($b_name_a,$b_kind_a) = split(/<>/, $bou_a);
    local($b_name_i,$b_kind_i) = split(/<>/, $item[5]);

    $up = ($level * $level) + ($level * $baseexp);

    if (($w_kind =~ /G|A/) && ($wtai == 0)) { #棍棒 or 弾無し銃 or 矢無し弓
        $watt_2 = int($watt/10) ;
    } else {
        $watt_2 = $watt ;
    }

    $ball = $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #装飾が防具？

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

    if (($we eq "B") && ($w_kind =~ /B/)) { $tactics2 = "棍"; }
    elsif (($we eq "P") && ($w_kind =~ /P/)) { $tactics2 = "殴"; }
    elsif (($we eq "A") && ($w_kind =~ /A/) && ($wtai > 0)) { $tactics2 = "弓"; }
    elsif (($we eq "G") && ($w_kind =~ /G/) && ($wtai > 0)) { $tactics2 = "銃"; }
    elsif (($we eq "N") && ($w_kind =~ /N/)) { $tactics2 = "斬"; }
    elsif (($we eq "S") && ($w_kind =~ /S/)) { $tactics2 = "刺"; }
    elsif (($we eq "D") && ($w_kind =~ /D/)) { $tactics2 = "爆"; }
    elsif (($we eq "C") && ($w_kind =~ /C/)) { $tactics2 = "投"; }
    else { $tactics2 = "指定無し"; }

    $kega ="" ;
    if ($inf =~ /頭/) {$kega = ($kega . "頭部　") ;}
    if ($inf =~ /腕/) {$kega = ($kega . "腕　") ;}
    if ($inf =~ /腹/) {$kega = ($kega . "腹部　") ;}
    if ($inf =~ /足/) {$kega = ($kega . "足　") ;}
    if ($inf =~ /毒/) {$kega = ($kega . "毒　") ;}
    if ($inf =~ /狂/) {$kega = ($kega . "狂気　") ;}
    if ($kega eq "") { $kega = "　" ;}

    local($p_wa) = int($wa/$BASE);
    local($p_wb) = int($wb/$BASE);
    local($p_wc) = int($wc/$BASE);
    local($p_wd) = int($wd/$BASE);
    local($p_wg) = int($wg/$BASE);
    local($p_ws) = int($ws/$BASE);
    local($p_wn) = int($wn/$BASE);
    local($p_wp) = int($wp/$BASE);

    local($hitbarleng,$hitbarlenr,$stabarleng,$stabarlenr);
    if ($hit > 0) { $hitbarleng = int($hit / $mhit * 45); } else { $hitbarleng = 0; }
    $hitbarlenr = 45 - $hitbarleng;
    $stabarleng = int($sta / $maxsta * 45);
    $stabarlenr = 45 - $stabarleng;

    $nowtime = sprintf("%04d年%02d月%02d日（%s）%02d:%02d:%02d", $year, $month, $mday, ('日','月','火','水','木','金','土') [$wday], $hour, $min, $sec);

    local(@ars) = split(/,/, $arealist[2]);
    local($info) = "";
    $info .= "<b><font color=\"lime\">平均レベル</FONT>：<font color=\"#00ffff\">" . $perlv/$perlv2 . "</font></b><br>\n";

    if($lim_sec) {
        $info .= "<b><font color=\"lime\">連続投稿制限</FONT>：<font color=\"#00ffff\">$lim_sec</font>秒</b><br>\n";
    }

    $info .= "<b><font color=\"lime\">行動中</font>：<font color=\"#00ffff\">$playmem</font>人</b><br>\n";
    $info .= "<b><font color=\"lime\">次回の禁止エリア</FONT></b><br>\n";

    if ($hackflg) {
        $info .= "<b><font color=\"aqua\">ハッキングされています！</font></b><br>\n";
    } else {
        $info .= "<b><font color=\"#ffff00\">$ars[$ar]　$ars[$ar+1]　$ars[$ar+2]</font></b><br>";
    }

print <<"_HERE_";
<TABLE width="610">
  <TBODY>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">$place[$pls]（$area[$pls]）</FONT></B></TD>
    </TR>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000">@links</FONT></B></TD>
    </TR>
    <TR>
      <TD valign="top" width="400" height="311">
      <TABLE border="1" width="400" cellspacing="0" height="300">
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
            <TH nowrap>グループ</TH><TD nowrap colspan="2">$group($gpass)</TD>
            <TH nowrap>攻撃力</TH><TD nowrap>$att+$watt_2</TD>
          </TR>
          <TR>
            <TH nowrap>方針</TH><TD nowrap colspan="2">$tactics(反撃：$tactics2)</TD>
            <TH nowrap>防御力</TH><TD nowrap>$def+$ball</TD>
          </TR>

          <TR><TH nowrap colspan="5">熟練度</TH></TR>
          <TR><TD nowrap colspan="5" align="center">射：$p_wa($wa) 棍：$p_wb($wb) 投：$p_wc($wc) 爆：$p_wd($wd) 銃：$p_wg($wg) 刺：$p_ws($ws) 斬：$p_wn($wn) 殴：$p_wp($wp)</TD></TR>

          <TR><TH nowrap>装備品</TH><TH nowrap colspan="2">装備名称</TH><TH nowrap>効果</TH><TH nowrap>回数</TH></TR>
          <TR><TH nowrap>武 器</TH><TD nowrap colspan="2">$w_name</TD><TD nowrap>$watt</TD><TD nowrap>$wtai</TD></TR>
          <TR><TH nowrap>体防具</TH><TD nowrap colspan="2">$b_name</TD><TD nowrap>$bdef</TD><TD nowrap>$btai</TD></TR>
          <TR><TH nowrap>頭防具</TH><TD nowrap colspan="2">$b_name_h</TD><TD nowrap>$bdef_h</TD><TD nowrap>$btai_h</TD></TR>
          <TR><TH nowrap>腕防具</TH><TD nowrap colspan="2">$b_name_a</TD><TD nowrap>$bdef_a</TD><TD nowrap>$btai_a</TD></TR>
          <TR><TH nowrap>足防具</TH><TD nowrap colspan="2">$b_name_f</TD><TD nowrap>$bdef_f</TD><TD nowrap>$btai_f</TD></TR>
          <TR><TH nowrap>装飾品</TH><TD nowrap colspan="2">$b_name_i</TD><TD nowrap>$eff[5]</TD><TD nowrap>$itai[5]</TD></TR>

          <TR height="9"><TH colspan="5">所持品</TH></TR>
          <TR height="70" valign="top">
            <TD nowrap colspan="5">
_HERE_

            for ($i=0; $i<5; $i++) {
                if ($item[$i] ne "なし") {
                    ($i_name,$i_kind) = split(/<>/, $item[$i]);
                    $i_kind2 = "";
                    if ($item[$i] =~ /<>W/) {
                        if ($i_kind =~ /G/) { $i_kind2 .= "『銃』"; }
                        if ($i_kind =~ /A/) { $i_kind2 .= "『弓』"; }
                        if ($i_kind =~ /B/) { $i_kind2 .= "『棍』"; }
                        if ($i_kind =~ /N/) { $i_kind2 .= "『斬』"; }
                        if ($i_kind =~ /S/) { $i_kind2 .= "『刺』"; }
                        if ($i_kind =~ /D/) { $i_kind2 .= "『爆』"; }
                        if ($i_kind =~ /C/) { $i_kind2 .= "『投』"; }
                        if ($i_kind =~ /P/) { $i_kind2 .= "『殴』"; }
                        $i_kind2 = "<FONT COLOR=\"yellow\">$i_kind2</FONT>\n";
                    } elsif ($item[$i] =~ /<>D|<>A/) {
                        if ($item[$i] =~ /<>A/) { $i_kind2 = "『装飾品』"; }
                        elsif ($i_kind =~ /DB/) { $i_kind2 = "『体防具』"; }
                        elsif ($i_kind =~ /DH/) { $i_kind2 = "『頭防具』"; }
                        elsif ($i_kind =~ /DA/) { $i_kind2 = "『腕防具』"; }
                        elsif ($i_kind =~ /DF/) { $i_kind2 = "『足防具』"; }
                        $i_kind2 = "<font color=\"orange\">$i_kind2</font>";
                    } elsif ($item[$i] =~ /<>S/) {
                        $i_kind2 = "『スタミナ回復』";
                        if($i_kind =~ /食/) { $i_kind2 .= "『食材』"; }
                        $i_kind2 = "<font color=\"aqua\">$i_kind2</font>";
                    } elsif ($item[$i] =~ /<>H/) {
                        $i_kind2 = "『体力回復』";
                        if($i_kind =~ /食/) { $i_kind2 .= "『食材』"; }
                        $i_kind2 = "<font color=\"aqua\">$i_kind2</font>";
                    } elsif ($item[$i] =~ /<>T/) { $i_kind2 = "<font color=\"yellow\">『罠』</font>";
                    } else { $i_kind2 = "<font color=\"silver\">『その他』</font>"; }
                    print "$i_name/$eff[$i]/$itai[$i] $i_kind2<BR>\n";
                }
            }

print <<"_HERE_";
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" width="210" height="365">
      <TABLE border="1" cellspacing="0">
        <TBODY>
          <TR><TH width="210">コマンド</TH>
          <TR>
            <TD align="left" valign="top" width="210" height="278">
            <FORM METHOD="POST" name="f1">
            <INPUT TYPE="HIDDEN" NAME="mode" VALUE="command">
            <INPUT TYPE="HIDDEN" NAME="Id" VALUE="$id2">
            <INPUT TYPE="HIDDEN" NAME="Password" VALUE="$password2">
_HERE_

            &COMMAND;

print <<"_HERE_";
            </FORM>
            </TD>
          </TR>
          <TR>
            <TH width="210" height="9">$pgday日目（残り$mem人）</TH>
          </TR>
          <TR>
            <TD width="210" height="70" nowrap>
$info
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
    </TR>
    <TR>
      <TD valign="top" height="151">
      <TABLE border="1" cellspacing="0" height="150" cellpadding="0">
        <TBODY>
          <TR>
            <TH width="400" height="10">ログウィンドウ</TH>
          </TR>
          <TR>
            <TD width="400" height="140" valign="top">$log</TD>
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
<BR>
_HERE_
}

#==================#
# ■ デコード処理  #
#==================#
sub DECODE {
    $p_flag=0;
    if ($ENV{'REQUEST_METHOD'} eq "POST") {
        $p_flag=1;
        if ($ENV{'CONTENT_LENGTH'} > 51200) { &ERROR("異常な入力です"); }
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    } else { $buffer = $ENV{'QUERY_STRING'}; }

    @pairs = split(/&/, $buffer);
    foreach (@pairs) {
        ($name,$value) = split(/=/, $_);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        &jcode::convert(*value, "euc", "", "z");
        &jcode::tr(\$value, '　', ' ');

        $value =~ s/&amp;/&/g;
        $value =~ s/&lt;/</g;
        $value =~ s/&gt;/>/g;
        $value =~ s/&quot;/"/g;
        $value =~ s/&nbsp;/ /g;

        $value =~ s/&/&amp;/g;
        $value =~ s/</&lt;/g;
        $value =~ s/>/&gt;/g;
        $value =~ s/"/&quot;/g;
        $value =~ s/ /&nbsp;/g;
        $value =~ s/,/，/g; #データ破損対策

        if ($name eq "ITDEL") { push(@IDEL,$value);}
        $in{$name} = $value;
    }

    $mode = $in{'mode'};
    $id2 = $in{'Id'};
    $password2 = $in{'Password'};

    $Command = $in{'Command'};
    $Command2 = $in{'Command2'};
    $Command3 = $in{'Command3'};
    $Command4 = $in{'Command4'};
    $Command5 = $in{'Command5'};
    $Command6 = $in{'Command6'};

    $l_name2 = $in{'L_Name'} ;
    $f_name2 = $in{'F_Name'} ;
    $a_name2 = $in{'A_Name'} ;
    $msg2  = $in{'Message'} ;
    $dmes2 = $in{'Message2'} ;
    $dengon = $in{'Dengon'} ;
    $com2 = $in{'Comment'} ;
    $sex2 = $in{'Sex'};
    $icon2 = $in{'Icon'};
    $itno2 = $in{'Itno'};
    $getid = $in{'WId'};
    $speech = $in{'speech'};
    $group2 = $in{'Group'};
    $gpass2 = $in{'Gpass'};

    srand;

}

#==================#
# ■ メニュー部    #
#==================#
sub COMMAND {

    local($i) = 0 ;
    local($n) = 0 ;

    if (($Command eq "HEAL2") || ($Command eq "INN2")) {
        if ($Command eq "HEAL2") {
            $log = ($log . "怪我の治療をしよう。<BR>") ;
            $sts = "治療" ;
            print "治療中・・・。<BR><BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"HEAL2\" checked>治療<BR><BR>\n";
        } elsif ($Command eq "INN2") {
            $log = ($log . "少し寝ておくか。<BR>") ;
            $sts = "睡眠" ;
            print "睡眠中・・・。<BR><BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"INN2\" checked>睡眠<BR><BR>\n";
        }
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MESSAGE\">ＢＲメッセ<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\">戻る<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
        return ;
    }

    if (($Command eq '')||($Command eq "MAIN")) {   #MAIN
        $log = ($log . "$jyulog$jyulog2$jyulog3$jyulog4さて、どうしよう・・・。<br>") ;
        print "何を行いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MOVE\">移動\n";
        local(@kin_ar) = split(/,/, $arealist[2]);
        if (($hackflg) || ($inf =~ /NPC/)) {
            $kinlist = "";
        }else{
            for($k=0;$k<$ar;$k++){
                $kinlist = ($kinlist . $kin_ar[$k]);
            }
        }
        print "　<select name=\"Command2\" onClick=\"sl($n)\">\n" ;
        for ($j=0; $j<$#place+1; $j++) {
            if (($place[$j] ne $place[$pls]) && ($kinlist !~ /$place[$j]/)) {
                print "<option value=\"MV$j\">$place[$j]($area[$j])</option>\n";
            }
        }
        print "</select><BR>\n";
        $n++;

        if (($place[$pls] ne "分校") || ($hackflg)) {
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"ACTION\">行動\n";
            print "　<select name=\"Command3\" onClick=\"sl($n)\">\n" ;
            print "<option value=\"SEARCH\">探索</option>\n";
            if (($inf !~ /狂/) && ($pgday < 7)) { print "<option value=\"HEAL\">治療</option>\n"; }
            print "<option value=\"INN\">睡眠</option>\n";
            print "</select><BR>\n";
            $n++;
        }

        print "　<INPUT type=\"radio\" name=\"Command\" value=\"ITMAIN\">道具\n";
        print "　<select name=\"Command4\" onClick=\"sl($n)\">\n" ;
        print "<option value=\"ITEM\">使用・装備</option>\n";
        print "<option value=\"DEL\">投棄</option>\n";
        print "<option value=\"SEIRI\">整理</option>\n";
        print "<option value=\"BUNKATU\">分割</option>\n";
        print "<option value=\"GOUSEI\">合成</option>\n";
        print "<option value=\"ITSEND\">譲渡</option>\n";
        print "<option value=\"WEPKAI\">装備品解除</option>\n";
        print "<option value=\"WEPDEL\">装備品投棄</option>\n";
        if(($wep =~ /<>WG|<>WA/) && ($wtai > 0)) { 
            print "<option value=\"SPLIT\">武器分解</option>\n"; 
        }
        print "</select><BR>\n";
        $n++;

        print "　<INPUT type=\"radio\" name=\"Command\" value=\"KOUDOU\">方針\n";
        print "　<select name=\"Command5\" onClick=\"sl($n)\">\n" ;
        print "<option value=\"KOU_0\">通常</option>\n";
        print "<option value=\"KOU_1\">攻撃重視</option>\n";
        if ($pgday <= $tactlim) { print "<option value=\"KOU_2\">防御重視</option>\n"; }
        print "<option value=\"KOU_3\">隠密行動</option>\n";
        print "<option value=\"KOU_4\">探索行動</option>\n";
        print "<option value=\"KOU_5\">先制行動</option>\n";
        print "<option value=\"KOU_6\">命中重視</option>\n";
        print "<option value=\"KOU_7\">回避重視</option>\n";
        if (($pgday > $tactlim) || ($mem <= 20 && $pgday > 1)) { print "<option value=\"KOU_8\">連闘行動</option>\n"; }
        print "</select><BR>\n";
        $n++;

        print "　<INPUT type=\"radio\" name=\"Command\" value=\"SPECIAL\">特殊\n";
        print "　<select name=\"Command6\" onClick=\"sl($n)\">\n" ;
        print "<option value=\"CATCHG\">反撃設定</option>\n";
        print "<option value=\"MESSAGE\">ＢＲメッセ</option>\n";
        print "<option value=\"WINCHG\">口癖変更</option>\n";
        print "<option value=\"GRPCHG\">所属変更</option>\n";
        print "<option value=\"OUKYU\">応急処置</option>\n";
        print "<option value=\"PSCHECK\">毒見</option>\n";
        for ($poi=0; $poi<5; $poi++){
            if ($item[$poi] eq "毒薬<>Y") {
                print "<option value=\"POISON\">毒物混入</option>\n";
                last;
            }
        }
        for ($poi2=0; $poi2<5; $poi2++){
            if ($item[$poi2] eq "毒中和剤<>Y") {
                print "<option value=\"ANTIPS\">毒中和</option>\n";
                last;
            }
        }
        for ($spi=0; $spi<5; $spi++){
            if (($item[$spi] eq "携帯スピーカ<>Y") || ($club eq "応援団")) {
                print "<option value=\"SPIICH\">叫ぶ</option>\n";
                last;
            }
        }
        for ($paso=0; $paso<5; $paso++){
            if (($item[$paso] eq "モバイルPC<>Y")&&($itai[$paso] >= 1)) {
                print "<option value=\"HACK\">ハッキング</option>\n";
                last;
            }
        }
        print "</select><BR>\n";
        $n++;

        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "ITEM")) {  #アイテム
        $log = ($log . "デイパックの中には、何が入っていたかな・・・。<BR>") ;
        print "何を使用しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"ITEM_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "DEL")) {   #アイテム投棄
        $log = ($log . "デイパックの中を整理するか・・・。<BR>") ;
        print "何を捨てますか？<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<input type=\"checkbox\" name=\"ITDEL\" value=\"$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "<input type=\"hidden\" name=\"Command\" value=\"ITEMDEL\">\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "SEIRI")) { #アイテム整理
        $log = ($log . "デイパックの中を整理するか・・・。<BR>") ;
        print "何と何を纏めますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "　<option value=\"MAIN\" selected>止める</option>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<option value=\"SEIRI_$i\">$in/$eff[$i]/$itai[$i]</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "　<select name=\"Command2\">\n" ;
        print "　<option value=\"MAIN\" selected>止める</option>\n";
        for ($i2=0; $i2<5; $i2++) {
            if ($item[$i2] ne "なし") {
                ($in2, $ik2) = split(/<>/, $item[$i2]);
                print "　<option value=\"SEIRI2_$i2\">$in2/$eff[$i2]/$itai[$i2]</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "BUNKATU")) { #アイテム整理
        $log = ($log . "アイテムを分割するか・・・。<BR>") ;
        print "何を分割しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"BUNKATU_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　いくつ分ける？：<INPUT type=\"text\" name=\"Command2\"><BR>\n";
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "GOUSEI")) { #アイテム合成
        $log = ($log . "今持っているものを組み合わせて、何か作れないかな？<BR>") ;
        print "何と何を合成しますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "　<option value=\"MAIN\" selected>止める</option>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<option value=\"GOUSEI_$i\">$in/$eff[$i]/$itai[$i]</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "　<select name=\"Command2\">\n" ;
        print "　<option value=\"MAIN\" selected>止める</option>\n";
        for ($i2=0; $i2<5; $i2++) {
            if ($item[$i2] ne "なし") {
                ($in2, $ik2) = split(/<>/, $item[$i2]);
                print "　<option value=\"GOUSEI2_$i2\">$in2/$eff[$i2]/$itai[$i2]</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "ITSEND")) { #アイテム合成
        $log = ($log . "仲間にアイテムを渡すか・・・<BR>") ;
        print "誰に渡しますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "<option value=\"MAIN\" selected>止める</option>\n";
        for ($k=0; $k<=$#userlist; $k++) {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$k]);
            if (($id ne $w_id) && ($gpass eq $w_gpass) && ($w_hit > 0)) {
                print "<option value=\"ITSEND_$w_id\_$k\">$w_f_name $w_l_name</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "何を渡しますか？<BR><BR>\n";
        print "　<select name=\"Command2\">\n" ;
        print "<option value=\"MAIN\" selected>止める</option>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "<option value=\"ITSEND_$i\">$in/$eff[$i]/$itai[$i]</option>\n";
            }
        }
        print "</select><BR>\n" ;
        print "<BR>\n";
        print "メッセージを入力してください。<BR><BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"speech\" maxlength=\"64\"><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "WEPKAI")) {   #装備解除
        print "何を外しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        if ($wep ne "素手<>WP") { #武器装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_W\">武器を外す<BR>\n";
        }
        if ($bou ne "下着<>DN") { #体防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_B\">体防具を外す<BR>\n";
        }
        if ($bou_h ne "なし") { #頭防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_H\">頭防具を外す<BR>\n";
        }
        if ($bou_a ne "なし") { #腕防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_A\">腕防具を外す<BR>\n";
        }
        if ($bou_f ne "なし") { #足防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_F\">足防具を外す<BR>\n";
        }
        if ($item[5] ne "なし") { #装飾品装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPKAI2_I\">装飾品を外す<BR>\n";
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "WEPDEL")) {   #装備投棄
        print "何を外しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        if ($wep ne "素手<>WP") { #武器装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_W\">武器を捨てる<BR>\n";
        }
        if ($bou ne "下着<>DN") { #体防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_B\">体防具を捨てる<BR>\n";
        }
        if ($bou_h ne "なし") { #頭防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_H\">頭防具を捨てる<BR>\n";
        }
        if ($bou_a ne "なし") { #腕防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_A\">腕防具を捨てる<BR>\n";
        }
        if ($bou_f ne "なし") { #足防具装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_F\">足防具を捨てる<BR>\n";
        }
        if ($item[5] ne "なし") { #装飾品装備？
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2_I\">装飾品を捨てる<BR>\n";
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "POISON")) {    #毒物混入
        $log = ($log . "この毒薬を混ぜれば・・・ふふふ。<BR>") ;
        print "何に毒物混入しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] =~ /<>SH|<>HH|<>SD|<>HD/) {
                local($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"POI_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL")&&($Command6 eq "ANTIPS")) {    #毒中和
        $log = ($log . "毒を中和してみるか・・・。<BR>") ;
        print "何に毒中和剤を使用しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] =~ /<>SH|<>HH|<>SD|<>HD/) {
                local($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATPS_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "PSCHECK")) {   #毒見
        $log = ($log . "何かが混入されていないか調べてみよう・・・。<BR>") ;
        print "何の毒見をしますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] =~ /<>SH|<>HH|<>SD|<>HD/) {
                local($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"PSC_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "HACK")) {  #ハッキング
        $log = ($log . "いくぞ。準備はぬかりないよな・・・<BR>\n") ;
        print "ハッキング開始？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"HACK2\">開始<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "SPIICH")) { #携帯スピーカ使用
        $log = ($log . "此処で叫べば、みんなに聞こえる筈だな・・・<BR>") ;
        print "全員に伝言を伝えます。<BR>\n";
        print "（全角２０文字まで）<BR><BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"speech\"maxlength=\"50\"><BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"SPEAKER\">伝える<BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>止める<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "WINCHG")) {    #設定変更
        $log = ($log . "口癖を変更します。<BR>") ;
        print "口癖を入力してください<BR>\n";
        print "（全角３２文字まで）<BR><BR>\n";
        print "殺害時：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Message\" maxlength=\"64\" value=\"$msg\"><BR><BR>\n";
        print "遺言：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Message2\" maxlength=\"64\" value=\"$dmes\"><BR><BR>\n";
        print "一言コメント：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Comment\" maxlength=\"64\" value=\"$com\"><BR><BR>\n";
        print "愛称：<BR>\n";
        print "　<INPUT size=\"16\" type=\"text\" name=\"A_Name\" maxlength=\"16\" value=\"$a_name\"><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "GRPCHG")) {    #設定変更
        $log = ($log . "所属グループを変更します。<BR>") ;
        print "所属するグループを入力してください<BR>\n";
        print "（全角１０文字まで）<BR><BR>\n";
        print "グループＩＤ：<font color=\"yellow\">スタミナ$group_sta消費</b></font><br>\n";
        print "　<INPUT size=\"20\" type=\"text\" name=\"Group\" maxlength=\"20\" value=\"$group\"><BR><BR>\n";
        print "グループパス：<BR>\n";
        print "　<INPUT size=\"20\" type=\"text\" name=\"Gpass\" maxlength=\"20\" value=\"$gpass\"><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "OUKYU")) { #応急処置
        $log = ($log . "怪我の治療をするか・・・。<BR>") ;

        print "何処を治療しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";

        if ($inf =~ /頭/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_0\">頭<BR>\n"; }
        if ($inf =~ /腕/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_1\">腕<BR>\n"; }
        if ($inf =~ /腹/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_2\">腹部<BR>\n"; }
        if ($inf =~ /足/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_3\">足<BR>\n"; }
        if ($inf =~ /毒/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_4\">毒<BR>\n"; }
        if ($inf =~ /狂/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_5\">狂気<BR>\n"; }

        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif (($Command eq "SPECIAL") && ($Command6 eq "CATCHG")) { #応急処置
        $log = ($log . "反撃方法を考えるか・・・。<BR>") ;

        print "どうやって反撃しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";

        ($w_name,$w_kind) = split(/<>/, $wep);
        if ($w_kind =~ /B/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WB\">棍($wb)<BR>\n"; }
        if ($w_kind =~ /P/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WP\">殴($wp)<BR>\n"; }
        if (($w_kind =~ /G/) && ($wtai > 0)) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WG\">銃($wg)<BR>\n"; }
        if (($w_kind =~ /A/) && ($wtai > 0)) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WA\">射($wa)<BR>\n"; }
        if ($w_kind =~ /N/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WN\">斬($wn)<BR>\n"; }
        if ($w_kind =~ /S/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WS\">刺($ws)<BR>\n"; }
        if ($w_kind =~ /C/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WC\">投($wc)<BR>\n"; }
        if ($w_kind =~ /D/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"CATCHG2_WD\">爆($wd)<BR>\n"; }

        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif ($Command =~ /BATTLE0/) {   #戦闘コマンド
        local($a,$wid) = split(/_/, $Command);
        $log = ($log . "さて、どうしよう・・・。") ;
        print "何をしますか？<BR>\n";
        print "<BR>　メッセージ<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Dengon\" maxlength=\"64\"><BR><BR>\n";
        $chk = "checked" ;
        ($w_name,$w_kind) = split(/<>/, $wep);
        if ($w_kind =~ /B/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WB_$wid\" $chk>殴る($wb)<BR>\n"; $chk="" ;}
        if ($w_kind =~ /P/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WP_$wid\" $chk>殴る($wp)<BR>\n"; $chk="" ;}
        if (($w_kind =~ /G/) && ($wtai > 0)) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WG_$wid\" $chk>撃つ($wg)<BR>\n"; $chk="" ;}
        if (($w_kind =~ /A/) && ($wtai > 0)) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WA_$wid\" $chk>射る($wa)<BR>\n"; $chk="" ;}
        if ($w_kind =~ /N/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WN_$wid\" $chk>斬る($wn)<BR>\n"; $chk="" ;}
        if ($w_kind =~ /S/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WS_$wid\" $chk>刺す($ws)<BR>\n"; $chk="" ;}
        if ($w_kind =~ /C/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WC_$wid\" $chk>投げる($wc)<BR>\n"; $chk="" ;}
        if ($w_kind =~ /D/) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WD_$wid\" $chk>投げる($wd)<BR>\n"; $chk="" ;}
        if (($w_kind !~ /S|N|C|P|D|B/)&&(($w_kind =~ /G|A/) && ($wtai == 0))) {print "　<INPUT type=\"radio\" name=\"Command\" value=\"ATK_WB_$wid\" $chk>殴る($wb)<BR>\n"; $chk="" ;}
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"RUNAWAY\">逃亡<BR>\n";
        print "<BR>\n";
        if($feel == 300) {print "　<INPUT type=\"checkbox\" name=\"Command2\" value=\"CATKon\">必殺技を使用する<BR><BR>\n";}
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif ($Command eq "BATTLE2") {   #アイテム強奪
        local($itno) = -1;
        for ($i=0; $i<5; $i++) {
            if ($item[$i] eq "なし") {
                $itno = $i ;
            }
        }
        print "何を奪いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "<INPUT TYPE=\"HIDDEN\" NAME=\"Itno\" VALUE=\"$itno\">\n";
        print "<INPUT TYPE=\"HIDDEN\" NAME=\"WId\" VALUE=\"$w_id\">\n";

        if ($w_wep !~ /素手/) { #武器所持？
            local($in, $ik) = split(/<>/, $w_wep);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_6\">$in/$w_watt/$w_wtai<BR>\n";
        }
        if ($w_bou !~ /下着/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_7\">$in/$w_bdef/$w_btai<BR>\n";
        }
        if ($w_bou_h !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_h);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_8\">$in/$w_bdef_h/$w_btai_h<BR>\n";
        }
        if ($w_bou_f !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_f);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_9\">$in/$w_bdef_f/$w_btai_f<BR>\n";
        }
        if ($w_bou_a !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_a);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_10\">$in/$w_bdef_a/$w_btai_a<BR>\n";
        }

        for ($i=0; $i<6; $i++) {
            if ($w_item[$i] ne "なし") {
                local($in, $ik) = split(/<>/, $w_item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_$i]\">$in/$w_eff[$i]/$w_itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } elsif ($Command eq "DEATHGET") {  #死体アイテム強奪
        local($itno) = -1;
        for ($i=0; $i<5; $i++) {
            if ($item[$i] eq "なし") {
                $itno = $i ;
            }
        }
        print "何を奪いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "<INPUT TYPE=\"HIDDEN\" NAME=\"Itno\" VALUE=\"$itno\">\n";
        print "<INPUT TYPE=\"HIDDEN\" NAME=\"WId\" VALUE=\"$w_id\">\n";

        if ($w_wep !~ /素手/) { #武器所持？
            local($in, $ik) = split(/<>/, $w_wep);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_6\">$in/$w_watt/$w_wtai<BR>\n";
        }
        if ($w_bou !~ /下着/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_7\">$in/$w_bdef/$w_btai<BR>\n";
        }
        if ($w_bou_h !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_h);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_8\">$in/$w_bdef_h/$w_btai_h<BR>\n";
        }
        if ($w_bou_f !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_f);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_9\">$in/$w_bdef_f/$w_btai_f<BR>\n";
        }
        if ($w_bou_a !~ /なし/) { #防具所持？
            local($in, $ik) = split(/<>/, $w_bou_a);
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_10\">$in/$w_bdef_a/$w_btai_a<BR>\n";
        }

        for ($i=0; $i<6; $i++) {
            if ($w_item[$i] ne "なし") {
                local($in, $ik) = split(/<>/, $w_item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"GET_$i\">$in/$w_eff[$i]/$w_itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    } else {
        print "何を行いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\" ondblclick=\"dbk()\">\n";
    }


}
#====================#
# ■ ユーザ情報保存  #
#====================#
sub SAVE {


    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    $chksts = "NG";
    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_i,$w_p,$a) = split(/,/, $userlist[$i]);
        if (($id2 eq $w_i) && ($password2 eq $w_p)) {   #ID一致？
            $chksts = "OK";$Index=$i;last;
        }
    }

    if ($chksts eq "OK") {
        if ($hit <= 0) { $sts = "死亡"; }
        $userlist[$Index] = "$id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$host,$os,\n" ;
        open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
    }


}
#====================#
# ■ 敵情報保存      #
#====================#
sub SAVE2 {


    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    if ($w_hit <= 0) { $w_sts = "死亡"; }
    $userlist[$Index2] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os,\n" ;

    open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);


}

#====================#
# ■ クッキー読込    #
#====================#
sub CREAD {
    local($xx, $name, $value);
    for $xx (split(/; */, $ENV{'HTTP_COOKIE'})) {
        if ($xx =~ /BR/){
            $cooks = $xx;
            $cooks =~ s/BR=//;
            $cooks =~ s/([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
            ($c_id,$c_password,$c_f_name,$c_l_name,$c_sex,$c_cl,$c_no,$c_endtime,$c_att,$c_def,$c_hit,$c_mhit,$c_level,$c_exp,$c_sta,$c_wep,$c_watt,$c_wtai,$c_bou,$c_bdef,$c_btai,$c_bou_h,$c_bdef_h,$c_btai_h,$c_bou_f,$c_bdef_f,$c_btai_f,$c_bou_a,$c_bdef_a,$c_btai_a,$c_tactics,$c_death,$c_msg,$c_sts,$c_pls,$c_kill,$c_icon,$c_item[0],$c_eff[0],$c_itai[0],$c_item[1],$c_eff[1],$c_itai[1],$c_item[2],$c_eff[2],$c_itai[2],$c_item[3],$c_eff[3],$c_itai[3],$c_item[4],$c_eff[4],$c_itai[4],$c_item[5],$c_eff[5],$c_itai[5],$c_log,$c_dmes,$c_bid,$c_club,$c_wn,$c_wp,$c_wa,$c_wg,$c_we,$c_wc,$c_wd,$c_wb,$c_wf,$c_ws,$c_com,$c_inf,$c_group,$c_gpass,$c_a_name,$c_feel,$c_host,$c_os) = split(/,/, $cooks);
        }
    }
}

#====================#
# ■ クッキー保存    #
#====================#
sub CSAVE {
    $cook = "$id,$password,$f_name,$l_name,$sex,$cl,$no,0,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$host,$os,";
    $cook =~ s/(.)/sprintf("%02X", unpack("C", $1))/eg;
    print "Set-Cookie: BR=$cook; expires=$expires\n";
}

#====================#
# ■ クッキー削除    #
#====================#
sub CDELETE {
    $cook = ",,,,,,,$now,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,";
    $cook =~ s/(.)/sprintf("%02X", unpack("C", $1))/eg;
    print "Set-Cookie: BR=$cook; expires=$expires\n";
}

#====================#
# ■ 戦略計算        #
#====================#
sub TACTGET {

    $chkpnt  = 6 ;   #敵、アイテム発見率
    $chkpnt2 = 5 ;  #先制攻撃率
    $atp = 0.5 ;
    $dfp = 1.0 ;

    $atp += $ar/100;
    $atp += int($feel/3)/200;

    if ($tactics eq "攻撃重視") {
        $atp+=0.4;
        $dfp-=0.4;
    } elsif ($tactics eq "防御重視") {
        $atp-=0.4;
        $dfp+=0.4;
    } elsif ($tactics eq "隠密行動") {
        $dfp-=0.2;
        $dfp-=0.2;
        $chkpnt -=4;
        $chkpnt2+=4;
    } elsif ($tactics eq "探索行動") {
        $atp-=0.2;
        $dfp-=0.2;
        $chkpnt +=4;
        $chkpnt2+=2;
    } elsif ($tactics eq "先制行動") {
        $atp-=0.2;
        $dfp-=0.2;
        $chkpnt +=2;
        $chkpnt2+=4;
    } elsif ($tactics eq "命中重視") {
        $afp-=0.4;
    } elsif ($tactics eq "回避重視") {
        $dfp-=0.4;
    } elsif ($tactics eq "連闘行動") {
    }

    if ($arsts[$pls] eq "WU") { #攻撃増
        $atp+=0.2 ;
    } elsif ($arsts[$pls] eq "WD") {    #攻撃減
        $atp-=0.2 ;
    } elsif ($arsts[$pls] eq "DU") {    #防御増
        $dfp+=0.2 ;
    } elsif ($arsts[$pls] eq "DD") {    #防御減
        $dfp-=0.2 ;
    } elsif ($arsts[$pls] eq "SU") {    #発見増
        $chkpnt+=2 ;
    } elsif ($arsts[$pls] eq "SD") {    #発見減
        $chkpnt-=2 ;
    }

    if ($inf =~ /腕/) { $atp -= 0.2; }
    if ($inf =~ /狂/) { $atp += 0.2; $dfp-=0.2 ; }

    local($kind) = $w_kind;
    local($wmei) = 0;
    local($wweps) = "" ;

    if (($kind =~ /B/) || (($kind =~ /G|A/) && ($wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wb/$BASE);
    } elsif ($kind =~ /A/) {        #
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wa/$BASE);
    }elsif ($kind =~ /C/) { #投
        $wweps = "L" ;
        $wmei = 70 ;
        $wmei += int($wc/$BASE);
    }elsif ($kind =~ /D/) { #爆
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wd/$BASE);
    }elsif ($kind =~ /G/) { #銃
        $wweps = "L" ;
        $wmei = 50 ;
        $wmei += int($wg/$BASE);
    }elsif ($kind =~ /N/) { #斬
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wn/$BASE);
    }elsif ($kind  =~ /S/) {    #刺
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($ws/$BASE);
    } else {    #手
        $wweps = "S" ;
        $wmei = 70 ;
        $wmei += int($wp/$BASE);
    }

    $weps = $wweps ;
    $mei = $wmei ;

    if ($inf =~ /頭/) { $mei -= 20; }
    if ($inf =~ /狂/) { $mei -= 10; }
    if ($w_inf =~ /狂/) { $mei += 10; }

    if ($tactics eq "命中重視") { $mei += 20; }
    if ($w_tactics eq "回避重視") { $mei -= 20; }

    $mei += int((300 - $feel) / 30);

    if ($mei > 90) { $mei = 90; }
    if ($mei < 30) { $mei = 30; }

}
#====================#
# ■ 戦略計算        #
#====================#
sub TACTGET2 {

    $atn = 0.5 ;
    $dfn = 1.0 ;
    $sen = 1.0 ;  # 被発見率… −ならＵＰ
    $sen2 = 1.0 ; # 被先制率… −ならＵＰ

    $atn += $ar/100;
    $atn += int($w_feel/3)/200;

    if ($w_tactics eq "攻撃重視") {
        $atn+=0.4 ;
        $dfn-=0.4 ;
    } elsif ($w_tactics eq "防御重視") {
        $atn-=0.4 ;
        $dfn+=0.4 ;
    } elsif ($w_tactics eq "隠密行動") {
        $atn-=0.2 ;
        $dfn-=0.2 ;
        $sen+=0.4 ;
    } elsif ($w_tactics eq "探索行動") {
        $atn-=0.2 ;
        $dfn-=0.2 ;
        $sen-=0.2 ;
    } elsif ($w_tactics eq "先制行動") {
        $atn-=0.2 ;
        $dfn-=0.2 ;
        $sen-=0.2 ;
    } elsif ($w_tactics eq "命中重視") {
        $afn-=0.4 ;
    } elsif ($w_tactics eq "回避重視") {
        $dfn-=0.4 ;
    } elsif ($w_tactics eq "連闘行動") {
    }

    if ($arsts[$w_pls] eq "WU") {   #攻撃増
        $atn+=0.2 ;
    } elsif ($arsts[$w_pls] eq "WD") {  #攻撃減
        $atn-=0.2 ;
    } elsif ($arsts[$w_pls] eq "DU") {  #防御増
        $dfn+=0.2 ;
    } elsif ($arsts[$w_pls] eq "DD") {  #防御減
        $dfn-=0.2 ;
    }

    if ($w_inf =~ /腕/) { $atn -= 0.2; }
    if ($w_inf =~ /狂/) { $atn += 0.2; $dfn -= 0.2; }

    local($kind) = $w_kind2;
    local($wmei) = 0;
    local($wweps) = "" ;

    if (($kind =~ /B/) || (($kind =~ /G|A/) && ($w_wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wb/$BASE);
    } elsif ($kind =~ /A/) {        #
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wa/$BASE);
    }elsif ($kind =~ /C/) { #投
        $wweps = "L" ;
        $wmei = 70 ;
        $wmei += int($wc/$BASE);
    }elsif ($kind =~ /D/) { #爆
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wd/$BASE);
    }elsif ($kind =~ /G/) { #銃
        $wweps = "L" ;
        $wmei = 50 ;
        $wmei += int($wg/$BASE);
    }elsif ($kind =~ /N/) { #斬
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wn/$BASE);
    }elsif ($kind  =~ /S/) {    #刺
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($ws/$BASE);
    } else {    #手
        $wweps = "S" ;
        $wmei = 70 ;
        $wmei += int($wp/$BASE);
    }

    $weps2 = $wweps ;
    $mei2 = $wmei ;

    if ($w_inf =~ /頭/) { $mei2 -= 20; }
    if ($w_inf =~ /狂/) { $mei2 -= 10; }
    if ($inf =~ /狂/) { $mei2 += 10; }

    if ($w_tactics eq "命中重視") { $mei2 += 20; }
    if ($tactics eq "回避重視") { $mei2 -= 20; }

    $mei2 += int((300 - $w_feel) / 30);

    if ($mei2 > 90) { $mei2 = 90; }
    if ($mei2 < 30) { $mei2 = 30; }
}

#====================#
# ■ スタミナ切れ    #
#====================#
sub DRAIN{
    local($d_mode) = $_[0];
    $log = ($log . "$l_nameは、スタミナが尽きた・・・。最大HPが減少した。<BR>") ;
    $sta = $maxsta ;
    local($dhit) = int(rand(($mhit/100)*20)+(($mhit/100)*10));
    if ($dhit <= 0) { $dhit = 1 ;}
    $mhit -= $dhit;
    if ($mhit <= 0) {
        $hit = $mhit = 0;
        $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
            &LOGSAVE("DEATH") ; #死亡ログ
            $mem--; if ($mem == 1) {&LOGSAVE("WINEND1") ;}
        if($d_mode eq "mov"){
            &SAVE;
        }elsif($d_mode eq "eve"){
            $Command = "EVENT";
        }
    } elsif ($hit > $mhit) { $hit = $mhit ; }
}

#====================#
# ■ グループ一覧表示#
#====================#
sub GrpMem {

    foreach (@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $_);
        if ($id ne $w_id) {
            if (($group eq $w_group) && ($gpass eq $w_gpass)) {
                if ($w_hit > 0) {
                    $w_hpper = $w_hit/$w_mhit ;
                    if ($w_hpper < 0.2) { $w_hpper="<font color=\"red\">瀕死</font>"; }
                    elsif ($w_hpper < 0.5) { $w_hpper="<font color=\"orange\">重傷</font>"; }
                    elsif ($w_hpper < 0.8) { $w_hpper="<font color=\"yellow\">軽傷</font>"; }
                    else { $w_hpper="<font color=\"lime\">正常</font>"; }
                } else {
                    $w_hpper="<font color=\"red\">死亡</font>";
                }
                push(@gr_list, "<b>$w_f_name $w_l_name $w_hpper</b><BR>\n");
            } elsif (($group eq $w_group) || ($gpass eq $w_gpass)) {
                if ($w_hit > 0) {
                    $w_hpper="<font color=\"lime\">生存</font>";
                } else {
                    $w_hpper="<font color=\"red\">死亡</font>";
                }
                push(@gp_list, "$w_f_name $w_l_name $w_hpper<BR>\n");
            }
        }
    }
    print "@gr_list @gp_list\n";
}
1
