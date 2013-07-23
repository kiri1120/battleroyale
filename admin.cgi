#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
require "$LIB_DIR/lib2.cgi";
&LOCK;
require "pref.cgi";

    &ADMDECODE ;
    # GET メソッドを拒否
    if ($Met_Post && !$p_flag) {
        &ERROR("不正なアクセスです。");
    }
    if ($admpass ne $a_pass){&MAIN;&UNLOCK;exit;};

    if ($Command eq "MAIN") {
        &MENU ;
    } elsif ($Command eq "BSAVE") {
        &BACKSAVE;
    } elsif ($Command eq "BREAD") {
        &BACKREAD;
    } elsif ($Command eq "RESET") {
        &DATARESET;
    } elsif ($Command eq "USERLIST") {
        &USERLIST;
    } elsif ($Command eq "USERDEL") {
        &USERDEL;
    } elsif ($Command eq "LOGON") {
        &MAIN;
    } else { &MAIN; }
&UNLOCK;

exit;

#==================#
# ■ メイン機能    #
#==================#
sub MAIN {

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"管理用パスワード\n");
    push(@log,"<FORM METHOD=\"POST\">\n");
    push(@log,"<INPUT TYPE=\"HIDDEN\" NAME=\"Command\" VALUE=\"MAIN\">\n");
    push(@log,"<INPUT size=\"16\" type=\"text\" name=\"Password\" maxlength=\"16\">\n");
    push(@log,"　<INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n");
    push(@log,"</FORM>\n");

    &HEADER ;
    print @log;
    &FOOTER;
}
#==================#
# ■ メイン機能    #
#==================#
sub MENU {

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"<FORM METHOD=\"POST\">\n");
    push(@log,"<TABLE border=\"0\">\n");
    push(@log,"<TR><TD>\n");
    push(@log,"<INPUT type=\"hidden\" name=\"Password\" value=\"$admpass\">\n");
    push(@log,"<INPUT type=\"radio\" name=\"Command\" value=\"USERLIST\">ユーザ一覧<BR>\n");
    push(@log,"<INPUT type=\"radio\" name=\"Command\" value=\"BSAVE\">バックアップ保存<BR>\n");
    push(@log,"<INPUT type=\"radio\" name=\"Command\" value=\"BREAD\">バックアップ読込<BR>\n");
    push(@log,"<INPUT type=\"radio\" name=\"Command\" value=\"RESET\">データ初期化<BR>\n");
    push(@log,"</TD></TR>\n");
    push(@log,"</TABLE>\n");
    push(@log,"<BR><INPUT type=\"submit\" name=\"Enter\" value=\"決定\">\n");
    push(@log,"</FORM>\n");

    &HEADER ;
    print @log;
    &FOOTER;
}
#==================#
# ■ バックアップ保存  #
#==================#
sub BACKSAVE {

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    open(DB,">$back_file"); seek(DB,0,0); print DB @userlist; close(DB);

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"バックアップを作成しました。<br>\n");

    &HEADER ;
    print @log;
    print "<br><B><FONT color=\"#ff0000\">>><a href=\"$home\">HOME</a> >><a href=\"admin.cgi\">ADMIN</a></b></FONT>\n";
    &FOOTER;

}
#==================#
# ■ バックアップ読込  #
#==================#
sub BACKREAD {

    open(DB,"$back_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"バックアップを読込ました。<br>\n");
    push(@log,"<br><B><FONT color=\"#ff0000\">>><a href=\"$home\">HOME</a> >><a href=\"admin.cgi\">ADMIN</a></b></FONT>\n");

    &HEADER ;
    print @log;
    &FOOTER;
}
#==================#
# ■ データ初期化    #
#==================#
sub DATARESET {

    if($npc_mode eq "0"){
        $userlist[0]="";
        open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
    }else{
        open(DB,"$npc_file");seek(DB,0,0); @baselist=<DB>;close(DB);
        $LEN = @baselist;

        if ($LEN > 0) {
            for ($i=0; $i<$LEN; $i++) {
                ($w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_com, $w_msg, $w_dmes) = split(/,/, $baselist[$i]);

                if (($w_cl eq "$BOSS")||($w_cl eq "$ZAKO")){  #政府側のNPC
                    $w_att = int(rand(10)) + 40 ;
                    $w_def = int(rand(10)) + 40 ;
                    $w_hit = int(rand(30)) + 80 ;
                    $w_level = 10; $w_exp = int($w_level*$baseexp+(($w_level-1)*$baseexp)) - 17;
                    $w_tactics = "なし"; $w_death = "" ;
                    $w_pls = 0;
                    $w_wn=$w_wp=$w_wa=$w_wg=$w_we=$w_wc=$w_wd=$w_wb=$w_wf=$w_ws= $BASE * 3;
                    $w_mhit=$w_hit; $w_sta = $maxsta;
                    $w_sts = "NPC0";
                }else{  #その他のNPCはこっち
                    $w_att = int(rand(5)) + 8 ;
                    $w_def = int(rand(5)) + 8 ;
                    $w_hit = int(rand(10)) + 40 ;
                    $w_level = 1; $w_exp = 0;
                    $w_tactics = "なし"; $w_death = "" ;
                    $w_pls = int(rand($#area)+1) ;
                    $w_wn=$w_wp=$w_wa=$w_wg=$w_we=$w_wc=$w_wd=$w_wb=$w_wf=$w_ws=0;
                    $w_mhit=$w_hit; $w_sta = $maxsta;
                    $w_sts = "NPC";
                }
                $w_kill = 0 ;
                $w_id = ($a_id . "$i"); $w_password = $a_pass;
                $w_tactics = "";
                $w_club="";
                $w_log = "" ; $w_bid = "" ; $w_inf="";

                $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,\n" ;
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
    $areadata[1] = "1,0,\n" ; #禁止エリア数、ハッキングフラグ

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
    $loglist = "$now,,,,,,,,,,,NEWGAME,,\n" ;
    open(DB,">$log_file"); seek(DB,0,0); print DB $loglist; close(DB);


    for ($i=0; $i<$#area+1; $i++) {
        @areaitem = "" ;
        $filename = "$LOG_DIR/$i$item_file";
        open(DB,">$filename"); seek(DB,0,0); print DB @areaitem; close(DB);
    }

    #アイテムファイル更新
    open(DB,"$DAT_DIR/itemfile.dat");seek(DB,0,0); @itemlist=<DB>;close(DB);

    for ($i=0; $i<$#itemlist+1; $i++) {
        ($idx, $w_i,$w_e,$w_t) = split(/,/, $itemlist[$i]);

        if ($idx == 99) { $idx = int(rand($#place)+1) ; }

        $filename = "$LOG_DIR/$idx$item_file";
        open(DB,"$filename");seek(DB,0,0); @areaitem=<DB>;close(DB);
        push(@areaitem,"$w_i,$w_e,$w_t,\n") ;
        open(DB,">$filename"); seek(DB,0,0); print DB @areaitem; close(DB);
    }

    #銃声ログファイル更新
    local($null_data) = "0,,,,";
    open(DB,">$gun_log_file");
    for ($i=0; $i<6; $i++){
        print DB "$null_data\n";
    }
    close(DB);

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

    push(@log,"<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">管理モード</FONT></B><BR><BR>\n");
    push(@log,"初期化しました。<br>\n");
    push(@log,"<br><B><FONT color=\"#ff0000\">>><a href=\"$home\">HOME</a> >><a href=\"admin.cgi\">ADMIN</a></b></FONT>\n");

    &HEADER ;
    print @log;
    &FOOTER;

}
#==================#
# ■ デコード処理  #
#==================#
sub ADMDECODE {
    $p_flag=0;
    if ($ENV{'REQUEST_METHOD'} eq "POST") {
        if ($ENV{'CONTENT_LENGTH'} > 51200) { &ERROR("異常な入力です"); }
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
        $p_flag=1;
    } else { $buffer = $ENV{'QUERY_STRING'}; }
    @pairs = split(/&/, $buffer);
    foreach (@pairs) {
        ($name,$value) = split(/=/, $_);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        # 文字コードをEUC変換
        if ($name eq "Del") { push(@DEL,$value);}
        &jcode'convert(*value, "euc", "", "z");
        &jcode::tr(\$value, '　', ' ');

        $value =~ s/</&lt;/g;
        $value =~ s/>/&gt;/g;
        $value =~ s/&/&amp;/g;
        $value =~ s/"/&quot;/g;
        $value =~ s/ /&nbsp;/g;
        $value =~ s/,/、/g; #データ破損対策

        $in{$name} = $value;
    }

    $id = $in{'Id'};
    $admpass = $in{'Password'};
    $Command = $in{'Command'};
    $Message = $in{'Message'};
    if($buffer eq ""){$Command = "LOGON"; $p_flag=1;}

}
#==================#
# ■ 一覧表示処理  #
#==================#
sub USERLIST {

    local($col_s1) = "<font color=white>" ;
    local($col_s2) = "<font color=red>" ;
    local($col_e) = "</font>" ;

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    push(@log,"<P align=\"center\"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">生存者一覧</FONT></B><BR></P>");
    push(@log,"<form action=\"admin.cgi\" method=\"POST\">\n");
    push(@log,"削除メッセージ：<INPUT size=\"64\" type=\"text\" name=\"Message\" maxlength=\"64\"><BR><BR>\n");
    push(@log,"<TABLE border=\"1\">\n");
    push(@log,"<tr align=\"center\"><td>殺害</td><td width=\"100\">名前</td><td width=\"50\">ID</td><td width=\50\">PASS</td><td>状態</td><td>基本行動</td><td>場所</td></tr>\n");
    foreach (0 .. $#userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$_]);

        if ($w_hit <= 0) { $col_s = $col_s2; $w_sts = "死亡";} else { $col_s = $col_s1;}
        push(@log,"<tr><td><input type=checkbox name=Del value=\"$_\"></td><td align=\"center\">$col_s$w_f_name $w_l_name$col_e</td><td>$col_s$w_id$col_e</td><td>$col_s$w_password$col_e</td><td>$col_s$w_sts$col_e</td><td>$col_s$w_tactics$col_e</td><td>$col_s$place[$w_pls]$col_e</td></tr>\n");

    }
    push(@log,"</table><BR>\n");
    push(@log,"<input type=hidden name=Command value=\"USERDEL\">\n") ;
    push(@log,"<input type=hidden name=Password value=$admpass>\n");
    push(@log,"<input type=submit value=\"削除する\"><input type=reset value=\"リセット\">\n") ;
    push(@log,"</form><BR>\n");

    &HEADER ;
    print @log;
    &FOOTER;

}
#==================#
# ■ 削除処理      #
#==================#
sub USERDEL {

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    foreach (0 .. $#DEL) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$DEL[$_]]);
        $w_msg = $Message;
        &LOGSAVE("DEATH4") ;
        $w_hit = 0 ; $w_sts = "死亡"; $w_death=$deth;
        $userlist[$DEL[$_]] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,\n" ;
    }

    open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);


    &USERLIST;


}
