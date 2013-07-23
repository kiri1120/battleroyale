# pref.cgi コア部分

    # アクセス禁止
    $host2 = $ENV{'REMOTE_ADDR'};
    $host = gethostbyaddr(pack("C4", split(/\./, $host2)), 2);

    if ($host eq "") {
        $host = $host2;
    }

    # OS・ブラウザ取得
    $os = $ENV{'HTTP_USER_AGENT'};
    $os =~ s/,/\0/g;

    $okflag = 0;
    foreach (@oklist) {
        if (!$_) { next; }
        $_ =~ s/\./\\\./g;
        $_ =~ s/\*/\.\*/g;
        if (($host =~ /$_/i) || ($host2 =~ /$_/i)) { $okflag = 1; last; }
    }

#   #アクセス禁止チェック
#   if ($okflg == 0) {
#       foreach (@kick) {
#           if (!$_) { next; }
#           $_ =~ s/\*/\.\*/g;
#           if (($host =~ /$_/i) || ($host2 =~ /$_/i) {
#               &ERROR("あなたのホストはアクセス禁止となっているか、ホストが判別出来ません。<BR>管理人にお問い合わせください。") ;
#           }
#       }
#   }

    ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($now);
    $year+=1900;$month++;

    if (!$okflag) {
        $proxy = 0;
        if ($ENV{'HTTP_VIA'} or $ENV{'HTTP_FORWARDED'} or $ENV{'HTTP_X_FORWARDED_FOR'}) {
            $proxy = 1;
        } else {
            @dummy = %ENV;
            $dummy = join("",@dummy);
            $proxy = 1 if $dummy =~ /proxy/i;
        }
        if ($proxy) {
            $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host2,proxy,$host,\n";
            open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
            &ERROR("proxy等は外してアクセスしてください。") ;
        }
    }

    #管理ファイル読込
    open(DB, $area_file);seek(DB,0,0); @arealist=<DB>;close(DB);
    open(DB, $user_file);seek(DB,0,0); @userlist=<DB>;close(DB);
    open(FLAG, $end_flag_file);seek(FLAG,0,0); $fl=<FLAG>; close(FLAG);

    ($y,$m,$d,$hh,$mm) = split(/,/, $arealist[0]);
    ($ar,$hackflg,$resfl) = split(/,/,$arealist[1]) ;
    $pgday = int(($ar + 2) / 3);

    if (($year eq $y) && ($month eq $m) && ($mday eq $d) && ($hour >= $hh)) { #禁止エリア追加？
        if ($resfl eq "初期化") {
            require "$LIB_DIR/adlib.cgi";
            &DATARESET;

            #管理ファイル再読込
            open(DB, $area_file);seek(DB,0,0); @arealist=<DB>;close(DB);
            open(DB, $user_file);seek(DB,0,0); @userlist=<DB>;close(DB);
            open(FLAG, $end_flag_file);seek(FLAG,0,0); $fl=<FLAG>; close(FLAG);
            ($ar,$hackflg,$resfl) = split(/,/,$arealist[1]) ;
            $pgday = int(($ar + 2) / 3);
        } elsif (($fl !~ /終了/) && ($ar < $#place)) {
            ($se,$mi,$ho,$md,$mo,$ye,$wd,$yd,$is) = localtime($now+(1*60*60*24));
            $ye+=1900; $mo++;
            $ar2 = $ar + 3;

            $newareadata[0] = "$ye,$mo,$md,0,0,\n" ;     #エリア追加時刻
            $newareadata[1] = "$ar2,0,,\n" ;             #禁止エリア数
            $newareadata[2] = $arealist[2] ;
            $newareadata[3] = $arealist[3] ;
            $newareadata[4] = $arealist[4] ;
            open(DB,">$area_file"); seek(DB,0,0); print DB @newareadata; close(DB);

            @ara = split(/,/, $arealist[4]);

            $pgday = int(($ar2 + 2) / 3);

            #禁止エリア追加ログ
            &LOGSAVE("AREAADD") ;

            for ($cnt=0; $cnt<$ar2; $cnt++) {
                for ($i=0; $i<$#userlist+1; $i++) {
                    ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
                    if (($w_inf !~ /NPC0/) && ($fl !~ /終了/) && ($w_hit > 0)) {
                        if (($w_inf =~ /NPC/) && ($ar2 < 21)) {
                            $w_pls = $ara[$ar2 + int(rand(22 - $ar2))];
                        } elsif ($place[$w_pls] eq $place[$ara[$cnt]]) {
                            &LOGSAVE("DEATHAREA") ;
                            $w_hit=0;$w_death=$deth;
                        }
                    }

                    if($w_tactics eq "防御重視" && $pgday > $tactlim) { $w_tactics = "通常"; }
                    $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os,\n" ;
                }
            }

            open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
            open(DB,">".$u_save_dir."user$pgday$u_save_file"); seek(DB,0,0); print DB @userlist; close(DB);
            $ar = $ar2;
            if ($pgday >= 8) {
                require "$LIB_DIR/adlib.cgi";
                &InitResetTime;
            }
        }
    }

($secc,$minc,$hourc,$mdaycook,$monthc,$yearc,$wdayc,$ydayc,$isdstc) = localtime($now + $save_limit*86400);
$weekcook = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') [$wdayc];
$mdaycook = "0$mdaycook" if ($mdaycook < 10);
$monthcook = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') [$monthc];
$yearcook = $yearc+1900;
$expires = "$weekcook, $mdaycook-$monthcook-$yearcook 00:00:00 GMT";

1
