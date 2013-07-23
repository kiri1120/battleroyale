#==================#
# ■ 叫ぶ          #
#==================#
sub SPEAKER {
    if ($club ne "応援団") {
        for ($i=0; $i<5; $i++){
            if ($item[$i] =~ /携帯スピーカ/) {
                last;
            }
        }
    }
    if (($item[$i] !~ /携帯スピーカ/) && ($club ne "応援団"))  {
        &ERROR("不正なアクセスです。");
    }

    $log = ($log . " $speech<BR>");
    $log = ($log . " ちゃんと伝わったかな？<BR>");
    open(DB,"$gun_log_file");seek(DB,0,0); @gunlog=<DB>;close(DB);
    $gunlog[2] = "$now,$place[$pls],$f_name $l_name,$speech,\n";
    open(DB,">$gun_log_file"); seek(DB,0,0); print DB @gunlog; close(DB);
    &LOGSAVE("SPEAKER");

    $Command = "MAIN" ;

}
1
