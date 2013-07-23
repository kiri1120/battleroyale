#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
&LOCK;
require "pref.cgi";



    open(DB,"$log_file");seek(DB,0,0); @loglist=<DB>;close(DB);

    ($ar[0],$ar[1],$ar[2],$ar[3],$ar[4],$ar[5],$ar[6],$ar[7],$ar[8],$ar[9],$ar[10],$ar[11],$ar[12],$ar[13],$ar[14],$ar[15],$ar[16],$ar[17],$ar[18],$ar[19],$ar[20],$ar[21],$ar[22]) = split(/,/, $arealist[4]);

    $getmonth=$getday=0;
    foreach $loglist(@loglist) {
        ($gettime,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_f_name2,$w_l_name2,$w_sex2,$w_cl2,$w_no2,$getkind,$host)= split(/,/, $loglist);
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

        if ($host eq "") { $host = ""; } else { $host = "($host)" ; }
        if((!$host_view)&&($getkind eq "ENTRY")){$host = "";}

        if ($getkind eq "DEATH") {  #死亡（自分が原因）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH1") { #死亡（毒殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH2") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH3") { #死亡（他殺）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATH4") { #死亡（政府）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "DEATHAREA") { #死亡（禁止エリア）
            push (@log,"<LI>$hour時$min分、<font color=\"red\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 禁止エリアの為、死亡した。<font color=\"red\"><b>$host</b></font><BR>\n") ;
        } elsif ($getkind eq "WINEND") { #優勝者決定
            $log_num = pop @log;
            if ($log_num =~ /ゲーム終了/){
                push (@log,$log_num);
            }else{
                push (@log,$log_num);
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>ゲーム終了・以上本プログラム実施本部選手確認モニタより</B></font> <BR>\n") ;
            }
        } elsif ($getkind eq "EX_END") { #プログラム停止
            $log_num = pop @log;
            if ($log_num =~ /ゲーム終了/){
                push (@log,$log_num);
            }else{
                push (@log,$log_num);
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>ゲーム終了・プログラム緊急停止</B></font> <BR>\n") ;
            }
        } elsif ($getkind eq "AREA") { #禁止エリア追加
            $log_num = pop @log;
            if (($log_num !~ /ゲーム終了/)||($log_num !~ /<UL>/)){
                push (@log,$log_num);
                push (@log,"<LI>$hour時$min分、<font color=\"lime\"><b>$place[$ar[$w_l_name]]、$place[$ar[$w_l_name+1]]、$place[$ar[$w_l_name+2]]</b></font> が 禁止エリアに指定された。次回禁止エリアは<font color=\"lime\"><b>$place[$ar[$w_f_name]]、$place[$ar[$w_f_name+1]]、$place[$ar[$w_f_name+2]]</b></font>。<BR>\n") ;
            }else{
                push (@log,$log_num);
            }
        } elsif ($getkind eq "ENTRY") { #新規登録
            push (@log,"<LI>$hour時$min分、<font color=\"yellow\"><b>$w_f_name $w_l_name（$w_cl $w_sex$w_no番）</b></font> が 転校してきた。$host<BR>\n") ;
        } elsif ($getkind eq "NEWGAME") { #管理人によるデータ初期化
            push (@log,"<LI>$hour時$min分、新規プログラム開始。<BR>\n") ;
        }

        $cnt++;
    }

    for ($i=0; $i<$arealist[1]  ; $i++) {
        $ars = ($ars . " $place[$ar[$i]]") ;
    }
    $ars = "<BR><font color=\"lime\"><B>現在の禁止エリア</B></FONT>  $ars<BR><font color=\"lime\"><B>次回の禁止エリア</B></FONT>  $place[$ar[$i]] $place[$ar[$i+1]] $place[$ar[$i+2]]\n" ;


    &HEADER ;
    print "</center>\n" ;
    print "<B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">進行状況</FONT></B><BR><BR>\n";
    print "『みんなー、元気にやってるかあ。<BR>それじゃ、これまでの状況でーす。<BR>今日も一日がんばろーなー。』<br>\n";
    print "$ars";
    print @log;
    print "<center>\n" ;
    print "<BR><B><a href=\"index.htm\">HOME</A></B><BR>\n";

    &FOOTER;
&UNLOCK;

exit;
