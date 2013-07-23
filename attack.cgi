#==================#
# ■ 先制攻撃処理  #
#==================#
sub ATTACK {

    $log = ($log . "$w_f_name $w_l_name（$w_cl $w_sex$w_no番）を発見した！<br>") ;
    $log = ($log . "$w_f_name $w_l_name　は こちらには気づいてないな・・・。<br>") ;

    $Command=("BATTLE0" . "_" . $w_id);

}
#==================#
# ■ 先制攻撃処理  #
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

    if ((($w_bid eq $group) && ($tactics ne "連闘行動")) || ($w_hit <= 0)) {
        $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host,rentou,$w_bid,\n";
        open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
        &ERROR("不正アクセスです") ;
    }

    &BB_CK; #ブラウザバック対処

    $log = ($log . "$w_f_name $w_l_name（$w_cl $w_sex$w_no番）と戦闘開始！<br>") ;

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

    &TACTGET; &TACTGET2;    #基本行動

    #プレイヤー
    if ((($wep =~ /G|A/) && ($wtai == 0)) || (($wep =~ /G|A/) && ($w_kind =~ /B/))) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #装飾が防具？
    $def_p = $ball * $dfp ;

    #敵
    if ((($w_wep =~ /G|A/) && ($w_wtai == 0)) || (($w_wep =~ /G|A/) && ($w_kind2 =~ /B/))) {
        $att_n = (($w_watt/10) + $w_att) * $atn ;
    } else {
        $att_n = ($w_watt + $w_att) * $atn ;
    }
    local($ball2) = $w_def + $w_bdef + $w_bdef_h + $w_bdef_a + $w_bdef_f ;
    if ($w_item[5] =~ /AD/) {$ball2 += $w_eff[5];} #装飾が防具？
    $def_n = $ball2 * $dfn ;
    $w_bid = $group ;
    $bid = $w_group ;

    &BLOG_CK;
    &EN_KAIFUKU;

    $Command="BATTLE";

    if ($w_pls ne $pls) {   #既に移動？
        $log = ($log . "しかし、$w_f_name $w_l_name（$w_cl $w_sex$w_no番）に逃げられてしまった！<br>") ;
        &SAVE;
        return ;
    }

    if (length($dengon) > 0) {
        $log = ($log . "<font color=\"lime\"><b>$f_name $l_name（$cl $sex$no番）「$dengon」</b></font><br>") ;
        $w_log = ($w_log . "<font color=\"lime\"><b>$hour:$min:$sec $f_name $l_name（$cl $sex$no番）「$dengon」</b></font><br>") ;
    }

    &WEPTREAT($w_name, $w_kind, $wtai, $l_name, $w_l_name, "攻撃", "PC") ;
    if ($Command2 eq "CATKon") {
        $log = ($log . "必殺の力を込めた一撃！！");
        $feel -= 50 + int(rand(100));
        $att_p = $att_p * 1.2;
    }
    if ($dice1 < $mei) {    #攻撃成功

        $result = ($att_p*$wk) - $def_n;
        $result /= 2 ;
        $result += rand($result);

        &DEFTREAT($w_kind, "NPC") ;
        $result = int($result * $pnt) ;

        if ($result <= 0) {$result = 1} ;
        $log = ($log . "<font color=\"red\"><b>$resultダメージ $hakaiinf3 $kega3 </b></font>！<br>") ;

        $w_hit -= $result;
        $w_btai--;
        if ($w_btai <= 0) { $w_bou = "下着<>DN"; $w_bdef=0; $w_btai="∞"; }

        $feel   += 1 + int(rand(3));
        $w_feel -= 1;

        $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;

        &SKILL_PC;

        &EXPPLUS_PC;

        if (($w_kind =~ /N|S/) && (int(rand(6)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_nameが刃こぼれした</b></font>！<br>") ;
            if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
        } elsif (($w_kind =~ /B/) && (int(rand(7)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_nameにひびが入った</b></font>！<br>") ;
            if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
        } elsif (($w_kind =~ /P/) && ($w_name ne "素手") && (int(rand(6)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_nameがすり減った</b></font>！<br>") ;
            if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
        } elsif (($w_kind =~ /C/) && ($wtai eq "∞") && (int(rand(7)) == 0)) {
            $watt--; if (int(rand(4)) == 0) { $watt--; }
            $log = ($log . "<font color=\"red\"><b>$w_nameが損耗した</b></font>！<br>") ;
            if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
        }
    } else {
        $kega3 = "" ;
        $log = ($log . "しかし、避けられた！<br>") ;
        $feel   -= 1 + int (rand(2));
        $w_feel += 1 + int (rand(3));

    }

    if (($w_item[5] =~ /<>AH/) && ($w_hit <= 0)) {
        ($w_in_a,$w_ik_a) = split(/<>/, $w_item[5]);
        $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）の$w_in_aが壊れた！</b></font><br>") ;
        $kega3 = ($kega3 . " <font color=\"red\">$w_in_a破壊！</font>") ;
        if($w_in_a eq "戦乙女の祝福") { $w_hit = int($w_mhit * 0.2); }
        elsif($w_in_a eq "死返玉") { $w_hit = int($w_mhit * 0.2); }
        else { $w_hit = 1; }
        $w_item[5] = "なし"; $w_eff[5] = 0; $w_itai[5] = 0;
    }

    if ($w_hit <= 0) {  #敵死亡？
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 被:$result $kega3 </b></font><br>") ;
        &DEATH2;
    } elsif (rand(10) < 5) {    #反撃

        if (($weps eq $weps2) || ($weps2 eq "L")) {  #距離一緒？

            &WEPTREAT($w_name2, $w_kind2,  $w_wtai, $w_l_name, $l_name, "反撃", "NPC") ;

            if ($dice2 < $mei2) {   #攻撃成功
                $result2 = ($att_n*$wk) - $def_p;
                $result2 /= 2 ;
                $result2 += rand($result2);

                &DEFTREAT($w_kind2, "PC") ;
                $result2 = int($result2 * $pnt) ;

                if ($result2 <= 0) {$result2 = 1 ;}
                $log = ($log . "<font color=\"red\"><b>$result2ダメージ $kega2</b></font>！<br>") ;

                $btai--;
                $hit -= $result2;

                $feel   -= 1;
                $w_feel += 1 + int (rand(3));

                if ($btai <= 0) { $bou = "下着<>DN"; $bdef=0; $btai="∞"; }

                if (($item[5] =~ /<>AH/)&&($hit <= 0)) {
                    ($in_a,$ik_a) = split(/<>/, $item[5]);
                    $log = ($log . "<font color=\"RED\"><b>$in_aが壊れてしまった！</b></font><br>") ;
                    if($in_a eq "戦乙女の祝福") { $hit = int($mhit * 0.2); }
                    elsif($in_a eq "死返玉") { $hit = int($mhit * 0.2); }
                    else { $hit = 1; }
                    $item[5] = "なし"; $eff[5] = 0; $itai[5] = 0;
                }

                if ($hit <=0) { #死亡？
                    &DEATH;
                } else {    #逃亡
                    $log = ($log . "$w_l_name は 逃げ切った・・・。<br>") ;
                }

                &EXPPLUS_NPC;
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result2 被:$result <font color=\"#00ffff\">Exp:$p_exp</font> $hakaiinf2 $kega3 </b></font><br>") ;
                $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;

                if ((($w_kind2 =~ /N|S|B|P/) || (($w_kind2 =~ /C/) && ($w_wtai eq "∞"))) && (int(rand(6)) == 0)) {
                    $w_watt--; if (int(rand(4)) == 0) { $w_watt--; }
                    if ($w_watt <= 0) { $w_wep ="素手<>WP"; $w_watt=0; $w_wtai="∞"; }
                }
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result2 被:$result $kega3 </b></font><br>") ;
                $log = ($log . "しかし、間一髪避けた！<br>") ;
                $feel   += 1 + int (rand(3));
                $w_feel -= 1 + int (rand(2));

            }

            if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #銃・射？
                $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
            } elsif (($w_kind2 =~ /C|D/) && ($w_wtai ne "∞")) {
                $w_wtai--; if ($w_wtai <= 0) { $w_wep ="素手<>WP"; $w_watt=0; $w_wtai="∞"; }
            }
        } else {
            $log = ($log . "$w_l_name は 反撃できない！<br>") ;
            $log = ($log . "$w_l_name は 逃げ切った・・・。<br>") ;
            $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 被:$result $hakaiinf2 $kega3 </b></font><br>") ;
        }
    } else {    #逃亡
        $log = ($log . "$w_l_name は 逃げ切った・・・。<br>") ;
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 被:$result $hakaiinf2 $kega3 </b></font><br>") ;
    }

    if (($w_kind =~ /G|A/) && ($wtai > 0)) {    #銃・射？
        $wtai--; if ($wtai <= 0) { $wtai = 0 ; }
    } elsif (($w_kind =~ /C|D/) && ($wtai ne "∞")) {
        $wtai--; if ($wtai <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
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
# ■ 後攻攻撃処理  #
#==================#
sub ATTACK2 {
    $kega2 = "" ; $kega3 = "" ;
    $hakaiinf2 = ""; $hakaiinf3 = "";
    $getexp = 0;

    if ($w_hit <= 0) {
        &ERROR("不正アクセスです") ;
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

    &TACTGET; &TACTGET2;    #基本行動

    #プレイヤー
    if ((($wep =~ /G|A/) && ($wtai == 0)) || (($wep =~ /G|A/) && ($w_kind =~ /B/))) {
        $att_p = (($watt/10) + $att) * $atp ;
    } else {
        $att_p = ($watt + $att) * $atp ;
    }
    local($ball) = $def + $bdef + $bdef_h + $bdef_a + $bdef_f ;
    if ($item[5] =~ /AD/) {$ball += $eff[5];} #装飾が防具？
    $def_p = $ball * $dfp ;

    #敵
    if ((($w_wep =~ /G|A/) && ($w_wtai == 0)) || (($w_wep =~ /G|A/) && ($w_kind2 =~ /B/))) {
        $att_n = (($w_watt/10) + $w_att) * $atn ;
    } else {
        $att_n = ($w_watt + $w_att) * $atn ;
    }
    local($ball2) = $w_def + $w_bdef + $w_bdef_h + $w_bdef_a + $w_bdef_f ;
    if ($w_item[5] =~ /AD/) {$ball += $w_eff[5];} #装飾が防具？
    $def_n = $ball2 * $dfn ;

    &BLOG_CK;
    &EN_KAIFUKU;

    $Command="BATTLE";

    $log = ($log . "$w_f_name $w_l_name（$w_cl $w_sex$w_no番）が突如襲い掛かってきた！<br>") ;

    &WEPTREAT($w_name2, $w_kind2,  $w_wtai, $w_l_name, $l_name, "攻撃", "NPC") ;
    if ($dice2 < $mei2) {    #攻撃成功

        $result = ($att_n*$wk) - $def_p;
        $result /= 2 ;
        $result += rand($result);
        $result = int($result) ;

        &DEFTREAT($w_kind2, "PC") ;
        $result = int($result * $pnt) ;

        if ($result <= 0) {$result = 1 ;}
        $log = ($log . "<font color=\"red\"><b>$resultダメージ $kega2</b></font>！<br>") ;

        $hit -= $result;
        $btai--;

        $feel   -= 1;
        $w_feel += 1 + int(rand(3));

        if ($btai <= 0) { $bou = "下着<>DN"; $bdef=0; $btai="∞"; }
        $w_wep = $w_wep_2; $w_watt = $w_watt_2; $w_wtai = $w_wtai_2; $inf = $inf_2 ;

        &EXPPLUS_NPC; $getexp = $p_exp;

        if ((($w_kind2 =~ /N|S|B|P/) || (($w_kind2 =~ /C/) && ($w_wtai eq "∞"))) && (int(rand(6)) == 0)) {
            $w_watt--; if (int(rand(4)) == 0) { $w_watt--; }
            if ($w_watt <= 0) { $w_wep ="素手<>WP"; $w_watt=0; $w_wtai="∞"; }
        }
    } else {
        $log = ($log . "しかし、間一髪避けた！<br>") ;
        $feel   += 1 + int(rand(3));
        $w_feel -= 1 + int(rand(2));
    }

    if (($item[5] =~ /<>AH/)&&($hit <= 0)) {
        ($in_a,$ik_a) = split(/<>/, $item[5]);
        $log = ($log . "<font color=\"RED\"><b>$in_aが壊れてしまった！</b></font><br>") ;
        if($in_a eq "戦乙女の祝福") { $hit = int($mhit * 0.2); }
        elsif($in_a eq "死返玉") { $hit = int($mhit * 0.2); }
        else { $hit = 1; }
        $item[5] = "なし"; $eff[5] = 0; $itai[5] = 0;
    }

    if ($hit <= 0) {    #死亡？
        &DEATH;
    } elsif (rand(10) <5) { #反撃

        if (($weps eq $weps2) || ($weps eq "L")) {

            &WEPTREAT($w_name, $w_kind,  $wtai, $l_name, $w_l_name, "反撃", "PC") ;
            if ($dice1 < $mei) {    #攻撃成功

                $result2 = ($att_p*$wk) - $def_n;
                $result2 /= 2 ;
                $result2 += rand($result2);
                $result2 = int($result2) ;

                &DEFTREAT($w_kind, "NPC") ;
                $result2 = int($result2 * $pnt) ;

                if ($result2 <= 0) {$result2 = 1 ;}
                $log = ($log . "<font color=\"red\"><b>$result2ダメージ $hakaiinf3 $kega3</b></font>！<br>") ;

                $w_hit -= $result2;

                $w_btai--;
                if ($w_btai <= 0) { $w_bou = "下着<>DN"; $w_bdef=0; $w_btai="∞"; }

                $feel   += 1 + int(rand(3));
                $w_feel -= 1;

                if (($w_item[5] =~ /<>AH/) && ($w_hit <= 0)) {
                    ($w_in_a,$w_ik_a) = split(/<>/, $w_item[5]);
                    $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）の$w_in_aが壊れた！</b></font><br>") ;
                    $kega3 = ($kega3 . " <font color=\"red\">$w_in_a破壊！</font>") ;
                    if($w_in_a eq "戦乙女の祝福") { $w_hit = int($w_mhit * 0.2); }
                    elsif($w_in_a eq "死返玉") { $w_hit = int($w_mhit * 0.2); }
                    else { $w_hit = 1; }
                    $w_item[5] = "なし"; $w_eff[5] = 0; $w_itai[5] = 0;
                }

                if ($w_hit <=0) {   #死亡？
                    &DEATH2;
                } else {    #逃亡
                    $log = ($log . "$l_name は 逃げ切った・・・。<br>") ;
                }
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result 被:$result2 <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
                $wep = $wep_2; $watt = $watt_2; $wtai = $wtai_2; $w_inf = $w_inf_2 ;

                &EXPPLUS_PC;

                if (($w_kind =~ /N|S/) && (int(rand(6)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_nameが刃こぼれした</b></font>！<br>") ;
                    if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
                } elsif (($w_kind =~ /B/) && (int(rand(7)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_nameにひびが入った</b></font>！<br>") ;
                    if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
                } elsif (($w_kind =~ /P/) && ($w_name ne "素手") && (int(rand(6)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_nameがすり減った</b></font>！<br>") ;
                    if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
                } elsif (($w_kind =~ /C/) && ($wtai eq "∞") && (int(rand(7)) == 0)) {
                    $watt--; if (int(rand(4)) == 0) { $watt--; }
                    $log = ($log . "<font color=\"red\"><b>$w_nameが損耗した</b></font>！<br>") ;
                    if ($watt <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
                }
            } else {
                $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result 被:$result2 <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 </b></font><br>") ;
                $log = ($log . "しかし、避けられた！<br>") ;
                $feel   -= 1 + int (rand(2));
                $w_feel += 1 + int (rand(3));
            }

            if (($w_kind =~ /G|A/) && ($wtai > 0)) {    #銃・射？
                $wtai--; if ($wtai <= 0) { $wtai = 0 ; }
            } elsif (($w_kind =~ /C|D/) && ($wtai ne "∞")) {
                $wtai--; if ($wtai <= 0) { $wep ="素手<>WP"; $watt=0; $wtai="∞"; }
            }
        } else {
            $log = ($log . "$l_name は 反撃できない！<br>") ;
            $log = ($log . "$l_name は 逃げ切った・・・。<br>") ;
            $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
        }
    } else {    #逃亡
        $log = ($log . "$l_name は 逃げ切った・・・。<br>") ;
        $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘：$f_name $l_name（$cl $sex$no番） 攻:$result <font color=\"#00ffff\">Exp:$getexp</font> $hakaiinf2 $kega3 </b></font><br>") ;
    }

    if (($w_kind2 =~ /G|A/) && ($w_wtai > 0)) { #銃・射？
        $w_wtai--; if ($w_wtai <= 0) {$w_wtai = 0 ;}
    } elsif (($w_kind2 =~ /C|D/) && ($w_wtai ne "∞")) {
        $w_wtai--; if ($w_wtai <= 0) { $w_wep ="素手<>WP"; $w_watt=0; $w_wtai="∞"; }
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
# ■ 武器種別処理  #
#==================#
sub WEPTREAT {

    local($wname)   = @_[0] ;   #武器
    local($wkind)   = @_[1] ;   #武器
    local($wwtai)   = @_[2] ;   #残数
    local($pn)      = @_[3] ;   #攻撃者名
    local($nn)      = @_[4] ;   #防御者名
    local($ind)     = @_[5] ;   #攻撃種別（攻撃/反撃)
    local($attman)  = @_[6] ;   #攻撃者（PC/NPC)

    local($dice3) = int(rand(100)) ;
    local($dice4) = int(rand(4)) ;
    local($dice5) = int(rand(100)) ;

    local($kega)    = 0 ;
    local($kegainf) = "" ;
    local($k_work) = "" ;
    local($hakai) =  0 ;

    if ((($wkind =~ /B/) || (($wkind =~ /G|A/) && ($wwtai == 0))) && ($wname ne "素手")) { #棍棒 or 弾無し銃 or 矢無し弓
        $log = ($log . "$pnの$ind！$wname で $nnに殴りかかった！") ;
        if ($attman eq "PC") {$wb++;$wk=$wb;} else {$w_wb++;$wk=$w_wb;}
        $kega = 15 ;$kegainf = "頭腕腹足" ; #怪我率、怪我個所
        $hakai = 3 ;    #破壊率
    } elsif ($wkind =~ /A/) {   #弓系？
        $log = ($log . "$pnの$ind！$wname を $nn目掛けて射た！") ;
        if ($attman eq "PC") {$wa++;$wk=$wa;} else {$w_wa++;$wk=$w_wa;}
        $kega = 25 ; $kegainf = "頭腕腹足" ;    #怪我率、怪我個所
        $hakai = 2 ;    #破壊率
    } elsif ($wkind =~ /C/) { #投系
        $log = ($log . "$pnの$ind！$wname を $nnに投げつけた！") ;
        if ($attman eq "PC") {$wc++;$wk=$wc;} else {$w_wc++;$wk=$w_wc;}
        $kega = 15 ;$kegainf = "頭腕腹足" ; #怪我率、怪我個所
        $hakai = 0 ; if ($wwtai eq "∞") { $hakai = 3; } #破壊率
        
    } elsif ($wkind =~ /D/) { #爆系
        $log = ($log . "$pnの$ind！$wname を $nnに投げつけた！") ;
        if ($attman eq "PC") {$wd++;$wk=$wd;$ps=$pls;} else {$w_wd++;$wk=$w_wd;$ps=$w_pls;}
        $kega = 30 ;$kegainf = "頭腕腹足" ; #怪我率、怪我個所
        $hakai = 0 ;    #破壊率
        open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
        $gunlog[3] = "$now,$place[$ps],$id,$w_id,\n";
        open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    } elsif ($wkind =~ /G/) { #銃系
        $log = ($log . "$pnの$ind！$wname を $nn目掛けて発砲した！") ;
        if ($attman eq "PC") {$wg++;$wk=$wg;$ps=$pls;} else {$w_wg++;$wk=$w_wg;$ps=$w_pls;}
        $kega = 25 ; $kegainf = "頭腕腹足" ;    #怪我率、怪我個所
        $hakai = 2 ;    #破壊率
        open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
        $gunlog[0] = "$now,$place[$ps],$id,$w_id,\n";
        open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    } elsif ($wkind =~ /S/) { #刺系
        $log = ($log . "$pnの$ind！$wname で $nnを刺した！") ;
        if ($attman eq "PC") {$ws++;$wk=$ws;} else {$w_ws++;$wk=$w_ws;}
        $kega = 20 ; $kegainf = "頭腕腹足" ;    #怪我率、怪我個所
        $hakai = 3 ;    #破壊率
    } elsif ($wkind =~ /N/) { #斬系
        $log = ($log . "$pnの$ind！$wname で $nnに斬りつけた！") ;
        if ($attman eq "PC") {$wn++;$wk=$wn;} else {$w_wn++;$wk=$w_wn;}
        $kega = 20 ; $kegainf = "頭腕腹足" ;    #怪我率、怪我個所
        $hakai = 3 ;    #破壊率
    } elsif ($wkind =~ /P/) { #殴系
        $log = ($log . "$pnの$ind！$wname で $nnを殴った！") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 10 ; $kegainf = "頭腕腹足" ; #怪我率、怪我個所
        if ($wname eq "素手") { $hakai = 0; } else { $hakai = 3; }   #破壊率
    } else { #その他
        $log = ($log . "$pnの$ind！$wname で $nnを殴った！") ;
        if ($attman eq "PC") {$wp++;$wk=$wp;} else {$w_wp++;$wk=$w_wp;}
        $kega = 0 ; $kegainf = "頭腕腹足" ; #怪我率、怪我個所
        $hakai = 0 ;    #破壊率
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

    # 武器破壊
    if ($dice5 < $hakai) {  #破壊？
        if ($attman eq "PC") {  #PC
            $wep_2 = "素手<>WP"; $watt_2 = 0 ; $wtai_2 = "∞" ;
            $hakaiinf3 = "武器損傷！" ;
        } else {
            $w_wep_2 = "素手<>WP"; $w_watt_2 = 0 ; $w_wtai_2 = "∞" ;
            $hakaiinf2 = "武器損傷！" ;
        }
    } else {
        $hakaiinf2 = "" ;
        $hakaiinf3 = "" ;
    }

    # 怪我処理
    if ($dice3 < $kega) {
        if (($dice4 == 0) && ($kegainf =~ /頭/)) {  #頭
            $k_work =  "頭" ;
        } elsif (($dice4 == 1) && ($kegainf =~ /腕/)) { #腕
            $k_work =  "腕" ;
        } elsif (($dice4 == 2) && ($kegainf =~ /腹/)) { #腹
            $k_work =  "腹" ;
        } elsif (($dice4 == 3) && ($kegainf =~ /足/)) { #足
            $k_work =  "足" ;
        } else {
            return ;
        }

        if ($attman eq "PC") {  #PC
            if ((($w_item[5] =~ /AD/)||($w_bou =~ /<>DB/)) && ($k_work eq "腹")) {    #腹？
                if($w_item[5] =~ /AD/){
                    $w_itai[5] --; if ($w_itai[5] <= 0) {$w_item[5]="なし"; $w_eff[5]=$w_itai[5]=0;}
                }else{
                    $w_btai --; if ($w_btai <= 0) { $w_bou = "下着<>DN"; $w_bdef=0; $w_btai="∞"; }
                }
                return ;
            } elsif (($w_bou_h =~ /<>DH/) && ($k_work eq "頭")) {   #頭？
                $w_btai_h --; if ($w_btai_h <= 0) {$w_bou_h="なし"; $w_bdef_h=$w_btai_h=0;}
                return ;
            } elsif (($w_bou_f =~ /<>DF/) && ($k_work eq "足")) {   #足？
                $w_btai_f --; if ($w_btai_f <= 0) {$w_bou_f="なし"; $w_bdef_f=$w_btai_f=0;}
                return ;
            } elsif (($w_bou_a =~ /<>DA/) && ($k_work eq "腕")) {   #腕？
                $w_btai_a --; if ($w_btai_a <= 0) {$w_bou_a="なし"; $w_bdef_a=$w_btai_a=0;}
                return ;
            } else {
                $kega3 = ($k_work . "部負傷");
                $w_inf_2 =~ s/$k_work//g ;
                $w_inf_2 = ($w_inf_2 . $k_work) ;
            }
        } else {
            if ((($item[5] =~ /AD/)||($bou =~ /<>DB/)) && ($k_work eq "腹")) {    #腹？
                if($item[5] =~ /AD/){
                    $itai[5] --; if ($itai[5] <= 0) {$item[5]="なし"; $eff[5]=$itai[5]=0;}
                }else{
                    $btai --; if ($btai <= 0) { $bou = "下着<>DN"; $bdef=0; $btai="∞"; }
                }
                return ;
            } elsif (($bou_h =~ /<>DH/) && ($k_work eq "頭")) { #頭？
                $btai_h --; if ($btai_h <= 0) {$bou_h="なし"; $bdef_h=$btai_h=0;}
                return ;
            } elsif (($bou_f =~ /<>DF/) && ($k_work eq "足")) { #足？
                $btai_f --; if ($btai_f <= 0) {$bou_f="なし"; $bdef_f=$btai_f=0;}
                return ;
            } elsif (($bou_a =~ /<>DA/) && ($k_work eq "腕")) { #腕？
                $btai_a --; if ($btai_a <= 0) {$bou_a="なし"; $bdef_a=$btai_a=0;}
                return ;
            } else {
                $kega2 = ($k_work . "部負傷");
                $inf_2 =~ s/$k_work//g ;
                $inf_2 = ($inf_2 . $k_work) ;
            }
        }
    }


}
#==================#
# ■ 自分死亡処理  #
#==================#
sub DEATH {

    $hit = 0;$w_kill++;
    $mem--;

    $com = int(rand(6)) ;

    $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
    if ($w_msg ne "") {
        $log = ($log . "<font color=\"lime\"><b>$w_f_name $w_l_name『$w_msg』</b></font><br>") ;
    }
    $w_log = ($w_log . "<font color=\"yellow\"><b>$hour:$min:$sec $f_name $l_name（$cl $sex$no番）と戦闘を行い、殺害した。【残り$mem人】</b></font><br>") ;

    $w_feel += int (rand(5)) + 18;

    local($b_limit) = ($battle_limit * 3) + 1;

    if (($mem == 1) && ($w_sts ne "NPC0") && ($ar > $b_limit)){$w_inf = ($w_inf . "勝") ;}

    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
    $gunlog[1] = "$now,$place[$pls],$id,$w_id,\n";
    open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);

    #死亡ログ
    &LOGSAVE("DEATH2") ;
    $death = $deth ;
}
#================#
# ■ 敵死亡処理  #
#================#
sub DEATH2 {

    $w_hit = 0;$kill++;
    $wf = $w_id; #ブラウザバック対処
    if (($w_cl ne "$BOSS")&&($w_cl ne "$ZAKO")){ $mem--; }

    $w_com = int(rand(6)) ;
    $log = ($log . "<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）を殺害した。【残り$mem人】</b></font><br>") ;

    if (length($w_dmes) > 1) {
        $log = ($log . "<font color=\"yellow\"><b>$w_f_name $w_l_name『$w_dmes』</b></font><br>") ;
    }
    if (length($msg) > 1) {
        $log = ($log . "<font color=\"lime\"><b>$f_name $l_name『$msg』</b></font><br>") ;
    }

    $feel += int (rand(5)) + 18;

    local($b_limit) = ($battle_limit * 3) + 1;
    if (($mem == 1)&& ($ar > $b_limit)) {$inf = ($inf . "勝") ;}

    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
    $gunlog[1] = "$now,$place[$pls],$id,$w_id,\n";
    open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);

    #死亡ログ
    &LOGSAVE("DEATH3") ;

    $Command = "BATTLE2" ;
    $w_death = $deth ;
    $w_bid = "";

}
#================#
# ■ 戦闘結果処理#
#================#
sub BATTLE {

    $cln = "$cl（$sex$no番）" ;
    local($hpper)=$hit/$mhit;
    local($wep_n,$n)=split(/<>/, $wep);
    local($bou_n,$n)=split(/<>/, $bou);

    $w_cln = "$w_cl（$w_sex$w_no番）" ;
    local($w_hpper)=$w_hit/$w_mhit;
    local($w_wep_n,$n)=split(/<>/, $w_wep);
    local($w_bou_n,$n)=split(/<>/, $w_bou);

    if($hit <= 0) {
        $hpper="<font color=\"red\">死亡</font>";
    }elsif($hpper < 0.2) {
        $hpper="<font color=\"red\">瀕死</font>";
    }elsif($hpper < 0.5) {
        $hpper="<font color=\"orange\">重傷</font>";
    }elsif($hpper < 0.8) {
        $hpper="<font color=\"yellow\">軽傷</font>";
    }else{
        $hpper="<font color=\"lime\">正常</font>";
    }
    if($w_hit <= 0) {
        $w_hpper="<font color=\"red\">死亡</font>";
    }elsif($w_club eq "演劇部") {
        $w_hpper="<b>状態不明</b>";
    }elsif($w_hpper < 0.2) {
        $w_hpper="<font color=\"red\">瀕死</font>";
    }elsif($w_hpper < 0.5) {
        $w_hpper="<font color=\"orange\">重傷</font>";
    }elsif($w_hpper < 0.8) {
        $w_hpper="<font color=\"yellow\">軽傷</font>";
    }else{
        $w_hpper="<font color=\"lime\">正常</font>";
    }

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
    if($w_feel == 300) {
        $w_tension = "<font color=\"red\">超越</font>";
    }elsif($w_feel > 240) {
        $w_tension = "<font color=\"orange\">超強気</font>";
    }elsif($w_feel > 180) {
        $w_tension = "<font color=\"yellow\">強気</font>";
    }elsif($w_feel > 120) {
        $w_tension = "<font color=\"lime\">普通</font>";
    }elsif($w_feel > 60) {
        $w_tension = "<font color=\"aqua\">弱気</font>";
    }elsif($w_feel > 0) {
        $w_tension = "<font color=\"blue\">鬱</font>";
    }else{
        $w_tension = "<font color=\"fuchsia\">混乱</font>";
    }

    if ($a_name ne "") {
        $nickname = "（$a_name）";
    }
    if ($w_a_name ne "") {
        $w_nickname = "（$w_a_name）";
    }

print <<"_HERE_";
<TABLE width="600">
  <TBODY>
    <TR>
      <TD align="center" colspan="2"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">戦闘発生</FONT></B></TD>
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
                  <TD>ＶＳ</TD>
                  <TD>$w_f_name $w_l_name</TD>
                </TR>
                <TR align="center">
                  <TD>$nickname</TD>
                  <TD></TD>
                  <TD>$w_nickname</TD>
                </TR>
                <TR align="center">
                  <TD>$group</TD>
                  <TD><font color="yellow"><b>所属</b></font></TD>
                  <TD>$w_group</TD>
                </TR>
                <TR align="center">
                  <TD>$hpper</TD>
                  <TD><font color="yellow"><b>状態</b></font></TD>
                  <TD>$w_hpper</TD>
                </TR>
                <TR align="center">
                  <TD>$tension</TD>
                  <TD><font color="yellow"><b>テンション</b></font></TD>
                  <TD>$w_tension</TD>
                </TR>
                <TR align="center">
                  <TD>$kill人</TD>
                  <TD><font color="yellow"><b>殺害人数</b></font></TD>
                  <TD>$w_kill人</TD>
                </TR>
                <TR align="center">
                  <TD>$wep_n</TD>
                  <TD><font color="yellow"><b>武器</b></font></TD>
                  <TD>$w_wep_n</TD>
                </TR>
                <TR align="center">
                  <TD>$bou_n</TD>
                  <TD><font color="yellow"><b>体防具</b></font></TD>
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
          <TR><TH width="200">コマンド</TH>
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

$mflg="ON"; #ステータス非表示
}
#==================#
# ■ 逃亡処理      #
#==================#
sub RUNAWAY {

    $log = ($log . "$l_name は 全速力で逃げ出した・・・。<BR>") ;

    $Command = "MAIN";

}

#==================#
# ■ 防具種別処理  #
#==================#
sub DEFTREAT {

    local($wkind)   = @_[0] ;   #武器種別
    local($defman)   = @_[1] ;  #防御側(PC/NPC)

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

    if (($wkind eq "WG") && ($b_kind_i eq "ADB")) { #銃→防弾
        $pnt = $p_down ;
    } elsif (($wkind eq "WG") && ($b_kind_h eq "DH")) { #銃→頭
        $pnt = $p_up ;
    } elsif (($wkind eq "WN") && ($b_kind eq "DBK")) { #斬→鎖
        $pnt = $p_down ;
    } elsif (($wkind eq "WN") && ($b_kind_i eq "ADB")) { #斬→防弾
        $pnt = $p_up ;
    } elsif ((($wkind eq "WB")||($wkind eq "WGB")||($wkind eq "WAB")) && ($b_kind_h eq "DH")) { #殴→頭
        $pnt = $p_down ;
    } elsif ((($wkind eq "WB")||($wkind eq "WGB")||($wkind eq "WAB")) && ($b_kind =~ /DBA/)) { #殴→鎧
        $pnt = $p_up ;
    } elsif (($wkind eq "WS") && ($b_kind =~ /DBA/)) { #刺→鎧
        $pnt = $p_down ;
    } elsif (($wkind eq "WS") && ($b_kind =~ /DBK/)) { #刺→鎖
        $pnt = $p_up ;
    } else {
        $pnt = 1.0 ;
    }

}
#======================#
# ■ レベルアップ処理  #
#======================#
sub LVUPCHK {

    if (($exp >= ($level * $level) + ($level * $baseexp))&&($hit > 0)) { #レベルアップ
        $log = ($log . "レベルが上がった。<br>") ;
        $mhit += int(rand(3)+2) ; $att += int(rand(3)+2); $def += int(rand(3)+2); $level++;
    }
    if (($w_exp >= ($w_level * $w_level) + ($w_level * $baseexp)) && ($w_hit > 0)) { #レベルアップ
        $w_log = ($w_log . "レベルが上がった。<br>") ;
        $w_mhit += int(rand(3)+2) ; $w_att += int(rand(3)+2); $w_def += int(rand(3)+2); $w_level++;
    }

}

#======================#
# ■ 敵回復処理        #
#======================#
sub EN_KAIFUKU{ #敵回復処理
    $up = ($now - $w_endtime) / (1 * $kaifuku_time);
    if ($w_inf =~ /腹/) { $up = $up / 2; }
    if ($w_inf =~ /NPC/) { $up = $up / 2; }
    if ($w_sts eq "睡眠") {
        if ($w_club eq "サバイバル部") { $up = $up * 1.5; }
        $up = int($up);
        $w_sta += $up;
        if ($w_sta > $maxsta) { $w_sta = $maxsta; }
        $w_endtime = $now;
    } elsif ($w_sts eq "治療") {
        if ($kaifuku_rate == 0){$kaifuku_rate = 1;}
        if ($w_club eq "保健委員") { $up = $up * 1.5; }
        $up = int($up / $kaifuku_rate);
        $w_hit += $up;
        if ($w_hit > $w_mhit) { $w_hit = $w_mhit; }
        $w_endtime = $now;
        if ($pgday > 6) { $w_sts = "睡眠"; }
    }
}

#===========================#
# ■ 敵戦闘ログ自動削除処理 #
#===========================#
sub BLOG_CK{
    $log_len = length($w_log);
    if($log_len > 2000) {
        $w_log = "<font color=\"yellow\"><b>$hour:$min:$sec 戦闘ログは自動削除されました。</b></font><br>";
    }
}

#==================#
# ■ 必殺技 行動側 #
#==================#
sub SKILL_PC {
    #必殺技フェイズ
    local($s_dice) = rand(100);
    local($s_res) = 0;
    local($s_ren) = 0;
    local($s_nam) = "";

    if ($w_kind =~ /G/) {
        $s_ren = $wg;
        if ($s_ren > 80) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『咆吼』";
        }
    } elsif ($w_kind =~ /A/) {
        $s_ren = $wa;
        if ($s_ren > 80) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『疾風』";
        }
    } elsif ($w_kind =~ /C/) {
        $s_ren = $wc;
        if ($s_ren > 60) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『流星』";
        }
    } elsif ($w_kind =~ /D/) {
        $s_ren = $wd;
        if ($s_ren > 60) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『混沌』";
        }
    } elsif ($w_kind =~ /B/) {
        $s_ren = $wb;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『怒濤』";
        }
    } elsif ($w_kind =~ /N/) {
        $s_ren = $wn;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『残心』";
        }
    } elsif ($w_kind =~ /S/) {
        $s_ren = $ws;
        if ($s_ren > 100) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『閃光』";
        }
    } elsif ($w_kind =~ /P/) {
        $s_ren = $wp;
        if ($s_ren > 120) {
            $s_res = int(rand($s_ren) * 0.15);
            $s_nam = "戦技『連撃』";
        }
    }

    if (($s_res > 0) && ($s_ren > 0) && ($s_nam ne "")) {
        if ($s_dice < (($s_ren / 10) + $level + 10)) {
            $log = $log . "<font color=\"yellow\"><b>$s_nam発動！ $s_res の追加ダメージ</b></font>！<br>";
            $w_hit -= $s_res; $result = "$result+$s_res";
        }
    }
}

#=====================#
# ■ 経験値追加 PC 側 #
#=====================#
sub EXPPLUS_PC {
    $p_exp = int(($w_level - $level + 1) / 2); if ($p_exp <= 0) { $p_exp = 0; } 
    $p_exp++;
    $log = ($log . "$l_name は<font color=\"yellow\"><b> $p_exp </b></font>の経験値を得た。<br>") ;
    $exp += $p_exp;
}

#=====================#
# ■ 経験値追加 NPC側 #
#=====================#
sub EXPPLUS_NPC {
    $p_exp = int(($level - $w_level + 1) / 2); if ($p_exp <= 0) { $p_exp = 0; } 
    $p_exp++;
    $w_exp += $p_exp;
}

1;
