#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
require "$LIB_DIR/lib2.cgi";


&LOCK ;

require "pref.cgi";
if ($lim_sec) { require "$LIB_DIR/post.cgi"; }

&DECODE;
    # 他サイトからのアクセスを排除
    if ($base_url && !$okflag) {
        local($url_ok) = 0;
        $ref_url = $ENV{'HTTP_REFERER'};
        $ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        foreach $kyoka_url(@base_list){
            if ($ref_url =~ /$kyoka_url/i) { $url_ok = 1; }
        }
        if(!$url_ok && $ref_url){ 
            $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host,keepout,$ref_url,\n";
            open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
            &ERROR("不正なアクセスです。");
        }
    }

    # GET メソッドを拒否
    if ($Met_Post && !$p_flag) {
        &ERROR("不正なアクセスです。");
    }
    # データ修復中の投稿排除
    if ($d_ricovor) {
        &ERROR("データメンテナンス中です。ちょっとだけお待ち下さい。");
    }
&CREAD ;
&IDCHK;

if ($mode eq "main") { &MAIN; }
elsif ($mode eq "command") { &COM; }
else { &ERROR("不正なアクセスです。") ; }
&UNLOCK;
exit;

#==================#
# ■ メイン処理    #
#==================#
sub MAIN {

    #画面表示（スタート地点）

    &HEADER;
    &STS();
    &FOOTER;

}
#==================#
# ■ コマンド処理  #
#==================#
sub COM {

    if ($Command eq "MOVE") {          #移動？
        &MOVE;
    } elsif (($Command eq "ACTION") && ($Command3 eq "SEARCH")) {  #探索
        &SEARCH;
    } elsif (($Command eq "ACTION") && ($Command3 eq "HEAL")) {    #治療
        &HEAL;
    } elsif (($Command eq "ACTION") && ($Command3 eq "INN")) {     #睡眠
        &INN;
    } elsif (($Command eq "ACTION") && ($Command3 eq "KYUKEI")) {     #睡眠
        &KYUKEI;
    } elsif ($Command =~ /ITEM_/) {   #アイテム使用
        require "$LIB_DIR/item.cgi";
        &ITEM;
    } elsif ($Command eq "ITEMDEL") { #アイテム投棄
        require "$LIB_DIR/item.cgi";
        &ITEMDEL;
    } elsif (($Command =~ /SEIRI_/) && ($Command2 =~ /SEIRI2_/)) { #アイテム整理
        require "$LIB_DIR/itemsei.cgi";
        &ITEMSEIRI;
    } elsif (($Command =~ /^BUNKATU_[0-9]$/) && ($Command2 =~ /^[0-9]+$/)) { #アイテム分割
        require "$LIB_DIR/itembun.cgi";
        &ITEMBUNKATU;
    } elsif (($Command =~ /GOUSEI_/) && ($Command2 =~ /GOUSEI2_/)) { #アイテム合成
        require "$LIB_DIR/itemgou.cgi";
        &ITEMGOUSEI;
    }elsif(($Command =~ /ITSEND_/)&&($Command2 =~ /ITSEND_/)) {    #アイテム譲渡
        require "$LIB_DIR/itsend.cgi";
        &ITEMSEND;
    } elsif ($Command =~ /WEPKAI2_/) {  #装備外す
        require "$LIB_DIR/item.cgi";
        &WEPKAI;
    } elsif ($Command =~ /WEPDEL2_/) {  #装備捨てる
        require "$LIB_DIR/item.cgi";
        &WEPDEL;
    } elsif (($Command eq "ITMAIN") && ($Command4 eq "SPLIT")) { #アイテム分解
        require "$LIB_DIR/item.cgi";
        &SPLIT;
    } elsif ($Command eq "KOUDOU") {    #基本方針
        &KOUDOU;
    } elsif ($Command =~ /POI_/) {      #毒物混入
        require "$LIB_DIR/poison.cgi";
        &POISON;
    }elsif($Command =~ /ATPS_/) {       #毒中和
        require "$LIB_DIR/poison.cgi";
        &ANTIPS;
    } elsif ($Command =~ /PSC_/) {      #毒見
        require "$LIB_DIR/poison.cgi";
        &PSCHECK;
    } elsif ($Command =~ /OUK_/) {      #応急処置
        &OUKYU;
    } elsif ((($Command eq "SPECIAL") && ($Command6 eq "MESSAGE")) || ($Command eq "MESSAGE")) {   #メッセンジャー（受信）
        $log = ($log . "メッセージ機能を使用します。<BR>");
        &HEADER;
        require "$LIB_DIR/brmes.cgi";
        &MESMAIN;
        &FOOTER;
    } elsif ($Command =~ /SENDMES_/) {  #メッセンジャー（送信）
        require "$LIB_DIR/brmes.cgi";
        &SENDMES;
    } elsif (($msg2 ne "")||($dmes2 ne "")||($com2 ne "")||($a_name2 ne "")) {  #口癖変更
        &WINCHG;
    } elsif (($group2 ne "") && ($gpass2 ne "")) {  #所属変更
        &GRPCHG;
    } elsif ($Command =~ /CATCHG2_/) {  #反撃設定
        &CATCHG;
    } elsif (($Command eq "SPEAKER") && ($speech ne "")) { #携帯スピーカ使用
        require "$LIB_DIR/speaker.cgi";
        &SPEAKER;
    } elsif ($Command eq "HACK2") {    #ハッキング
        require "$LIB_DIR/hack.cgi";
        &HACKING;
    } elsif ($Command =~ /GET_/) {    #戦利品
        &WINGET;
    } elsif ($Command =~ /ATK/) {     #攻撃
        require "attack.cgi";
        &ATTACK1;
    } elsif ($Command eq "RUNAWAY") { #逃亡
        require "attack.cgi";
        &RUNAWAY;
    }

    if(($Command =~ /BATTLE/)||($Command =~ /ATK/)) {   #戦闘結果
        &HEADER;
        require "attack.cgi";
        &BATTLE;
        &FOOTER;
    } elsif ($mflg ne "ON") {
        &MAIN;
    }
}
#==================#
# ■ コマンド処理  #
#==================#
sub MOVE {

    local($mv) = $Command2;
    $mv =~ s/MV//g ;

    ($ar[0],$ar[1],$ar[2],$ar[3],$ar[4],$ar[5],$ar[6],$ar[7],$ar[8],$ar[9],$ar[10],$ar[11],$ar[12],$ar[13],$ar[14],$ar[15],$ar[16],$ar[17],$ar[18],$ar[19],$ar[20],$ar[21]) = split(/,/, $arealist[2]);
    ($war,$a) = split(/,/, $arealist[1]);
    if(($ar[$war] eq $place[$mv])||($ar[$war+1] eq $place[$mv])||($ar[$war+2] eq $place[$mv])) {
        $log = ($log . "$place[$mv]に移動した。次にここは禁止エリアになってしまうな。<br>$arinfo[$mv]<br>") ;
    } else {
        if (($inf !~ /NPC/) && ($hackflg == 0)) {
            for ($i=0; $i<$war; $i++) {
                if (($ar[$i] eq $place[$mv])) {   #禁止エリア？
                    $log = ($log . "$place[$mv]は禁止エリアだ。移動することは出来ないな・・・。<BR>") ;
                    $Command = "MAIN";
                    return ;
                    $chkflg = 1 ;
                }
            }
        }
        $log = ($log . "$place[$mv]に移動した。<BR>$arinfo[$mv]<br>") ;
    }


    $pls = $mv ;
    $Command = "MAIN";

    if ($inf =~ /足/) {
        $sta -= int(rand(5) + 13) ;
    } elsif ($bou_f eq "陸上用シューズ<>DF") {
        $sta -= int(rand(5))+5 ;
    } else {
        $sta -= int(rand(5))+8 ;
    }

    if ($tactics eq "連闘行動") { $sta -= 4; }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("mov");
    }

    if ($inf =~ /毒/) {
        $hit -= int(rand(5))+8 ;
        if ($hit <= 0) {
            $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
            &LOGSAVE("DEATH") ; #死亡ログ
            $mem--; if ($mem == 1) { &LOGSAVE("WINEND1") ; }
            &SAVE;
        }
    }

    if ($hit <= 0) { return; }

    &SEARCH2;

    &SAVE;

}
#==================#
# ■ 探索処理      #
#==================#
sub SEARCH {

    $log = ($log . "$l_nameは、辺りを探索した・・・。<br>") ;

    if ($inf =~ /足/) {
        $sta -= int(rand(5) + 23) ;
    } elsif ($bou_f eq "陸上用シューズ<>DF") {
        $sta -= int(rand(5))+13;
    } else {
        $sta -= int(rand(5))+18 ;
    }

    if ($tactics eq "連闘行動") { $sta -= 4; }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("mov");
    }

    if ($inf =~ /毒/) {
        $hit -= int(rand(5))+18 ;
        if ($hit <= 0) {
            $log = ($log . "<font color=\"red\"><b>$f_name $l_name（$cl $sex$no番）は死亡した。</b></font><br>") ;
            &LOGSAVE("DEATH") ; #死亡ログ
            $mem--; if ($mem == 1) { &LOGSAVE("WINEND1") ; }
            &SAVE;
        }
    }

    if ($hit <= 0) { return; }

    &SEARCH2;

    if ($chksts ne "OK") {
        $log = ($log . "しかし、何も見つからなかった。<BR>") ;
        $Command = "MAIN" ;
    }

    &SAVE;
}

