#==================#
# ■ 毒物混入処理  #
#==================#
sub POISON {

    for ($i=0; $i<5; $i++) {
        if ($item[$i] =~ /毒薬/) {
            last ;
        }
    }
    local($wk) = $Command;
    $wk =~ s/POI_//g;
    if (($item[$wk] !~ /<>SH|<>HH|<>SD|<>HD/) || ($item[$i] !~ /毒薬/)) {
        &ERROR("不正なアクセスです。");
    }
    $itai[$i]--;
    if ($itai[$i] <= 0) {
        $item[$i] = "なし"; $eff[$i] = $itai[$i] = 0 ;
    }
    local($in, $ik) = split(/<>/, $item[$wk]);
    $log = ($log . "$inに毒物を混入した。自分で口にしないよう気をつけよう・・・。<br>") ;
    if ($club eq "料理研究部") {
        $item[$wk] =~ s/<>H.*/<>HD2/g;
        $item[$wk] =~ s/<>S.*/<>SD2/g;
    } else {
        $item[$wk] =~ s/<>HH/<>HD/g;
        $item[$wk] =~ s/<>SH/<>SD/g;
    }
    &SAVE ;
    $Command = "MAIN" ;
}
#==================#
# ■ 毒中和処理    #
#==================#
sub ANTIPS {

    for ($i=0; $i<5; $i++) {
        if ($item[$i] =~ /毒中和剤/) {
            last ;
        }
    }
    local($wk) = $Command;
    $wk =~ s/ATPS_//g;
    if (($item[$wk] !~ /<>SH|<>HH|<>SD|<>HD/) || ($item[$i] !~ /毒中和剤/)) {
        &ERROR("不正なアクセスです。");
    }
    $itai[$i]--;
    if ($itai[$i] <= 0) {
        $item[$i] = "なし"; $eff[$i] = $itai[$i] = 0 ;
    }
    local($in, $ik) = split(/<>/, $item[$wk]);
    $log = ($log . "$inの毒を中和した。これで大丈夫だろう・・・。<br>") ;
    $item[$wk] =~ s/<>H.*/<>HH/g;
    $item[$wk] =~ s/<>S.*/<>SH/g;

    &SAVE ;
    $Command = "MAIN" ;
}
#==================#
# ■ 毒見処理      #
#==================#
sub PSCHECK {

    local($wk) = $Command;
    $wk =~ s/PSC_//g;
    if ($item[$wk] !~ /<>SH|<>HH|<>SD|<>HD/) {
        &ERROR("不正なアクセスです。");
    }

    local($in, $ik) = split(/<>/, $item[$wk]);
    if ($ik =~ /SH|HH/) {
        $log = ($log . "ん？ $in は 口にしても安全そうだ・・・。<br>") ;
    } else {
        $log = ($log . "ん？ $in には 毒物が混入してありそうだ・・・。<br>") ;
    }

    if ($club eq "料理研究部" ) {
        $sta -= int($dokumi_sta / 2);
    } else {
        $sta -= $dokumi_sta;
    }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("com");
    }

    &SAVE ;
    $Command = "MAIN" ;
}

1
