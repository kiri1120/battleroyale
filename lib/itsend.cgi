#==================#
# ■ アイテム譲渡  #
#==================#
sub ITEMSEND {
    local($a,$z_id,$k) = split(/_/, $Command);
    local($b,$i) = split(/_/, $Command2);

    if ($item[$i] eq "なし") {
        &ERROR("不正なアクセスです。");
    }

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    if ($k<=$#userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$k]);
        if ($w_id eq $z_id) {
            local($z_chk)="NG";
        } else {
            &ERROR("不正なアクセスです。");
        }
    } else {
        &ERROR("不正なアクセスです。");
    }

    for ($j=0; $j<5; $j++) {
        if ($w_item[$j] eq "なし") {
            $z_chk = "OK" ; last;
        }
    }

    if($z_chk eq "OK") {
        $w_item[$j] = $item[$i]; $w_eff[$j] = $eff[$i]; $w_itai[$j] = $itai[$i];
        $item[$i] = "なし"; $eff[$i] = 0; $itai[$i] = 0;
        local($in, $ik) = split(/<>/, $w_item[$j]);
        if($speech ne "") { $speech = "<BR>『$speech』"; }
        $log = ($log . "$w_f_name $w_l_name（$w_cl $w_sex$w_no番）に $in を譲渡しました。<br>\n") ;
        $w_log = ($w_log . "<font color=\"lime\"><b>$hour:$min:$sec　$f_name $l_name（$cl $sex$no番）から $in をもらいました。$speech</b></font><br>") ;
        $Index2 = $k;
        &SAVE2;
        # 譲渡用ログ作成
        if ($w_item[$j] =~ /<>W/) { $z_kind = "武器"; }
        elsif ($w_item[$j] =~ /<>D|<>A/) { $z_kind = "防具"; }
        elsif ($w_item[$j] =~ /<>H|<>S/) { $z_kind = "回復アイテム"; }
        else { $z_kind = "その他"; }
        open(DB,"$joutolog_file"); seek(DB,0,0); @loglist=<DB>; close(DB);
        unshift(@loglist,"$now,$f_name,$l_name,$sex,$cl,$no,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,JOUTO,$in,$ik,$z_kind,$host,$w_host,\n");
        open(DB,">$joutolog_file"); seek(DB,0,0); print DB @loglist; close(DB);
    } else {
        $log = ($log . "相手のデイパックがいっぱいです。<br>\n") ;
    }

    &SAVE;
    $Command = "MAIN";
}
1
