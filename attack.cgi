#==================#
# ¢£ ÀèÀ©¹¶·â½èÍý  #
#==================#
sub ATTACK {

    $log = ($log . "$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤òÈ¯¸«¤·¤¿¡ª<br>") ;
    $log = ($log . "$w_f_name $w_l_name¡¡¤Ï ¤³¤Á¤é¤Ë¤Ïµ¤¤Å¤¤¤Æ¤Ê¤¤¤Ê¡¦¡¦¡¦¡£<br>") ;

    $Command=("BATTLE0" . "_" . $w_id);

}
#==================#
# ¢£ ÀèÀ©¹¶·â½èÍý  #
#==================#
sub ATTACK1 {
    $kega2 = "" ; $kega3 = "" ;
    $hakaiinf2 = ""; $hakaiinf3 = "";

    local($i) = 0 ;
    local($result) = 0 ;
    local($result2) = 0 ;
    local($dice1) = int(rand(100)) ;
    local($dice2) = int(rand(100)) ;

    local($a,$w_kind,$wid) = split(/_/, $Command);

    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
        if ($w_id eq $wid) {
            $Index2=$i ; last;
        }
    }

    if ((($w_bid eq $group) && ($tactics ne "Ï¢Æ®¹ÔÆ°")) || ($w_hit <= 0)) {
        $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host,rentou,$w_bid,\n";
        open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
        &ERROR("ÉÔÀµ¥¢¥¯¥»¥¹¤Ç¤¹") ;
    }

    &BB_CK; #¥Ö¥é¥¦¥¶¥Ð¥Ã¥¯ÂÐ½è

    $log = ($log . "$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤ÈÀïÆ®³«»Ï¡ª<br>") ;

    ($w_name,$a) = split(/<>/, $wep);
    ($w_name2,$w_kind2) = split(/<>/, $w_wep);

    if (($w_we =~ /B/) && ($w_kind2 =~ /B/)) {
        $w_kind2 = "WB";
    } elsif (($w_we =~ /P/) && ($w_kind2 =~ /P/)) {
        $w_kind2 = "WP";
    } elsif (($w_we =~ /N/) && ($w_kind2 =~ /N/)) {
        $w_kind2 = "WN";
    } elsif (($w_we =~ /S/) && ($w_kind2 =~ /S/)) {
        $w_kind2 = "WS";
    } elsif (($w_we =~ /D/) && ($w_kind2 =~ /D/)) {
        $w_kind2 = "WD";
    } elsif (($w_we =~ /C/) && ($w_kind2 =~ /C/)) {
        $w_kind2 = "WC";
    } elsif ((($w_we =~ /G/) || ($w_wtai > 0)) && ($w_kind2 =~ /G/)) {
        $w_kind2 = "WG";
    } elsif ((($w_we =~ /A/) || ($w_wtai > 0)) && ($w_kind2 =~ /A/)) {
        $w_kind2 = "WA";
    }

    &TACTGET; &TACTGET2;    #´ðËÜ¹ÔÆ°

    #¥×¥ì¥¤¥ä¡¼
    if ((($wep =~ /G|A/) && ($wtai == 0)) || (($wep =~ /G|A/) && ($w_kind =~ /B/))) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_p = $ball * $dfp ;

    #Å¨
    if ((($w_wep =~ /G|A/) && ($w_wtai == 0)) || (($w_wep =~ /G|A/) && ($w_kind2 =~ /B/))) {
        $att_n = (($w_watt/10) + $w_att) * $atn ;
    } else {
        $att_n = ($w_watt + $w_att) * $atn ;
    }
    local($ball2) = $w_def + $w_bdef + $w_bdef_h + $w_bdef_a + $w_bdef_f ;
    if ($w_item[5] =~ /AD/) {$ball2 += $w_eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_n = $ball2 * $dfn ;
    $w_bid = $group ;
    $bid = $w_group ;

    &BLOG_CK;
    &EN_KAIFUKU;

    $Command="BATTLE";

    if ($w_pls ne $pls) {   #´û¤Ë°ÜÆ°¡©
        $log = ($log . "¤·¤«¤·¡¢$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤ËÆ¨¤²¤é¤ì¤Æ¤·¤Þ¤Ã¤¿¡ª<br>") ;
        &SAVE;
        return ;
    }

    if (length($dengon) > 0) {
        $log = ($log . "<font color=\"lime\"><b>$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë¡Ö$dengon¡×</b></font><br>") ;
        $w_log = ($w_log . "<font color=\"lime\"><b>$hour:$min:$sec $f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë¡Ö$dengon¡×</b></font><br>") ;
    }

    &WEPTREAT($w_name, $w_kind, $wtai, $l_name, $w_l_name, "¹¶·â", "PC") ;
    if ($Command2 eq "CATKon") {
        $log = ($log . "É¬»¦¤ÎÎÏ¤ò¹þ¤á¤¿°ì·â¡ª¡ª");
        $feel -= 50 + int(rand(100));
        $att_p = $att_p * 1.2;
    }
    if ($dice1 < $mei) {    #¹¶·âÀ®¸ù

        $result = ($att_p*$wk) - $def_n;
        $result /= 2 ;
        $result += rand($result);

        &DEFTREAT($w_kind, "NPC") ;
        $result = int($result * $pnt) ;

        if ($result <= 0) {$result = 1} ;
        $log = ($log . "<font color=\"red\"><b>$result¥À¥á¡¼¥¸ $hakaiinf3 $kega3 </b></font>¡ª<br>") ;

        $w_hit -= $result;
        $w_btai--;
        if ($w_btai <= 0) { $w_bou = "²¼Ãå<>DN"; $w_bdef=0; $w_btai="¡ç"; }

        $feel   += 1 + int(rand(3));
        $w_feel -= 1;

        $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;

        &SKILL_PC;

        &EXPPLUS_PC;

        if (($w_kind =~ /N|S/) && (int(rand(6)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_name¤¬¿Ï¤³¤Ü¤ì¤·¤¿</b></font>¡ª<br>") ;
            if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
        } elsif (($w_kind =~ /B/) && (int(rand(7)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_name¤Ë¤Ò¤Ó¤¬Æþ¤Ã¤¿</b></font>¡ª<br>") ;
            if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
        } elsif (($w_kind =~ /P/) && ($w_name ne "ÁÇ¼ê") && (int(rand(6)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_name¤¬¤¹¤ê¸º¤Ã¤¿</b></font>¡ª<br>") ;
            if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
        } elsif (($w_kind =~ /C/) && ($wtai eq "¡ç") && (int(rand(7)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_name¤¬Â»Ì×¤·¤¿</b></font>¡ª<br>") ;
            if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
        }
    } else {
        $kega3 = "" ;
        $log = ($log . "¤·¤«¤·¡¢Èò¤±¤é¤ì¤¿¡ª<br>") ;
        $feel   -= 1 + int (rand(2));
        $w_feel += 1 + int (rand(3));

    }

    if (($w_item[5] =~ /<>AH/) && ($w_hit <= 0)) {
        ($w_in_a,$w_ik_a) = split(/<>/, $w_item[5]);
        $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤Î$w_in_a¤¬²õ¤ì¤¿¡ª</b></font><br>") ;
        $kega3 = ($kega3 . " <font color=\"red\">$w_in_aÇË²õ¡ª</font>") ;
        if($w_in_a eq "Àï²µ½÷¤Î½ËÊ¡") { $w_hit = int($w_mhit * 0.2); }
        elsif($w_in_a eq "»àÊÖ¶Ì") { $w_hit = int($w_mhit * 0.2); }
        else { $w_hit = 1; }
        $w_item[5] = "¤Ê¤·"; $w_eff[5] = 0; $w_itai[5] = 0;
    }

    if ($w_hit <= 0) {  #Å¨»àË´¡©
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë Èï:$result $kega3 </b></font><br>") ;
        &DEATH2;
    } elsif (rand(10) < 5) {    #È¿·â

        if (($weps eq $weps2) || ($weps2 eq "L")) {  #µ÷Î¥°ì½ï¡©

            &WEPTREAT($w_name2, $w_kind2,  $w_wtai, $w_l_name, $l_name, "È¿·â", "NPC") ;

            if ($dice2 < $mei2) {   #¹¶·âÀ®¸ù
                $result2 = ($att_n*$wk) - $def_p;
                $result2 /= 2 ;
                $result2 += rand($result2);

                &DEFTREAT($w_kind2, "PC") ;
                $result2 = int($result2 * $pnt) ;

                if ($result2 <= 0) {$result2 = 1 ;}
                $log = ($log . "<font color=\"red\"><b>$result2¥À¥á¡¼¥¸ $kega2</b></font>¡ª<br>") ;

                $btai--;
                $hit -= $result2;

                $feel   -= 1;
                $w_feel += 1 + int (rand(3));

                if ($btai <= 0) { $bou = "²¼Ãå<>DN"; $bdef=0; $btai="¡ç"; }

                if (($item[5] =~ /<>AH/)&&($hit <= 0)) {
                    ($in_a,$ik_a) = split(/<>/, $item[5]);
                    $log = ($log . "<font color=\"RED\"><b>$in_a¤¬²õ¤ì¤Æ¤·¤Þ¤Ã¤¿¡ª</b></font><br>") ;
                    if($in_a eq "Àï²µ½÷¤Î½ËÊ¡") { $hit = int($mhit * 0.2); }
                    elsif($in_a eq "»àÊÖ¶Ì") { $hit = int($mhit * 0.2); }
                    else { $hit = 1; }
                    $item[5] = "¤Ê¤·"; $eff[5] = 0; $itai[5] = 0;
                }

                if ($hit <=0) { #»àË´¡©
                    &DEATH;
                } else {    #Æ¨Ë´
                    $log = ($log . "$w_l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
                }

                &EXPPLUS_NPC;
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result2 Èï:$result <font color=\"#00ffff\">Exp:$p_exp</font> $hakaiinf2 $kega3 </b></font><br>") ;
                $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;

                if ((($w_kind2 =~ /N|S|B|P/) || (($w_kind2 =~ /C/) && ($w_wtai eq "¡ç"))) && (int(rand(6)) == 0)) {
                    $w_watt--; if (int(rand(4)) == 0) { $w_watt--; }
                    if ($w_watt <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
                }
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result2 Èï:$result $kega3 </b></font><br>") ;
                $log = ($log . "¤·¤«¤·¡¢´Ö°ìÈ±Èò¤±¤¿¡ª<br>") ;
                $feel   += 1 + int (rand(3));
                $w_feel -= 1 + int (rand(2));

            }

            if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #½Æ¡¦¼Í¡©
                $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
            } elsif (($w_kind2 =~ /C|D/) && ($w_wtai ne "¡ç")) {
                $w_wtai--; if ($w_wtai <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
            }
        } else {
            $log = ($log . "$w_l_name ¤Ï È¿·â¤Ç¤­¤Ê¤¤¡ª<br>") ;
            $log = ($log . "$w_l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
            $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë Èï:$result $hakaiinf2 $kega3 </b></font><br>") ;
        }
    } else {    #Æ¨Ë´
        $log = ($log . "$w_l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë Èï:$result $hakaiinf2 $kega3 </b></font><br>") ;
    }

    if (($w_kind =~ /G|A/) && ($wtai > 0)) {    #½Æ¡¦¼Í¡©
        $wtai--; if ($wtai <= 0) { $wtai = 0 ; }
    } elsif (($w_kind =~ /C|D/) && ($wtai ne "¡ç")) {
        $wtai--; if ($wtai <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
    }

    &LVUPCHK() ;

    if ($feel > 300) { $feel = 300; }
    elsif ($feel < 0) { $feel = 0; }
    elsif ($feel < 60) {
        if (int(rand(10)) == 0) { $feel = 300; }
    }

    if ($w_feel > 300) { $w_feel = 300; }
    elsif ($w_feel < 0) { $w_feel = 0; }
    elsif ($w_feel < 60) {
        if (int(rand(10)) == 0) { $w_feel = 300; }
    }

    &SAVE;
    &SAVE2;
}
#==================#
# ¢£ ¸å¹¶¹¶·â½èÍý  #
#==================#
sub ATTACK2 {
    $kega2 = "" ; $kega3 = "" ;
    $hakaiinf2 = ""; $hakaiinf3 = "";
    $getexp = 0;

    if ($w_hit <= 0) {
        &ERROR("ÉÔÀµ¥¢¥¯¥»¥¹¤Ç¤¹") ;
    }

    local($result) = 0 ;
    local($result2) = 0 ;
    local($i) = 0 ;
    local($dice1) = int(rand(100)) ;
    local($dice2) = int(rand(100)) ;
    ($w_name,$w_kind) = split(/<>/, $wep);
    ($w_name2,$w_kind2) = split(/<>/, $w_wep);

    if (($we =~ /B/) && ($w_kind =~ /B/)) {
        $w_kind = "WB";
    } elsif (($we =~ /P/) && ($w_kind =~ /P/)) {
        $w_kind = "WP";
    } elsif (($we =~ /N/) && ($w_kind =~ /N/)) {
        $w_kind = "WN";
    } elsif (($we =~ /S/) && ($w_kind =~ /S/)) {
        $w_kind = "WS";
    } elsif (($we =~ /D/) && ($w_kind =~ /D/)) {
        $w_kind = "WD";
    } elsif (($we =~ /C/) && ($w_kind =~ /C/)) {
        $w_kind = "WC";
    } elsif ((($we =~ /G/) || ($w_wtai > 0)) && ($w_kind =~ /G/)) {
        $w_kind = "WG";
    } elsif ((($we =~ /A/) || ($w_wtai > 0)) && ($w_kind =~ /A/)) {
        $w_kind = "WA";
    }

    if (($w_we =~ /B/) && ($w_kind2 =~ /B/)) {
        $w_kind2 = "WB";
    } elsif (($w_we =~ /P/) && ($w_kind2 =~ /P/)) {
        $w_kind2 = "WP";
    } elsif (($w_we =~ /N/) && ($w_kind2 =~ /N/)) {
        $w_kind2 = "WN";
    } elsif (($w_we =~ /S/) && ($w_kind2 =~ /S/)) {
        $w_kind2 = "WS";
    } elsif (($w_we =~ /D/) && ($w_kind2 =~ /D/)) {
        $w_kind2 = "WD";
    } elsif (($w_we =~ /C/) && ($w_kind2 =~ /C/)) {
        $w_kind2 = "WC";
    } elsif ((($w_we =~ /G/) || ($w_wtai > 0)) && ($w_kind2 =~ /G/)) {
        $w_kind2 = "WG";
    } elsif ((($w_we =~ /A/) || ($w_wtai > 0)) && ($w_kind2 =~ /A/)) {
        $w_kind2 = "WA";
    }

    &TACTGET; &TACTGET2;    #´ðËÜ¹ÔÆ°

    #¥×¥ì¥¤¥ä¡¼
    if ((($wep =~ /G|A/) && ($wtai == 0)) || (($wep =~ /G|A/) && ($w_kind =~ /B/))) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_p = $ball * $dfp ;

    #Å¨
    if ((($w_wep =~ /G|A/) && ($w_wtai == 0)) || (($w_wep =~ /G|A/) && ($w_kind2 =~ /B/))) {
        $att_n = (($w_watt/10) + $w_att) * $atn ;
    } else {
        $att_n = ($w_watt + $w_att) * $atn ;
    }
    local($ball2) = $w_def + $w_bdef + $w_bdef_h + $w_bdef_a + $w_bdef_f ;
    if ($w_item[5] =~ /AD/) {$ball += $w_eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_n = $ball2 * $dfn ;

    &BLOG_CK;
    &EN_KAIFUKU;

    $Command="BATTLE";

    $log = ($log . "$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤¬ÆÍÇ¡½±¤¤³Ý¤«¤Ã¤Æ¤­¤¿¡ª<br>") ;

    &WEPTREAT($w_name2, $w_kind2,  $w_wtai, $w_l_name, $l_name, "¹¶·â", "NPC") ;
    if ($dice2 < $mei2) {    #¹¶·âÀ®¸ù

        $result = ($att_n*$wk) - $def_p;
        $result /= 2 ;
        $result += rand($result);
        $result = int($result) ;

        &DEFTREAT($w_kind2, "PC") ;
        $result = int($result * $pnt) ;

        if ($result <= 0) {$result = 1 ;}
        $log = ($log . "<font color=\"red\"><b>$result¥À¥á¡¼¥¸ $kega2</b></font>¡ª<br>") ;

        $hit -= $result;
        $btai--;

        $feel   -= 1;
        $w_feel += 1 + int(rand(3));

        if ($btai <= 0) { $bou = "²¼Ãå<>DN"; $bdef=0; $btai="¡ç"; }
        $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;

        &EXPPLUS_NPC; $getexp = $p_exp;

        if ((($w_kind2 =~ /N|S|B|P/) || (($w_kind2 =~ /C/) && ($w_wtai eq "¡ç"))) && (int(rand(6)) == 0)) {
            $w_watt--; if (int(rand(4)) == 0) { $w_watt--; }
            if ($w_watt <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
        }
    } else {
        $log = ($log . "¤·¤«¤·¡¢´Ö°ìÈ±Èò¤±¤¿¡ª<br>") ;
        $feel   += 1 + int(rand(3));
        $w_feel -= 1 + int(rand(2));
    }

    if (($item[5] =~ /<>AH/)&&($hit <= 0)) {
        ($in_a,$ik_a) = split(/<>/, $item[5]);
        $log = ($log . "<font color=\"RED\"><b>$in_a¤¬²õ¤ì¤Æ¤·¤Þ¤Ã¤¿¡ª</b></font><br>") ;
        if($in_a eq "Àï²µ½÷¤Î½ËÊ¡") { $hit = int($mhit * 0.2); }
        elsif($in_a eq "»àÊÖ¶Ì") { $hit = int($mhit * 0.2); }
        else { $hit = 1; }
        $item[5] = "¤Ê¤·"; $eff[5] = 0; $itai[5] = 0;
    }

    if ($hit <= 0) {    #»àË´¡©
        &DEATH;
    } elsif (rand(10) <5) { #È¿·â

        if (($weps eq $weps2) || ($weps eq "L")) {

            &WEPTREAT($w_name, $w_kind,  $wtai, $l_name, $w_l_name, "È¿·â", "PC") ;
            if ($dice1 < $mei) {    #¹¶·âÀ®¸ù

                $result2 = ($att_p*$wk) - $def_n;
                $result2 /= 2 ;
                $result2 += rand($result2);
                $result2 = int($result2) ;

                &DEFTREAT($w_kind, "NPC") ;
                $result2 = int($result2 * $pnt) ;

                if ($result2 <= 0) {$result2 = 1 ;}
                $log = ($log . "<font color=\"red\"><b>$result2¥À¥á¡¼¥¸ $hakaiinf3 $kega3</b></font>¡ª<br>") ;

                $w_hit -= $result2;

                $w_btai--;
                if ($w_btai <= 0) { $w_bou = "²¼Ãå<>DN"; $w_bdef=0; $w_btai="¡ç"; }

                $feel   += 1 + int(rand(3));
                $w_feel -= 1;

                if (($w_item[5] =~ /<>AH/) && ($w_hit <= 0)) {
                    ($w_in_a,$w_ik_a) = split(/<>/, $w_item[5]);
                    $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤Î$w_in_a¤¬²õ¤ì¤¿¡ª</b></font><br>") ;
                    $kega3 = ($kega3 . " <font color=\"red\">$w_in_aÇË²õ¡ª</font>") ;
                    if($w_in_a eq "Àï²µ½÷¤Î½ËÊ¡") { $w_hit = int($w_mhit * 0.2); }
                    elsif($w_in_a eq "»àÊÖ¶Ì") { $w_hit = int($w_mhit * 0.2); }
                    else { $w_hit = 1; }
                    $w_item[5] = "¤Ê¤·"; $w_eff[5] = 0; $w_itai[5] = 0;
                }

                if ($w_hit <=0) {   #»àË´¡©
                    &DEATH2;
                } else {    #Æ¨Ë´
                    $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
                }
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result Èï:$result2 <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
                $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;

                &EXPPLUS_PC;

                if (($w_kind =~ /N|S/) && (int(rand(6)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_name¤¬¿Ï¤³¤Ü¤ì¤·¤¿</b></font>¡ª<br>") ;
                    if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
                } elsif (($w_kind =~ /B/) && (int(rand(7)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_name¤Ë¤Ò¤Ó¤¬Æþ¤Ã¤¿</b></font>¡ª<br>") ;
                    if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
                } elsif (($w_kind =~ /P/) && ($w_name ne "ÁÇ¼ê") && (int(rand(6)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_name¤¬¤¹¤ê¸º¤Ã¤¿</b></font>¡ª<br>") ;
                    if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
                } elsif (($w_kind =~ /C/) && ($wtai eq "¡ç") && (int(rand(7)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_name¤¬Â»Ì×¤·¤¿</b></font>¡ª<br>") ;
                    if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
                }
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result Èï:$result2 <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 </b></font><br>") ;
                $log = ($log . "¤·¤«¤·¡¢Èò¤±¤é¤ì¤¿¡ª<br>") ;
                $feel   -= 1 + int (rand(2));
                $w_feel += 1 + int (rand(3));
            }

            if (($w_kind =~ /G|A/) && ($wtai > 0)) {    #½Æ¡¦¼Í¡©
                $wtai--; if ($wtai <= 0) { $wtai = 0 ; }
            } elsif (($w_kind =~ /C|D/) && ($wtai ne "¡ç")) {
                $wtai--; if ($wtai <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
            }
        } else {
            $log = ($log . "$l_name ¤Ï È¿·â¤Ç¤­¤Ê¤¤¡ª<br>") ;
            $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
            $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
        }
    } else {    #Æ¨Ë´
        $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
    }

    if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #½Æ¡¦¼Í¡©
        $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
    } elsif (($w_kind2 =~ /C|D/) && ($w_wtai ne "¡ç")) {
        $w_wtai--; if ($w_wtai <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
    }

    &LVUPCHK();

    if ($feel > 300) { $feel = 300; }
    elsif ($feel < 0) {
        if (int(rand(2)) == 0) { $feel = 300; }
        else { $feel = 0; }
    }

    if ($w_feel > 300) { $w_feel = 300; }
    elsif ($w_feel < 0) {
        if (int(rand(2)) == 0) { $w_feel = 300; }
        else { $w_feel = 0; }
    }

    &SAVE;
    &SAVE2;
}
#==================#
# ¢£ Éð´ï¼ïÊÌ½èÍý  #
#==================#
sub WEPTREAT {

    local($wname)   = @_[0] ;   #Éð´ï
    local($wkind)   = @_[1] ;   #Éð´ï
    local($wwtai)   = @_[2] ;   #»Ä¿ô
    local($pn)      = @_[3] ;   #¹¶·â¼ÔÌ¾
    local($nn)      = @_[4] ;   #ËÉ¸æ¼ÔÌ¾
    local($ind)     = @_[5] ;   #¹¶·â¼ïÊÌ¡Ê¹¶·â/È¿·â)
    local($attman)  = @_[6] ;   #¹¶·â¼Ô¡ÊPC/NPC)

    local($dice3) = int(rand(100)) ;
    local($dice4) = int(rand(4)) ;
    local($dice5) = int(rand(100)) ;

    local($kega)    = 0 ;
    local($kegainf) = "" ;
    local($k_work) = "" ;
    local($hakai) =  0 ;

    if ((($wkind =~ /B/) || (($wkind =~ /G|A/) && ($wwtai == 0))) && ($wname ne "ÁÇ¼ê")) { #ÛþËÀ or ÃÆÌµ¤·½Æ or ÌðÌµ¤·µÝ
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤Ë²¥¤ê¤«¤«¤Ã¤¿¡ª") ;
        if ($attman eq "PC") {$wb++;$wk=$wb;} else {$w_wb++;$wk=$w_wb;}
        $kega = 15 ;$kegainf = "Æ¬ÏÓÊ¢Â­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /A/) {   #µÝ·Ï¡©
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nnÌÜ³Ý¤±¤Æ¼Í¤¿¡ª") ;
        if ($attman eq "PC") {$wa++;$wk=$wa;} else {$w_wa++;$wk=$w_wa;}
        $kega = 25 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 2 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /C/) { #Åê·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nn¤ËÅê¤²¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wc++;$wk=$wc;} else {$w_wc++;$wk=$w_wc;}
        $kega = 15 ;$kegainf = "Æ¬ÏÓÊ¢Â­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ; if ($wwtai eq "¡ç") { $hakai = 3; } #ÇË²õÎ¨
        
    } elsif ($wkind =~ /D/) { #Çú·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nn¤ËÅê¤²¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wd++;$wk=$wd;$ps=$pls;} else {$w_wd++;$wk=$w_wd;$ps=$w_pls;}
        $kega = 30 ;$kegainf = "Æ¬ÏÓÊ¢Â­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ;    #ÇË²õÎ¨
        open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
        $gunlog[3] = "$now,$place[$ps],$id,$w_id,\n";
        open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    } elsif ($wkind =~ /G/) { #½Æ·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nnÌÜ³Ý¤±¤ÆÈ¯Ë¤¤·¤¿¡ª") ;
        if ($attman eq "PC") {$wg++;$wk=$wg;$ps=$pls;} else {$w_wg++;$wk=$w_wg;$ps=$w_pls;}
        $kega = 25 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 2 ;    #ÇË²õÎ¨
        open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
        $gunlog[0] = "$now,$place[$ps],$id,$w_id,\n";
        open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    } elsif ($wkind =~ /S/) { #»É·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò»É¤·¤¿¡ª") ;
        if ($attman eq "PC") {$ws++;$wk=$ws;} else {$w_ws++;$wk=$w_ws;}
        $kega = 20 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /N/) { #»Â·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤Ë»Â¤ê¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wn++;$wk=$wn;} else {$w_wn++;$wk=$w_wn;}
        $kega = 20 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /P/) { #²¥·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò²¥¤Ã¤¿¡ª") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 10 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        if ($wname eq "ÁÇ¼ê") { $hakai = 0; } else { $hakai = 3; }   #ÇË²õÎ¨
    } else { #¤½¤ÎÂ¾
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò²¥¤Ã¤¿¡ª") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 0 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ;    #ÇË²õÎ¨
    }

    $wk = int($wk/$BASE) ;
    if ($wk == 0) { $wk = 0.9 ;
    }elsif ($wk == 1) { $wk = 0.95 ;
    }elsif ($wk == 2) { $wk = 1.0 ;
    }elsif ($wk == 3) { $wk = 1.05 ;
    }elsif ($wk == 4) { $wk = 1.1 ;
    } else {$wk = 1.15 ;}

    if ($attman eq "PC") {  #PC
        $wep_2 = $wep; $watt_2 = $watt; $wtai_2 = $wtai ;$w_inf_2 = $w_inf ;
    } else {
        $w_wep_2 = $w_wep; $w_watt_2 = $w_watt; $w_wtai_2 = $w_wtai ;$inf_2 = $inf ;
    }

    # Éð´ïÇË²õ
    if ($dice5 < $hakai) {  #ÇË²õ¡©
        if ($attman eq "PC") {  #PC
            $wep_2 = "ÁÇ¼ê<>WP"; $watt_2 = 0 ; $wtai_2 = "¡ç" ;
            $hakaiinf3 = "Éð´ïÂ»½ý¡ª" ;
        } else {
            $w_wep_2 = "ÁÇ¼ê<>WP"; $w_watt_2 = 0 ; $w_wtai_2 = "¡ç" ;
            $hakaiinf2 = "Éð´ïÂ»½ý¡ª" ;
        }
    } else {
        $hakaiinf2 = "" ;
        $hakaiinf3 = "" ;
    }

    # ²ø²æ½èÍý
    if ($dice3 < $kega) {
        if (($dice4 == 0) && ($kegainf =~ /Æ¬/)) {  #Æ¬
            $k_work =  "Æ¬" ;
        } elsif (($dice4 == 1) && ($kegainf =~ /ÏÓ/)) { #ÏÓ
            $k_work =  "ÏÓ" ;
        } elsif (($dice4 == 2) && ($kegainf =~ /Ê¢/)) { #Ê¢
            $k_work =  "Ê¢" ;
        } elsif (($dice4 == 3) && ($kegainf =~ /Â­/)) { #Â­
            $k_work =  "Â­" ;
        } else {
            return ;
        }

        if ($attman eq "PC") {  #PC
            if ((($w_item[5] =~ /AD/)||($w_bou =~ /<>DB/)) && ($k_work eq "Ê¢")) {    #Ê¢¡©
                if($w_item[5] =~ /AD/){
                    $w_itai[5] --; if ($w_itai[5] <= 0) {$w_item[5]="¤Ê¤·"; $w_eff[5]=$w_itai[5]=0;}
                }else{
                    $w_btai --; if ($w_btai <= 0) { $w_bou = "²¼Ãå<>DN"; $w_bdef=0; $w_btai="¡ç"; }
                }
                return ;
            } elsif (($w_bou_h =~ /<>DH/) && ($k_work eq "Æ¬")) {   #Æ¬¡©
                $w_btai_h --; if ($w_btai_h <= 0) {$w_bou_h="¤Ê¤·"; $w_bdef_h=$w_btai_h=0;}
                return ;
            } elsif (($w_bou_f =~ /<>DF/) && ($k_work eq "Â­")) {   #Â­¡©
                $w_btai_f --; if ($w_btai_f <= 0) {$w_bou_f="¤Ê¤·"; $w_bdef_f=$w_btai_f=0;}
                return ;
            } elsif (($w_bou_a =~ /<>DA/) && ($k_work eq "ÏÓ")) {   #ÏÓ¡©
                $w_btai_a --; if ($w_btai_a <= 0) {$w_bou_a="¤Ê¤·"; $w_bdef_a=$w_btai_a=0;}
                return ;
            } else {
                $kega3 = ($k_work . "ÉôÉé½ý");
                $w_inf_2 =~ s/$k_work//g ;
                $w_inf_2 = ($w_inf_2 . $k_work) ;
            }
        } else {
            if ((($item[5] =~ /AD/)||($bou =~ /<>DB/)) && ($k_work eq "Ê¢")) {    #Ê¢¡©
                if($item[5] =~ /AD/){
                    $itai[5] --; if ($itai[5] <= 0) {$item[5]="¤Ê¤·"; $eff[5]=$itai[5]=0;}
                }else{
                    $btai --; if ($btai <= 0) { $bou = "²¼Ãå<>DN"; $bdef=0; $btai="¡ç"; }
                }
                return ;
            } elsif (($bou_h =~ /<>DH/) && ($k_work eq "Æ¬")) { #Æ¬¡©
                $btai_h --; if ($btai_h <= 0) {$bou_h="¤Ê¤·"; $bdef_h=$btai_h=0;}
                return ;
            } elsif (($bou_f =~ /<>DF/) && ($k_work eq "Â­")) { #Â­¡©
                $btai_f --; if ($btai_f <= 0) {$bou_f="¤Ê¤·"; $bdef_f=$btai_f=0;}
                return ;
            } elsif (($bou_a =~ /<>DA/) && ($k_work eq "ÏÓ")) { #ÏÓ¡©
                $btai_a --; if ($btai_a <= 0) {$bou_a="¤Ê¤·"; $bdef_a=$btai_a=0;}
                return ;
            } else {
                $kega2 = ($k_work . "ÉôÉé½ý");
                $inf_2 =~ s/$k_work//g ;
                $inf_2 = ($inf_2 . $k_work) ;
            }
        }
    }


}
#==================#
# ¢£ ¼«Ê¬»àË´½èÍý  #
#==================#
sub DEATH {

    $hit = 0;$w_kill++;
    $mem--;

    $com = int(rand(6)) ;

    $log = ($log . "<font color=\"red\"><b>$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë¤Ï»àË´¤·¤¿¡£</b></font><br>") ;
    if ($w_msg ne "") {
        $log = ($log . "<font color=\"lime\"><b>$w_f_name $w_l_name¡Ø$w_msg¡Ù</b></font><br>") ;
    }
    $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec $f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë¤ÈÀïÆ®¤ò¹Ô¤¤¡¢»¦³²¤·¤¿¡£¡Ú»Ä¤ê$mem¿Í¡Û</b></font><br>") ;

    $w_feel += int (rand(5)) + 18;

    local($b_limit) = ($battle_limit * 3) + 1;

    if (($mem == 1) && ($w_sts ne "NPC0") && ($ar > $b_limit)){$w_inf = ($w_inf . "¾¡") ;}

    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
    $gunlog[1] = "$now,$place[$pls],$id,$w_id,\n";
    open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);

    #»àË´¥í¥°
    &LOGSAVE("DEATH2") ;
    $death = $deth ;
}
#================#
# ¢£ Å¨»àË´½èÍý  #
#================#
sub DEATH2 {

    $w_hit = 0;$kill++;
    $wf = $w_id; #¥Ö¥é¥¦¥¶¥Ð¥Ã¥¯ÂÐ½è
    if (($w_cl ne "$BOSS")&&($w_cl ne "$ZAKO")){ $mem--; }

    $w_com = int(rand(6)) ;
    $log = ($log . "<font color=\"red\"><b>$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤ò»¦³²¤·¤¿¡£¡Ú»Ä¤ê$mem¿Í¡Û</b></font><br>") ;

    if (length($w_dmes) > 1) {
        $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name¡Ø$w_dmes¡Ù</b></font><br>") ;
    }
    if (length($msg) > 1) {
        $log = ($log . "<font color=\"lime\"><b>$f_name $l_name¡Ø$msg¡Ù</b></font><br>") ;
    }

    $feel += int (rand(5)) + 18;

    local($b_limit) = ($battle_limit * 3) + 1;
    if (($mem == 1)&& ($ar > $b_limit)) {$inf = ($inf . "¾¡") ;}

    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
    $gunlog[1] = "$now,$place[$pls],$id,$w_id,\n";
    open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);

    #»àË´¥í¥°
    &LOGSAVE("DEATH3") ;

    $Command = "BATTLE2" ;
    $w_death = $deth ;
    $w_bid = "";

}
#================#
# ¢£ ÀïÆ®·ë²Ì½èÍý#
#================#
sub BATTLE {

    $cln = "$cl¡Ê$sex$noÈÖ¡Ë" ;
    local($hpper)=$hit/$mhit;
    local($wep_n,$n)=split(/<>/, $wep);
    local($bou_n,$n)=split(/<>/, $bou);

    $w_cln = "$w_cl¡Ê$w_sex$w_noÈÖ¡Ë" ;
    local($w_hpper)=$w_hit/$w_mhit;
    local($w_wep_n,$n)=split(/<>/, $w_wep);
    local($w_bou_n,$n)=split(/<>/, $w_bou);

    if($hit <= 0) {
        $hpper="<font color=\"red\">»àË´</font>";
    }elsif($hpper < 0.2) {
        $hpper="<font color=\"red\">ÉÎ»à</font>";
    }elsif($hpper < 0.5) {
        $hpper="<font color=\"orange\">½Å½ý</font>";
    }elsif($hpper < 0.8) {
        $hpper="<font color=\"yellow\">·Ú½ý</font>";
    }else{
        $hpper="<font color=\"lime\">Àµ¾ï</font>";
    }
    if($w_hit <= 0) {
        $w_hpper="<font color=\"red\">»àË´</font>";
    }elsif($w_club eq "±é·àÉô") {
        $w_hpper="<b>¾õÂÖÉÔÌÀ</b>";
    }elsif($w_hpper < 0.2) {
        $w_hpper="<font color=\"red\">ÉÎ»à</font>";
    }elsif($w_hpper < 0.5) {
        $w_hpper="<font color=\"orange\">½Å½ý</font>";
    }elsif($w_hpper < 0.8) {
        $w_hpper="<font color=\"yellow\">·Ú½ý</font>";
    }else{
        $w_hpper="<font color=\"lime\">Àµ¾ï</font>";
    }

    if($feel == 300) {
        $tension = "<font color=\"red\">Ä¶±Û</font>";
    }elsif($feel > 240) {
        $tension = "<font color=\"orange\">Ä¶¶¯µ¤</font>";
    }elsif($feel > 180) {
        $tension = "<font color=\"yellow\">¶¯µ¤</font>";
    }elsif($feel > 120) {
        $tension = "<font color=\"lime\">ÉáÄÌ</font>";
    }elsif($feel > 60) {
        $tension = "<font color=\"aqua\">¼åµ¤</font>";
    }elsif($feel > 0) {
        $tension = "<font color=\"blue\">Ýµ</font>";
    }else{
        $tension = "<font color=\"fuchsia\">º®Íð</font>";
    }
    if($w_feel == 300) {
        $w_tension = "<font color=\"red\">Ä¶±Û</font>";
    }elsif($w_feel > 240) {
        $w_tension = "<font color=\"orange\">Ä¶¶¯µ¤</font>";
    }elsif($w_feel > 180) {
        $w_tension = "<font color=\"yellow\">¶¯µ¤</font>";
    }elsif($w_feel > 120) {
        $w_tension = "<font color=\"lime\">ÉáÄÌ</font>";
    }elsif($w_feel > 60) {
        $w_tension = "<font color=\"aqua\">¼åµ¤</font>";
    }elsif($w_feel > 0) {
        $w_tension = "<font color=\"blue\">Ýµ</font>";
    }else{
        $w_tension = "<font color=\"fuchsia\">º®Íð</font>";
    }

    if ($a_name ne "") {
        $nickname = "¡Ê$a_name¡Ë";
    }
    if ($w_a_name ne "") {
        $w_nickname = "¡Ê$w_a_name¡Ë";
    }

print <<"_HERE_";
<TABLE width="600">
  <TBODY>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000" size="+3" face="£Í£Ó ÌÀÄ«">ÀïÆ®È¯À¸</FONT></B></TD>
    </TR>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000">@links</FONT></B></TD>
    </TR>
    <TR>
      <TD valign="top" width="398" height="300">
      <TABLE border="1" width="397" cellspacing="0" height="300">
        <TBODY>
          <TR align="center">
            <TD valign="top"><BR>
            <BR>
            <TABLE border="0">
              <TBODY>
                <TR align="center">
                  <TD width="40%"><IMG src="$imgurl$icon" width="70" height="70" border="0" align="middle"></TD>
                  <TD width="20%"></TD>
                  <TD width="40%"><IMG src="$imgurl$w_icon" width="70" height="70" border="0" align="middle"></TD>
                </TR>
                <TR align="center">
                  <TD>$cln</TD>
                  <TD></TD>
                  <TD>$w_cln</TD>
                </TR>
                <TR align="center">
                  <TD>$f_name $l_name</TD>
                  <TD>£Ö£Ó</TD>
                  <TD>$w_f_name $w_l_name</TD>
                </TR>
                <TR align="center">
                  <TD>$nickname</TD>
                  <TD></TD>
                  <TD>$w_nickname</TD>
                </TR>
                <TR align="center">
                  <TD>$group</TD>
                  <TD><font color="yellow"><b>½êÂ°</b></font></TD>
                  <TD>$w_group</TD>
                </TR>
                <TR align="center">
                  <TD>$hpper</TD>
                  <TD><font color="yellow"><b>¾õÂÖ</b></font></TD>
                  <TD>$w_hpper</TD>
                </TR>
                <TR align="center">
                  <TD>$tension</TD>
                  <TD><font color="yellow"><b>¥Æ¥ó¥·¥ç¥ó</b></font></TD>
                  <TD>$w_tension</TD>
                </TR>
                <TR align="center">
                  <TD>$kill¿Í</TD>
                  <TD><font color="yellow"><b>»¦³²¿Í¿ô</b></font></TD>
                  <TD>$w_kill¿Í</TD>
                </TR>
                <TR align="center">
                  <TD>$wep_n</TD>
                  <TD><font color="yellow"><b>Éð´ï</b></font></TD>
                  <TD>$w_wep_n</TD>
                </TR>
                <TR align="center">
                  <TD>$bou_n</TD>
                  <TD><font color="yellow"><b>ÂÎËÉ¶ñ</b></font></TD>
                  <TD>$w_bou_n</TD>
                </TR>
              </TBODY>
            </TABLE>
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" width="199" height="300">
      <TABLE border="1" cellspacing="0">
        <TBODY>
          <TR><TH width="200">¥³¥Þ¥ó¥É</TH>
          <TR>
            <TD align="left" valign="top" width="198" height="280">
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
        </TBODY>
      </TABLE>
      </TD>
    </TR>
    <TR>
      <TD colspan="2" valign="top" width="600" height="101">
      <TABLE border="1" cellspacing="0" width="600" height="150" cellpadding="0">
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

$mflg="ON"; #¥¹¥Æ¡¼¥¿¥¹ÈóÉ½¼¨
}
#==================#
# ¢£ Æ¨Ë´½èÍý      #
#==================#
sub RUNAWAY {

    $log = ($log . "$l_name ¤Ï Á´Â®ÎÏ¤ÇÆ¨¤²½Ð¤·¤¿¡¦¡¦¡¦¡£<BR>") ;

    $Command = "MAIN";

}

#==================#
# ¢£ ËÉ¶ñ¼ïÊÌ½èÍý  #
#==================#
sub DEFTREAT {

    local($wkind)   = @_[0] ;   #Éð´ï¼ïÊÌ
    local($defman)   = @_[1] ;  #ËÉ¸æÂ¦(PC/NPC)

    local($p_up) = 1.5 ;
    local($p_down) = 0.5 ;

    if ($defman eq "PC") {  #PC?
        local($b_name,$b_kind) = split(/<>/, $bou);
        local($b_name_h,$b_kind_h) = split(/<>/, $bou_h);
        local($b_name_f,$b_kind_f) = split(/<>/, $bou_f);
        local($b_name_a,$b_kind_a) = split(/<>/, $bou_a);
        local($b_name_i,$b_kind_i) = split(/<>/, $item[5]);
    } else {
        local($b_name,$b_kind) = split(/<>/, $w_bou);
        local($b_name_h,$b_kind_h) = split(/<>/, $w_bou_h);
        local($b_name_f,$b_kind_f) = split(/<>/, $w_bou_f);
        local($b_name_a,$b_kind_a) = split(/<>/, $w_bou_a);
        local($b_name_i,$b_kind_i) = split(/<>/, $w_item[5]);
    }

    if (($wkind eq "WG") && ($b_kind_i eq "ADB")) { #½Æ¢ªËÉÃÆ
        $pnt = $p_down ;
    } elsif (($wkind eq "WG") && ($b_kind_h eq "DH")) { #½Æ¢ªÆ¬
        $pnt = $p_up ;
    } elsif (($wkind eq "WN") && ($b_kind eq "DBK")) { #»Â¢ªº¿
        $pnt = $p_down ;
    } elsif (($wkind eq "WN") && ($b_kind_i eq "ADB")) { #»Â¢ªËÉÃÆ
        $pnt = $p_up ;
    } elsif ((($wkind eq "WB")||($wkind eq "WGB")||($wkind eq "WAB")) && ($b_kind_h eq "DH")) { #²¥¢ªÆ¬
        $pnt = $p_down ;
    } elsif ((($wkind eq "WB")||($wkind eq "WGB")||($wkind eq "WAB")) && ($b_kind =~ /DBA/)) { #²¥¢ª³»
        $pnt = $p_up ;
    } elsif (($wkind eq "WS") && ($b_kind =~ /DBA/)) { #»É¢ª³»
        $pnt = $p_down ;
    } elsif (($wkind eq "WS") && ($b_kind =~ /DBK/)) { #»É¢ªº¿
        $pnt = $p_up ;
    } else {
        $pnt = 1.0 ;
    }

}
#======================#
# ¢£ ¥ì¥Ù¥ë¥¢¥Ã¥×½èÍý  #
#======================#
sub LVUPCHK {

    if (($exp >= ($level * $level) + ($level * $baseexp))&&($hit > 0)) { #¥ì¥Ù¥ë¥¢¥Ã¥×
        $log = ($log . "¥ì¥Ù¥ë¤¬¾å¤¬¤Ã¤¿¡£<br>") ;
        $mhit += int(rand(3)+2) ; $att += int(rand(3)+2); $def += int(rand(3)+2); $level++;
    }
    if (($w_exp >= ($w_level * $w_level) + ($w_level * $baseexp)) && ($w_hit > 0)) { #¥ì¥Ù¥ë¥¢¥Ã¥×
        $w_log = ($w_log . "¥ì¥Ù¥ë¤¬¾å¤¬¤Ã¤¿¡£<br>") ;
        $w_mhit += int(rand(3)+2) ; $w_att += int(rand(3)+2); $w_def += int(rand(3)+2); $w_level++;
    }

}

#======================#
# ¢£ Å¨²óÉü½èÍý        #
#======================#
sub EN_KAIFUKU{ #Å¨²óÉü½èÍý
    $up = ($now - $w_endtime) / (1 * $kaifuku_time);
    if ($w_inf =~ /Ê¢/) { $up = $up / 2; }
    if ($w_inf =~ /NPC/) { $up = $up / 2; }
    if ($w_sts eq "¿çÌ²") {
        if ($w_club eq "¥µ¥Ð¥¤¥Ð¥ëÉô") { $up = $up * 1.5; }
        $up = int($up);
        $w_sta += $up;
        if ($w_sta > $maxsta) { $w_sta = $maxsta; }
        $w_endtime = $now;
    } elsif ($w_sts eq "¼£ÎÅ") {
        if ($kaifuku_rate == 0){$kaifuku_rate = 1;}
        if ($w_club eq "ÊÝ·ò°Ñ°÷") { $up = $up * 1.5; }
        $up = int($up / $kaifuku_rate);
        $w_hit += $up;
        if ($w_hit > $w_mhit) { $w_hit = $w_mhit; }
        $w_endtime = $now;
        if ($pgday > 6) { $w_sts = "¿çÌ²"; }
    }
}

#===========================#
# ¢£ Å¨ÀïÆ®¥í¥°¼«Æ°ºï½ü½èÍý #
#===========================#
sub BLOG_CK{
    $log_len = length($w_log);
    if($log_len > 2000) {
        $w_log = "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¥í¥°¤Ï¼«Æ°ºï½ü¤µ¤ì¤Þ¤·¤¿¡£</b></font><br>";
    }
}

#==================#
# ¢£ É¬»¦µ» ¹ÔÆ°Â¦ #
#==================#
sub SKILL_PC {
    #É¬»¦µ»¥Õ¥§¥¤¥º
    local($s_dice) = rand(100);
    local($s_res) = 0;
    local($s_ren) = 0;
    local($s_nam) = "";

    if ($w_kind =~ /G/) {
        $s_ren = $wg;
        if ($s_ren > 80) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡ØÒöÒã¡Ù";
        }
    } elsif ($w_kind =~ /A/) {
        $s_ren = $wa;
        if ($s_ren > 80) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡Ø¼ÀÉ÷¡Ù";
        }
    } elsif ($w_kind =~ /C/) {
        $s_ren = $wc;
        if ($s_ren > 60) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡ØÎ®À±¡Ù";
        }
    } elsif ($w_kind =~ /D/) {
        $s_ren = $wd;
        if ($s_ren > 60) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡Øº®ÆÙ¡Ù";
        }
    } elsif ($w_kind =~ /B/) {
        $s_ren = $wb;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡ØÅÜÞ¹¡Ù";
        }
    } elsif ($w_kind =~ /N/) {
        $s_ren = $wn;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡Ø»Ä¿´¡Ù";
        }
    } elsif ($w_kind =~ /S/) {
        $s_ren = $ws;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡ØÁ®¸÷¡Ù";
        }
    } elsif ($w_kind =~ /P/) {
        $s_ren = $wp;
        if ($s_ren > 120) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "Àïµ»¡ØÏ¢·â¡Ù";
        }
    }

    if (($s_res > 0) && ($s_ren > 0) && ($s_nam ne "")) {
        if ($s_dice < (($s_ren / 10) + $level + 10)) {
            $log = $log . "<font color=\"yellow\"><b>$s_namÈ¯Æ°¡ª $s_res ¤ÎÄÉ²Ã¥À¥á¡¼¥¸</b></font>¡ª<br>";
            $w_hit -= $s_res; $result = "$result+$s_res";
        }
    }
}

#=====================#
# ¢£ ·Ð¸³ÃÍÄÉ²Ã PC Â¦ #
#=====================#
sub EXPPLUS_PC {
    $p_exp = int(($w_level - $level + 1) / 2); if ($p_exp <= 0) { $p_exp = 0; } 
    $p_exp++;
    $log = ($log . "$l_name ¤Ï<font color=\"yellow\"><b> $p_exp </b></font>¤Î·Ð¸³ÃÍ¤òÆÀ¤¿¡£<br>") ;
    $exp += $p_exp;
}

#=====================#
# ¢£ ·Ð¸³ÃÍÄÉ²Ã NPCÂ¦ #
#=====================#
sub EXPPLUS_NPC {
    $p_exp = int(($level - $w_level + 1) / 2); if ($p_exp <= 0) { $p_exp = 0; } 
    $p_exp++;
    $w_exp += $p_exp;
}

1;
