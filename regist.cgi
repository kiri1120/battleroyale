#!/usr/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
require "$LIB_DIR/lib2.cgi";
&LOCK;
require "pref.cgi";

&DECODE;
&CREAD ;

# データ修復中の投稿排除
if ($d_ricovor) { &ERROR("データメンテナンス中です。ちょっとだけお待ち下さい。"); }

if ($mode eq "regist") { &REGIST; }
elsif ($mode eq "info") { &INFO; }
elsif ($mode eq "info2") { &INFO2; }
elsif ($mode eq "icon") { &ICON; }
else { &MAIN; }
&UNLOCK;
exit;

#==================#
# ■ メイン        #
#==================#
sub MAIN {

&Checker;

&HEADER;
print <<"_HERE_";
<P align="center"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">転校手続き</FONT></B><BR><BR>
<BR>
<img src="$imgurl$n_icon_file[$#n_icon_file]"><BR><BR>
『君が転校生だね？僕が担任です。<BR>
生徒からは、「とんぼ」とかいわれてるけどね。<BR>
あ、そんな事はどうでもいいね。<BR>
<BR>
とりあえず、ここに氏名と、性別を記入して、<BR>
提出してもらえるかな？</P>
<CENTER>
<FORM METHOD="POST">
<INPUT TYPE="HIDDEN" NAME="mode" VALUE="regist">
姓：<INPUT size="16" type="text" name="F_Name" maxlength="16"><BR>
名：<INPUT size="16" type="text" name="L_Name" maxlength="16"><BR>
愛称：<INPUT size="16" type="text" name="A_Name" maxlength="16"><BR>
<BR>
性別：<SELECT name="Sex">
  <OPTION value="NOSEX" selected>- 性別 -</OPTION>
  <OPTION value="男子">男子</OPTION>
  <OPTION value="女子">女子</OPTION>
</SELECT>
_HERE_

    print "　アイコン：<SELECT name=\"Icon\">\n";
    print "<OPTION value=\"NOICON\" selected>- アイコン -</OPTION>\n";
    for ($i=0;$i<$icon_check3;$i++){
            print "<OPTION value=\"$i\">$icon_name[$i]</OPTION>\n";
    }
    print "</SELECT>\n";

print <<"_HERE_";
<BR><a href="regist.cgi?mode=icon" target="_brank">アイコン一覧</a>
<BR><BR>
ID：<INPUT size="8" type="text" name="Id" maxlength="8">　パスワード：<INPUT size="8" type="text" name="Password" maxlength="8"><BR>
（ID,パスワードは半角英数字8文字以内）<BR>
<BR>
グループ名：<INPUT size="10" type="text" name="Group" maxlength="20">　グループパス：<INPUT size="10" type="text" name="Gpass" maxlength="20"><BR>
（全角10文字以内でグループに入っていない人も入力してください。）<BR>
<BR>
口癖：<INPUT size="32" type="text" name="Message" maxlength="64"><BR>
（相手殺害時の台詞。全角３２文字まで）<BR>
遺言：<INPUT size="32" type="text" name="Message2" maxlength="64"><BR>
（自分死亡時の台詞）<BR>
自己アピール：<INPUT size="32" type="text" name="Comment" maxlength="64"><BR>
（一言コメント。生存者一覧に記載される。）<BR>
<BR>
<FONT color="#ffff00" size="+1"><B>
同一プレイヤーの複数登録、ゲームの世界観を<BR>
損なう名前の登録はご遠慮ください。<BR>
（例：外人名、姓名と判断出来ない名前、性別と違う名前、原作の名前）<BR>
管理人の一存でデータを強制削除します。<BR>
<BR>
また、<a href="rule.htm" target="_blank">説明書</a>はきちんと読んでください。<BR>
「説明書を読んでいなかったから」というのは、違反行為を許される理由にはなりません。<BR>
</B></FONT>
<BR>
<INPUT type="submit" name="Enter" value="実 行"> 　<INPUT type="reset" name="Reset" value="リセット"><BR>
</FORM>
</CENTER>
<P align="center"><A href="$home"><B><FONT color="#ff0000" size="+2">戻る</FONT></B></A></P>
_HERE_

&FOOTER;

}
#==================#
# ■ 登録処理      #
#==================#
sub REGIST {

&Checker;

    #入力情報チェック
    if ($f_name2 eq '') { &ERROR("姓が未入力です。") ; }
    elsif (length($f_name2) > 8) { &ERROR("姓の文字数がオーバーしています。（全角４文字まで）") ; }
    elsif ($f_name2 =~ /\w/) { &ERROR("氏名に半角文字は利用できません。") ; }

    elsif ($l_name2 eq '') { &ERROR("名が未入力です。") ; }
    elsif (length($l_name2) > 8) { &ERROR("名の文字数がオーバーしています。（全角４文字まで）") ; }
    elsif ($l_name2 =~ /\w/) { &ERROR("氏名に半角文字は利用できません。") ; }

    elsif (length($id2) > 8) { &ERROR("IDの文字数がオーバーしています。（半角8文字まで）") ; }
    elsif ($id2 eq '') { &ERROR("IDが未入力です。") ; }
    elsif ($id2 =~ /\W/) { &ERROR("IDは半角で入力してください。（半角８文字まで）") ; }
    elsif ($id2 =~ /\_|\,|\;|\<|\>|\(|\)|&|\/|\./) { &ERROR("IDに使用禁止文字が入っています。") ; }

    elsif ($password2 eq '') { &ERROR("パスワードが未入力です。") ; }
    elsif (length($password2) > 8) { &ERROR("パスワードの文字数がオーバーしています。（半角８文字まで）") ; }
    elsif ($password2 =~ /\W/) { &ERROR("パスワードは半角で入力してください。（半角８文字まで）") ; }
    elsif ($password2 =~ /\_|\,|\;|\<|\>|\(|\)|&|\/|\./) { &ERROR("パスワードに使用禁止文字が入っています。") ; }

    elsif ($group2 eq '') { &ERROR("グループ名が未入力です。") ; }
    elsif (length($group2) > 20) { &ERROR("グループ名の文字数がオーバーしています。（全角８文字まで）") ; }
    elsif ($group2 =~ /^(\x81\x40|\s|&nbsp;)+$/) { &error("グループ名は正しく記入してください"); }
    elsif ($gpass2 eq '') { &ERROR("グループパスが未入力です。") ; }
    elsif (length($gpass2) > 20) { &ERROR("グループパスの文字数がオーバーしています。（全角８文字まで）") ; }
    elsif ($gpass2 =~ /^(\x81\x40|\s|&nbsp;)+$/) { &error("グループパスは正しく記入してください"); }

    elsif ($sex2 eq "NOSEX") { &ERROR("性別が未選択です。") ; }
    elsif ($icon2 eq "NOICON") { &ERROR("アイコンが未選択です。") ; }
    elsif ($id2 eq $password2) { &ERROR("IDと同じ文字列はパスワードに使えません。") ; }
    elsif (length($msg2) > 64) { &ERROR("口癖の文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif (length($dmes2) > 64) { &ERROR("遺言の文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif (length($com2) > 64) { &ERROR("コメントの文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif (($icon2 >= $icon_check2)&&($password2 ne $s_icon_pass[$icon2 - $icon_check2])) { &ERROR("このアイコンは$icon_name[$icon2]です。") ; }
    elsif ($icon2 < $icon_check2){
        if(($sex2 =~ /男子/)&&($icon2 >= $icon_check )) { &ERROR("性別と違うアイコンを選択しています。") ; }
        elsif(($sex2 =~ /女子/)&&($icon2 < $icon_check )){ &ERROR("性別と違うアイコンを選択しています。") ; }
    }

    #同姓同名、ＩＤチェック
    $grpmem = $gpsmem = 0;
    foreach $userlist(@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist);
        if (($id2 eq $w_id) || (($f_name2 eq $w_f_name)&&($l_name2 eq $w_l_name)&&($w_sts ne "死亡"))) {    #同一ID or 同姓同名?
            &ERROR("同一ＩＤ、若しくは、同姓同名のキャラクタが既に存在します。") ;
        }
        if ($group2 eq $w_group) {
            $grpmem++;
            if ($grpmem >= 6) { &ERROR("同一グループＩＤは６人までです。") ; }
        }
        if ($gpass2 eq $w_gpass) {
            $gpsmem++;
            if ($gpsmem >= 6) { &ERROR("同一グループパスは６人までです。") ; }
        }
    }

    #支給武器ファイル
    open(DB,"$wep_file") || exit; seek(DB,0,0); @weplist=<DB>; close(DB);

    #私物ファイル
    open(DB,"$stitem_file") || exit; seek(DB,0,0); @stitemlist=<DB>; close(DB);

    #生徒番号ファイル
    open(DB,"$member_file") || exit; seek(DB,0,0); $memberlist=<DB>; close(DB);
    ($m,$f,$mc,$fc) = split(/,/, $memberlist);

    #性別人数チェック
    if ($sex2 eq "男子") {
        if ($mc >= $clmax) { #登録不可能？
            &ERROR("男子生徒はこれ以上登録できません。") ;
        }
        $m+=1;$no=$m;$cl=$clas[$mc];
        if ($m >= $manmax) {    #クラス更新？
            $m=0;$mc+=1;
        }
    } else {
        if ($fc >= $clmax) { #登録不可能？
            &ERROR("女子生徒はこれ以上登録できません。") ;
        }
        $f+=1;$no=$f;$cl=$clas[$fc];
        if ($f >= $manmax) {    #クラス更新？
            $f=0;$fc+=1;
        }
    }

    #生徒番号ファイル更新
    $memberlist="$m,$f,$mc,$fc,\n" ;
    open(DB,">$member_file"); seek(DB,0,0); print DB $memberlist; close(DB);

    #初期配布武器リスト取得
    $index = int(rand($#weplist+1));
    ($w_wep,$w_att,$w_tai) = split(/,/, $weplist[$index]);

    #私物アイテムリスト取得
    $index = int(rand($#stitemlist+1));
    local($st_item,$st_eff,$st_tai) = split(/,/, $stitemlist[$index]);

    #所持品初期化
    for ($i=0; $i<6; $i++) {
        $item[$i] = "なし"; $eff[$i]=$itai[$i]=0;
    }

    #初期能力
    $att = int(rand(5)) + 8 ;
    $def = int(rand(5)) + 8 ;
    $hit = int(rand(20)) + 90 ;
    $mhit = $hit ;
    $kill = 0;
    $sta = 100;
    $level = 1; $exp = 0;
    $death = $msg = "";
    $sts = "正常"; $pls = 0;
    $tactics = "通常" ;
    $endtime = 0 ;
    $log = "";
    $dmes = "" ; $bid = "" ; $wf=""; $inf = "" ;
    $we = "";
    $feel = int(rand(20)) + 120;
    $icon2 = $icon_file[$icon2];

    #初期アイテム＆初期配布武器
    $item[0] = "パン<>SH"; $eff[0] = 50; $itai[0] = 2;
    $item[1] = "水<>HH"; $eff[1] = 20; $itai[1] = 2;
    $item[2] = $w_wep; $eff[2] = $w_att; $itai[2] = $w_tai;

    $wep = "素手<>WP";
    $watt = 0;
    $wtai = "∞" ;

    if ($sex2 eq "男子" ) {
        $bou = "学ラン<>DBN";
    } else {
        $bou = "セーラー服<>DBN";
    }
    $bdef = 5;
    $btai = 30;

    $bou_h = $bou_f = $bou_a = "なし" ;
    $bdef_h = $bdef_f = $bdef_a = 0;
    $btai_h = $btai_f = $btai_a = 0 ;

    #弾又は矢支給
    if ($w_wep =~ /<>WG/) { #弾
        $item[3] = "弾丸<>Y"; $eff[3] = 36; $itai[3] = 1;
        $item[4] = $st_item; $eff[4] = $st_eff; $itai[4] = $st_tai;
    } elsif ($w_wep =~ /<>WA/) {    #矢
        $item[3] = "矢<>Y"; $eff[3] = 36; $itai[3] = 1;
        $item[4] = $st_item; $eff[4] = $st_eff; $itai[4] = $st_tai;
    } else {
        $item[3] = $st_item; $eff[3] = $st_eff; $itai[3] = $st_tai;
    }

    &CLUBMAKE ; #クラブ作成

    #新規ユーザ情報格納
    $newuser = "$id2,$password2,$f_name2,$l_name2,$sex2,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg2,$sts,$pls,$kill,$icon2,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes2,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com2,$inf,$group2,$gpass2,$a_name2,$feel,$host,$os,\n" ;
    open(DB,">>$user_file"); seek(DB,0,0); print DB $newuser; close(DB);

    #新規追加ログ
    &LOGSAVE("NEWENT") ;

    $id=$id2; $password=$password2;

    &CSAVE ;    #クッキー保存

&HEADER;

print <<"_HERE_";
<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">転校手続き完了</FONT></B><BR></P>
<TABLE border="1" width="280" cellspacing="0">
  <TBODY>
    <TR>
      <TD width="60">クラス</TD>
      <TD colspan="3" width="113">$cl</TD>
    </TR>
    <TR>
      <TD>氏名</TD>
      <TD colspan="3">$f_name2 $l_name2</TD>
    </TR>
    <TR>
      <TD>番号</TD>
      <TD colspan="3">$sex2$no番</TD>
    </TR>
    <TR>
      <TD>クラブ</TD>
      <TD colspan="3">$club</TD>
    </TR>
    <TR>
      <TD>体力</TD>
      <TD>$hit/$mhit</TD>
      <TD>スタミナ</TD>
      <TD>$sta</TD>
    </TR>
    <TR>
      <TD>攻撃力</TD>
      <TD>$att</TD>
      <TD>武器</TD>
      <TD>　</TD>
    </TR>
    <TR>
      <TD>防御力</TD>
      <TD>$def</TD>
      <TD>防具</TD>
      <TD>　</TD>
    </TR>
  </TBODY>
</TABLE>
<P align="center"><BR>
<img src="$imgurl$n_icon_file[$#n_icon_file]"><BR>
_HERE_

    if ($sex2 eq "男子") {
        print "$f_name2 $l_name2くんだね？<BR>\n" ;
    } else {
        print "$f_name2 $l_name2さんだね？<BR>\n" ;
    }

print <<"_HERE_";

転校早々だけど、明日は修学旅行だ。<BR>
<BR>
きちんと遅れずにくるんだぞ！<BR><BR>
<FORM METHOD="POST"  ACTION="regist.cgi">
<INPUT TYPE="HIDDEN" NAME="mode" VALUE="info">
<INPUT TYPE="HIDDEN" NAME="Id" VALUE="$id2">
<INPUT TYPE="HIDDEN" NAME="Password" VALUE="$password2">
<center>
<INPUT type="submit" name="Enter" value="修学旅行へ出発">
</center>
</FORM>
</P>
_HERE_
&FOOTER;
}

#==================#
# ■ 説明処理      #
#==================#
sub INFO {

&HEADER;

print <<"_HERE_";
<P align="center"><B><FONT color="#ff0000" size="+3" face="ＭＳ 明朝">登録完了</FONT></B><BR><BR>
目がさめると、教室のような所にいた。修学旅行に行ったはずなのに・・・。<BR>
「そうだ、修学旅行に行くバスの中で急に眠気が襲ってきて・・・」<BR>
周りを見渡すと、他の生徒もいるようだ。よく見ると、皆、銀色の首輪がはめられている事に気づいた<BR>
自分の首に触れると、冷たい金属の感触が伝わってきた。<BR>
皆と同様、あの銀色の首輪がはめられていた。<BR>
<BR>
突然、前の扉から、一人の男が入ってきた・・・。<BR><BR>
<BR>
<img src="$imgurl$n_icon_file[0]"><BR><BR>
『じゃ、説明しまーす。みんなにここに来てもらったのは他でもありませーん。<BR>
今日は、皆さんにちょっと、殺し合いをしてもらいまーす。<BR>
<BR>
逆らったり、その首輪をはずしたり、脱走しようと試みた場合は即座に殺されると思ってください。<BR>
<BR>
皆さんは、今年の“プログラム”対象クラスに選ばれました。<BR>
<BR>
ルールは簡単です。お互い、殺しあってくれればいいだけです。<BR>
反則はありませーん。<BR><BR>
ああ、先生言い忘れてたけど、ここは島でーす。<BR>
<BR>
いいかー、ここはこの島の分校です。<BR>
先生、ここにずっといるからなー。みんながんばるの、見守ってるからなー。<BR>
<BR>
さて、いいですかぁ。ここを出たらどこへ行っても構\いません。<BR>
けど、毎日零時に、全島放送をします。一日一回なー。<BR>
<BR>
そこで、みんながもってる地図に従って、何時からこのエリアは危ないぞー、<BR>
って先生知らせます。<BR>
地図を良く見て、磁石と地形を照らし合わせて、<BR>
速やかにそのエリアを出てください。<BR>
<BR>
なんでかというとー、その首輪はやっぱり爆発します。<BR>
<BR>
いいか、だからぁ、建物の中にいてもだめだぞぉ。<BR>
穴掘って隠れても電波は届きまーす。<BR>
あーそうそう、ついでですがー、建物の中に隠れるのは勝手でーす。<BR>
<BR>
あー、それともう一つ。タイムリミットがあります。<BR>
いいですか、タイムリミットでーす。<BR>
<BR>
プログラムでは、どんどん人が死にますがぁ、24時間に渡って死んだ人が誰もでなかったらぁ、<BR>
それが時間切れでーす。あと何人残っていようと、コンピュータが作動して、<BR>
残ってる人全員の首輪が爆発しまーす。優勝者はありませーん。<BR>
<BR>
さーて、それじゃ一人づつ、このデイパックを持って、教室をでてもらいまーす。』<BR>
<BR>
<FORM METHOD="POST"  ACTION="battle.cgi">
<INPUT TYPE="HIDDEN" NAME="mode" VALUE="main">
<INPUT TYPE="HIDDEN" NAME="Id" VALUE="$id2">
<INPUT TYPE="HIDDEN" NAME="Password" VALUE="$password2">
<center>
<INPUT type="submit" name="Enter" value="教室を出る">
</center>
</FORM>
_HERE_

&FOOTER;

}

#==================#
# ■ クラブ作成    #
#==================#
sub CLUBMAKE {

    $wa = $wg = $wc = $wd = $ws = $wn = $wb = $wp = 0;

    local($dice) =  rand(100) ;
    local($dice2) = int(rand(8)) ;
    local($dice3) = int(rand(8)) ;

    if ($dice < 80) {
        if ($dice2 == 0) {
            $club = "弓道部";
            $wa = 2 * $BASE;
        } elsif ($dice2 == 1) {
            $club = "射撃部";
            $wg = 2 * $BASE;
        } elsif ($dice2 == 2) {
            $club = "空手部";
            $wb = 2 * $BASE;
        } elsif ($dice2 == 3) {
            $club = "バスケ部";
            $wc = 2 * $BASE;
        } elsif ($dice2 == 4) {
            $club = "科学部";
            $wd = 2 * $BASE;
        } elsif ($dice2 == 5) {
            $club = "フェンシング部";
            $ws = 2 * $BASE;
        } elsif ($dice2 == 6) {
            $club = "剣道部";
            $wn = 2 * $BASE;
        } else {
            $club = "ボクシング部";
            $wp = 2 * $BASE;
        }
    } else {
        if ($dice3 == 0) {
            $club = "陸上部" ;
            $bou_f = "陸上用シューズ<>DF" ; $bdef_f = 5; $btai_f = 15;
        } elsif ($dice3 == 1) {
            $club = "料理研究部" ;
            $item[5] = "エプロン<>AD" ; $eff[5] = 4; $itai[5] = 10;
        } elsif ($dice3 == 2) {
            $club = "パソコン部" ;
            $wep = "フロッピーディスク<>WC"; $watt = 3; $wtai = 10;
        } elsif ($dice3 == 3) {
            $club = "保健委員" ;
            $wep = "注射器<>WS"; $watt = 3; $wtai = "∞";
        } elsif ($dice3 == 4) {
            $club = "サバイバル部" ;
            $item[5] = "地図<>Y" ; $eff[5] = 1; $itai[5] = 1;
        } elsif ($dice3 == 5) {
            $club = "応援団" ;
            $mhit += 30;
            $hit = $mhit;
            $bou = "長ラン<>DBN"; $bdef = 5; $btai = 50;
        } elsif ($dice3 == 6) {
            $club = "天才" ;
            $wa = $wg = $wc = $wd = $ws = $wn = $wb = $wp = 2 * $BASE;
        } else {
            $club = "演劇部" ;
            $def += int(rand(3)+2);
            $item[5] = "演劇小道具<>ADB" ; $eff[5] = 3; $itai[5] = 10;
        }
    }

}

#==================#
# ■ 重複チェック  #
#==================#
sub Checker {

    if(($limit == "")||($limit == 0)){ $limit = 7; }
    local($t_limit) = ($limit * 3) + 1;

    if (($fl =~ /終了/)||($ar >= $t_limit)){
        &ERROR("プログラムの受付は終了いたしました。<br><br>　次回プログラム開始をお待ち下さい。") ;
    }


    $chktim = $c_endtime + (1*60*60*2) ;    #死亡時間取得
    ($csec,$cmin,$chour,$cmday,$cmonth,$cyear,$cwday,$cyday,$cisdst) = localtime($chktim);
    $cyear+=1900; $cmonth++;

    if ($chktim > $now) {   #登録時間エラー？
        &ERROR("キャラ死亡確認後、２時間は再登録出来ません。<br><br>　次回登録可能\時間：$cyear/$cmonth/$cmday $chour:$cmin:$csec") ;
    }

    #ユーザーファイル取得
    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    if ($npc_mode){
        if (($#userlist+1 - $npc_num) >= $maxmem) {    #最大人数超過？
            &ERROR("申\し訳ございませんが、定員($maxmem人)オーバーです。") ;
        }
    }else{
        if ($#userlist+1 >= $maxmem) {    #最大人数超過？
            &ERROR("申\し訳ございませんが、定員($maxmem人)オーバーです。") ;
        }
    }

    #重複チェック
    foreach $userlist(@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf,$w_group,$w_gpass,$w_a_name,$w_feel,$w_host,$w_os) = split(/,/, $userlist);
        if (($c_id eq $w_id) && ($c_password eq $w_password) && ($w_hit > 0)) {   #同一ID?
            $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host,cookie,$c_id $w_id,\n";
            open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
            &ERROR("キャラクタの複数登録は禁止しています。管理人にお問い合わせください。") ;
        }
        if ($IP_deny && ($host eq $w_host) && (($w_hit > 0) || ($w_death eq "政府による処刑"))) {   #同一ＩＰ
            $newerror = "$now,$year/$month/$mday $hour:$min:$sec,$host($os),host,$w_id,\n";
            open(DB,">>$error_file"); seek(DB,0,0); print DB $newerror; close(DB);
            &ERROR("キャラクタの複数登録は禁止しています。管理人にお問い合わせください。") ;
        }
    }
}

#==================#
# ■ アイコン表示  #
#==================#
sub ICON {

    local($i,$j,$stop);

    &HEADER ;
    print "<center><hr width=\"75%\">\n";
    print "<b><big>アイコンサンプル</big></b>\n";
    print "<P><small>- 現在登録されているアイコンは以下のとおりです -</small>\n";
    print "<hr width=\"75%\">\n";
    print "<P><table border=1 cellpadding=5 cellspacing=0 width=\"600\">\n";
    print "<tr align=\"center\">\n";

    $i=0; $j=0;
    $stop = $icon_check2;
    foreach (0 .. $icon_check2-1) {
        $i++; $j++;
        print "<td><img src=\"$imgurl$icon_file[$_]\" ALIGN=middle alt=\"$icon_name[$_]\"><BR>$icon_name[$_]</td>\n";
        if ($j != $stop && $i >= 7) { print "</tr><tr align=\"center\">\n"; $i=0; }
        elsif ($j == $stop) {
            if ($i == 0) { last; }
            while ($i < 7) { print "<td><br></td>"; $i++; }
        }
    }
    print "</tr></table><br>\n";

    # 専用アイコン
    print "<hr width=\"75%\">\n";
    print "<b><big>専用アイコン</big></b>\n";
    print "<P><small>- 現在登録されている専用アイコンは以下のとおりです -</small>\n";
    print "<hr width=\"75%\">\n";
    print "<P><table border=1 cellpadding=5 cellspacing=0 width=\"600\">\n";
    print "<tr align=\"center\">\n";

    $i=0; $j=0;
    $stop = $icon_check3 - $icon_check2;
    foreach ($icon_check2 .. $icon_check3-1) {
        $i++; $j++;
        print "<td><img src=\"$imgurl$icon_file[$_]\" ALIGN=middle alt=\"$icon_name[$_]\"><BR>$icon_name[$_]</td>\n";
        if ($j != $stop && $i >= 7) { print "</tr><tr align=\"center\">\n"; $i=0; }
        elsif ($j == $stop) {
            if ($i == 0) { last; }
            while ($i < 7) { print "<td><br></td>"; $i++; }
        }
    }
    print "</tr></table><br>\n";

    print "<FORM><INPUT TYPE=\"button\" VALUE=\"  CLOSE  \" onClick=\"top.close();\"></FORM>\n";
    &FOOTER;

}
1
