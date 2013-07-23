# 汎用サブルーチン集2

#==================#
# ■ ホスト名取得  #
#==================#
sub GetHostName {
    my($ip_address) = @_;
    my(@addr) = split(/\./, $ip_address);
    my($packed_addr) = pack("C4", $addr[0], $addr[1], $addr[2], $addr[3]);
    my($name, $aliases, $addrtype, $length, @addrs);
    ($name, $aliases, $addrtype, $length, @addrs) = gethostbyaddr($packed_addr, 2);
    return $name;
}


#==================#
# ■ ヘッダー部    #
#==================#
sub HEADER {
print "Content-type: text/html\n\n";
print <<"_HERE_";
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html;CHARSET=x-euc-jp">
<TITLE>$game</TITLE>
</HEAD>
<BODY bgcolor="#000000" text="#ffffff" link="#ff0000" vlink="#ff0000" style='font-size : 13px;font-family : "MS UI Gothic";font-weight : normal;font-style : normal;font-variant : normal;'>
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
<DIV align="right"><B><A href="http://www.happy-ice.com/battle/">BATTLE ROYALE $ver</A></B></DIV>
</BODY>
</HTML>
_HERE_
}

#==================#
# ■ エラー処理    #
#==================#
sub ERROR{#■エラー画面
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
        $newlog = "$now,$f_name2,$l_name2,$sex2,$cl,$no,,,,,$host2,ENTRY,$host,\n" ;
    } elsif ($work eq "DEATH" ){ #自分死亡（要因：罠、体力切れ）
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH,$dmes,\n" ;
        $death = "衰弱死";$msg=$dmes;
    } elsif ($work eq "DEATH1" ){ #自分死亡（要因：毒殺）
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH1,$dmes,\n" ;
        $death = "毒物摂取";$msg=$dmes;
    } elsif ($work eq "DEATH2" ){ #自分死亡（要因：敗死）
        local($w_name,$w_kind) = split(/<>/, $w_wep);
        if ($w_kind =~ /N/) {           #斬系
            $d2 = "斬殺" ;
        } elsif (($w_kind =~ /A/) && ($w_wtai > 0)) {   #矢系
            $d2 = "射殺" ;
        } elsif (($w_kind =~ /G/) && ($w_wtai > 0)) {   #銃系
            $d2 = "銃殺" ;
        } elsif ($w_kind =~ /C/) {  #投系
            $d2 = "殺害" ;
        } elsif ($w_kind =~ /D/) {  #爆系
            $d2 = "爆殺" ;
        } elsif ($w_kind =~ /S/) {  #刺系
            $d2 = "刺殺" ;
        } elsif (($w_kind =~ /B/) || (($w_kind =~ /G|A/) && ($w_wtai == 0))) { #棍棒 or 弾無し銃 or 矢無し弓
            $d2 = "撲殺" ;
        } else {
            $d2 = "殺害" ;
        }

        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,DEATH2,$dmes,\n" ;
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
        local($w_name,$w_kind) = split(/<>/, $wep);
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
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$f_name,$l_name,$sex,$cl,$no,DEATH3,$w_dmes,\n" ;
        $deth = "$f_name $l_name（$cl $sex$no番）により$d2";
        if ($msg ne "") {
            $w_msg = "$f_name $l_name『$msg』" ;
        } else {
            $w_msg = "" ;
        }
        $w_log = "";
    } elsif ($work eq "DEATH4" ){ #政府による殺害
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,,,,,,DEATH4,$w_dmes,\n" ;
        $deth = "政府による処刑";
        $log ="";
        if ($w_msg ne "") {
            $msg = "政府『$w_msg』" ;
        } else {
            $msg = "" ;
        }
    } elsif ($work eq "DEATH5" ){ #政府による殺害2
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,DEATH4,$dmes,\n" ;
        $deth = "政府による処刑";
        $log ="";
        $msg = "政府『ダメだなあ、不審な行動を取ったら首輪を爆破するって言ったよな』" ;
    } elsif ($work eq "DEATHAREA" ){ #死亡（要因：禁止エリア）
        $newlog = "$now,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,,,,,,DEATHAREA,$w_dmes,\n" ;
        $deth = "禁止エリア滞在";
        $msg = "" ;$log ="";
    } elsif ($work eq "WINEND1" ){ #優勝決定
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,WINEND,$dmes,\n" ;
        open(FLAG,">$end_flag_file"); print(FLAG "終了\n"); close(FLAG);
    } elsif ($work eq "EX_END" ){ #ハッキングによりプログラムを停止
        $newlog = "$now,$f_name,$l_name,$sex,$cl,$no,,,,,,EX_END,$dmes,\n" ;
    } elsif ($work eq "AREAADD" ){ #禁止エリア追加
        $ar = $ar2 - 3 ;
        $newlog = "$now,$ar2,$ar,,,,,,,,,AREA,,\n" ;
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
    # Tripod用（暫定）
    } elsif ($lkey == 3) {
        local($lk) = mkdir($lockf, 0755);
        if ($lk == 0) {  &ERROR("ただいま大変混み合っております。しばらくお待ち下さい。"); }
    }
    $lockflag=1;
}

#====================#
# ■ UNLOCK          #
#====================#

sub UNLOCK {
    if ($lkey == 1) { unlink($lockf); }
    elsif ($lkey == 2) { rmdir($lockf); }
    elsif ($lkey == 3) { rmdir($lockf); }
    $lockflag=0;
}

1