#==================#
# ■ 探索処理2     #
#==================#
sub SEARCH2 {

    local($i) = 0 ;
    local($j) = 0;

    local($dice1) = int(rand(10)) ; #敵、アイテムどちらを発見

    &TACTGET ;

    $chksts="NG";$chksts2="NG";

    if ($dice1 <= 5) {  #敵発見？
        for ($i=0; $i<$#userlist+1; $i++) {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
            push(@plist,$i) if (($w_pls eq $pls) && ($w_id ne $id) && (($w_bid ne $group) || ($tactics eq "連闘行動")));
        }

        for ($i=$#plist; $i>=0; $i--) {
            $j = int(rand($i+1));
            if ($i == $j) { next; }
            @plist[$i, $j] = @plist[$j, $i];
        }

        foreach $i(@plist){
            local($dice2) = int(rand(10)) ; #敵、アイテム発見
            local($dice3) = int(rand(10)) ; #先制攻撃

            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);

            &TACTGET2 ;

            if (($tactics eq "連闘行動") && ($tactics eq "連闘行動")) {
                $w_bid2 = "";
            } else {
                $w_bid2 = $w_bid;
            }

            if (($w_pls eq $pls) && ($w_id ne $id) && ($w_bid2 ne $group)) {    #場所一致他プレイヤー？
                local($chk) = int($dice2 * $sen);

                if ($chk < $chkpnt) {
                    if ($w_hit > 0) {
                        if (($group ne $w_group) || ($gpass ne $w_gpass) || ($pgday >= 7 && !$hackflg) || ($tactics eq "連闘行動")) {
                            $wf = $w_id; #ブラウザバック対処用
                            local($chk2) = int($dice3 * $sen2);
                            if ($chk2 <= $chkpnt2) {   #先制攻撃
                                require "attack.cgi";
                                &ATTACK ;$chksts="OK";$chksts2="NG";last;
                            } else {    #奇襲
                                $Index2 = $i;
                                $w_bid = $group ;
                                $bid = $w_group ;
                                require "attack.cgi";
                                &ATTACK2 ;$chksts="OK";$chksts2="NG";last;
                            }
                        }
                    } else {
                        local($chkflg) = 0 ;
                        local($dice4) = int(rand(10));
                        #if ($dice4 > 8){
                            for ($j=0; $j<6; $j++) {
                                if ($w_item[$j] ne "なし" && $w_item[$j] ne "") {
                                    $chkflg=1;
                                    last;
                                }
                            }
                            unless ($chkflg){
                                if ($w_wep !~ /素手/ || $w_bou !~ /下着/ || $w_bou_h ne "なし" || $w_bou_f ne "なし" ||$w_bou_a ne "なし") { $chkflg = 1; }
                            }
                            if ($chkflg == 1) { #死体発見？
                                $w_bid = $group ;
                                $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,-1,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os,\n" ;
                                open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
                                $wf = $w_id; #ブラウザバック対処用
                                &DEATHGET ;last;
                            }
                        #}
                    }
                } else { $chksts2="OK";}
            }
        }
        if ($chksts2 eq "OK") {
            $log = ($log . "何者かが潜んでいる気配がする・・・。気のせいか？<BR>") ;
        }
    } else {
        $dice2 = int(rand(10)) ;    #敵、アイテム発見
        if (($dice2 < $chkpnt) && ($Command eq "ACTION") && ($Command3 eq "SEARCH")) { #アイテム発見
            require "$LIB_DIR/item.cgi";
            &ITEMGET;
        } else {
            require "$LIB_DIR/event.cgi";
            &EVENT ;
        }
    }
}

