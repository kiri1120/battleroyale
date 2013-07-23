#==================#
# ■ アイテム整理 #
#==================#
sub ITEMSEIRI {

    local($wk) = $Command;
    $wk =~ s/SEIRI_//g;
    local($in, $ik) = split(/<>/, $item[$wk]);

    local($wk2) = $Command2;
    $wk2 =~ s/SEIRI2_//g;
    local($in2, $ik2) = split(/<>/, $item[$wk2]);

    if (($item[$wk] eq "なし")||($item[$wk2] eq "なし")) {
        &ERROR("不正なアクセスです。");
    }

    $log = ($log . "アイテムを整理します。<br>") ;

    if ($wk == $wk2) { #同アイテム選択？
        $log = ($log . "$inを入れ直しました。<br>") ;
    }elsif (($in eq $in2)&&($eff[$wk] eq $eff[$wk2])&&($ik =~ /HH|HD/)&&($ik2 =~ /HH|HD/)) { #体力回復アイテム整理
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        if (($ik eq "HD")||($ik2 eq "HD")) {
            $item[$wk] = "$in<>HD";
        }
        if(($ik eq "HD2")||($ik2 eq "HD2")) {
            $item[$wk] = "$in<>HD2";
        }
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif (($in eq $in2)&&($eff[$wk] eq $eff[$wk2])&&($ik =~ /SH|SD/)&&($ik2 =~ /SH|SD/)) { #スタミナ回復アイテム整理
            $itai[$wk] = $itai[$wk] + $itai[$wk2];
        if (($ik eq "SD")||($ik2 eq "SD")) {
            $item[$wk] = "$in<>SD";
        }
        if(($ik eq "SD2")||($ik2 eq "SD2")) {
            $item[$wk] = "$in<>SD2";
        }
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif (($in eq $in2)&&($ik eq $ik2)&&($ik =~ /W/)&&($ik =~ /C|D/) && ($itai[$wk] ne "∞") && ($itai[$wk2] ne "∞")) { #爆発・投武器
        $eff[$wk] = int((($eff[$wk] * $itai[$wk]) + ($eff[$wk2] * $itai[$wk2])) / ($itai[$wk] + $itai[$wk2]));
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif (($in eq $in2)&&($ik eq $ik2)&&($ik eq "Y")&&($in =~ /砥石|釘|火薬/)) { #武器強化アイテム
        $eff[$wk] = int((($eff[$wk] * $itai[$wk]) + ($eff[$wk2] * $itai[$wk2])) / ($itai[$wk] + $itai[$wk2]));
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif (($in eq $in2)&&($ik eq $ik2)&&($ik eq "Y")&&($in =~ /毒薬|毒中和剤/)) { #毒関係整理
        $eff[$wk] = int((($eff[$wk] * $itai[$wk]) + ($eff[$wk2] * $itai[$wk2])) / ($itai[$wk] + $itai[$wk2]));
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif (($in eq $in2)&&($ik eq $ik2)&&($ik eq "Y")&&($in =~ /修繕道具/)) { #修繕道具整理
        $eff[$wk] = int((($eff[$wk] * $itai[$wk]) + ($eff[$wk2] * $itai[$wk2])) / ($itai[$wk] + $itai[$wk2]));
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif ((($in eq $in2)&&($ik eq $ik2)&&($ik eq "Y"))&&($in =~ /弾|矢/)) { #弾丸・矢
        $eff[$wk] = $eff[$wk] + $eff[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }elsif ((($in eq $in2)&&($ik eq $ik2)&&($ik eq "Y"))&&($in =~ /バッテリ/)) { #バッテリ
        $itai[$wk] = $itai[$wk] + $itai[$wk2];
        $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        $log = ($log . "$inを纏めました。<br>") ;
    }else { #違うアイテム・纏められない物選択
    $log = ($log . "$inと$in2は纏められないな。<br>") ;
    }

    $Command = "MAIN";
    $Command2 = "";

    &SAVE;

}
1
