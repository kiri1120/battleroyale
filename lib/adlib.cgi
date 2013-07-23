#==================#
# ■ データ初期化    #
#==================#
sub DATARESET {

    @userlist = ();
    if($npc_mode eq "0"){
        open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
    }else{
        open(DB,"$npc_file");seek(DB,0,0); @baselist=<DB>;close(DB);
        $LEN = @baselist;

        if ($LEN > 0) {
            for ($i=0; $i<$LEN; $i++) {
                ($w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_att,$w_def,$w_mhit,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_msg,$w_sts,$w_pls,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_dmes,$w_com,$w_inf,$w_feel,$w_group,$w_gpass) = split(/,/, $baselist[$i]);

                if ($w_cl eq $BOSS) {  #政府側のNPC
                    $w_att = int(rand(10)) + $w_att ;
                    $w_def = int(rand(10)) + $w_def ;
                    $w_mhit = int(rand(30)) + $w_mhit ;
                    $w_icon = $n_icon_file[$w_icon];
                } elsif ($w_cl eq $ZAKO) {  #政府側のNPC
                    $w_att = int(rand(5)) + $w_att ;
                    $w_def = int(rand(5)) + $w_def ;
                    $w_mhit = int(rand(15)) + $w_mhit ;
                    $w_icon = $n_icon_file[$w_icon];
                } else {  #その他のNPCはこっち
                    $w_att = int(rand(5))  + $w_att ;
                    $w_def = int(rand(5))  + $w_def ;
                    $w_mhit = int(rand(10)) + $w_mhit ;
                    $w_icon = $icon_file[$w_icon];
                }
                if ($w_pls == 99) { $w_pls = int(rand($#area)+1) ; }
                $w_level = 1; $w_exp = 0;
                $w_kill = 0 ;
                $w_death = "" ;
                $w_we = $w_wf = "";
                $w_log = "" ; $w_bid = "" ;
                $w_host = $w_os = "";
                $w_a_name = "";

                $w_id = ($a_id . "$i"); $w_password = $a_pass2;
                $w_hit=$w_mhit; $w_sta = $maxsta;
                $w_feel = int(rand(20)) + $w_feel ;
                if ($w_feel > 300) { $w_feel = 300;}

                for ($j=0; $j<5; $j++) {
                    if($w_item[$j] =~ /<>HH/){
                        if (int(rand(2)) == 0) { $w_item[$j] =~ s/<>HH/<>HD2/g; }
                    }elsif ($w_item[$j] =~ /<>SH/) {
                        if (int(rand(2)) == 0) { $w_item[$j] =~ s/<>SH/<>SD2/g; }
                    }
                }

                &NPCCLUBMAKE;

                $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os,\n" ;
            }
        }
        open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
    }

    #時間ファイル更新
    $endtime = $now + ($battle_limit*60*60*24);
    $timelist="$now,$endtime,\n" ;
    open(DB,">$time_file"); seek(DB,0,0); print DB $timelist; close(DB);

    #生徒番号ファイル更新
    $memberlist="0,0,0,0,\n" ;
    open(DB,">$member_file"); seek(DB,0,0); print DB $memberlist; close(DB);

    #禁止エリアファイル更新
    ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($now+(1*60*60*24));
    $year+=1900;
    $min = "0$min" if ($min < 10);  $month++;
    $areadata[0] = ($year . "," . $month . "," . $mday . "," . "0,0\n") ;   #エリア追加時刻
    $areadata[1] = "1,0,,\n" ; #禁止エリア数、ハッキングフラグ

    @work = @place ;
    @work2 = @area ;
    @work3 = @arno ;

    $ar = splice(@work,0,1) ;
    $areadata[2] = "$ar," ;
    $ar2 = splice(@work2,0,1) ;
    $areadata[3] = "$ar2," ;
    $ar3 = splice(@work3,0,1) ;
    $areadata[4] = "$ar3," ;

    for ($i=1; $i<$#place+1; $i++) {
        $chk=$#work+1;$index = int(rand($chk));
        $ar = splice(@work,$index,1) ;
        $areadata[2] = ($areadata[2] . "$ar,");
        $ar2 = splice(@work2,$index,1) ;
        $areadata[3] = ($areadata[3] . "$ar2,");
        $ar3 = splice(@work3,$index,1) ;
        $areadata[4] = ($areadata[4] . "$ar3,");
    }
    $areadata[2] = ($areadata[2] . "\n");
    $areadata[3] = ($areadata[3] . "\n");
    $areadata[4] = ($areadata[4] . "\n");

    open(DB,">$area_file"); seek(DB,0,0); print DB @areadata; close(DB);

    #ログ更新
    $loglist = "$now,,,,,,,,,,,NEWGAME,,,,,\n" ;
    open(DB,">$log_file"); seek(DB,0,0); print DB $loglist; close(DB);
    open(DB,">$joutolog_file"); seek(DB,0,0); print DB $loglist; close(DB);

    $loglist = "" ;
    open(DB,">$error_file"); seek(DB,0,0); print DB $loglist; close(DB);

    open(DB, "$A_Rogin_file"); seek(DB,0,0); @loglist=<DB>;close(DB);
    while (50 <= @loglist) { shift(@loglist); }
    @loglist = (@loglist, "$now,$year/$month/$mday $hour:$min:$sec,$admpass,$host,FORMATED,\n");
    open(DB,">$A_Rogin_file"); seek(DB,0,0); print DB @loglist; close(DB);

    for($i=1; $i<=7; $i++) {
        open(DB,">$ADM_DIR/succeed$i.log"); seek(DB,0,0); print DB $loglist; close(DB);
        open(DB,">$ADM_DIR/faired$i.log"); seek(DB,0,0); print DB $loglist; close(DB);
    }

    for ($i=0; $i<$#area+1; $i++) {
        @areaitem = "" ;
        $filename = "$LOG_DIR/$i$item_file";
        open(DB,">$filename"); seek(DB,0,0); print DB @areaitem; close(DB);
    }

    #メッセ保存データ削除
    open(DB,">$MES_DIR$mes_file"); seek(DB,0,0); print DB $loglist; close(DB);

    #アイテムファイル更新
    open(DB, "$haitem_file");seek(DB,0,0); @itemlist=<DB>;close(DB);

    for ($i=0; $i<$#itemlist+1; $i++) {
        ($w_i,$w_e,$w_t) = split(/,/, $itemlist[$i]);

        $idx = int(rand($#place)+1) ;

        $filename = "$LOG_DIR/$idx$item_file";
        $newitem = "$w_i,$w_e,$w_t,\n";
        open(DB,">>$filename"); seek(DB,0,0); print DB $newitem; close(DB);
    }

    #銃声ログファイル更新
    local($null_data) = "0,,,,\n";
    open(DB,">$gun_log_file");
    for ($i=0; $i<6; $i++){
        print DB $null_data;
    }
    close(DB);

    @f_list = ();
    #ユーザ保存データ削除
    opendir(DIR, "$u_save_dir");
    foreach $file (readdir(DIR)) {
        unless($file =~ /^\.{1,2}$/){
            if($file =~ /$u_save_file/){
                push (@f_list,"$u_save_dir$file");
            }
        }
    }
    closedir(DIR);
    unlink(@f_list);

    #FLAGファイル更新
    open(FLAG,">$end_flag_file"); print FLAG ""; close(FLAG);

}
#==================#
# ■ 履歴作成      #
#==================#
sub WINLOG {

    if($fl !~ /終了/) { &ERROR("まだ終了していません。") ; }

    #設定
    $game = "第$kaisuu回正式プログラム結果";
    $imgurl = "../iconimg/";

    #優勝者判別
    $mem = 0; $winkind = "";
    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
        if ($w_inf =~ /勝/) {    #優勝？
            ($id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$ho2,$os2) = split(/,/, $userlist[$i]);
            $winkind = "優勝";
            last;
        } elsif ($w_inf =~ /解/){
            ($id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$ho2,$os2) = split(/,/, $userlist[$i]);
            $winkind = "解除キー使用";
            last;
        } else {
            if (($w_hit > 0) && ($w_inf !~ /NPC/)) {
                $mem++;
                $no = $i;
            }
        }
    }
    if ($winkind eq "") {
        if ($mem == 1) {
            ($id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$ho2,$os2) = split(/,/, $userlist[$no]);
            $winkind = "優勝";
        } else {
            &ERROR("まだ終了していません。");
        }
    }

    #表示用計算
    local($w_name,$w_kind) = split(/<>/, $wep);
    local($b_name,$b_kind) = split(/<>/, $bou);
    local($b_name_h,$b_kind_h) = split(/<>/, $bou_h);
    local($b_name_f,$b_kind_f) = split(/<>/, $bou_f);
    local($b_name_a,$b_kind_a) = split(/<>/, $bou_a);
    local($b_name_i,$b_kind_i) = split(/<>/, $item[5]);

    $up = ($level * $level) + ($level * $baseexp);

    $cln = "$cl $sex$no番" ;

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

    if (($we eq "B") && ($w_kind =~ /B/)) { $tactics2 = "（反撃：棍）"; }
    elsif (($we eq "P") && ($w_kind =~ /P/)) { $tactics2 = "（反撃：殴）"; }
    elsif (($we eq "A") && ($w_kind =~ /A/) && ($wtai > 0)) { $tactics2 = "（反撃：弓）"; }
    elsif (($we eq "G") && ($w_kind =~ /G/) && ($wtai > 0)) { $tactics2 = "（反撃：銃）"; }
    elsif (($we eq "N") && ($w_kind =~ /N/)) { $tactics2 = "（反撃：斬）"; }
    elsif (($we eq "S") && ($w_kind =~ /S/)) { $tactics2 = "（反撃：刺）"; }
    elsif (($we eq "D") && ($w_kind =~ /D/)) { $tactics2 = "（反撃：爆）"; }
    elsif (($we eq "C") && ($w_kind =~ /C/)) { $tactics2 = "（反撃：投）"; }
    else { $tactics2 = "（反撃：指定無し）"; }

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

    local($hitbarleng) = int($hit / $mhit * 45);
    local($hitbarlenr) = 45 - $hitbarleng;
    local($stabarleng) = int($sta / $maxsta * 45);
    local($stabarlenr) = 45 - $stabarleng;

    local($nowtime) = sprintf("%04d年%02d月%02d日（%s）%02d:%02d:%02d",$year, $month, $mday, ('日','月','火','水','木','金','土') [$wday], $hour, $min, $sec);

    &HEADER ;
print <<"_HERE_";
<TABLE width="400">
  <TBODY>
    <TR>
      <TD align="center">
       <B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">$game</FONT></B><BR><BR>
       <B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">$winkind者</FONT></B>
      </TD>
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
            <TH width="16%" nowrap>氏 名</TH><TD nowrap colspan="3">$f_name $l_name ($cln)</TD>
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
            <TH nowrap>負傷個所</TH>
            <TD nowrap colspan="2">$kega</TD>
            <TH nowrap>殺害</TH><TD nowrap><font color="red"><b>$kill</b></font>人殺害</TD>
          </TR>
          <TR>
            <TH nowrap>グループ</TH><TD nowrap colspan="2">$group</TD>
            <TH nowrap>攻撃力</TH><TD nowrap>$att+$watt_2</TD>
          </TR>
          <TR>
            <TH nowrap>方針</TH><TD nowrap colspan="2">$tactics $tactics2</TD>
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
                    print "$i_name/$eff[$i]/$itai[$i]<BR>\n";
                }
            }

print <<"_HERE_";
            </TD>
          </TR>
          <TR height="9"><TH colspan="5">コメント</TH></TR>
          <TR height="70" align="center">
            <TD nowrap colspan="5"><B>$com</B></TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
    </TR>
  </TBODY>
</TABLE>
<BR>
_HERE_

    if($winkind eq "解除キー使用") {
        push(@log,"<P align=\"center\"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">脱走者一覧</FONT></B><BR></P>");
        push(@log,"<TABLE border=\"1\" cellspacing=\"0\" width=\"568\">\n");
        push(@log,"<tr align=\"center\"><th nowrap>アイコン</th><th nowrap>名前</th><th nowrap>部活</th><th nowrap>グループ</th><th width=\"100%\">コメント</th></tr>\n");
        foreach (0 .. $#userlist) {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$_]);

            if (($w_hit > 0) && ($id ne $w_id) && (($w_inf !~ /NPC0/) || ($hackflg))) {
                if ($w_a_name ne "") { $w_a_name = "($w_a_name)"; }
                push(@log,"<tr><td align=\"center\"><IMG src=\"$imgurl$w_icon\" width=\"70\" height=\"70\" border=\"0\"></td><td align=\"center\" nowrap>$w_cl $w_sex$w_no番<br>$w_f_name $w_l_name<br>$w_a_name</td><td align=\"center\" nowrap>$w_club<br><font color=\"red\"><b>$w_kill</b></font>人殺害</td><td align=\"center\" nowrap>$w_group</td><td width=\"100%\">$w_com</td></tr>\n");
            }
        }
        push(@log,"</table><BR>\n");
    }

    push (@log,"</CENTER>\n") ;
    push (@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">進行状況</FONT></B><BR><BR>\n");

    open(DB,"$log_file");seek(DB,0,0); @loglist=<DB>;close(DB);

    $getmonth=$getday=0;
    foreach $loglist(@loglist) {
        ($gettime,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_f_name2,$w_l_name2,$w_sex2,$w_cl2,$w_no2,$getkind,$info1,$info2,$info3)= split(/,/, $loglist);
        ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($gettime);
        $hour = "0$hour" if ($hour < 10);
        $min = "0$min" if ($min < 10);  $month++;
        $year += 1900;
        $week = ('日','月','火','水','木','金','土') [$wday];
        if (($getmonth != $month) || ($getday != $mday)) {
            if ($getmonth !=0) { push (@log,"</LI></UL>\n"); }
            $getmonth=$month;$getday = $mday;
            push (@log,"<P><font color=\"lime\"><B>$month月 $mday日 ($week曜日)</B></font><BR>\n");
            push (@log,"<UL>\n");
        }

        if ($info1 eq "") { $info1 = ""; } else { $info1 = "($info1)" ; }

        if ($getkind eq "DEATH") {  #死亡（自分が原因）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>死亡</b></font>した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH1") { #死亡（毒殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>服毒死</b></font>した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH2") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"yellow\"><b>$w_f_name2 $w_l_name2（$w_cl2 $w_sex2$w_no2番）</b></font>に<font color=\"aqua\"><b>$info2</b></font>で<font color=\"red\"><b>返り討ち</b></font>にされた。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH3") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"yellow\"><b>$w_f_name2 $w_l_name2（$w_cl2 $w_sex2$w_no2番）</b></font>に<font color=\"aqua\"><b>$info2</b></font>で<font color=\"red\"><b>$info3</b></font>された。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH4") { #死亡（政府）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が政府に<font color=\"red\"><b>処刑</b></font>された。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATHAREA") { #死亡（禁止エリア）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>禁止エリア</b></font>の為、死亡した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "WINEND") { #優勝者決定
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>ゲーム終了・以上本プログラム実施本部選手確認モニタより</B></font> <BR>\n") ;
        } elsif ($getkind eq "EX_END") { #プログラム停止
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>ゲーム終了・プログラム緊急停止</B></font> <BR>\n") ;
        } elsif ($getkind eq "HACK") { #ハッキング
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）によってハッキングを受け、分校の機能が停止！！</B></font> <BR>\n") ;
        } elsif ($getkind eq "SPEAKER") { #叫ぶ
            push (@log,"<LI>$hour時$min分、<font color=\"aqua\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が <font color=\"aqua\"><b>$info1</b></font> と叫んだ。<BR>\n") ;
        } elsif ($getkind eq "AREA") { #禁止エリア追加
            if ($info2 == 7) {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>プログラム最終日開始</b></font>。<BR>\n") ;
            } elsif ($info2 == 8) {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>時間切れによりゲーム終了</b></font>。<BR>\n") ;
            } else {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>プログラム$info2日目開始</b></font>。<BR>\n") ;
            }
        } elsif ($getkind eq "ENTRY") { #新規登録
            push (@log,"<LI>$hour時$min分、<font color=\"yellow\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 転校してきた。<font color=\"yellow\">$info1</font><BR>\n") ;
        } elsif ($getkind eq "NEWGAME") { #管理人によるデータ初期化
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>新規プログラム開始</b></font>。<BR>\n") ;
        }
    }

    push (@log,"</UL>\n<CENTER>\n");
    push (@log,"<BR><B><a href=\"$home\">HOME</A></B><BR>\n");

    print @log;
    &FOOTER;
}

#==================#
# ■ クラブ作成    #
#==================#
sub NPCCLUBMAKE {


    local($dice) =  rand(100) ;
    local($dice2) = int(rand(8)) ;
    local($dice3) = int(rand(6)) ;

    if (($w_cl eq $BOSS) || ($w_cl eq $ZAKO)) {
        $w_club = "政府軍";
        $w_wa = $w_wg = $w_wc = $w_wd = $w_ws = $w_wn = $w_wb = $w_wp = 4 * $BASE;
    } else {
        $w_wa = int(rand(15)); $w_wg = int(rand(15));
        $w_wc = int(rand(15)); $w_wd = int(rand(15));
        $w_ws = int(rand(15)); $w_wn = int(rand(15));
        $w_wb = int(rand(15)); $w_wp = int(rand(15));
        if ($dice < 80) {
            if ($dice2 == 0) {
                $w_club = "弓道部";
                $w_wa += 1 * $BASE;
            }elsif ($dice2 == 1) {
                $w_club = "射撃部";
                $w_wg += 1 * $BASE;
            }elsif ($dice2 == 2) {
                $w_club = "空手部";
                $w_wb += 1 * $BASE;
            }elsif ($dice2 == 3) {
                $w_club = "バスケ部";
                $w_wc += 1 * $BASE;
            }elsif ($dice2 == 4) {
                $w_club = "科学部";
                $w_wd += 1 * $BASE;
            }elsif ($dice2 == 5) {
                $w_club = "フェンシング部";
                $w_ws += 1 * $BASE;
            }elsif ($dice2 == 6) {
                $w_club = "剣道部";
                $w_wn += 1 * $BASE;
            }else {
                $w_club = "ボクシング部";
                $w_wp += 1 * $BASE;
            }
        } else {
            if ($dice3 == 0) {
                $w_club = "陸上部" ;
            }elsif ($dice3 == 1) {
                $w_club = "料理研究部" ;
            }elsif ($dice3 == 2) {
                $w_club = "パソコン部" ;
            }elsif ($dice3 == 31) {
                $w_club = "保健委員" ;
            }elsif ($dice3 == 4) {
                $w_club = "サバイバル部" ;
            }else {
                $w_club = "演劇部" ;
            }
        }
    }
}

#================#
# ■ 初期化準備  #
#================#
sub InitResetTime {
    if ($auto_reset) {
        local($sec,$min,$hour,$mday,$month,$year) = localtime($now+(60*60*12)+int(rand(60*60*12)));
        $year += 1900; $month++;
        $newareadata[0] = "$year,$month,$mday,$hour,0,\n";   #自動初期化時刻
        $newareadata[1] = "$ar,0,初期化,\n";
        $newareadata[2] = $arealist[2];
        $newareadata[3] = $arealist[3];
        $newareadata[4] = $arealist[4];
        open(DB,">$area_file"); seek(DB,0,0); print DB @newareadata; close(DB);
    }
}

#==================#
# ■ 設定フォーム  #
#==================#
sub INITFORM {

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"初期化時間設定\n");
    push(@log,"<FORM METHOD=\"POST\">\n");
    push(@log,"<INPUT TYPE=\"HIDDEN\" NAME=\"Command\" VALUE=\"RESINI2\">\n");
    push(@log,"<INPUT type=\"hidden\" name=\"Password\" value=\"$admpass\">\n");
    push(@log,"年：<INPUT size=\"8\" type=\"text\" name=\"resyear\" maxlength=\"8\"><br>\n");
    push(@log,"月：<INPUT size=\"8\" type=\"text\" name=\"resmon\" maxlength=\"8\"><br>\n");
    push(@log,"日：<INPUT size=\"8\" type=\"text\" name=\"resday\" maxlength=\"8\"><br>\n");
    push(@log,"時：<INPUT size=\"8\" type=\"text\" name=\"reshour\" maxlength=\"8\"><br>\n");
    push(@log,"分：<INPUT size=\"8\" type=\"text\" name=\"resmin\" maxlength=\"8\"><br>\n");
    push(@log,"<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n");
    push(@log,"</FORM>\n");

    &HEADER ;
    print @log;
    &FOOTER;
}

#==================#
# ■ 初期化時間設定#
#==================#
sub RESINIT {

    if ($in{'resyear'} ne "" && $in{'resmon'} ne "" && $in{'resday'} ne "" && $in{'reshour'} ne "" && $in{'resmin'} ne "") {
        $newareadata[0] = "$in{'resyear'},$in{'resmon'},$in{'resday'},$in{'reshour'},$in{'resmin'},\n";   #自動初期化時刻
        $newareadata[1] = "$ar,0,初期化,\n";
        $newareadata[2] = $arealist[2];
        $newareadata[3] = $arealist[3];
        $newareadata[4] = $arealist[4];
        open(DB,">$area_file"); seek(DB,0,0); print DB @newareadata; close(DB);
        open(FLAG,">$end_flag_file"); print FLAG "終了\n"; close(FLAG);
        push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
        push(@log,"初期化時刻を”$in{'resyear'}/$in{'resmon'}/$in{'resday'} $in{'reshour'}:$in{'resmin'}:0”に設定しました。<br>\n");
        push(@log,"<br><B><FONT color=\"#ff0000\">>><a href=\"$home\">HOME</a> >><a href=\"$adm\">ADMIN</a></b></FONT>\n");
        &HEADER;
        print @log;
        &FOOTER;
    } else {
        &MENU;
        print "”$in{'resyear'}/$in{'resmon'}/$in{'resday'} $in{'reshour'}:$in{'resmin'}:0”";
    }
}

1