#==================#
# ■ 治療処理      #
#==================#
sub HEAL {

    $sts = "治療";
    $endtime = $now ;
    $Command = "HEAL2" ;

    &SAVE;
    &u_save;
}

#==================#
# ■ 睡眠処理      #
#==================#
sub INN {

    $sts = "睡眠";
    $endtime = $now ;
    $Command = "INN2" ;

    &SAVE;
    &u_save;
}

#==================#
# ■ 戦利品取得    #
#==================#
sub WINGET {

    if ($item[$itno2] ne "なし" or $itno2>4 or $itno2<0) {
        $log = ($log . "それ以上所持品をもてない。<br>") ;
        $Command = "MAIN";
        return;
    }
    if ($getid eq $id){
        $log = ($log . "自分で自分の持ち物を奪ってみた。<br>空しい・・・。<br>") ;
        $Command = "MAIN";
        return;
    }

    local($wk) = $Command;
    $wk =~ s/GET_//g;
    $wk+=0;
    $wk=int($wk);
    local($witem,$weff,$witai);

    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist[$i]);
        if ($w_id eq $getid) {
            &BB_CK; #ブラウザバック対処
            if ($w_hit>0 || ($group eq $w_bid && $w_sta>-1)){
                $log = ($log . "$w_f_nameのあの持ち物が欲しいと強く念じてみた。<br>空しい・・・。<br>") ;
                $Command = "MAIN";
                return;
            }

            if ($wk==6) {
                ($witem,$weff,$witai) = ($w_wep,$w_watt,$w_wtai);
                $w_wep = "素手<>WP"; $w_watt = 0; $w_wtai = "∞";
            }elsif ($wk==7) {
                ($witem,$weff,$witai) = ($w_bou,$w_bdef,$w_btai);
                $w_bou = "下着<>DN"; $w_bdef = 0; $w_btai = "∞";
            }elsif ($wk==8) {
                ($witem,$weff,$witai) = ($w_bou_h,$w_bdef_h,$w_btai_h);
                $w_bou_h = "なし"; $w_bdef_h = $w_btai_h = 0;
            }elsif ($wk==9) {
                ($witem,$weff,$witai) = ($w_bou_f,$w_bdef_f,$w_btai_f);
                $w_bou_f = "なし"; $w_bdef_f = $w_btai_f = 0;
            }elsif ($wk==10) {
                ($witem,$weff,$witai) = ($w_bou_a,$w_bdef_a,$w_btai_a);
                $w_bou_a = "なし"; $w_bdef_a = $w_btai_a = 0;
            } else {
                ($witem,$weff,$witai) = ($w_item[$wk],$w_eff[$wk],$w_itai[$wk]);
                $w_item[$wk] = "なし"; $w_eff[$wk]=$w_itai[$wk] = 0;
            }
            $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$id,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os,\n" ;
            open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
            last;
        }
    }

    if ($witem!~/^(なし|素手|下着)$/ && $i!=$#userlist+1){
        $item[$itno2] = $witem ;
        $eff[$itno2] = $weff; $itai[$itno2] = $witai ;
        ($witem)=split(/<>/,$witem,2);
        $log = ($log . "$l_name は $witemを手に入れた。<BR>") ;
        &SAVE;
    }else{
        $log = ($log . "拾うのを諦めた。<BR>") ;
    }


    $Command = "MAIN";
}

