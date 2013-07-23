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

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);
        if ($w_id eq $wid) {
            $Index2=$i ; last;
        }
    }

    if (($w_bid eq $id)||($w_hit <= 0)) {
        &ERROR("ÉÔÀµ¥¢¥¯¥»¥¹¤Ç¤¹") ;
    }

    &BB_CK; #¥Ö¥é¥¦¥¶¥Ð¥Ã¥¯ÂÐ½è

    $log = ($log . "$w_f_name $w_l_name¡Ê$w_cl $w_sex$w_noÈÖ¡Ë¤ÈÀïÆ®³«»Ï¡ª<br>") ;

    ($w_name,$a) = split(/<>/, $wep);
    ($w_name2,$w_kind2) = split(/<>/, $w_wep);

    &TACTGET; &TACTGET2;    #´ðËÜ¹ÔÆ°

    #¥×¥ì¥¤¥ä¡¼
    if ((($wep =~ /G|A/) && ($wtai == 0)) || (($wep =~ /G|A/) && ($w_kind eq "WB"))) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_p = $ball * $dfp ;

    #Å¨
    if (($w_wep =~ /G|A/) && ($w_wtai == 0)) {
        $att_n = (($w_watt/10) + $w_att) * $atn ;
    } else {
        $att_n = ($w_watt + $w_att) * $atn ;
    }
    local($ball2) = $w_def + $w_bdef + $w_bdef_h + $w_bdef_a + $w_bdef_f ;
    if ($w_item[5] =~ /AD/) {$ball2 += $w_eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_n = $ball2 * $dfn ;
    $w_bid = $id ;
    $bid = $w_id ;

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

        $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;

        $exp++;

    } else {
        $kega3 = "" ;
        $log = ($log . "¤·¤«¤·¡¢Èò¤±¤é¤ì¤¿¡ª<br>") ;
    }

    if ($w_hit <= 0) {  #Å¨»àË´¡©
        &DEATH2;
    } elsif (rand(10) < 5) {    #È¿·â

        if ($weps eq $weps2) {  #µ÷Î¥°ì½ï¡©

            &WEPTREAT($w_name2, $w_kind2,  $w_wtai, $w_l_name, $l_name, "È¿·â", "NPC") ;

            if ($dice2 < $mei2) {   #¹¶·âÀ®¸ù
                $result2 = ($att_n*$wk) - $def_p;
                $result2 /= 2 ;
                $result2 += rand($result2);

                &DEFTREAT($w_kind2, "PC") ;
                $result2 = int($result2 * $pnt) ;

                if ($result2 <= 0) {$result2 = 1 ;}
                $log = ($log . "<font color=\"red\"><b>$result2¥À¥á¡¼¥¸ $kega2</b></font>¡ª<br>") ;

                $btai--;$hit -= $result2;

                if ($btai <= 0) { $bou = "²¼Ãå<>DN"; $bdef=0; $btai="¡ç"; }

                if ($hit <=0) { #»àË´¡©
                    &DEATH;
                } else {    #Æ¨Ë´
                    $log = ($log . "$w_l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
                }
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result2 Èï:$result $hakaiinf2 $kega3 </b></font><br>") ;
                $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;
                $w_exp++;
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë Èï:$result $kega3 </b></font><br>") ;
                $log = ($log . "¤·¤«¤·¡¢´Ö°ìÈ±Èò¤±¤¿¡ª<br>") ;
            }

            if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #½Æ¡¦¼Í¡©
                $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
            } elsif ($w_kind2 =~ /C|D/) {
                $w_wtai--; if ($w_wtai <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
            } elsif (($w_kind2 =~ /N/) && (int(rand(5)) == 0)) {
                $w_watt -= int(rand(2)+1) ; if ($w_watt <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
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
    } elsif ($w_kind =~ /C|D/) {
        $wtai--; if ($wtai <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
    } elsif (($w_kind =~ /N/) && (int(rand(5)) == 0)) {
        $watt -= int(rand(2)+1) ; if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
    }

    &LVUPCHK() ;


    &SAVE;
    &SAVE2;

}
#==================#
# ¢£ ¸å¹¶¹¶·â½èÍý  #
#==================#
sub ATTACK2 {
    $kega2 = "" ; $kega3 = "" ;
    $hakaiinf2 = ""; $hakaiinf3 = "";

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

    &TACTGET; &TACTGET2;    #´ðËÜ¹ÔÆ°

    #¥×¥ì¥¤¥ä¡¼
    if (($wep =~ /G|A/) && ($wtai == 0)) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #Áõ¾þ¤¬ËÉ¶ñ¡©
    $def_p = $ball * $dfp ;

    #Å¨
    if (($w_wep =~ /G|A/) && ($w_wtai == 0)) {
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

        if ($btai <= 0) { $bou = "²¼Ãå<>DN"; $bdef=0; $btai="¡ç"; }
        $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;
        ($w_name2,$w_kind2) = split(/<>/, $w_wep);
        $w_exp++;
    } else {
        $log = ($log . "¤·¤«¤·¡¢´Ö°ìÈ±Èò¤±¤¿¡ª<br>") ;
    }

    if ($hit <= 0) {    #»àË´¡©
        &DEATH;
    } elsif (rand(10) <5) { #È¿·â

        if ($weps eq $weps2) {

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

                if ($w_hit <=0) {   #»àË´¡©
                    &DEATH2;
                } else {    #Æ¨Ë´
                    $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
                }
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result Èï:$result2 $hakaiinf2 $kega3 </b></font><br>") ;
                $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;
                ($w_name,$w_kind) = split(/<>/, $wep);
                $exp++;
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result $hakaiinf2 </b></font><br>") ;
                $log = ($log . "¤·¤«¤·¡¢Èò¤±¤é¤ì¤¿¡ª<br>") ;
            }

            if (($w_kind =~ /G|A/) && ($wtai > 0)) {    #½Æ¡¦¼Í¡©
                $wtai--; if ($wtai <= 0) { $wtai = 0 ; }
            } elsif ($w_kind =~ /C|D/) {
                $wtai--; if ($wtai <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
            } elsif (($w_kind =~ /N/) && (int(rand(5)) == 0)) {
                $watt -= int(rand(2)+1) ; if ($watt <= 0) { $wep ="ÁÇ¼ê<>WP"; $watt=0; $wtai="¡ç"; }
            }
        } else {
            $log = ($log . "$l_name ¤Ï È¿·â¤Ç¤­¤Ê¤¤¡ª<br>") ;
            $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
            $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result $hakaiinf2 $kega3 </b></font><br>") ;
        }
    } else {    #Æ¨Ë´
        $log = ($log . "$l_name ¤Ï Æ¨¤²ÀÚ¤Ã¤¿¡¦¡¦¡¦¡£<br>") ;
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec ÀïÆ®¡§$f_name $l_name¡Ê$cl $sex$noÈÖ¡Ë ¹¶:$result $hakaiinf2 $kega3 </b></font><br>") ;
    }

    if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #½Æ¡¦¼Í¡©
        $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
    } elsif ($w_kind2 =~ /C|D/) {
        $w_wtai--; if ($w_wtai <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
    } elsif (($w_kind2 =~ /N/) && (int(rand(5)) == 0)) {
        $w_watt -= int(rand(2)+1) ; if ($w_watt <= 0) { $w_wep ="ÁÇ¼ê<>WP"; $w_watt=0; $w_wtai="¡ç"; }
    }

    &LVUPCHK();


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
        $kega = 15 ;$kegainf = "Æ¬ÏÓ" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /A/) {   #µÝ·Ï¡©
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nnÌÜ³Ý¤±¤Æ¼Í¤¿¡ª") ;
        if ($attman eq "PC") {$wa++;$wk=$wa;} else {$w_wa++;$wk=$w_wa;}
        $kega = 20 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /C/) { #Åê·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nn¤ËÅê¤²¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wc++;$wk=$wc;} else {$w_wc++;$wk=$w_wc;}
        $kega = 15 ;$kegainf = "Æ¬ÏÓ" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /D/) { #Çú·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nn¤ËÅê¤²¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wd++;$wk=$wd;} else {$w_wd++;$wk=$w_wd;}
        $kega = 15 ;$kegainf = "Æ¬ÏÓÏÓÂ­" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /G/) { #½Æ·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤ò $nnÌÜ³Ý¤±¤ÆÈ¯Ë¤¤·¤¿¡ª") ;
        if ($attman eq "PC") {$wg++;$wk=$wg;$ps=$pls;} else {$w_wg++;$wk=$w_wg;$ps=$w_pls;}
        $kega = 25 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
        open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
        $gunlog[0] = "$now,$place[$ps],$id,$w_id,\n";
        open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    } elsif ($wkind =~ /S/) { #»É·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò»É¤·¤¿¡ª") ;
        if ($attman eq "PC") {$ws++;$wk=$ws;} else {$w_ws++;$wk=$w_ws;}
        $kega = 25 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /N/) { #»Â·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤Ë»Â¤ê¤Ä¤±¤¿¡ª") ;
        if ($attman eq "PC") {$wn++;$wk=$wn;} else {$w_wn++;$wk=$w_wn;}
        $kega = 25 ; $kegainf = "Æ¬ÏÓÊ¢Â­" ;    #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 3 ;    #ÇË²õÎ¨
    } elsif ($wkind =~ /P/) { #²¥·Ï
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò²¥¤Ã¤¿¡ª") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 0 ; $kegainf = "" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
        $hakai = 0 ;    #ÇË²õÎ¨
    } else { #¤½¤ÎÂ¾
        $log = ($log . "$pn¤Î$ind¡ª$wname ¤Ç $nn¤ò²¥¤Ã¤¿¡ª") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 0 ; $kegainf = "" ; #²ø²æÎ¨¡¢²ø²æ¸Ä½ê
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
# ¢£ ÀïÆ®·ë²Ì½èÍý  #
#================#
sub BATTLE {

    $cln = "$w_cl¡Ê$w_sex$w_noÈÖ¡Ë" ;

print <<"_HERE_";
<P align="center"><B><FONT color="#ff0000" size="+3" face="£Í£Ó ÌÀÄ«">$place[$pls]¡Ê$area[$pls]¡Ë</FONT></B><BR>
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
          <TR align="center">
            <TD valign="top"><BR>
            <B><FONT color="#ff0000" size="5" face="£Í£Ó ÌÀÄ«">ÀïÆ®È¯À¸</FONT></B><BR>
            <BR>
            <TABLE border="0">
              <TBODY>
_HERE_

if($icon_mode){
    print "<TR align=\"center\">\n";
    print "<TD><IMG src=\"$imgurl$icon_file[$icon]\" width=\"70\" height=\"70\" border=\"0\" align=\"middle\"></TD>\n";
    print "<TD></TD>\n";
    print "<TD><IMG src=\"$imgurl$icon_file[$w_icon]\" width=\"70\" height=\"70\" border=\"0\" align=\"middle\"></TD>\n";
    print "</TR>\n";
}

print <<"_HERE_";
                <TR align="center">
                  <TD>$cl¡Ê$sex$noÈÖ¡Ë</TD>
                  <TD width="50" align="center">£Ö£Ó</TD>
                  <TD>$cln</TD>
                </TR>
                <TR align="center">
                  <TD>$f_name $l_name</TD>
                  <TD></TD>
                  <TD>$w_f_name $w_l_name</TD>
                </TR>
              </TBODY>
            </TABLE>
            <BR><BR><BR><BR>
            <BR>
            </TD>
          </TR>
        </TBODY>
      </TABLE>
      </TD>
      <TD valign="top" width="200" height="311">
      <TABLE border="1" cellspacing="0">
        <TBODY>
          <TR><TD align="center" width="250"><B>¥³¥Þ¥ó¥É</B></TD>
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
# ¢£ Æ¨Ë´½èÍý  #
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

    if (($exp >= int($level*$baseexp+(($level-1)*$baseexp)))&&($hit > 0)) { #¥ì¥Ù¥ë¥¢¥Ã¥×
        $log = ($log . "¥ì¥Ù¥ë¤¬¾å¤¬¤Ã¤¿¡£<br>") ;
        $mhit += int(rand(3)+7) ; $att += int(rand(3)+2); $def += int(rand(3)+2); $level++;
    }
    if (($w_exp >= int($w_level*$baseexp+(($w_level-1)*$baseexp)))&&($w_hit > 0)) { #¥ì¥Ù¥ë¥¢¥Ã¥×
        $w_log = ($w_log . "¥ì¥Ù¥ë¤¬¾å¤¬¤Ã¤¿¡£<br>") ;
        $w_mhit += int(rand(3)+7) ; $w_att += int(rand(3)+2); $w_def += int(rand(3)+2); $w_level++;
    }

}

#======================#
# ¢£ Å¨²óÉü½èÍý        #
#======================#
sub EN_KAIFUKU{ #Å¨²óÉü½èÍý
    $up = int(($now - $w_endtime) / (1 * $kaifuku_time));
    if ($w_inf =~ /Ê¢/) { $up = int($up / 2); }
    if ($w_sts eq "¿çÌ²") {
        $w_sta += $up;
        if ($w_sta > $maxsta) { $w_sta = $maxsta; }
        $w_endtime = $now;
    } elsif ($w_sts eq "¼£ÎÅ") {
        if($kaifuku_rate == 0){$kaifuku_rate = 1;}
        $up = int($up / $kaifuku_rate);
        $w_hit += $up;
        if ($w_hit > $w_mhit) { $w_hit = $w_mhit; }
        $w_endtime = $now;
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

1;
