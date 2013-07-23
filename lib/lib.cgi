# 汎用サブルーチン集2

#==================#
# ■ ヘッダー部    #
#==================#
sub HEADER {
print "Content-type: text/html\n\n";
print <<"_HERE_";
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=euc-jp">
<TITLE>$game</TITLE>
<SCRIPT language="JavaScript">
<!--
    function sl(x) {
        document.f1.Command[x].checked = true;
    }
    function dbk(){
        window.alert("ダブルクリックは禁止です。");
    }
//-->
</SCRIPT>
<STYLE type="text/css">
<!--
BODY {
    FONT-SIZE   : 9pt;
    font-family : "MS UI Gothic";
}
TH {
    FONT-SIZE:      9pt;
    BACKGROUND:     #005; 
    BORDER-RIGHT:   #336 1px solid; 
    BORDER-TOP:     #99c 1px solid; 
    BORDER-LEFT:    #99c 1px solid; 
    BORDER-BOTTOM:  #336 1px solid; 
}
TD      { FONT-SIZE: 9pt; }
A:hover { COLOR: #ffff99 }
-->
</STYLE>
</HEAD>
<BODY bgcolor="#000000" text="#ffffff" link="#ff0000" vlink="#ff0000">
<CENTER>
_HERE_
}
#==================#
# ■ フッタ部      #
#==================#
sub FOOTER {
print <<"_HERE_";
</CENTER>
<HR>
<DIV align="right"><B><A href="http://www.happy-ice.com/battle/">BATTLE ROYALE V01.19</A></B></DIV>
</BODY>
</HTML>
_HERE_
}

#==================#
# ■ エラー処理    #
#==================#
sub ERROR{
if ($lockflag) { &UNLOCK; }

$errmes = @_[0] ;
&HEADER;
print <<"_HERE_";
<B><FONT color="#ff0000" size="+2" face="ＭＳ 明朝">エラー発生</FONT></B><BR><BR>
$errmes<BR>
<BR>
<B><FONT color="#ff0000"><A href="$home">HOME</A></B>
_HERE_
&FOOTER;
exit;
}

#====================#
# ■ ログ保存        #
#====================#
sub LOGSAVE {

    local($work) = @_[0] ;
    local($newlog) = "" ;

    if ($work eq "NEWENT") { #新規登録
        $newlog = "$now,$f_name2,$l_name2,$sex2,$cl,$no,,,,,$host2,ENTRY,$host,$os,,\n" ;
    } elsif ($work eq "DEATH" ){ #自分死亡（要因：罠、体力切れ）
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH,$dmes,,,\n" ;
        $death = "衰弱死";$msg=$dmes;
    } elsif ($work eq "DEATH1" ){ #自分死亡（要因：毒殺）
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH1,$dmes,,,\n" ;
        $death = "毒物摂取";$msg=$dmes;
    } elsif ($work eq "DEATH2" ){ #自分死亡（要因：敗死）
        if ($w_kind2 =~ /N/) {           #斬系
            $d2 = "斬殺" ;
        } elsif (($w_kind2 =~ /A/) && ($w_wtai > 0)) {   #矢系
            $d2 = "射殺" ;
        } elsif (($w_kind2 =~ /G/) && ($w_wtai > 0)) {   #銃系
            $d2 = "銃殺" ;
        } elsif ($w_kind2 =~ /C/) {  #投系
            $d2 = "殺害" ;
        } elsif ($w_kind2 =~ /D/) {  #爆系
            $d2 = "爆殺" ;
        } elsif ($w_kind2 =~ /S/) {  #刺系
            $d2 = "刺殺" ;
        } elsif (($w_kind2 =~ /B/) || (($w_kind2 =~ /G|A/) && ($w_wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
            $d2 = "撲殺" ;
        } else {
            $d2 = "殺害" ;
        }

        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,DEATH2,$dmes,$w_name2,,\n" ;
        if ($w_no eq "政府") {
            $deth = "$w_f_name $w_l_nameにより$d2";
        } else {
            $deth = "$w_f_name $w_l_name（$w_cl $w_sex$w_no番）により$d2";
        }
        if ($w_msg ne "") {
            $msg = "$w_f_name $w_l_name『$w_msg』" ;
        } else {
            $msg = "" ;
        }
    } elsif ($work eq "DEATH3" ){ #敵死亡（要因：敗死）
        if ($w_kind =~ /N/) {           #斬系
            $d2 = "斬殺" ;
        } elsif (($w_kind =~ /A/) && ($wtai > 0)) { #矢系
            $d2 = "射殺" ;
        } elsif (($w_kind =~ /G/) && ($wtai > 0)) { #銃系
            $d2 = "銃殺" ;
        } elsif ($w_kind =~ /C/) {  #投系
            $d2 = "殺害" ;
        } elsif ($w_kind =~ /D/) {  #爆系
            $d2 = "爆殺" ;
        } elsif ($w_kind =~ /S/) {  #刺系
            $d2 = "刺殺" ;
        } elsif (($w_kind =~ /B/) || (($w_kind =~ /G|A/) && ($wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
            $d2 = "撲殺" ;
        } else {
            $d2 = "殺害" ;
        }
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$f_name,$l_name,$sex,$cl,$no,DEATH3,$w_dmes,$w_name,$d2,\n" ;
        $deth = "$f_name $l_name（$cl $sex$no番）により$d2";
        if ($msg ne "") {
            $w_msg = "$f_name $l_name『$msg』" ;
        } else {
            $w_msg = "" ;
        }
    } elsif ($work eq "DEATH4" ){ #政府による殺害
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,,,,,,DEATH4,$w_dmes,,,\n" ;
        $deth = "政府による処刑";
        $log ="";
        if ($w_msg ne "") {
            $msg = "政府『$w_msg』" ;
        } else {
            $msg = "" ;
        }
    } elsif ($work eq "DEATH5" ){ #政府による殺害2
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH4,$dmes,,,\n" ;
        $deth = "政府による処刑";
        $log ="";
        $msg = "政府『ダメだなあ、不審な行動を取ったら首輪を爆破するって言ったよな』" ;
    } elsif ($work eq "DEATHAREA" ){ #死亡（要因：禁止エリア）
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,,,,,,DEATHAREA,$w_dmes,,,\n" ;
        $deth = "禁止エリア滞在";
        $msg = "" ;$log ="";
    } elsif ($work eq "WINEND1" ){ #優勝決定
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,WINEND,$dmes,,,\n" ;
        open(FLAG,">$end_flag_file"); print(FLAG "終了\n"); close(FLAG);
        require "$LIB_DIR/adlib.cgi";
        &InitResetTime;
    } elsif ($work eq "EX_END" ){ #プログラムを停止
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,EX_END,$dmes,,,\n" ;
        require "$LIB_DIR/adlib.cgi";
        &InitResetTime;
    } elsif ($work eq "HACK" ){ #ハッキング
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,HACK,,,,\n" ;
    } elsif ($work eq "SPEAKER" ){ #叫ぶ
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,SPEAKER,$speech,,,\n" ;
    } elsif ($work eq "AREAADD" ){ #禁止エリア追加
        $ar = $ar2 - 3 ;
        $newlog = "$now,$ar2,$ar,,,,,,,,,AREA,,$pgday,,\n" ;
    }

    open(DB,"$log_file") || exit; seek(DB,0,0); @loglist=<DB>; close(DB);
    unshift(@loglist,$newlog);

    open(DB,">$log_file"); seek(DB,0,0); print DB @loglist; close(DB);


}

#====================#
# ■ LOCK            #
#====================#
sub LOCK {
    local($retry,$mtime);
    # 1分以上古いロックは削除する
    if (-e $lockf) {
        ($mtime) = (stat($lockf))[9];
        if ($mtime < time - 60) { &UNLOCK; }
    }
    # symlink関数式ロック
    if ($lkey == 1) {
        $retry = 5;
        while (!symlink(".", $lockf)) {
            if (--$retry <= 0) { &ERROR("ただいま大変混み合っております。しばらくお待ち下さい。"); }
            sleep(1);
        }
    # mkdir関数式ロック
    } elsif ($lkey == 2) {
        $retry = 5;
        while (!mkdir($lockf, 0755)) {
            if (--$retry <= 0) {  &ERROR("ただいま大変混み合っております。しばらくお待ち下さい。"); }
            sleep(1);
        }
    }
    $lockflag=1;
}

#====================#
# ■ UNLOCK          #
#====================#

sub UNLOCK {
    if ($lkey == 1) { unlink($lockf); }
    elsif ($lkey == 2) { rmdir($lockf); }
    $lockflag=0;
}

1
