#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
require "$LIB_DIR/lib2.cgi";

&LOCK ;

require "pref.cgi";

&DECODE;
    # 他サイトからのアクセスを排除
    if ($base_url) {
        local($url_ok) = 0;
        foreach $kyoka_url(@base_list){
            $ref_url = $ENV{'HTTP_REFERER'};
            $ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
            if ($ref_url =~ /$kyoka_url/i) { $url_ok = 1; }
        }
        if(!$url_ok){ &ERROR("不正なアクセスです。");}
    }
    # GET メソッドを拒否
    if ($Met_Post && !$p_flag) {
        &ERROR("不正なアクセスです。");
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

    if($Command =~ /MV/) {          #移動？
        &MOVE;
    }elsif($Command eq "SEARCH") {  #探索
        &SEARCH;
    }elsif($Command =~ /ITEM_/) {   #アイテム使用
        require "$LIB_DIR/item.cgi";
        &ITEM;
    }elsif($Command =~ /DEL_/) {    #アイテム投棄
        require "$LIB_DIR/item.cgi";
        &ITEMDEL;
    }elsif(($Command =~ /SEIRI_/)&&($Command2 =~ /SEIRI2_/)) { #アイテム整理
        require "$LIB_DIR/itemsei.cgi";
        &ITEMSEIRI;
    }elsif(($Command =~ /GOUSEI_/)&&($Command2 =~ /GOUSEI2_/)) { #アイテム合成
        require "$LIB_DIR/itemgou.cgi";
        &ITEMGOUSEI;
    }elsif($Command eq "HEAL") {    #治療
        &HEAL;
    }elsif($Command eq "INN") {     #睡眠
        &INN;
    }elsif($Command =~ /POI_/) {    #毒物混入
        require "$LIB_DIR/poison.cgi";
        &POISON;
    }elsif($Command =~ /PSC_/) {    #毒見
        require "$LIB_DIR/poison.cgi";
        &PSCHECK;
    }elsif($Command =~ /GET_/) {    #戦利品
        &WINGET;
    }elsif($Command =~ /OUK_/) {    #応急処置
        &OUKYU;
    }elsif(($msg2 ne "")||($dmes2 ne "")||($com2 ne "")) {          #口癖変更
        &WINCHG;
    }elsif($Command eq "WEPDEL") {  #武器外す
        require "$LIB_DIR/item.cgi";
        &WEPDEL;
    }elsif($Command eq "WEPDEL2") { #武器捨てる
        require "$LIB_DIR/item.cgi";
        &WEPDEL2;
    }elsif($Command eq "WEPPNT") {  #熟練度確認
        &WEPPNT;
    }elsif($Command eq "DEFCHK") {  #装備確認
        &DEFCHK;
    }elsif($Command eq "SPEAKER") { #携帯スピーカ使用
        require "$LIB_DIR/speaker.cgi";
        &SPEAKER;
    }elsif($Command eq "HACK") {   #ハッキング
        require "$LIB_DIR/hack.cgi";
        &HACKING;
    }elsif($Command =~ /ATK/) {     #攻撃
        require "attack.cgi";
        &ATTACK1;
    }elsif($Command eq "RUNAWAY") { #逃亡
        require "attack.cgi";
        &RUNAWAY;
    }elsif($Command eq "BSAVE") {   #バックアップ保存
        require "admin.cgi";
        &BACKSAVE;
    }elsif($Command eq "BREAD") {   #バックアップ読出
        require "admin.cgi";
        &BACKREAD;
    }elsif($Command eq "RESET") {   #データ初期化
        require "admin.cgi";
        &DATARESET;
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

    local($mv) = $Command;
    $mv =~ s/MV//g ;

    ($ar[0],$ar[1],$ar[2],$ar[3],$ar[4],$ar[5],$ar[6],$ar[7],$ar[8],$ar[9],$ar[10],$ar[11],$ar[12],$ar[13],$ar[14],$ar[15],$ar[16],$ar[17],$ar[18],$ar[19],$ar[20],$ar[21]) = split(/,/, $arealist[2]);
    ($war,$a) = split(/,/, $arealist[1]);
    if(($ar[$war] eq $place[$mv])||($ar[$war+1] eq $place[$mv])||($ar[$war+2] eq $place[$mv])) {
        $log = ($log . "$place[$mv]に移動した。次にここは禁止エリアになってしまうな。<br>$arinfo[$mv]<br>") ;
    } else {
        $log = ($log . "$place[$mv]に移動した。<BR>$arinfo[$mv]<br>") ;
        for ($i=0; $i<$war; $i++) {
            if (($ar[$i] eq $place[$mv]) && ($hackflg == 0)) {   #禁止エリア？
                $log = ("$place[$mv]は禁止エリアだ。移動することは出来ないな・・・。<BR>") ;
                $Command = "MAIN";
                return ;
                $chkflg = 1 ;
            }
        }
    }


    $pls = $mv ;
    $Command = "MAIN";

    if ($inf =~ /足/) {
        $sta -= int(rand(5) + 13) ;
    } elsif ($club eq "陸上部") {
        $sta -= int(rand(5))+5 ;
    } else {
        $sta -= int(rand(5))+8 ;
    }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("mov");
    }

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
    } elsif ($club eq "陸上部") {
        $sta -= int(rand(5))+13;
    } else {
        $sta -= int(rand(5))+18 ;
    }

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("mov");
    }

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
    srand(time ^ $i) ;

    srand($now);
    local($a) = int(rand(1)) ;  #敵、アイテムどちらを発見
    local($dice1) = int(rand(10)) ; #敵、アイテムどちらを発見

    &TACTGET ;

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    $chksts="NG";$chksts2="NG";

    if ($dice1 <= 5) {  #敵発見？
        for ($i=0; $i<$#userlist+1; $i++) {
            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);
    push(@plist,$i) if (($w_pls eq $pls) && ($w_id ne $id) && ($w_bid ne $id));
        }

    for ($i=0;$i<@plist+5;$i++){
    push(@plist,splice(@plist,int(rand @plist+0),1));
    }

    foreach $i(@plist){
            local($dice2) = int(rand(10)) ; #敵、アイテム発見
            local($dice3) = int(rand(10)) ; #先制攻撃

            ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);

            &TACTGET2 ;

            if (($w_pls eq $pls) && ($w_id ne $id) && ($w_bid ne $id)) {    #場所一致他プレイヤー？
                local($chk) = int($dice2 * $sen);

                if ($chk < $chkpnt) {
                    if ($w_hit > 0) {
                        $wf = $w_id; #ブラウザバック対処用
                        if ($dice3 <= $chkpnt2) {   #先制攻撃
                            require "attack.cgi";
                            &ATTACK ;$chksts="OK";$chksts2="NG";last;
                        } else {    #奇襲
                            $Index2 = $i;
                            $w_bid = $id ;
                            $bid = $w_id ;
                            require "attack.cgi";
                            &ATTACK2 ;$chksts="OK";$chksts2="NG";last;
                        }
                    } else {
                        local($chkflg) = 0 ;
                        local($dice4) = int(rand(10));
                        if ($dice4 > 8){
                            for ($j=0; $j<6; $j++) {
                                if ($w_item[$j] ne "なし" && $w_item[$j] ne "") {
                                    $chkflg=1;
                                    last;
                                }
                            }
#)))))))))))))))))))))))))))))
unless ($chkflg){if ($w_wep !~ /素手/ || $w_bou !~ /下着/ || $w_bou_h ne "なし" || $w_bou_f ne "なし" ||$w_bou_a ne "なし")
{$chkflg=1}}
#)))))))))))))))))))))))))))))
                        if ($chkflg == 1) { #死体発見？
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
$userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,-1,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$id,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,\n" ;
open(DB,">$user_file"); seek(DB,0,0); print DB @userlist; close(DB);
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                            $wf = $w_id; #ブラウザバック対処用
                            &DEATHGET ;last;
                        }
                    }}
                }else{ $chksts2="OK";}
            }
        }
        if ($chksts2 eq "OK") {
            $log = ($log . "何者かが潜んでいる気配がする・・・。気のせいか？<BR>") ;
        }
    } else {
        $dice2 = int(rand(10)) ;    #敵、アイテム発見
        if (($dice2 < $chkpnt)&&($Command eq "SEARCH")) { #アイテム発見
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
}

#==================#
# ■ 睡眠処理      #
#==================#
sub INN {

    $sts = "睡眠";
    $endtime = $now ;
    $Command = "INN2" ;
    &SAVE;

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

    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    for ($i=0; $i<$#userlist+1; $i++) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist[$i]);
        if ($w_id eq $getid) {
            &BB_CK; #ブラウザバック対処
            if ($w_hit>0 || ($id eq $w_bid && $w_sta>-1)){
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
            $userlist[$i] = "$w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$id,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,\n" ;
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
    }elsif ($w_death =~ /絞殺/) {
        if ($w_com == 0) {$log = ($log . "何かで首を締められたのだろうか・・・。口からは大量の吐しゃ物を撒き散らしている。<br>") ;}
        elsif ($w_com == 1) {$log = ($log . "絞殺体か・・・恨めしそうにこちらに視線を向けている。<br>") ;}
        elsif ($w_com == 2) {$log = ($log . "何かで首を絞められたのであろうか。舌を出し、白目を向いて無残な姿だ・・・。<br>") ;}
        elsif ($w_com == 3) {$log = ($log . "誰かに首を絞め殺されたようだ。失禁している・・・。<br>") ;}
        elsif ($w_com == 4) {$log = ($log . "首を締められながら激しく抵抗したんだろうか。爪には肉のようなものが食い込んでいる・・。<br>") ;}
        elsif ($w_com == 5) {$log = ($log . "首吊り死体だ・・・殺された後、吊るされたとしか考えられないな・・・。<br>") ;}
        else {$log = ($log . "首筋に、何かで締め付けられたような紫色の痣がある・・・。<br>") ;}
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
# ■ 熟練度確認処理#
#==================#
sub WEPPNT {

    $log = ("現在の熟練レベルは・・・<br>") ;

    local($p_wa) = int($wa/$BASE);
    local($p_wb) = int($wb/$BASE);
    local($p_wc) = int($wc/$BASE);
    local($p_wd) = int($wd/$BASE);
    local($p_wg) = int($wg/$BASE);
    local($p_ws) = int($ws/$BASE);
    local($p_wn) = int($wn/$BASE);
    local($p_wp) = int($wp/$BASE);

    $log = ($log . "<BR>所属クラブ：$club<br><br>") ;
    $log = ($log . "　射：$p_wa($wa)　棍：$p_wb($wb)　投：$p_wc($wc)　爆：$p_wd($wd)<br>") ;
    $log = ($log . "　銃：$p_wg($wg)　刺：$p_ws($ws)　斬：$p_wn($wn)　殴：$p_wp($wp)<br>") ;

}
#==================#
# ■ 装備確認処理  #
#==================#
sub DEFCHK {

    local($w_name,$w_kind) = split(/<>/, $wep);
    local($b_name,$b_kind) = split(/<>/, $bou);
    local($b_name_h,$b_kind_h) = split(/<>/, $bou_h);
    local($b_name_f,$b_kind_f) = split(/<>/, $bou_f);
    local($b_name_a,$b_kind_a) = split(/<>/, $bou_a);
    local($b_name_i,$b_kind_i) = split(/<>/, $item[5]);

    $log = ("現在装備している防具は・・・<br><br>") ;

    $log = ($log . "　武　：　$w_name/$watt/$wtai<br>") ;
    $log = ($log . "　体　：　$b_name/$bdef/$btai<br>") ;
    $log = ($log . "　頭　：　$b_name_h/$bdef_h/$btai_h<br>") ;
    $log = ($log . "　腕　：　$b_name_a/$bdef_a/$btai_a<br>") ;
    $log = ($log . "　足　：　$b_name_f/$bdef_f/$btai_f<br>") ;
    $log = ($log . "　飾　：　$b_name_i/$eff[5]/$itai[5]<br>") ;

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
    }

    $log = ($log . "応急処置をした。<BR>") ;

    $sta -= $okyu_sta ;

    if ($sta <= 0) {    #スタミナ切れ？
        &DRAIN("com");
    }

    &SAVE ;

    $Command = "MAIN" ;
}

#===========================#
# ■ ブラウザバック不正防止 #
#===========================#
sub BB_CK{

    if($wf eq $w_id){ $wf = ""; }else{ &ERROR("不正アクセスです") ; }

}

1