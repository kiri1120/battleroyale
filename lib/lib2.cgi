# 汎用サブルーチン集

#==================#
# ■ IDチェック処理#
#==================#
sub IDCHK {


    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);


    $mem=0;
    $chksts = "NG";
    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);
        if ($w_id eq $id2) {    #ID一致？
            if ($w_password eq $password2) {    #パスワード正常？
                if ($w_hit > 0) {
                    $chksts = "OK";$Index=$i;$mem++;$plsmem[$w_pls]++ ;
                    ($id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf) = split(/,/, $userlist[$i]);
                    &CSAVE;
                    #銃声ログ読込

                    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);

                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[0]) ;
                    if (($now < ($guntime+(15)))&& ($wid ne $id) && ($wid2 ne $id)) {   #銃使用から15秒以内？
                        $jyulog = "<font color=\"yellow\"><b>$gunpls の方で、銃声が聞こえた・・・。</b></font><br>" ;
                    } else { $jyulog = "" ; }
                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[1]) ;
                    if (($now < ($guntime+(15)))&& ($wid ne $id) && ($wid2 ne $id) && ($place[$pls] eq $gunpls)) {  #殺害から15秒以内？
                        $jyulog2 = "<font color=\"yellow\"><b>近くで悲鳴が？誰か、殺されたのか・・・？</b></font><br>" ;
                    } else { $jyulog2 = "" ; }
                    local($guntime,$gunpls,$wid,$wid2,$a) = split(/,/,$gunlog[2]) ;
                    if (($now < ($guntime+(30)))) { #スピーカ使用から30秒以内？
                        $jyulog3 = "<font color=\"yellow\"><b>$gunpls の方から$widの声が聞こえる・・・</b></font><br><font color=\"lime\"><b>『$wid2』</b></font><br>" ;
                    } else { $jyulog3 = "" ; }
                } else {
                    &CDELETE;
                    &ERROR("既に死亡しています。<BR><BR>死因：$w_death<BR><BR><font color=\"lime\"><b>$w_msg</b></font><br>") ;
                }
            } else {
                &ERROR("パスワードが一致しません。") ;
            }
        } else {
            if ($w_hit > 0) {
                $plsmem[$w_pls]++ ;
                if ($w_sts ne "NPC0"){ $mem ++ ; }
                }
        }
    }

    if ($chksts eq "NG") {
        &ERROR("ＩＤが見つかりません。") ;
    }

    local($b_limit) = ($battle_limit * 3) + 1;
    if ((($mem == 1) && ($inf =~ /勝/) && ($ar > $b_limit))||(($mem == 1) && ($ar > $b_limit))) {    #優勝？
        if($fl !~ /終了/){
            open(FLAG,">$end_flag_file"); print(FLAG "終了\n"); close(FLAG);
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

    if (($Command ne "INN2")&&($Command ne "HEAL2")) {
        $up = int(($now - $endtime) / (1*$kaifuku_time));
        if ($inf =~ /腹/) { $up = int($up / 2) ; }
        if ($sts eq "睡眠") {
            $maxp = $maxsta - $sta ;    #最大値までいくつ
            if ($up > $maxp) { $up = $maxp ; }
            $sta += $up ;
            if ($sta > $maxsta) { $sta = $maxsta ; }
            $log = ($log . "睡眠の結果、スタミナが $up 回復した。<BR>") ;
            $sts = "正常"; $endtime = 0 ;
            &SAVE ;
        } elsif ($sts eq "治療") {
            if ($kaifuku_rate == 0){$kaifuku_rate = 1;}
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

    ($w_name,$w_kind) = split(/<>/, $wep);
    ($b_name,$b_kind) = split(/<>/, $bou);

    $up = int(($level*$baseexp)+(($level-1)*$baseexp)) ;

    $cln = "$cl $sex$no番" ;

    if (($w_kind =~ /G|A/) && ($wtai == 0)) { #棍棒 or 弾無し銃 or 矢無し弓
        $watt_2 = int($watt/10) ;
    } else {
        $watt_2 = $watt ;
    }

    $ball = $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #装飾が防具？

    if($icon_mode){ $colum = 2;}else{$colum = 3;}

print <<"_HERE_";
<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">$place[$pls]（$area[$pls]）</FONT></B><BR>
</P>
<TABLE width="568">
<TR><TD><B><FONT color="#ff0000">
@links
</FONT></B></TD></TR>
</TABLE>

<TABLE width="568">
  <TBODY>
    <TR>
      <TD valign="top" width="279" height="311">
      <TABLE border="1" width="389" cellspacing="0" height="300">
        <TBODY>
          <TR>
            <TD colspan="4" align="center"><B>ステータス</B></TD>
          </TR>
          <TR>
_HERE_
            if($icon_mode){
                print "<TD ROWSPAN=\"3\" width=\"70\"><IMG src=\"$imgurl$icon_file[$icon]\" width=\"70\" height=\"70\" border=\"0\" align=\"middle\"></TD>\n";
            }
print <<"_HERE_";
            <TD width="60"><B>　氏　名</B></TD>
            <TD colspan="$colum" width="224">$f_name $l_name</TD>
          </TR>
          <TR>
            <TD><B>出席番号</B></TD>
            <TD colspan="$colum">$cln</TD>
          </TR>
          <TR>
            <TD ><B>負傷個所</B></TD>
_HERE_
            $kega ="" ;
            if ($inf =~ /頭/) {$kega = ($kega . "頭部　") ;}
            if ($inf =~ /腕/) {$kega = ($kega . "腕　") ;}
            if ($inf =~ /腹/) {$kega = ($kega . "腹部　") ;}
            if ($inf =~ /足/) {$kega = ($kega . "足　") ;}
            if ($kega eq "") { $kega = "　" ;}
print <<"_HERE_";
            <TD colspan="$colum">$kega</TD>
          </TR>
          <TR>
            <TD width="45"><B>レベル</B></TD>
            <TD width="45">$level</TD>
            <TD width="45"><B>経験値</B></TD>
            <TD>$exp/$up</TD>
          </TR>
          <TR>
            <TD><B>体力</B></TD>
            <TD>$hit/$mhit</TD>
            <TD><B>スタミナ</B></TD>
            <TD>$sta/$maxsta</TD>
          </TR>
          <TR>
            <TD><B>攻撃力</B></TD>
            <TD>$att+$watt_2</TD>
            <TD><B>武器</B></TD>
            <TD>$w_name/$wtai</TD>
          </TR>
          <TR>
            <TD><B>防御力</B></TD>
            <TD>$def+$ball</TD>
            <TD><B>防具</B></TD>
            <TD>$b_name/$btai</TD>
          </TR>
          <TR>
            <TD height="9" colspan="4" align="center"><B>所持品</B></TD>
          </TR>
          <TR>
            <TD colspan="4" height="80" valign="top">
_HERE_

            for ($i=0; $i<5; $i++) {
                if ($item[$i] ne "なし") {
                    ($i_name,$i_kind) = split(/<>/, $item[$i]);
                    print "$i_name/$eff[$i]/$itai[$i]<BR>\n";
                }
            }

print <<"_HERE_";
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" width="200" height="310">
      <TABLE border="1" cellspacing="0">
        <TBODY>
          <TR><TD align="center" width="250"><B>コマンド</B></TD>
          <TR>
            <TD align="left" valign="top" height="280" width="240">
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
            <TD height="20" valign="top" width="600">$log</TD>
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
            if ($ENV{'CONTENT_LENGTH'} > 51200) {
                &ERROR("異常な入力です"); }
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

        $in{$name} = $value;
    }

    $mode = $in{'mode'};
    $id2 = $in{'Id'};
    $password2 = $in{'Password'};

    $Command = $in{'Command'};
    $Command2 = $in{'Command2'};

    $l_name2 = $in{'L_Name'} ;
    $f_name2 = $in{'F_Name'} ;
    $msg2 = $in{'Message'} ;
    $dmes2 = $in{'Message2'} ;
    $dengon = $in{'Dengon'} ;
    $com2 = $in{'Comment'} ;
    $sex2 = $in{'Sex'};
    $icon2 = $in{'Icon'};
    $itno2 = $in{'Itno'};
    $getid = $in{'WId'};
    $speech = $in{'speech'};

    srand;

}

#==================#
# ■ メニュー部    #
#==================#
sub COMMAND {

    local($i) = 0 ;

    if (($Command eq "INN2") || ($Command eq "HEAL2") || ($Command eq "KEIKAI2")) {
        if ($Command eq "HEAL2") {
            $log = ($log . "怪我の治療をしよう。<BR>") ;
            $sts = "治療" ;
            print "治療中・・・。<BR><BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"HEAL2\" checked>治療<BR><BR>\n";
        } else {
            $log = ($log . "少し寝ておくか。<BR>") ;
            $sts = "睡眠" ;
            print "睡眠中・・・。<BR><BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"INN2\" checked>睡眠<BR><BR>\n";
        }
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\">戻る<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
        return ;
    }

    if (($Command eq '')||($Command eq "MAIN")) {   #MAIN
        $log = ($log . "$jyulog$jyulog2$jyulog3さて、どうしよう・・・。<br>") ;
        print "何を行いますか？<BR><BR>\n";
        if ($place[$pls] eq "分校") {
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"MOVE\" checked>移動<BR>\n";
            if ($hackflg == 1) {
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"SEARCH\">探索<BR>\n";
            }
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"ITMAIN\">アイテム<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"SPECIAL\">特殊\<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"USRSAVE\">セーブ\<BR>\n";
        } else {
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"MOVE\" checked>移動<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"SEARCH\">探索<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"ITMAIN\">アイテム<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"HEAL\">治療<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"INN\">睡眠<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"SPECIAL\">特殊\<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"USRSAVE\">セーブ\<BR>\n";
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "MOVE") {  #移動

        $log = ($log . "$place[$pls]から、他の場所へ移動するか・・・。<br>") ;
        print "何処へ行きますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "<option value=\"MAIN\" selected>戻る\n";
        for ($j=0; $j<$#place+1; $j++) {
            if ($place[$j] ne $place[$pls]) {
                print "<option value=\"MV$j\">$place[$j]($area[$j])</option>\n";
            }
        }
        print "</select><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "ITEM") {  #アイテム
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "DEL") {   #アイテム投棄
        $log = ($log . "デイパックの中を整理するか・・・。<BR>") ;
        print "何を捨てますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        for ($i=0; $i<5; $i++) {
            if ($item[$i] ne "なし") {
                ($in, $ik) = split(/<>/, $item[$i]);
                print "　<INPUT type=\"radio\" name=\"Command\" value=\"DEL_$i\">$in/$eff[$i]/$itai[$i]<BR>\n";
            }
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "SEIRI") { #アイテム整理
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "GOUSEI") { #アイテム合成
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "OUKYU") { #応急処置
        $log = ($log . "怪我の治療をするか・・・。<BR>") ;

        print "何処を治療しますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";

        if ($inf =~ /頭/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_0\">頭<BR>\n"; }
        if ($inf =~ /腕/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_1\">腕<BR>\n"; }
        if ($inf =~ /腹/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_2\">腹部<BR>\n"; }
        if ($inf =~ /足/) { print "　<INPUT type=\"radio\" name=\"Command\" value=\"OUK_3\">足<BR>\n"; }

        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "POISON") {    #毒物混入
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "PSCHECK") {   #毒見
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
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "SPIICH") { #携帯スピーカ使用
        $log = ($log . "これを使えば、みんなに聞こえる筈だな・・・<BR>") ;
        print "携帯スピーカを使って、全員に伝言を伝えます。<BR>\n";
        print "（全角２０文字まで）<BR><BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"speech\"maxlength=\"50\"><BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"SPEAKER\">伝える<BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>止める<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "WINCHG") {    #口癖変更
        $log = ($log . "殺害時、死亡時の口癖を変更します。<BR>") ;
        print "口癖を入力してください<BR>\n";
        print "（全角３２文字まで）<BR><BR>\n";
        print "殺害時：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Message\" maxlength=\"64\" value=\"$msg\"><BR><BR>\n";
        print "遺言：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Message2\" maxlength=\"64\" value=\"$dmes\"><BR><BR>\n";
        print "一言コメント：<BR>\n";
        print "　<INPUT size=\"30\" type=\"text\" name=\"Comment\" maxlength=\"64\" value=\"$com\"><BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "ITMAIN") {    #アイテム
        $log = ($log . "デイパックの中には、何が入っていたかな・・・。<BR>") ;
        print "何を行いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"ITEM\">アイテム使用・装備<BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"DEL\">アイテム投棄<BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"SEIRI\">アイテム整理<BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"GOUSEI\">アイテム合成<BR>\n";
        if ($wep ne "素手<>WP") {
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL\">装備武器を外す<BR>\n";
            print "　<INPUT type=\"radio\" name=\"Command\" value=\"WEPDEL2\">装備武器投棄<BR>\n";
        }
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "SPECIAL") {   #特殊
        $log = ($log . "特殊コマンドです。<BR>") ;
        print "何を行いますか？<BR><BR>\n";
        print "　<select name=\"Command\">\n" ;
        print "　<option value=\"MAIN\" selected>戻る</option>\n";
        print "　<option value=\"DEFCHK\">装備確認</option>\n";
        print "　<option value=\"WINCHG\">口癖変更</option>\n";
        print "　<option value=\"WEPPNT\">熟練レベル確認</option>\n";
        print "　<option value=\"OUKYU\">応急処置</option>\n";
        if ($club eq "料理研究部" ) { print "　<option value=\"PSCHECK\">毒見</option>\n"; }
        for ($poi=0; $poi<5; $poi++){
            if ($item[$poi] eq "毒薬<>Y") {
                print "　<option value=\"POISON\">毒物混入</option>\n";
                last;
            }
        }
        for ($spi=0; $spi<5; $spi++){
            if ($item[$spi] eq "携帯スピーカ<>Y") {
                print "　<option value=\"SPIICH\">スピーカ使用</option>\n";
                last;
            }
        }
        for ($paso=0; $paso<5; $paso++){
            if (($item[$paso] eq "モバイルPC<>Y")&&($itai[$paso] >= 1)) {
                print "　<option value=\"HACK\">ハッキング</option>\n";
                last;
            }
        }

        print "</select><BR>\n" ;
        print "<BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    } elsif ($Command eq "USRSAVE") {   #ユーザデータ保存
        &u_save;
    } else {
        print "何を行いますか？<BR><BR>\n";
        print "　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
        print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
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
        if ($hit <= 0) {
            $userlist[$Index] = "$id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,\n" ;
        } else {
            $userlist[$Index] = "$id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,\n" ;
        }
        open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
    }


}
#====================#
# ■ 敵情報保存      #
#====================#
sub SAVE2 {


    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    if ($w_hit <= 0) { $w_sts = "死亡"; }
    $userlist[$Index2] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,\n" ;

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
            ($c_id,$c_password,$c_f_name,$c_l_name,$c_sex,$c_cl,$c_no,$c_endtime,$c_att,$c_def,$c_hit,$c_mhit,$c_level,$c_exp,$c_sta,$c_wep,$c_watt,$c_wtai,$c_bou,$c_bdef,$c_btai,$c_bou_h,$c_bdef_h,$c_btai_h,$c_bou_f,$c_bdef_f,$c_btai_f,$c_bou_a,$c_bdef_a,$c_btai_a,$c_tactics,$c_death,$c_msg,$c_sts,$c_pls,$c_kill,$c_icon,$c_item[0],$c_eff[0],$c_itai[0],$c_item[1],$c_eff[1],$c_itai[1],$c_item[2],$c_eff[2],$c_itai[2],$c_item[3],$c_eff[3],$c_itai[3],$c_item[4],$c_eff[4],$c_itai[4],$c_item[5],$c_eff[5],$c_itai[5],$c_log,$c_dmes,$c_bid,$c_club,$c_wn,$c_wp,$c_wa,$c_wg,$c_we,$c_wc,$c_wd,$c_wb,$c_wf,$c_ws,$c_com,$c_inf,$c_f_name_y,$c_l_name_y,$c_koma) = split(/,/, $cooks);
        }
    }
}

#====================#
# ■ クッキー保存    #
#====================#
sub CSAVE {
    $cook = "$id,$password,$f_name,$l_name,$sex,$cl,$no,0,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,";
    $cook =~ s/(.)/sprintf("%02X", unpack("C", $1))/eg;
    print "Set-Cookie: BR=$cook; expires=$expires\n";
}

#====================#
# ■ クッキー削除    #
#====================#
sub CDELETE {
    $cook = ",,,,,,,$now,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,";
    $cook =~ s/(.)/sprintf("%02X", unpack("C", $1))/eg;
    print "Set-Cookie: BR=$cook; expires=$expires\n";
}

#====================#
# ■ 戦略計算        #
#====================#
sub TACTGET {

    $chkpnt = 5 ;   #敵、アイテム発見率
    $chkpnt2 = 5 ;  #先制攻撃率
    $atp = 1.00 ;
    $dfp = 1.00 ;

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

    local($kind) = $w_kind ;
    local($wmei) = 0;
    local($wweps) = "" ;

    if (($kind =~ /B/) || (($kind =~ /G|A/) && ($wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wb/$BASE);
    } elsif ($kind =~ /A/) {        #射
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wa/$BASE);
    }elsif ($kind =~ /C/) { #投
        $wweps = "L" ;
        $wmei = 70 ;
        $wmei += int($wc/$BASE);
    }elsif ($kind =~ /D/) { #爆
        $wweps = "L" ;
        $wmei = 50 ;
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
}
#====================#
# ■ 戦略計算        #
#====================#
sub TACTGET2 {

    $atn = 1.00 ;
    $dfn = 1.00 ;
    $sen = 1.0 ;

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

    local($kind) = $w_kind2 ;
    local($wmei) = 0;
    local($wweps) = "" ;

    if (($kind =~ /B/) || (($kind =~ /G|A/) && ($w_wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
        $wweps = "S" ;
        $wmei = 80 ;
        $wmei += int($wb/$BASE);
    } elsif ($kind =~ /A/) {        #射
        $wweps = "L" ;
        $wmei = 60 ;
        $wmei += int($wa/$BASE);
    }elsif ($kind =~ /C/) { #投
        $wweps = "L" ;
        $wmei = 70 ;
        $wmei += int($wc/$BASE);
    }elsif ($kind =~ /D/) { #爆
        $wweps = "L" ;
        $wmei = 50 ;
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
            &SAVE;return;
        }elsif($d_mode eq "eve"){
            $Command = "EVENT";
        }
    } elsif ($hit > $mhit) { $hit = $mhit ; }
}

#=============================#
# ■ ユーザ単位のデータセーブ #
#=============================#
sub u_save{
    local($u_dat) = "$id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,\n" ;

    open(DB,">$u_save_dir$id$u_save_file"); seek(DB,0,0); print DB $u_dat; close(DB);

    $log = ($log . "セーブは正常に終了しました。<BR>") ;
    print "<br>　<INPUT type=\"radio\" name=\"Command\" value=\"MAIN\" checked>戻る<BR><BR>\n";
    print "　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n";
    return ;

}

1
