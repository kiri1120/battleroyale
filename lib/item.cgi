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
            if ($item[$i] eq "なし") {
                $chkflg = $i;last;
            } elsif (($item[$i] eq $getitem) && ($getitem =~ /<>TN|弾丸|矢/)) {
                $chkflg = $i;last;
            } elsif (($item[$i] eq $getitem) && ($getitem =~ /<>WC|<>WD/) && ($itai[$i] ne "∞")) {
                $chkflg = $i;last;
            }
        }

        if ($getitem =~ /<>TO/) { #礬
            open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);

            $result = int(rand($geteff * 0.4)+($geteff * 0.8));
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
            } elsif($getitem =~ /<>TN/) { #礬
                $sub = "これで罠を仕掛ける事が出来そうだな。";
            } else {
                $sub = "きっと何かに使えるだろう。";
            }

            ($itname,$kind) = split(/<>/, $getitem) ;
            $log = ($log . "$itnameを発見した。$sub<BR>") ;

            if ($item[$chkflg] eq "なし") {
                $item[$chkflg] = $getitem; $eff[$chkflg] = $geteff; $itai[$chkflg] = $gettai;
            } elsif ($item[$chkflg] =~ /弾丸|矢/) {
                $eff[$chkflg] += $geteff;
            } else {
                if ($item[$chkflg] =~ /<>WC|<>WD/) {
                    $eff[$chkflg] = int(($eff[$chkflg]*$itai[$chkflg] + $geteff*$gettai) / ($itai[$chkflg]+$gettai));
                }
                $itai[$chkflg] += $gettai;
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
    local($d_name_h,$d_kind_h) = split(/<>/, $bou_h);
    local($d_name_a,$d_kind_a) = split(/<>/, $bou_a);
    local($d_name_f,$d_kind_f) = split(/<>/, $bou_f);

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
            $result = int($eff[$wk]*1.5);
        } else {
            $result = $eff[$wk];
        }
        $hit -= $result ;
        $inf =~ s/毒//g ;
        $inf = ($inf . "毒") ;
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
    } elsif ($item[$wk] =~ /<>W/) {  #武器装備
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        if (($in eq "バンテージ") && ($w_name eq "バンテージ")) {
            $watt += $eff[$wk]; if ($watt > 25) { $watt = 25 ; }
            $log = ($log . "$inを重ねて巻いた。$w_nameの攻撃力が $watt になった。<BR>");
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        } else {
            $log = ($log . "$inを装備した。<BR>") ;
            $wep2 = $wep; $watt2 = $watt; $wtai2 = $wtai ;
            $wep = $item[$wk]; $watt = $eff[$wk]; $wtai = $itai[$wk] ;
            if ($wep2 !~ /素手/) {
                $item[$wk] = $wep2; $eff[$wk] = $watt2; $itai[$wk] = $wtai2 ;
            } else {
                $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
            }
        }
    } elsif ($item[$wk] =~ /<>DB/) { #防具装備（体）
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        $log = ($log . "$inを体に装備した。<BR>");
        $bou2 = $bou; $bdef2 = $bdef; $btai2 = $btai ;
        $bou = $item[$wk]; $bdef = $eff[$wk]; $btai = $itai[$wk] ;
        if ($bou2 ne "下着<>DN") {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DH/) { #防具装備（頭）
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        $log = ($log . "$inを頭に装備した。<BR>");
        $bou2 = $bou_h; $bdef2 = $bdef_h; $btai2 = $btai_h ;
        $bou_h = $item[$wk]; $bdef_h = $eff[$wk]; $btai_h = $itai[$wk] ;
        if ($bou2 ne "なし") {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DF/) { #防具装備（足）
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        $log = ($log . "$inを足に装備した。<BR>");
        $bou2 = $bou_f; $bdef2 = $bdef_f; $btai2 = $btai_f ;
        $bou_f = $item[$wk]; $bdef_f = $eff[$wk]; $btai_f = $itai[$wk] ;
        if ($bou2 ne "なし") {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>DA/) { #防具装備（腕）
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        $log = ($log . "$inを腕に装備した。<BR>");
        $bou2 = $bou_a; $bdef2 = $bdef_a; $btai2 = $btai_a ;
        $bou_a = $item[$wk]; $bdef_a = $eff[$wk]; $btai_a = $itai[$wk] ;
        if ($bou2 ne "なし") {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>A/) {  #アクセサリ装備
        if ($ik =~ /狂/) {
            $inf =~ s/狂//g ;
            $inf = ($inf . "狂") ;
        }
        $log = ($log . "$inを身に付けた。<BR>");
        $bou2 = $item[5]; $bdef2 = $eff[5]; $btai2 = $itai[5] ;
        $item[5] = $item[$wk]; $eff[5] = $eff[$wk]; $itai[5] = $itai[$wk] ;
        if ($bou2 ne "なし") {
            $item[$wk] = $bou2; $eff[$wk] = $bdef2; $itai[$wk] = $btai2 ;
        } else {
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }
    } elsif($item[$wk] =~ /<>R/) {  #レーダー
        $log = ($log . "レーダーを使用した。<BR><BR>数字：エリアにいる人数<BR>赤数字：自分がいるエリアの人数");
        &HEADER;
        require "$LIB_DIR/reader.cgi";
        &READER;
        &FOOTER;
    } elsif($item[$wk] =~ /<>TN/) { #礬
        $log = ($log . "$inを罠として仕掛けた。自分も注意しなきゃな・・・。<BR>");

        $item[$wk] =~ s/TN/TO/g ;

        $filename = "$LOG_DIR/$pls$item_file";

        open(DB,"$filename");seek(DB,0,0); @itemlist=<DB>;close(DB);
        push(@itemlist,"$item[$wk],$eff[$wk],$itai[$wk],\n") ;
        open(DB,">$filename"); seek(DB,0,0); print DB @itemlist; close(DB);
        $itai[$wk] -- ;
        $item[$wk] =~ s/TO/TN/g ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "砥石") && ($w_kind =~ /N|S/)) { #砥石使用＆斬or刺系装備？
        if($wep =~ /毒塗り/) {
            $watt -= 10 - $eff[$wk]; if ($watt > 30) { $watt = 30 ; }
            $wep =~ s/毒塗り//g;
            $log = ($log . "しまった！$inで毒を落としてしまった！$w_nameの攻撃力が $watt になった・・・。<BR>");
        } else {
            $watt += $eff[$wk]; if ($watt > 30) { $watt = 30 ; }
            $log = ($log . "$inを使用した。$w_nameの攻撃力が $watt になった。<BR>");
        }
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "毒薬") && ($w_kind =~ /N|S/)) { #毒薬使用＆斬系or刺系装備？
        $watt += $eff[$wk]; if ($watt > 40) { $watt = 40 ; }
        if($wep !~ /毒/) { $wep = ("毒塗り" . $wep); }
        $log = ($log . "$inを使用した。$w_nameの攻撃力が $watt になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "釘") && ($w_kind =~ /B/) && ($w_kind !~ /G|A/)) { #釘使用＆棍系装備？
        $watt += $eff[$wk]; if ($watt > 30) { $watt = 30 ; }
        if($wep !~ /釘/) { $wep = ("釘付き" . $wep); }
        $log = ($log . "$inを使用した。$w_nameの攻撃力が $watt になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif (($in eq "修繕道具[体]") && ($d_name ne "下着")) { #体防具装備？
        $btai += $eff[$wk]; if ($btai > 30) { $btai = 30 ; }
        $log = ($log . "$inを使用した。$d_nameの耐久力が $btai になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif (($in eq "修繕道具[頭]") && ($d_name_h ne "なし")) { #頭防具装備？
        $btai_h += $eff[$wk]; if ($btai_h > 20) { $btai_h = 20 ; }
        $log = ($log . "$inを使用した。$dh_nameの耐久力が $btai_h になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif (($in eq "修繕道具[腕]") && ($d_name_a ne "なし")) { #腕防具装備？
        $btai_a += $eff[$wk]; if ($btai_a > 20) { $btai_a = 20 ; }
        $log = ($log . "$inを使用した。$da_nameの耐久力が $btai_a になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif (($in eq "修繕道具[足]") && ($d_name_f ne "なし")) { #足防具装備？
        $btai_f += $eff[$wk]; if ($btai_f > 20) { $btai_f = 20 ; }
        $log = ($log . "$inを使用した。$df_nameの耐久力が $btai_f になった。<BR>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
    } elsif(($in eq "弾丸") && ($wep =~ /<>WG/)) {  #弾丸使用＆銃系装備？
        $up = $eff[$wk] + $wtai;if ($up > 12) { $up = 12 - $wtai ; } else { $up = $eff[$wk]; }
        $wtai += $up ; $eff[$wk] -= $up ;
        if ($eff[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        $log = ($log . "$inを、$w_name に装填した。<BR>$w_nameの使用回数が $up 向上した。<BR>");
    } elsif(($in eq "矢") && ($wep =~ /<>WA/)) {    #矢使用＆弓系装備？
        $up = $eff[$wk] + $wtai;if ($up > 12) { $up = 12 - $wtai ; }else { $up = $eff[$wk]; }
        $wtai += $up ; $eff[$wk] -= $up ;
        if ($eff[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        $log = ($log . "$inを、$w_name を補充した。<BR>$w_nameの使用回数が $up 向上した。<BR>");
    } elsif($in eq "バッテリ"){
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
    } elsif($in eq "狂気の魂") {
        $inf =~ s/狂//g ;
        $inf = ($inf . "狂") ;
        $log = ($log . "狂気が満ちてゆく・・・<BR><br><font color=\"red\"><b>──スベテ、壊シテシマエ。</b></font><br><br>$l_nameは狂気に侵された。<br>");
        $itai[$wk] -- ;
        if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
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
    } elsif($in eq "携帯電話") {	#携帯電話使用
        $log = ($log . "携帯電話で自宅に電話した。<BR>「ルルルルル・・・ガチャ、もしもし・・・<BR>$f_nameか？言っておくが、携帯はつかえないぞー、$f_name。」<BR>新担任が電話にでた・・・。<BR>\n");
    } elsif($in eq "御神籤") {    #御神籤使用
        $log = ($log . "御神籤か・・・開いてみよう。<BR>\n");
        local($dice) = int(rand(10)) ;
        if ($dice < 5) {
            $log = ($log . "吉だ！<BR>攻撃力・防御力が上がった！<br>\n");
            $att += int(rand(2) + 1) ; $def += int(rand(2) + 1) ;
        } elsif ($dice < 8) {
            $log = ($log . "凶だ！<BR>攻撃力・防御力が下がった・・・。<br>\n");
            $att -= int(rand(2) + 1) ; $def -= int(rand(2) + 1) ;
        } else {
            $log = ($log . "大吉だ！<BR>攻撃力・防御力・最大体力が上がった！！<br>\n");
            $mhit += int(rand(3)+3) ; $att += int(rand(3)+1); $def += int(rand(3)+1);
        }
        $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
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

    foreach (0 .. $#IDEL) {
        $wk = $IDEL[$_];
        if ($item[$wk] eq "なし") {
            &ERROR("不正なアクセスです。");
        }

        local($in, $ik) = split(/<>/, $item[$wk]);

        $log = ($log . "$inを捨てた。<br>") ;

        local($filename) = "$LOG_DIR/$pls$item_file";
        $delitem = "$item[$wk],$eff[$wk],$itai[$wk],\n";
        open(DB,">>$filename"); seek(DB,0,0); print DB $delitem; close(DB);

        $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
    }

    $Command = "MAIN";

    &SAVE;

}
#==================#
# ■ 装備品解除    #
#==================#
sub WEPKAI {

    local($wk) = $Command;
    $wk =~ s/WEPKAI2_//g;
    local($j) = 0 ;

    local($chk) = "NG" ;
    for ($j=0; $j<5; $j++) {
        if ($item[$j] eq "なし") {
            $chk = "ON" ; last;
        }
    }

    if ($chk eq "NG") {
        $log = ($log . "それ以上デイパックに入りません。<br>") ;
    } else {
        if ($wk eq "W") {
            if ($wep eq "素手<>WP") {
                $log = ($log . "$l_nameは武器を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $wep);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $wep; $eff[$j] = $watt; $itai[$j] = $wtai ;
            $wep = "素手<>WP"; $watt = 0; $wtai = "∞" ;
        } elsif ($wk eq "B") {
            if ($bou eq "下着<>DN") {
                $log = ($log . "$l_nameは体防具を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $bou);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $bou; $eff[$j] = $bdef; $itai[$j] = $btai ;
            $bou = "下着<>DN"; $bdef = 0; $btai = "∞" ;
        } elsif ($wk eq "H") {
            if ($bou_h eq "なし") {
                $log = ($log . "$l_nameは頭防具を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $bou_h);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $bou_h; $eff[$j] = $bdef_h; $itai[$j] = $btai_h ;
            $bou_h = "なし"; $bdef_h = 0; $btai_h = 0 ;
        } elsif ($wk eq "A") {
            if ($bou_a eq "なし") {
                $log = ($log . "$l_nameは腕防具を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $bou_a);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $bou_a; $eff[$j] = $bdef_a; $itai[$j] = $btai_a ;
            $bou_a = "なし"; $bdef_a = 0; $btai_a = 0 ;
        } elsif ($wk eq "F") {
            if ($bou_f eq "なし") {
                $log = ($log . "$l_nameは足防具を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $bou_f);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $bou_f; $eff[$j] = $bdef_f; $itai[$j] = $btai_f ;
            $bou_f = "なし"; $bdef_f = 0; $btai_f = 0 ;
        } elsif ($wk eq "I") {
            if ($item[5] eq "なし") {
                $log = ($log . "$l_nameは装飾品を装備していません。<br>") ;
                $Command = "MAIN" ;
                return ;
            }

            local($w_name,$w_kind) = split(/<>/, $item[5]);
            $log = ($log . "$w_nameをデイパックにしまいました。<br>") ;
            $item[$j] = $item[5]; $eff[$j] = $eff[5]; $itai[$j] = $itai[5] ;
            $item[5] = "なし"; $eff[5] = 0; $itai[5] = 0 ;
        }
        &SAVE ;
    }

    $Command = "MAIN" ;

}
#==================#
# ■ 装備品投棄    #
#==================#
sub WEPDEL {

    local($wk) = $Command;
    $wk =~ s/WEPDEL2_//g;
    local($in, $ik, $delitem);

    if ($wk eq "W") {
        if ($wep eq "素手<>WP") {
            $log = ($log . "$l_nameは武器を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $wep);
        $delitem = "$wep,$watt,$wtai,\n";
        $wep = "素手<>WP"; $watt = 0; $wtai = "∞" ;
    } elsif ($wk eq "B") {
        if ($bou eq "下着<>DN") {
            $log = ($log . "$l_nameは体防具を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $bou);
        $delitem = "$bou,$bdef,$btai,\n";
        $bou = "下着<>DN"; $bdef = 0; $btai = "∞" ;
    } elsif ($wk eq "H") {
        if ($bou_h eq "なし") {
            $log = ($log . "$l_nameは頭防具を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $bou_h);
        $delitem = "$bou_h,$bdef_h,$btai_h,\n";
        $bou_h = "なし"; $bdef_h = 0; $btai_h = 0 ;
    } elsif ($wk eq "A") {
        if ($bou_a eq "なし") {
            $log = ($log . "$l_nameは腕防具を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $bou_a);
        $delitem = "$bou_a,$bdef_a,$btai_a,\n";
        $bou_a = "なし"; $bdef_a = 0; $btai_a = 0 ;
    } elsif ($wk eq "F") {
        if ($bou_f eq "なし") {
            $log = ($log . "$l_nameは足防具を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $bou_f);
        $delitem = "$bou_f,$bdef_f,$btai_f,\n";
        $bou_f = "なし"; $bdef_f = 0; $btai_f = 0 ;
    } elsif ($wk eq "I") {
        if ($item[5] eq "なし") {
            $log = ($log . "$l_nameは装飾品を装備していません。<br>") ;
            $Command = "MAIN" ;
            return ;
        }

        ($in, $ik) = split(/<>/, $item[5]);
        $delitem = "$item[5],$eff[5],$itai[5],\n";
        $item[5] = "なし"; $eff[5] = 0; $itai[5] = 0 ;
    } else {
        &ERROR("不正なアクセスです。");
    }

    $log = ($log . "$inを捨てた。<br>") ;

    local($filename) = "$LOG_DIR/$pls$item_file";
    open(DB,">>$filename"); seek(DB,0,0); print DB $delitem; close(DB);

    $Command = "MAIN";

    &SAVE;

}

#==================#
# ■ 武器分解      #
#==================#
sub SPLIT {

    local($j) = 0;

    local($chk) = "NG" ;
    if (($wep =~ /<>WG/) && ($wtai > 0)) {
        for ($j=0; $j<5; $j++) {
            if (($item[$j] eq "なし") || ($item[$j] eq "弾丸<>Y")) {
                $chk = "ON" ; last;
            }
        }
        if ($chk eq "NG") {
            $log = ($log . "それ以上デイパックに入りません。<br>") ;
        } else {
            $log = ($log . "弾丸をデイパックにしまいました。<br>") ;
            $item[$j] ="弾丸<>Y"; $eff[$j] += $wtai; $itai[$j] = 1 ;
            $wtai = 0 ;
        }
    } elsif (($wep =~ /<>WA/) && ($wtai > 0)) {
        for ($j=0; $j<5; $j++) {
            if (($item[$j] eq "なし") || ($item[$j] eq "矢<>Y")) {
                $chk = "ON" ; last;
            }
        }
        if ($chk eq "NG") {
            $log = ($log . "それ以上デイパックに入りません。<br>") ;
        } else {
            $log = ($log . "矢をデイパックにしまいました。<br>") ;
            $item[$j] ="矢<>Y"; $eff[$j] += $wtai; $itai[$j] = 1 ;
            $wtai = 0 ;
        }
    } else {
        local($wn,$wk) = split(/<>/, $wep);
        $log = ($log . "$wnは分解できません。<br>") ;
    }

    &SAVE;

    $Command = "MAIN" ;

}
1
