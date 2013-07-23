#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";

    push(@log,"<P align=\"center\"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">生存者一覧</FONT></B><BR></P>");
    foreach (0 .. $#userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$_]);
        $count{$w_id} = $w_kill * 1000 + ($w_att + $w_def)*2 + $w_watt + $w_bou + $w_bou_h + $w_bou_a + $w_bou_f;
    }
    if ($ENV{'QUERY_STRING'} =~ /sort/) {
        push(@log,"<B><a href=\"rank.cgi\">通常</A></B><BR><BR>\n");
        @userlist = sort sortfunc @userlist;
    } else {
        push(@log,"<B><a href=\"rank.cgi?sort\">戦闘力順</A></B><BR><BR>\n");
    }
    push(@log,"<TABLE border=\"1\" cellspacing=\"0\" width=\"568\">\n");
    push(@log,"<tr align=\"center\"><th nowrap>アイコン</th><th nowrap>名前</th><th nowrap>部活</th><th nowrap>グループ</th><th nowrap>戦闘力</th><th width=\"100%\">コメント</th></tr>\n");
    foreach (0 .. $#userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$_]);
        if (($w_hit > 0) && (($w_inf !~ /NPC0/) || $hackflg)) {
            if ($w_a_name ne "") { $w_a_name = "($w_a_name)"; }
            push(@log,"<tr><td align=\"center\"><IMG src=\"$imgurl$w_icon\" width=\"70\" height=\"70\" border=\"0\"></td><td align=\"center\" nowrap>$w_cl $w_sex$w_no番<br>$w_f_name $w_l_name<br>$w_a_name</td><td align=\"center\" nowrap>$w_club<br><font color=\"red\"><b>$w_kill</b></font>人殺害</td><td align=\"center\" nowrap>$w_group</td><td align=\"center\" nowrap><font color=\"orange\">$count{$w_id}</font></td><td width=\"100%\">$w_com</td></tr>\n");
            $ok++;
        }
    }
    push(@log,"</table><BR>\n");
    push(@log,"【残り$ok人】<BR><BR>\n");
    push(@log,"<B><a href=\"$home\">HOME</A></B><BR>\n");

    &HEADER ;
    print @log;
    &FOOTER;
&UNLOCK;

exit;

# ソート関数
sub sortfunc {
    $count{(split(/,/,$b))[0]} <=> $count{(split(/,/,$a))[0]};
}
