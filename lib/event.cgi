#==================#
# ■ イベント処理  #
#==================#
sub EVENT {

    local($dice) = int(rand(5)) ;
    local($dice2) = int(rand(5)+5) ;
    $Command = "MAIN";
    if ($dice < 2) {return ; }


    if ($pls == 0) {    #分校




    } elsif ($pls == 1) {   #北の岬


    } elsif ($pls == 2) {   #鎌石村住宅街
        $log = ($log . "ふと、空を見上げると、烏の群れだ！<BR>") ;
        if ($dice == 2) {
            $log = ($log . "烏に襲われ、頭を負傷した！<BR>") ;
            $inf =~ s/頭//g ;
            $inf = ($inf . "頭") ;
        } elsif ($dice == 3) {
            $log = ($log . "烏に襲われ、<font color=\"red\"><b>$dice2ダメージ</b></font> を受けた！<BR>") ;
            $hit-=$dice2;
            if ($hit <= 0) {
                $hit = $mhit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;

                #死亡ログ
                &LOGSAVE("DEATH") ;
                $Command = "EVENT";
            }
        } else {
        $log = ($log . "ふぅ、なんとか撃退した・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 3) {   #鎌石村役場
    } elsif ($pls == 4) {   #郵便局
    } elsif ($pls == 5) {   #消防署
    } elsif ($pls == 6) {   #観音堂
    } elsif ($pls == 7) {   #高原池
    } elsif ($pls == 8) {   #菅原神社
    } elsif ($pls == 9) {   #ホテル跡
    } elsif ($pls == 10) {  #山岳地帯
        $log = ($log . "しまった、土砂崩れだ！<BR>") ;
        if ($dice == 2) {
            $log = ($log . "何とかかわしたが、落石で足を負傷した！<BR>") ;
            $inf =~ s/足//g ;
            $inf = ($inf . "足") ;
        } elsif ($dice == 3) {
            $log = ($log . "落石により、<font color=\"red\"><b>$dice2ダメージ</b></font> を受けた！<BR>") ;
            $hit-=$dice2;
            if ($hit <= 0) {
                $hit = $mhit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;

                #死亡ログ
                &LOGSAVE("DEATH") ;
                $Command = "EVENT";
            }
        } else {
            $log = ($log . "ふぅ、なんとかかわした・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 11) {  #トンネル
    } elsif ($pls == 12) {  #平瀬村住宅街
        $log = ($log . "ふと、空を見上げると、烏の群れだ！<BR>") ;
        if ($dice == 2) {
            $log = ($log . "烏に襲われ、頭を負傷した！<BR>") ;
            $inf =~ s/頭//g ;
            $inf = ($inf . "頭") ;
        } elsif ($dice == 3) {
            $log = ($log . "烏に襲われ、<font color=\"red\"><b>$dice2ダメージ</b></font> を受けた！<BR>") ;
            $hit-=$dice2;
            if ($hit <= 0) {
                $hit = $mhit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;

                #死亡ログ
                &LOGSAVE("DEATH") ;
                $Command = "EVENT";
            }
        } else {
            $log = ($log . "ふぅ、なんとか撃退した・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 13) {  #無学寺
    } elsif ($pls == 14) {  #分校跡
    } elsif ($pls == 15) {  #鷹野神社
    } elsif ($pls == 16) {  #森林地帯
        $log = ($log . "突如、野犬が襲い掛かってきた！<BR>") ;
        if ($dice == 2) {
            $log = ($log . "腕をかまれ、腕を負傷した！<BR>") ;
            $inf =~ s/腕//g ;
            $inf = ($inf . "腕") ;
        } elsif ($dice == 3) {
            $log = ($log . "野犬に襲われ、<font color=\"red\"><b>$dice2ダメージ</b></font> を受けた！<BR>") ;
            $hit-=$dice2;
            if ($hit <= 0) {
                $hit = $mhit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;

                #死亡ログ
                &LOGSAVE("DEATH") ;
                $Command = "EVENT";
            }
        } else {
            $log = ($log . "ふぅ、なんとか撃退した・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 17) {  #源五郎池
        $log = ($log . "しまった、足を滑らせた！<BR>") ;
        if ($dice <= 3) {
            $dice2 += 10;
            $log = ($log . "池の中に落下したが、なんとか這い上がった！<BR>スタミナを <font color=\"red\"><b>$dice2ポイント</b></font> 消費した！<BR>") ;
            $sta-=$dice2;
            if ($sta <= 0) {    #スタミナ切れ？
                &DRAIN("eve");
            }
        } else {
            $log = ($log . "ふぅ、なんと落ちずに済んだ・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 18) {  #氷川村住宅街
        $log = ($log . "ふと、空を見上げると、烏の群れだ！<BR>") ;
        if ($dice == 2) {
            $log = ($log . "烏に襲われ、頭を負傷した！<BR>") ;
            $inf =~ s/頭//g ;
            $inf = ($inf . "頭") ;
        } elsif ($dice == 3) {
            $log = ($log . "烏に襲われ、<font color=\"red\"><b>$dice2ダメージ</b></font> を受けた！<BR>") ;
            $hit-=$dice2;
            if ($hit <= 0) {
                $hit = $mhit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;

                #死亡ログ
                &LOGSAVE("DEATH") ;
                $Command = "EVENT";
            }
        } else {
            $log = ($log . "ふぅ、なんとか撃退した・・・。<BR>") ;
        }
        $chksts="OK";
    } elsif ($pls == 19) {  #診療所
    } elsif ($pls == 20) {  #灯台
    } elsif ($pls == 21) {  #南の岬
    }
}

1