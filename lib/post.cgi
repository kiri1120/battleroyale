#==================#
# ■ 連続投稿禁止  #
#==================#

    local($iplog) = "$ADM_DIR/post.log";  # 記録データファイル名

    open(IN,"$iplog"); @data = <IN>; close(IN);

    @new=();
    $flag=0;
    foreach (@data) {
        ($w_now,$w_host) = split(/<>/);

        if (($now - 60) > $w_now) { next; }
        elsif ($w_host eq $host) {
            if (($w_now + $lim_sec) > $now) { &ERROR("連続投稿制限をしています。もう少しゆっくり行動してください。"); }
            $_ = "$now<>$host<>\n";
            $flag=1;
        }
        push(@new,$_);
    }

    if (!$flag) {
        push(@new,"$now<>$host<>\n");
    }
    $playmem = @new;

    open(OUT,">$iplog"); seek(OUT,0,0); print OUT @new; close(OUT);

1