#==================#
# ■ 口癖変更処理  #
#==================#
sub WINCHG {

    $log = ($log . "口癖を変更しました。<br>") ;
    $msg = $msg2;
    $dmes = $dmes2 ;
    $com = $com2 ;
    $a_name = $a_name2 ;
    if ($gpass2 ne "") { $gpass = $gpass2; }

    &SAVE ;

    $Command = "MAIN" ;

}

#==================#
# ■ 所属変更処理  #
#==================#
sub GRPCHG {

    #人数チェック
    $grpmem = $gpsmem = 0;
    foreach $userlist(@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist);
        if ($w_id ne $id) {
            if ($group2 eq $w_group) { $grpmem++; }
            if ($gpass2 eq $w_gpass) { $gpsmem++; }
        }
    }

    if ($group ne $group2) {
        if ($grpmem < 6) {
            $sta -= $group_sta;
            if ($sta <= 0) { &DRAIN("com"); }
            if ($hit <= 0) { &SAVE; return; }
            $group = $group2;
            $log = ($log . "グループ名を「$group2」に設定しました。<br>");
        } else {
            $log = ($log . "人数オーバーのため、グループ名を「$group2」に設定できませんでした。<br>");
        }
    }

    if ($gpass ne $gpass2) {
        if ($gpsmem < 6) {
            $gpass = $gpass2;
            $log = ($log . "グループパスを「$gpass2」に設定しました。<br>");
        } else {
            $log = ($log . "人数オーバーのため、グループパスを「$gpass2」に設定できませんでした。<br>");
        }
    }

    &SAVE ;

    $Command = "MAIN" ;

}
#==================#
# ■ 死体発見処理  #
#==================#
sub DEATHGET {

    $log = ($log . "$w_f_name $w_l_nameの死体を発見した。<br>") ;

    if ($w_death =~ /斬殺/) {
        if ($w_com == 0) {$log = ($log . "頭部が首の皮一枚でつながってる状態だ・・・。首を刎ねられたようだ。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "腹部が鋭利な刃物のようなもので裂かれて、内臓がはみ出している・・・。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "肩口から胸にかけての袈裟切りだ。見事に切り裂かれてる・・・。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "首・胴・両腕・両足が分断されている。こういう事が正気の人間に出来るのだろうか・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "顔を集中的に切り刻まれている。生前の面影など全く無い・・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "腹部を切り裂かれているが、よく見ると手首にも切り傷が数多くある・・・。<BR>相手に切られた後に自殺をしようと思ったのだろうか？<br>") ;}
        else {$log = ($log . "頭から胸にかけて無残に切り裂かれている・・・。<br>") ;}
    }elsif ($w_death =~ /射殺/) {
        if ($w_com == 0) {$log = ($log . "額に一本の矢が突き刺さっている・・・。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "背中に何本も矢が刺さっている。逃げようとした所、背後から射られたようだ。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "心臓の場所に一本正確に矢が刺さっている。相当な腕の持ち主だろう・・・。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "足と頭に矢が立っている。足を射て、逃げれなくさせておいてから急所を射たようだ・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "壁に矢で縫い付けられたようになっている・・・ゴルゴダの丘で処刑された聖者のような体勢だ・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "何本もの矢がささり、ハリネズミのようになっている・・・。<br>") ;}
        else {$log = ($log . "首に数本の矢が刺さっている・・・。一本は顎の下に突き抜けている・・・。<br>") ;}
    }elsif ($w_death =~ /銃殺/) {
        if ($w_com == 0) {$log = ($log . "胸に・・・３発、額に１発の弾痕がある・・・。額の一発が致命傷になったみたいだ・・・。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "腹部に数発の弾痕があり、血が流れ出している。しかし、その血ももう乾いている。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "頭が原形をとどめていない位吹き飛んでいる・・・。名札から辛うじて名前が分かったくらいだ。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "胸に数発。そして、脳髄が吹き飛んでいる。殺した後、口に銃を突っ込んで撃ったんだろう。ふざけたことをしている・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "腹部にぽっかり穴があり、向こう側が見える。これじゃ絶対生きていれないな・・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "顔に何発もの弾痕がある・・・。恨みでもあったのであろうか。<br>") ;}
        else {$log = ($log . "右頭部が激しく損傷し、脳が流れ出している・・・・。<br>") ;}
    }elsif ($w_death =~ /爆殺/) {
        if ($w_com == 0) {$log = ($log . "そこらじゅうに、体のパーツが分散している。派手にやられたみたいだ・・・。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "両足が吹き飛ばされている。腕だけで這って逃げようとしたのか・・・。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "爆弾にでも攻撃されたのであろうか、頭と右腕しか残っていない・・・。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "爆弾に吹き飛ばされたのであろうか、頭が半分欠けて中身がのぞいている・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "爆風で吹き飛ばされた片腕が、５ｍほど先にころがっている・・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "死体というより、肉の塊だな・・・。<br>") ;}
        else {$log = ($log . "首と手が見当たらないな・・・。爆風で吹き飛ばされたんだろうか・・・。<br>") ;}
    }elsif ($w_death =~ /撲殺/) {
        if ($w_com == 0) {$log = ($log . "腹を抑えた体制で、うずくまっているが・・・どうやら、そのまま息絶えたようだ・・・。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "相当派手に殴られたみたいだ・・・。顔が紫に腫れ上がっている・・・。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "首の骨が折られ、首から骨が突き出ている・・・。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "地面に顔を埋め、大量の血を顔面から流している・・。倒れた所、後頭部を殴打されたようだ。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "後ろから鈍器のようなもので殴られたのだろうか？頭を抱えたまま倒れている・・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "額が割れ、血と脳漿がながれている。真正面から激しく殴られたようだな・・。<br>") ;}
        else {$log = ($log . "首が見事に横に向いている。どうみても、首の骨が折れているな・・・。<br>") ;}
    }elsif ($w_death =~ /刺殺/) {
        if ($w_com == 0) {$log = ($log . "全身に、何か鋭利な刃物で刺された傷が、大量にある・・・。死体の回りは、血の海だ・・・。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "馬乗りになられて、何度も何度も刺されたような痕跡がある・・・。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "心臓を一突き。未だに傷から血が湧き出ている・・・。殺されたのはつい先程のようだ。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "喉を刺されている・・。目は白目をむいている・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "後ろから腹部を刺されて倒れている。不意打ちだったのだろうか・・？<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "左腹部が激しく損傷している。刺した後、えぐったような傷がある・・・。<br>") ;}
        else {$log = ($log . "両目が、なにかで刺されている・・・。血の涙を流しているようだ・・・。<br>") ;}
    }elsif ($w_death =~ /毒/) {
        if ($w_com == 0) {$log = ($log . "毒物を口にしたのかな・・？嘔吐した形跡もある・・・。<br>\n") ;}
        elsif ($w_com == 1) {$log = ($log . "口から一筋の血が流れている。ぱっとみは、眠っているようにしかみえないな・・・。<br>\n") ;}
        elsif ($w_com == 2) {$log = ($log . "死体に顔を近づけると特有のアーモンド臭がある。毒殺されたのか・・・。<br>\n") ;}
        elsif ($w_com == 3) {$log = ($log . "毒殺されたのか。口から大量の血の混じった泡を吹いている・・・。<br>\n") ;}
        elsif ($w_com == 4) {$log = ($log . "毒を飲んで苦しんだんだろうか。喉を自分で激しく爪でかきむしっている・・・。<br>\n") ;}
        elsif ($w_com == 5) {$log = ($log . "何者かに毒薬でもかけられたのか？皮膚が激しく変色している・・・。<br>\n") ;}
        else {$log = ($log . "皮膚がどす黒い色に変色して、口からは大量の血を吐いている・・・。<br>\n") ;}
    } else {
        $log = ($log . "無残にも仰向けに転がっている・・・。<br>") ;
    }
    $log = ($log . "デイパックの中身を物色させてもらうか・・・。<br>") ;
    $Command = "DEATHGET";

    $chksts="OK";

}

#==================#
# ■ 応急処置処理  #
#==================#
sub OUKYU {

    local($wk) = $Command;
    $wk =~ s/OUK_//g;

    if ($wk == 0) { #頭
        $inf =~ s/頭//g ;
    }elsif ($wk == 1) { #腕
        $inf =~ s/腕//g ;
    }elsif ($wk == 2) { #腹部
        $inf =~ s/腹//g ;
    }elsif ($wk == 3) { #足
        $inf =~ s/足//g ;
    }elsif ($wk == 4) { #毒
        $inf =~ s/毒//g ;
    }elsif ($wk == 5) { #狂気
        $inf =~ s/狂//g ;
    }

    $log = ($log . "応急処置をした。<BR>") ;

    if ($club eq "保健委員") {
        $sta -= int($okyu_sta / 2);
    } else {
        $sta -= $okyu_sta;
    }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("com");
    }

    &SAVE ;

    $Command = "MAIN" ;
}

#==================#
# ■ 基本方針変更  #
#==================#
sub KOUDOU {

    local($wk) = $Command5;
    $wk =~ s/KOU_//g;

    if ($wk == 0) {
        $tactics = "通常";
    } elsif ($wk == 1) {
        $tactics = "攻撃重視";
    } elsif ($wk == 2) {
        $tactics = "防御重視";
    } elsif ($wk == 3) {
        $tactics = "隠密行動";
    } elsif ($wk == 4) {
        $tactics = "探索行動";
    } elsif ($wk == 5) {
        $tactics = "先制行動";
    } elsif ($wk == 6) {
        $tactics = "命中重視";
    } elsif ($wk == 7) {
        $tactics = "回避重視";
    } else {
        $tactics = "連闘行動";
    }

    $log = ($log . "基本方針を$tacticsに変更した。<BR>") ;

    &SAVE ;

    $Command = "MAIN" ;
}

#==================#
# ■ 反撃設定変更  #
#==================#
sub CATCHG {

    local($wk) = $Command;
    $wk =~ s/CATCHG2_//g;

    if ($wk eq "WB") {
        $we = "B";
    } elsif ($wk eq "WP") {
        $we = "P";
    } elsif ($wk eq "WA") {
        $we = "A";
    } elsif ($wk eq "WG") {
        $we = "G";
    } elsif ($wk eq "WN") {
        $we = "N";
    } elsif ($wk eq "WS") {
        $we = "S";
    } elsif ($wk eq "WD") {
        $we = "D";
    } elsif ($wk eq "WC") {
        $we = "C";
    } else {
        $we = "";
    }

    $log = ($log . "反撃方法を変更した。<BR>") ;

    &SAVE ;

    $Command = "MAIN" ;
}

#=============================#
# ■ ユーザ単位のデータセーブ #
#=============================#
sub u_save{

    local($u_dat) = "$id,$password,$f_name,$l_name,$sex,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg,$sts,$pls,$kill,$icon,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],,$dmes,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com,$inf,$group,$gpass,$a_name,$feel,$host,$os,\n" ;

    open(DB,">$u_save_dir$id$u_save_file"); seek(DB,0,0); print DB $u_dat; close(DB);

    $log = ($log . "セーブは正常に終了しました。<BR>") ;

}

#===========================#
# ■ ブラウザバック不正防止 #
#===========================#
sub BB_CK{

    if($wf eq $w_id){ $wf = ""; }else{ &ERROR("不正アクセスです") ; }

}
1
