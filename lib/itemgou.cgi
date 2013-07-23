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

    $log = ($log . "アイテムを合成します。<br>") ;
    if (($wk == $wk2)||($in eq $in2)) { #同アイテム選択？
        $log = ($log . "$inを眺めてみた。<br>") ;
    }else{
        require "$g_table";

        if($gousei{$in}{$in2}) { #合成テーブル使用合成
            local($w_item,$w_eff,$w_itai,$type) = split(/,/, $gousei{$in}{$in2});
            local($w_in,$w_ik) = split(/<>/, $w_item);

            if($w_eff eq "k1") { $w_eff = $eff[$wk]; }
            elsif($w_eff eq "k2") { $w_eff = $eff[$wk2]; }
            elsif($w_eff eq "k3") { $w_eff = $eff[$wk] + $eff[$wk2]; }

            if($w_itai eq "k1") { $w_itai = $itai[$wk]; }
            elsif($w_itai eq "k2") { $w_itai = $itai[$wk2]; }
            elsif($w_itai eq "k3") { $w_itai = $itai[$wk] + $itai[$wk2]; }

            if($type == 0) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk] = $w_item; $eff[$wk] = $w_eff; $itai[$wk] = $w_itai;
                $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0;
            } elsif($type == 1) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk] = $w_item; $eff[$wk] = $w_eff; $itai[$wk] = $w_itai;
                $itai[$wk2]--;
                if ($itai[$wk2] <= 0) { $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0; }
            } elsif($type == 2) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk2] = $w_item; $eff[$wk2] = $w_eff; $itai[$wk2] = $w_itai;
                $itai[$wk]--;
                if ($itai[$wk] <= 0) { $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0; }
            } else {
                $chk = "NG" ;
                if($itai[$wk] == 1) {
                    $chk = "ON"; $j=$wk;
                } elsif($itai[$wk2] == 1) {
                    $chk = "ON"; $j=$wk2;
                } else {
                    for ($j=0; $j<5; $j++) {
                        if ($item[$j] eq "なし") { $chk = "ON" ; last; }
                    }
                }

                if ($chk eq "NG") {
                    $log = ($log . "それ以上デイパックに入りません。<br>") ;
                } else {
                    $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                    $itai[$wk]--; if ($itai[$wk] <= 0) { $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0; }
                    $itai[$wk2]--; if ($itai[$wk2] <= 0) { $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0; }
                    $item[$j] = $w_item; $eff[$j] = $w_eff; $itai[$j] = $w_itai;
                }
            }
        } elsif($gousei{$in2}{$in}) { #合成テーブル使用合成(逆)
            local($w_item,$w_eff,$w_itai,$type) = split(/,/, $gousei{$in2}{$in});
            local($w_in,$w_ik) = split(/<>/, $w_item);

            if($w_eff eq "k1") { $w_eff = $eff[$wk2]; }
            elsif($w_eff eq "k2") { $w_eff = $eff[$wk]; }
            elsif($w_eff eq "k3") { $w_eff = $eff[$wk] + $eff[$wk2]; }

            if($w_itai eq "k1") { $w_itai = $itai[$wk2]; }
            elsif($w_itai eq "k2") { $w_itai = $itai[$wk]; }
            elsif($w_itai eq "k3") { $w_itai = $itai[$wk] + $eff[$wk2]; }

            if($type == 0) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk] = $w_item; $eff[$wk] = $w_eff; $itai[$wk] = $w_itai;
                $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0;
            } elsif($type == 1) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk2] = $w_item; $eff[$wk2] = $w_eff; $itai[$wk2] = $w_itai;
                $itai[$wk]--;
                if ($itai[$wk] <= 0) { $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0; }
            } elsif($type == 2) {
                $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                $item[$wk] = $w_item; $eff[$wk] = $w_eff; $itai[$wk] = $w_itai;
                $itai[$wk2]--;
                if ($itai[$wk2] <= 0) { $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0; }
            } elsif($type == 3) {
                $chk = "NG" ;
                if($itai[$wk] == 1) {
                    $chk = "ON"; $j=$wk;
                } elsif($itai[$wk2] == 1) {
                    $chk = "ON"; $j=$wk2;
                } else {
                    for ($j=0; $j<5; $j++) {
                        if ($item[$j] eq "なし") { $chk = "ON" ; last; }
                    }
                }

                if ($chk eq "NG") {
                    $log = ($log . "それ以上デイパックに入りません。<br>") ;
                } else {
                    $log = ($log . "$inと$in2で$w_inが出来た！<BR>");
                    $itai[$wk]--; if ($itai[$wk] <= 0) { $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0; }
                    $itai[$wk2]--; if ($itai[$wk2] <= 0) { $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0; }
                    $item[$j] = $w_item; $eff[$j] = $w_eff; $itai[$j] = $w_itai;
                }
            }
        } elsif(($ik =~ /食/) && ($ik2 =~ /食/)) { #食材合成
            $chk = "NG" ;
            if($itai[$wk] == 1) {
                $chk = "ON"; $j=$wk;
            } elsif($itai[$wk2] == 1) {
                $chk = "ON"; $j=$wk2;
            } else {
                for ($j=0; $j<5; $j++) {
                    if ($item[$j] eq "なし") { $chk = "ON" ; last; }
                }
            }

            if ($chk eq "NG") {
                $log = ($log . "それ以上デイパックに入りません。<br>") ;
            } else {
                $log = ($log . "$inと$in2で$f_name特製料理が出来た！<BR>");
                $itai[$wk]--; if ($itai[$wk] <= 0) { $item[$wk] = "なし"; $eff[$wk] = 0; $itai[$wk] = 0; }
                $itai[$wk2]--; if ($itai[$wk2] <= 0) { $item[$wk2] = "なし"; $eff[$wk2] = 0; $itai[$wk2] = 0; }

                if(int(rand(2))==0) { $item[$j] = "$f_name特製料理<>SH"; }
                else { $item[$j] = "$f_name特製料理<>HH"; }

                if ($club ne "料理研究部") {
                    if(($ik =~ /HD|SD/) || ($ik2 =~ /HD|SD/)) {
                        $item[$j] =~ s/<>HH/<>HD/g;
                        $item[$j] =~ s/<>SH/<>SD/g;
                    } elsif(int(rand(3))==0) {
                        $log = ($log . "しかし、何故か食べてはならない物を作ったような気がする…<BR>");
                        $item[$j] =~ s/<>HH/<>HD/g;
                        $item[$j] =~ s/<>SH/<>SD/g;
                    }
                }
                $eff[$j] = int(rand(21)+20);
                $itai[$j] = int(rand(2)+1);
            }
        } else { #違うアイテム・合成できない物選択
            $log = ($log . "$inと$in2は組み合わせられないな。<br>") ;
        }
    }

    $Command = "MAIN";
    $Command2 = "";

    &SAVE;

}

1
