#==================#
# ■ アイテム合成  #
#==================#
sub ITEMGOUSEI {

    $wk = $Command;
    $wk =~ s/GOUSEI_//g;
    ($in, $ik) = split(/<>/, $item[$wk]);

    $wk2 = $Command2;
    $wk2 =~ s/GOUSEI2_//g;
    ($in2, $ik2) = split(/<>/, $item[$wk2]);

    if (($item[$wk] eq "なし")||($item[$wk2] eq "なし")) {
        &ERROR("不正なアクセスです。");
    }

    $chk = "NG" ;

    if(($itai[$wk] == 1)||($itai[$wk] eq "∞")){
        $chk = "ON"; $itai[$wk] == 1;$j=$wk;
    }elsif($ik =~ /DB|DH|DF|DA/){
        $chk = "ON"; ;$j=$wk;
    }elsif(($itai[$wk2] == 1)||($itai[$wk2] eq "∞")){
        $chk = "ON"; $itai[$wk2] == 1;$j=$wk2;
    }elsif($ik2 =~ /DB|DH|DF|DA/){
        $chk = "ON"; ;$j=$wk2;
    }else{
        for ($j=0; $j<5; $j++) {
            if ($item[$j] eq "なし") {
                $chk = "ON" ; last;
            }
        }
    }

    if ($chk eq "NG") {
        $log = ($log . "それ以上デイパックに入りません。<br>") ;
    } else {
        $log = ($log . "アイテムを合成します。<br>") ;
        if (($wk == $wk2)||($in eq $in2)) { #同アイテム選択？
            $log = ($log . "$inを眺めてみた。<br>") ;
        }else{
            require "$g_table";

            #テーブル作成
            local($k) = 0;
            local($l) = $#g_item1+1;
            for ($k=0; $k<$l; $k++) {
                $gousei{"$g_item1[$k]"}{"$g_item2[$k]"}{"name"} = "$g_name[$k]";
                $gousei{"$g_item1[$k]"}{"$g_item2[$k]"}{"kind"} = "$g_kind[$k]";
                $gousei{"$g_item1[$k]"}{"$g_item2[$k]"}{"eff"}  = "$g_eff[$k]";
                $gousei{"$g_item1[$k]"}{"$g_item2[$k]"}{"itai"} = "$g_itai[$k]";
            }

            if($gousei{$in}{$in2}{name}){ #合成テーブル使用合成
                $log = ($log . "$inと$in2で$gousei{$in}{$in2}{name}が出来た！<BR>");
                $item[$j] = "$gousei{$in}{$in2}{name}<>$gousei{$in}{$in2}{kind}";
                $eff[$j] = $gousei{$in}{$in2}{eff} ;
                $itai[$j] = $gousei{$in}{$in2}{itai} ;
                &ITEMCOUNT;
            }elsif($gousei{$in2}{$in}{name}){ #合成テーブル使用合成(逆)
                $log = ($log . "$inと$in2で$gousei{$in2}{$in}{name}が出来た！<BR>");
                $item[$j] = "$gousei{$in2}{$in}{name}<>$gousei{$in2}{$in}{kind}";
                $eff[$j] = $gousei{$in2}{$in}{eff} ;
                $itai[$j] = $gousei{$in2}{$in}{itai} ;
                &ITEMCOUNT;
            }else { #違うアイテム・合成できない物選択
                $log = ($log . "$inと$in2は組み合わせられないな。<br>") ;
            }
        }
    }

    $Command = "MAIN";
    $Command2 = "";

    &SAVE;

}

sub ITEMCOUNT{
    if($wk == $j){
        if($ik2 =~ /DB|DH|DF|DA/){
            $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        }else{
            $itai[$wk2] -= 1;
            if ($itai[$wk2] <= 0) {$item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;}
        }
    }elsif($wk2 == $j){
        if($ik =~ /DB|DH|DF|DA/){
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }else{
            $itai[$wk] -= 1;
            if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        }
    }else{
        if($ik =~ /DB|DH|DF|DA/){
            $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;
        }else{
            $itai[$wk] -= 1;
            if ($itai[$wk] <= 0) {$item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0 ;}
        }
        if($ik2 =~ /DB|DH|DF|DA/){
            $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;
        }else{
            $itai[$wk2] -= 1;
            if ($itai[$wk2] <= 0) {$item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0 ;}
        }
    }
}

1
