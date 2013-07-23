#==================#
# ■ アイテム整理  #
#==================#
sub ITEMBUNKATU {

    local($wk) = $Command;
    $wk =~ s/BUNKATU_//g;
    local($in, $ik) = split(/<>/, $item[$wk]);

    $j = $Command2;

    if (($item[$wk] eq "なし") || ($j < 1)) {
        &ERROR("不正なアクセスです。");
    }

    local($chk) = "NG" ;
    for ($wk2=0; $wk2<5; $wk2++) {
        if ($item[$wk2] eq "なし") {
            $chk = "ON" ; last;
        }
    }

    if ($chk eq "NG") {
        $log = ($log . "それ以上デイパックに入りません。<br>") ;
    } elsif (($ik =~ /HH|HD|SH|SD/) && ($j < $itai[$wk])) { # 回復アイテム
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik =~ /W/) && ($ik =~ /C|D/) && ($itai[$wk] ne "∞") && ($j < $itai[$wk])) { # 爆・投武器
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik eq "Y") && ($in =~ /砥石|釘/) && ($j < $itai[$wk])) {  # 武器強化アイテム
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik eq "Y") && ($in =~ /毒薬|毒中和剤/) && ($j < $itai[$wk])) {    # 毒関係
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik eq "Y") && ($in =~ /修繕道具/) && ($j < $itai[$wk])) { # 修繕道具
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik eq "Y") && ($in =~ /弾|矢/) && ($j < $eff[$wk])) { # 弾丸・矢
        $eff[$wk] = $eff[$wk] - $j;
        $eff[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $itai[$wk2] = $itai[$wk];
        $log = $log . "$inを分割しました。<br>";
    } elsif (($ik eq "Y") && ($in =~ /バッテリ/) && ($j < $itai[$wk])) { # バッテリ
        $itai[$wk] = $itai[$wk] - $j;
        $itai[$wk2] = $j;
        $item[$wk2] = $item[$wk]; $eff[$wk2] = $eff[$wk];
        $log = $log . "$inを分割しました。<br>";
    } else { # 分割できない物選択
        $log = $log . "分割失敗。<br>";
    }

    $Command = "MAIN";
    $Command2 = "";

    &SAVE;

}
1
