#==================#
# ■ アイテム取得  #
#==================#
sub ITEMGET {

    local($i) = 0 ;
    local($chkflg) = -1;
    local($sub) = "";

    local($filename) = "$LOG_DIR/$pls$item_file";


    open(DB,"$filename");seek(DB,0,0); @itemlist=<DB>;close(DB);

    if ($#itemlist < 0) {
        $log = ($log . "もう、このエリアには何も無いのかな・・・？<BR>") ;
        $chksts="OK";
        return ;
    } else {
        local($work) = int(rand($#itemlist)) ;
        local($getitem,$geteff,$gettai) = split(/,/, $itemlist[$work]) ;
        local($itname,$itkind) = split(/<>/, $getitem);
        local($delitem) = splice(@itemlist,$work,1) ;
        for ($i=0; $i<5; $i++) {
            if (($item[$i] eq "なし") || (($item[$i] eq $getitem) && ($getitem =~ /<>WC|<>TN|<>NR|弾丸|矢/))) {
                $chkflg = $i;last;
            }
        }

        if ($getitem =~ /<>TO/) { #罠
            open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);

            $result = int(rand($geteff/2)+($geteff/2));
            $log = ($log . "罠だ！仕掛けられていた $itname で傷をおい、<font color=\"red\"><b>$resultのダメージ</b></font>を受けた！。<BR>") ;
            $hit-=$result;
            if ($hit <= 0) {
                $hit = 0;
                $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
                #死亡ログ
                &LOGSAVE("DEATH") ;
                $mem--;
                if ($mem == 1) {&LOGSAVE("WINEND1") ;}
            }
            return ;
        }

        if ($chkflg == -1) { #所持品オーバー
            $log = ($log . "$itnameを発見した。しかし、これ以上カバンに入らない。<BR>$itnameをあきらめた・・・。<BR>") ;
            $Command = "MAIN";
        } else {
            open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);

            if($getitem =~ /<>HH|<>HD/) {
                $sub = "口にすれば体力が回復出来そうだな。";
            } elsif($getitem =~ /<>SH|<>SD/) {
                $sub = "口にすればスタミナが回復出来そうだな。";
            } elsif ($getitem =~ /<>W/) { #武器？
                $sub = "こいつは武器になりそうだな。";
            } elsif($getitem =~ /<>D/) { #防具
                $sub = "こいつは防具に出来そうだな。";
            } elsif($getitem =~ /<>A/) { #装飾
                $sub = "こいつは身に付けることが出来そうだな。";
            } elsif($getitem =~ /<>TN/) { #罠
                $sub = "これで罠を仕掛ける事が出来そうだな。";
            } else {
                $sub = "きっと何かに使えるだろう。";
            }

            ($itname,$kind) = split(/<>/, $getitem) ;
            $log = ($log . "$itnameを発見した。$sub<BR>") ;

            if ($item[$chkflg] eq "なし") {
                $item[$chkflg] = $getitem; $eff[$chkflg] = $geteff; $itai[$chkflg] = $gettai;
            }elsif ($item[$chkflg] =~ /弾丸|矢/) {
                $eff[$chkflg] += $geteff;
            } else {
                $itai[$chkflg] += $gettai ;
            }
        }
    }
    $chksts="OK";

}
#==================#
# ■ アイテム使用  #
#==================#
sub ITEM {

    local($result) = 0;
    local($wep2) = "" ;
    local($watt2) = 0;
    local($wtai2) = 0 ;
    local($up) = 0 ;

    local($wk) = $Command;
    $wk =~ s/ITEM_//g;

    if ($item[$wk] eq "なし") {
        &ERROR("不正なアクセスです。");
    }

    local($in, $ik) = split(/<>/, $item[$wk]);
    local($w_name,$w_kind) = split(/<>/, $wep);
    local($d_name,$d_kind) = split(/<>/, $bou);

    if ($item[$wk] =~ /<>SH/) { #スタミナ回復
        $log = ($log . "$inを使用した。<BR>スタミナが回復した<BR>");
        $sta += $eff[$wk] ;
        if ($sta > $maxsta) {$sta = $maxsta;}
        $itai[$wk] --;
        if ($itai[$wk] == 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ; }
    } elsif($item[$wk] =~ /<>HH/) { #体力回復
        $log = ($log . "$inを使用した。<BR>体力が回復した<BR>");
        $hit += $eff[$wk] ;
        if ($hit > $mhit) {$hit = $mhit;}
        $itai[$wk] --;
        if ($itai[$wk] == 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ; }
    } elsif($item[$wk] =~ /<>SD|<>HD/) {    #毒入り
        if ($item[$wk] =~ /<>SD2|<>HD2/) {  #料理研究部特製？
            $result = int($eff[$wk]*1.5) ;
        } else { $result = $eff[$wk] ; }
        $hit -= $result ;
        $log = ($log . "うっ・・・しまった！どうやら、毒物が混入されていたみたいだ！<font color=\"red\"><b>$resultダメージ</b></font>！<BR>\n") ;
        $itai[$wk] --;
        if ($itai[$wk] == 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ; }
        if ($hit <= 0) {
            $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>\n") ;
            $com = int(rand(6)) ;
            #死亡ログ
            &LOGSAVE("DEATH1") ;
            $mem--;
            if ($mem == 1) { &LOGSAVE("WINEND1"); }
            &SAVE;return;
        }
    } elsif(($item[$wk] =~ /<>W/) && ($item[$wk] !~ /<>WF/)) {  #武器装備
        $log = ($log . "$inを装備した。<BR>") ;
        $wep2 = $wep; $watt2 = $watt; $wtai2 = $wtai ;
        $wep = $item[$wk]; $watt = $eff[$wk]; $wtai = $itai[$wk] ;
        if ($wep2 !~ /素手/) {
            $item[$wk] = $wep2; $eff[$wk] = $watt2; $itai[$wk] = $wtai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DB/) { #防具装備（体）
        $log = ($log . "$inを体に装備した。<BR>");
        $bou2 = $bou; $bdef2 = $bdef; $btai2 = $btai ;
        $bou = $item[$wk]; $bdef = $eff[$wk]; $btai = $itai[$wk] ;
        if ($bou2 !~ /下着/) {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DH/) { #防具装備（頭）
        $log = ($log . "$inを頭に装備した。<BR>");
        $bou2 = $bou_h; $bdef2 = $bdef_h; $btai2 = $btai_h ;
        $bou_h = $item[$wk]; $bdef_h = $eff[$wk]; $btai_h = $itai[$wk] ;
        if ($bou2 !~ /なし/) {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DF/) { #防具装備（足）
        $log = ($log . "$inを足に装備した。<BR>");
        $bou2 = $bou_f; $bdef2 = $bdef_f; $btai2 = $btai_f ;
        $bou_f = $item[$wk]; $bdef_f = $eff[$wk]; $btai_f = $itai[$wk] ;
        if ($bou2 !~ /なし/) {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DA/) { #防具装備（腕）
        $log = ($log . "$inを腕に装備した。<BR>");
        $bou2 = $bou_a; $bdef2 = $bdef_a; $btai2 = $btai_a ;
        $bou_a = $item[$wk]; $bdef_a = $eff[$wk]; $btai_a = $itai[$wk] ;
        if ($bou2 !~ /なし/) {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>A/) {  #アクセサリ装備
        $log = ($log . "$inを身に付けた。<BR>");
        $bou2 = $item[5]; $bdef2 = $eff[5]; $btai2 = $itai[5] ;
        $item[5] = $item[$wk]; $eff[5] = $eff[$wk]; $itai[5] = $itai[$wk] ;
        if ($bou2 !~ /なし/) {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>R/) {  #レーダー
        &HEADER;
        require "$LIB_DIR/reader.cgi";
        &READER;
        &FOOTER;
    } elsif($item[$wk] =~ /<>TN/) { #罠
        $log = ($log . "$inを罠として仕掛けた。自分も注意しなきゃな・・・。<BR>");

        $item[$wk] =~ s/TN/TO/g ;

        $filename = "$LOG_DIR/$pls$item_file";

        open(DB,"$filename");seek(DB,0,0); @itemlist=<DB>;close(DB);
        push(@itemlist,"$item[$wk],$eff[$wk],$itai[$wk],\n") ;
        open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);
        $itai[$wk] -- ;
        $item[$wk] =~ s/TO/TN/g ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif((($in eq "砥石")||($in eq "布きれ")) && ($wep =~ /<>WN/)) { #砥石使用＆ナイフ系装備？
        $watt += $eff[$wk]; if ($watt > 30) { $watt = 30 ; }
        $log = ($log . "$inを使用した。$w_nameの攻撃力が $watt になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "裁縫道具") && ($d_kind eq "DBN") && ($d_name ne "下着")) { #裁縫道具＆服系装備？
        $btai += $eff[$wk]; if ($btai > 30) { $btai = 30 ; }
        $log = ($log . "$inを使用した。$d_nameの耐久力が $btai になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "弾丸") && ($wep =~ /<>WG/)) {  #弾丸使用＆銃系装備？
        $up = $eff[$wk] + $wtai;if ($up > 6) { $up = 6 - $wtai ; } else { $up = $eff[$wk]; }
        $wtai += $up ; $eff[$wk] -= $up ;
        if ($eff[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        if ($wep =~ /<>WGB/) { $wep =~ s/<>WGB/<>WG/g ; }
        $log = ($log . "$inを、$w_name に装填した。<BR>$w_nameの使用回数が $up 向上した。<BR>");
    } elsif(($in =~ /矢/) && ($wep =~ /<>WA/)) {    #矢使用＆弓系装備？
        $up = $eff[$wk] + $wtai;if ($up > 6) { $up = 6 - $wtai ; }else { $up = $eff[$wk]; }
        $wtai += $up ; $eff[$wk] -= $up ;
        if ($eff[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        if ($wep =~ /<>WAB/) { $wep =~ s/<>WAB/<>WA/g ; }
        $log = ($log . "$inを使用し、$w_nameを補充した。<BR>$w_nameの使用回数が $up 向上した。<BR>");
    } elsif($in =~ /バッテリ/){
        my($pc_ck) = 0;
        for ($paso=0; $paso<5; $paso++){
            if (($item[$paso] eq "モバイルPC<>Y")&&($itai[$paso] < 5)){
                $itai[$paso] += $eff[$wk];
                if($itai[$paso] > 5){ $itai[$paso] = 5; }
                $itai[$wk] -- ;
                if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
                $log = ($log . "$in で モバイルPC を充電した。モバイルPC の使用回数が $itai[$paso] になった。<BR>");
                $pc_ck = 1;
                last;
            }
        }
        if ($pc_ck == 0){
            $log = ($log . "こいつは何に使うんだろう・・・。<BR>");$Command="MAIN";
        }
    } elsif($in eq "プログラム解除キー") {
        if ($pls == 0){
            $inf = ($inf . "解");
            open(FLAG,">$end_flag_file"); print(FLAG "解除終了\n"); close(FLAG);
            &LOGSAVE("EX_END");
            $log = ($log . "解除キーを使ってプログラムを停止した。<br>首輪が外れた！<BR>");$Command="MAIN";
            &SAVE;
        }else{
            $log = ($log . "ここで使っても意味がない・・・。<BR>");$Command="MAIN";
        }
    } else {
        $log = ($log . "こいつは何に使うんだろう・・・。<BR>");$Command="MAIN";
    }

    $Command = "MAIN";

    &SAVE;

}

#==================#
# ■ アイテム投棄  #
#==================#
sub ITEMDEL {

    local($wk) = $Command;
    $wk =~ s/DEL_//g;

    if ($item[$wk] eq "なし") {
        &ERROR("不正なアクセスです。");
    }

    local($in, $ik) = split(/<>/, $item[$wk]);

    $log = ($log . "$inを捨てた。<br>") ;

    local($filename) = "$LOG_DIR/$pls$item_file";
    open(DB,"$filename");seek(DB,0,0); @itemlist=<DB>;close(DB);
    push(@itemlist,"$item[$wk],$eff[$wk],$itai[$wk],\n") ;
    open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);

    $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
    $Command = "MAIN";

    &SAVE;

}
#==================#
# ■ 装備武器外す処理  #
#==================#
sub WEPDEL {

    local($j) = 0 ;

    if ($wep =~ /素手/) {
        $log = ($log . "$l_nameは武器を装備していません。<br>") ;
        $Command = "MAIN" ;
        return ;
    }

    ($w_name,$w_kind) = split(/<>/, $wep);

    local($chk) = "NG" ;
    for ($j=0; $j<5; $j++) {
        if ($item[$j] eq "なし") {
            $chk = "ON" ; last;
        }
    }

    if ($chk eq "NG") {
        $log = ($log . "それ以上デイパックに入りません。<br>") ;
    } else {
        $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
        $item[$j] = $wep; $eff[$j] = $watt; $itai[$j] = $wtai ;
        $wep = "素手<>WP"; $watt = 0; $wtai = "∞" ;
        &SAVE ;
    }

    $Command = "MAIN" ;

}
#==================#
# ■ 装備武器投棄  #
#==================#
sub WEPDEL2 {

    if ($wep =~ /素手/) {
        $log = ($log . "$l_nameは武器を装備していません。<br>") ;
        $Command = "MAIN" ;
        return ;
    }

    local($in, $ik) = split(/<>/, $wep);

    $log = ($log . "$inを捨てた。<br>") ;

    local($filename) = "$LOG_DIR/$pls$item_file";
    open(DB,"$filename");seek(DB,0,0); @itemlist=<DB>;close(DB);
    push(@itemlist,"$wep,$watt,$wtai,\n") ;
    open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);

    $wep = "素手<>WP"; $watt = 0; $wtai = "∞" ;
    $Command = "MAIN";

    &SAVE;

}
1