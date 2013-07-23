### ハッキング処理 by kelp###

sub HACKING {

    for ($paso=0; $paso<5; $paso++){
        if (($item[$paso] eq "モバイルPC<>Y") && ($itai[$paso] >= 1)) { last; }
    }

    if (($Command ne "HACK2") || ($item[$paso] ne "モバイルPC<>Y") || ($itai[$paso] <= 0)) {
        &ERROR("不正なアクセスです。");
    }

    local($bonus) = 2;  #基本成功率(0の時10%)
    local($dice1) = int(rand(10)) ;
    local($dice2) = int(rand(10)) ;

    if ($club =~ /パソコン/){ #パソコン部の基本成功率
        $bonus = 5;
    }


    local($kekka) = $bonus;
    if ($dice1 <= $kekka){     #ハッキング成否判定
        open(DB,"$area_file");seek(DB,0,0); my(@wk_arealist)=<DB>;close(DB);
        my($wk_ar,$wk_hack,$wk_a) = split(/,/, $wk_arealist[1]);  #ハッキングフラグ取得
        $wk_hack = 1;
        $wk_arealist[1] = "$wk_ar,$wk_hack,,\n";
        open(DB,">$area_file"); seek(DB,0,0); print DB @wk_arealist; close(DB);
        $log = ($log . "ハッキング成功！全ての禁止エリアが解除された！！<BR>") ;
        &LOGSAVE("HACK");
    }else{
        $log = ($log . "ハッキングは失敗した・・・<BR>") ;
    }

    if ($dice1 >= 9){   #バッテリ消耗＆ファンブル時機材破壊
        $item[$paso] = "なし"; $eff[$paso] = $itai[$paso] = 0 ;
        $log = ($log . "何てこった！機材が壊れてしまった。<BR>") ;
        if ($dice2 >= 9){  #神様(％ファンブル)時政府により首輪爆破！
            $hit = 0 ; $sts = "死亡"; $death = $deth = "政府による処刑";$mem--;
            if ($mem == 1) {
                open(FLAG,">$end_flag_file"); print(FLAG "終了\n"); close(FLAG);
            }
            &LOGSAVE("DEATH5") ;
            open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
            $gunlog[1] = "$now,$place[$pls],$id,,\n";
            open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
            $log = ($log . "何てこった！機材が壊れてしまった。<BR><br>・・・何だ？・・・首輪から警告音が・・・！？<BR><BR><font color=\"red\">・・・！！・・・<br><br><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
        }
    }else{
        $itai[$paso] --;
        if ($itai[$paso] == 0) {
            $log = ($log . "モバイルPC のバッテリの電力を使い果たした。<BR>") ;
        }
    }

    &SAVE;
}
1
