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
        if($item[$wk] =~ /<>H.*/){
            $item[$wk] =~ s/<>H.*/<>HD2/g;
        }else{ $item[$wk] =~ s/<>S.*/<>SD2/g; }
    } else {
        if($item[$wk] =~ /<>HH/){
            $item[$wk] =~ s/<>HH/<>HD/g;
        }else{ $item[$wk] =~ s/<>SH/<>SD/g; }
    }
    &SAVE ;
    $Command = "MAIN" ;
}
#==================#
# ■ 毒見処理      #
#==================#
sub PSCHECK {

    local($wk) = $Command;
    $wk =~ s/PSC_//g;
    if (($item[$wk] !~ /<>SH|<>HH|<>SD|<>HD/)||($club ne "料理研究部" )) {
        &ERROR("不正なアクセスです。");
    }
    
    local($in, $ik) = split(/<>/, $item[$wk]);
    if ($ik =~ /SH|HH/) {
        $log = ($log . "ん？ $in は 口にしても安全そうだ・・・。<br>") ;
    } else {
        $log = ($log . "ん？ $in には 毒物が混入してありそうだ・・・。<br>") ;
    }
    $sta -= $dokumi_sta ;
    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("com");
    }
    &SAVE ;
    $Command = "MAIN" ;
}

1
