#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";

    open(DB,"$log_file");seek(DB,0,0); @loglist=<DB>;close(DB);

    @ar = split(/,/, $arealist[4]);

    $getmonth=$getday=0;
    foreach $loglist(@loglist) {
        ($gettime,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_f_name2,$w_l_name2,$w_sex2,$w_cl2,$w_no2,$getkind,$info1,$info2,$info3)= split(/,/, $loglist);
        ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($gettime);
        $hour = sprintf("%02d", $hour);
        $min  = sprintf("%02d", $min);
        $month++; $year += 1900;
        $week = ('日','月','火','水','木','金','土') [$wday];
        if (($getmonth != $month) || ($getday != $mday)) {
            if ($getmonth !=0) { push (@log,"</LI></UL>\n"); }
            $getmonth=$month;$getday = $mday;
            push (@log,"<P><font color=\"lime\"><B>$month月 $mday日 ($week曜日)</B></font><BR>\n");
            push (@log,"<UL>\n");
        }

        if ($info1 ne "") { $info1 = "($info1)" ; }

        if ($getkind eq "DEATH") {  #死亡（自分が原因）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>死亡</b></font>した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH1") { #死亡（毒殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>服毒死</b></font>した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH2") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"yellow\"><b>$w_f_name2 $w_l_name2（$w_cl2 $w_sex2$w_no2番）</b></font>に<font color=\"aqua\"><b>$info2</b></font>で<font color=\"red\"><b>返り討ち</b></font>にされた。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH3") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"yellow\"><b>$w_f_name2 $w_l_name2（$w_cl2 $w_sex2$w_no2番）</b></font>に<font color=\"aqua\"><b>$info2</b></font>で<font color=\"red\"><b>$info3</b></font>された。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH4") { #死亡（政府）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が政府に<font color=\"red\"><b>処刑</b></font>された。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATHAREA") { #死亡（禁止エリア）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font>が<font color=\"red\"><b>禁止エリア</b></font>の為、死亡した。<font color=\"red\"><b>$info1</b></font><BR>\n") ;
        } elsif ($getkind eq "WINEND") { #優勝者決定
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>ゲーム終了・以上本プログラム実施本部選手確認モニタより</B></font> <BR>\n") ;
        } elsif ($getkind eq "EX_END") { #プログラム停止
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）がプログラム解除キーを使用・プログラム緊急停止</B></font> <BR>\n") ;
        } elsif ($getkind eq "HACK") { #ハッキング
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）によってハッキングを受け、分校の機能が停止！！</B></font> <BR>\n") ;
        } elsif ($getkind eq "SPEAKER") { #叫ぶ
            push (@log,"<LI>$hour時$min分、<font color=\"aqua\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が <font color=\"aqua\"><b>$info1</b></font> と叫んだ。<BR>\n") ;
        } elsif ($getkind eq "AREA") { #禁止エリア追加
            if ($info2 == 7) {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>プログラム最終日開始</b></font>。<BR>\n") ;
            } elsif ($info2 == 8) {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>時間切れによりゲーム終了</b></font>。<BR>\n") ;
            } else {
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>プログラム$info2日目開始</b></font>。<BR>\n") ;
            }
        } elsif ($getkind eq "ENTRY") { #新規登録
            push (@log,"<LI>$hour時$min分、<font color=\"yellow\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 転校してきた。<font color=\"yellow\">$info1</font><BR>\n") ;
        } elsif ($getkind eq "NEWGAME") { #管理人によるデータ初期化
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>新規プログラム開始</b></font>。<BR>\n") ;
        }

        $cnt++;
    }

    if ($hackflg) {
        $ars1 = "なし";
        for ($i=0; $i<$ar+3  ; $i++) {
            $ars2 .= " $place[$ar[$i]]";
        }
    } else {
        for ($i=0; $i<$ar; $i++) {
            $ars1 .= " $place[$ar[$i]]";
        }
        for ($i=$ar; $i<$ar+3; $i++) {
            $ars2 .= " $place[$ar[$i]]";
        }
    }
    $ars = "<BR><font color=\"lime\"><B>現在の禁止エリア</B></FONT>  $ars1<BR><font color=\"lime\"><B>次回の禁止エリア</B></FONT>  $ars2\n" ;

    &HEADER ;
    print "</center>\n" ;
    print "<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">進行状況</FONT></B><BR><BR>\n";
    print "<table><tr><td width=\"70\" height=\"70\"><img src=\"$imgurl$n_icon_file[0]\"></td><td>『みんなー、元気にやってるかあ。<BR>それじゃ、これまでの状況でーす。<BR>今日も一日がんばろーなー。』</td></tr></table><br>\n";
    print "$ars";
    print @log;
    print "</UL>\n<center>\n" ;
    print "<B><a href=\"$home\">HOME</A></B><BR>\n";

    &FOOTER;
&UNLOCK;

exit;
