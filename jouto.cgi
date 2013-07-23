#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";



    open(DB,"$joutolog_file");seek(DB,0,0); @joutolog=<DB>;close(DB);

    @ar = split(/,/, $arealist[4]);

    $getmonth=$getday=0;
    foreach $joutolog(@joutolog) {
        ($gettime,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_f_name2,$w_l_name2,$w_sex2,$w_cl2,$w_no2,$getkind,$z_in,$z_ik,$z_kind,$host1,$host2)= split(/,/, $joutolog);
        ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($gettime);
        $hour = "0$hour" if ($hour < 10);
        $min = "0$min" if ($min < 10);  $month++;
        $year += 1900;
        $week = ('日','月','火','水','木','金','土') [$wday];
        if (($getmonth != $month) || ($getday != $mday)) {
            if ($getmonth !=0) { push (@log,"</LI></UL>\n"); }
            $getmonth=$month;$getday = $mday;
            push (@log,"<P><font color=\"lime\"><B>$month月 $mday日 ($week曜日)</B></font><BR>\n");
            push (@log,"<UL>\n");
        }

        if ($getkind eq "JOUTO") {  #譲渡
            push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が <font color=\"yellow\"><b>$w_f_name2 $w_l_name2（$w_cl2 $w_sex2$w_no2番）</b></font> に <font color=\"aqua\">$z_kind</font> を譲渡した。<br>\n") ;
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
    print "<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">譲渡履歴</FONT></B><BR><BR>\n";
    print "<table border=\"0\"><tr><td width=\"70\" height=\"70\" align=\"middle\"><img src=\"$imgurl$n_icon_file[0]\"></td><td valign=\"middle\">『お前らー、協力するのもいいが<BR>監視されてることを忘れるなよー』</td></tr></table><br>\n";
    print "$ars";
    print @log;
    print "<center>\n" ;
    print "<BR><B><a href=\"$home\">HOME</A></B><BR>\n";

    &FOOTER;
&UNLOCK;

exit;
