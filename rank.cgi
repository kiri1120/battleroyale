#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    push(@log,"<P align=\"center\"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">生存者一覧</FONT></B><BR></P>");
    push(@log,"<TABLE border=\"1\">\n");
    if($icon_mode){
        push(@log,"<tr align=\"center\"><td width=\"70\">アイコン</td><td width=\"100\">名前</td><td width=\"50\">クラス</td><td width=\"50\">番号</td><td width=\"300\">コメント</td></tr>\n");
    }else{
        push(@log,"<tr align=\"center\"><td width=\"100\">名前</td><td width=\"50\">クラス</td><td width=\"50\">番号</td><td width=\"300\">コメント</td></tr>\n");
    }
    foreach (0 .. $#userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$_]);

        if (($w_hit > 0) && ($w_sts ne "NPC0") ) {
            if($icon_mode){
                push(@log,"<tr><td align=\"center\"><IMG src=\"$imgurl$icon_file[$w_icon]\" width=\"70\" height=\"70\" border=\"0\" align=\"absmiddle\"></td><td align=\"center\">$w_f_name $w_l_name</td><td align=\"center\">$w_cl</td><td align=\"center\">$w_sex$w_no番</td><td>$w_com</td></tr>\n");
            }else{
                push(@log,"<tr><td align=\"center\">$w_f_name $w_l_name</td><td align=\"center\">$w_cl</td><td align=\"center\">$w_sex$w_no番</td><td>$w_com</td></tr>\n");
            }
            $rnk2++;$ok++;
        } else { $ng++; }

    }
    push(@log,"</table><BR>\n");
    push(@log,"【残り$ok人】</table><BR><BR>\n");
    push(@log,"<B><a href=\"index.htm\">HOME</A></B><BR>\n");

    &HEADER ;
    print @log;
    &FOOTER;
&UNLOCK;

exit;
