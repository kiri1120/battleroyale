#! /usr/local/bin/perl
require "jcode.pl";
require "br.cgi";
require "$LIB_DIR/lib.cgi";
require "$LIB_DIR/lib2.cgi";
&LOCK;
require "pref.cgi";

&DECODE;
&CREAD ;

if ($mode eq "regist") { &REGIST; }
elsif ($mode eq "info") { &INFO; }
elsif ($mode eq "info2") { &INFO2; }
else { &MAIN; }
&UNLOCK;
exit;

#==================#
# ■ メイン        #
#==================#
sub MAIN {
    &checker;

&HEADER;
print <<"_HERE_";
<P align="center"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">転校手続き</FONT></B><BR><BR>
<BR>
『君が転校生だね？僕が担任です。<BR>
生徒からは、「とんぼ」とかいわれてるけどね。<BR>
あ、そんな事はどうでもいいね。<BR>
<BR>
とりあえず、ここに氏名と、性別を記入して、<BR>
提出してもらえるかな？</P>
<CENTER>
<FORM METHOD="POST"  ACTION="regist.cgi">
<INPUT TYPE="HIDDEN" NAME="mode" VALUE="regist">
姓：<INPUT size="16" type="text" name="F_Name" maxlength="16"><BR>
名：<INPUT size="16" type="text" name="L_Name" maxlength="16"><BR>
<BR>
性別：<SELECT name="Sex">
  <OPTION value="NOSEX" selected>- 性別 -</OPTION>
  <OPTION value="男子">男子</OPTION>
  <OPTION value="女子">女子</OPTION>
</SELECT>
_HERE_

if($icon_mode){
    print "　アイコン：<SELECT name=\"Icon\">\n";
    print "<OPTION value=\"NOICON\" selected>- アイコン -</OPTION>\n";
    if($icon_check2 == 0){
        for ($i=0;$i<$#icon_file + 1;$i++){
            print "<OPTION value=\"$i\">$icon_name[$i]</OPTION>\n";
        }
    }else{
        for ($i=0;$i<$icon_check2;$i++){
            print "<OPTION value=\"$i\">$icon_name[$i]</OPTION>\n";
        }
    }

    print "</SELECT>\n";
}

print <<"_HERE_";
<BR><BR>
ID：<INPUT size="8" type="text" name="Id" maxlength="8">　パスワード：<INPUT size="8" type="text" name="Password" maxlength="8"><BR>
（ID,パスワードは半角英数字8文字以内）<BR>
<BR>
口癖：<INPUT size="32" type="text" name="Message" maxlength="64"><BR>
（相手殺害時の台詞。全角３２文字まで）<BR>
遺言：<INPUT size="32" type="text" name="Message2" maxlength="64"><BR>
（自分死亡時の台詞）<BR>
自己アピール：<INPUT size="32" type="text" name="Comment" maxlength="64"><BR>
（一言コメント。生存者一覧に記載される。）<BR>
<BR>
<FONT color="#ffff00" size="+1"><B>同一プレイヤーの複数登録、ゲームの世界観を<BR>
損なう名前の登録はご遠慮ください。<BR>
（例：外人名、姓名と判断出来ない名前、性別と違う名前、原作の名前）<BR>
管理人の一存でデータを強制削除します。<BR>
</B></FONT><BR>
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
    &checker;

    #入力情報チェック
    if ($f_name2 eq '') { &ERROR("姓が未入力です。") ; }
    elsif (length($f_name2) > 8) { &ERROR("姓の文字数がオーバーしています。（全角４文字まで）") ; }
    elsif ((grep /[a-z]|[A-Z]|[0-9]/, $f_name2) == 1) { &ERROR("氏名に半角文字は利用できません。（全角４文字まで）") ; }
    elsif ($l_name2 eq '') { &ERROR("名が未入力です。") ; }
    elsif (length($l_name2) > 8) { &ERROR("名の文字数がオーバーしています。（全角４文字まで）") ; }
    elsif ((grep /[a-z]|[A-Z]|[0-9]/, $l_name2) == 1) { &ERROR("氏名に半角文字は利用できません。（全角４文字まで）") ; }
    elsif ($sex2 eq "NOSEX") { &ERROR("性別が未選択です。") ; }
    elsif (length($id2) > 8) { &ERROR("IDの文字数がオーバーしています。（半角8文字まで）") ; }
    elsif ($id2 eq '') { &ERROR("IDが未入力です。") ; }
    elsif ((grep /[a-z]|[A-Z]|[0-9]/, $id2) == 0) { &ERROR("IDは半角で入力してください。（半角８文字まで）") ; }
    elsif ($id2 =~ /\_|\,|\;|\<|\>|\(|\)|&|\/|\./) { &ERROR("ＩＤに使用禁止文字が入っています。") ; }
    elsif ($password2 eq '') { &ERROR("パスワードが未入力です。") ; }
    elsif (length($password2) > 8) { &ERROR("パスワードの文字数がオーバーしています。（半角８文字まで）") ; }
    elsif ((grep /[a-z]|[A-Z]|[0-9]/, $password2) == 0) { &ERROR("passwordは半角で入力してください。（半角８文字まで）") ; }
    elsif ($password2 =~ /\_|\,|\;|\<|\>|\(|\)|&|\/|\./) { &ERROR("パスワードに使用禁止文字が入っています。") ; }
    elsif ($icon2 eq "NOICON") { &ERROR("アイコンが未選択です。") ; }
    elsif ($id2 eq $password2) { &ERROR("IDと同じ文字列はパスワードに使えません。") ; } #joeチェック(^_^;)
    elsif (length($msg2) > 64) { &ERROR("口癖の文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif (length($dmes2) > 64) { &ERROR("遺言の文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif (length($com2) > 64) { &ERROR("コメントの文字数がオーバーしています。（全角３２文字まで）") ; }
    elsif ($icon_check && $icon_mode){
        if(($sex2 =~ /男子/)&&($icon2 >= $icon_check )) { &ERROR("性別と違うアイコンを選択しています。") ; }
        elsif(($sex2 =~ /女子/)&&($icon2 < $icon_check )){ &ERROR("性別と違うアイコンを選択しています。") ; }
    }

    #ユーザファイル取得
    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    #同姓同名、ＩＤチェック
    foreach $userlist(@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist);
        if (($id2 eq $w_id) || (($f_name2 eq $w_f_name)&&($l_name2 eq $w_l_name)&&($w_sts ne "死亡"))) {    #同一ID or 同姓同名?
            &ERROR("同一ＩＤ、若しくは、同姓同名のキャラクタが既に存在します。") ;
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
    $hit = int(rand(20)) + 30 ;
    $mhit = $hit ;
    $kill=0;
    $sta = $maxsta ;
    $level=1; $exp=0;
    $death = $msg = "";
    $sts = "正常"; $pls=0;
    $tactics = "通常" ;
    $endtime = 0 ;
    $log = "";
    $dmes = "" ; $bid = "" ; $inf = "" ;

    #初期アイテム＆初期配布武器
    $item[0] = "パン<>SH"; $eff[0] = 20; $itai[0] = 2;
    $item[1] = "水<>HH"; $eff[1] = 15; $itai[1] = 2;
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
        $item[3] = "弾丸<>Y"; $eff[3] = 12; $itai[3] = 1;
        $item[4] = $st_item; $eff[4] = $st_eff; $itai[4] = $st_tai;
    } elsif ($w_wep =~ /<>WA/) {    #矢
        $item[3] = "矢<>Y"; $eff[3] = 12; $itai[3] = 1;
        $item[4] = $st_item; $eff[4] = $st_eff; $itai[4] = $st_tai;
    } else {
        $item[3] = $st_item; $eff[3] = $st_eff; $itai[3] = $st_tai;
    }

    &CLUBMAKE ; #クラブ作成

    #ユーザファイル
    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);

    $newuser = "$id2,$password2,$f_name2,$l_name2,$sex2,$cl,$no,$endtime,$att,$def,$hit,$mhit,$level,$exp,$sta,$wep,$watt,$wtai,$bou,$bdef,$btai,$bou_h,$bdef_h,$btai_h,$bou_f,$bdef_f,$btai_f,$bou_a,$bdef_a,$btai_a,$tactics,$death,$msg2,$sts,$pls,$kill,$icon2,$item[0],$eff[0],$itai[0],$item[1],$eff[1],$itai[1],$item[2],$eff[2],$itai[2],$item[3],$eff[3],$itai[3],$item[4],$eff[4],$itai[4],$item[5],$eff[5],$itai[5],$log,$dmes2,$bid,$club,$wn,$wp,$wa,$wg,$we,$wc,$wd,$wb,$wf,$ws,$com2,$inf,\n" ;

    #新規ユーザ情報格納
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
<A href="regist.cgi?mode=info&Id=$id2&Password=$password2"><B><FONT color="#ff0000" size="+2">修学旅行へ出発</FONT></B></A><BR>
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
<P align="center"><B><FONT color=\"#ff0000\" size=\"+3\" face=\"ＭＳ 明朝\">登録完了</FONT></B><BR><BR>
目がさめると、教室のような所にいた。修学旅行に行ったはずなのに・・・。<BR>
「そうだ、修学旅行に行くバスの中で急に眠気が襲ってきて・・・」<BR>
周りを見渡すと、他の生徒もいるようだ。よく見ると、皆、銀色の首輪がはめられている事に気づいた<BR>
自分の首に触れると、冷たい金属の感触が伝わってきた。<BR>
皆と同様、あの銀色の首輪がはめられていた。<BR>
<BR>
突然、前の扉から、一人の男が入ってきた・・・。<BR><BR>
<BR>
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

    $wa=$wg=$wb=$wc=$wd=$ws=$wn=$wf=$wp=$we=0 ;

    local($dice) = int(rand(11)) ;

    if ($dice == 0) {
        $club = "弓道部" ;
        $wa = 1 * $BASE ;
    }elsif ($dice == 1) {
        $club = "射撃部" ;
        $wg = 1 * $BASE ;
    }elsif ($dice == 2) {
        $club = "空手部" ;
        $wb = 1 * $BASE ;
    }elsif ($dice == 3) {
        $club = "バスケ部" ;
        $wc = 1 * $BASE ;
    }elsif ($dice == 4) {
        $club = "科学部" ;
        $wd = 1 * $BASE ;
    }elsif ($dice == 5) {
        $club = "フェンシング部" ;
        $ws = 1 * $BASE ;
    }elsif ($dice == 6) {
        $club = "剣道部" ;
        $wn = 1 * $BASE ;
    }elsif ($dice == 7) {
        $club = "ボクシング部" ;
        $wp = 1 * $BASE ;
    }elsif ($dice == 8) {
        $club = "陸上部" ;
    }elsif ($dice == 9) {
        $club = "料理研究部" ;
    }elsif ($dice == 10) {
        $club = "パソコン部" ;
    }

}

#==================#
# ■ チェック      #
#==================#
sub checker{
    if(($limit == "")||($limit == 0)){ $limit = 7; }
    local($t_limit) = ($limit * 3) + 1;

    if (($fl =~ /終了/)||($ar >= $t_limit)){
        &ERROR("プログラムの受付は終了いたしました。<br><br>　次回プログラム開始をお待ち下さい。") ;
    }


    $chktim = $c_endtime + (1*60*60*2) ;    #死亡時間取得
    ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime($chktim);
    $year+=1900; $month++;

    if ($chktim > $now) {   #登録時間エラー？
        &ERROR("キャラ死亡確認後、２時間は再登録出来ません。<br><br>　次回登録可能\時間：$year/$month/$mday $hour:$min:$sec") ;
    }

    $IP_chk = 1;
    foreach $ipok(@IP_ok){
        if($IP_host){
            if($host =~ /$ipok$/){ $IP_chk = 0; last;}
        }else{
            if($host =~ /^$ipok/){ $IP_chk = 0; last;}
        }
    }

    if(($IP_deny)&&($IP_chk)){
        #ログファイル取得
        open(DB,"$log_file");seek(DB,0,0); @loglist=<DB>;close(DB);

        foreach $loglist(reverse(@loglist)) {
            ($gettime,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_f_name2,$w_l_name2,$w_sex2,$w_cl2,$w_no2,$getkind,$log_host)= split(/,/, $loglist);
            if($loglist =~ /ENTRY/){
                $hostdat{"$w_f_name$w_l_name"} = "$log_host";
            }elsif($loglist =~ /DEATH/){
                $chktim = $gettime + (1*60*60*2) ;    #死亡時間取得
                if ($chktim < $now) {
                    delete $hostdat{"$w_f_name$w_l_name"};
                }
            }
        }

        foreach $log_host(values(%hostdat)) {
            $hostlist = ( $hostlist . "$log_host ");
        }

        if($hostlist =~ /$host/){&ERROR("キャラクタの複数登録は禁止しています。管理人にお問い合わせください。") ;}

    }

    #ユーザーファイル取得
    open(DB,"$user_file");seek(DB,0,0); @userlist=<DB>;close(DB);
    $listnum = @userlist;
    if ($npc_mode){
        if (($listnum - $npc_num) >= $maxmem) {    #最大人数超過？
            &ERROR("申\し訳ございませんが、定員($maxmem人)オーバーです。") ;
        }
    }else{
        if ($listnum >= $maxmem) {    #最大人数超過？
            &ERROR("申\し訳ございませんが、定員($maxmem人)オーバーです。") ;
        }
    }

    #重複チェック
    foreach $userlist(@userlist) {
        ($w_id,$w_password,$w_f_name,$w_l_name,$w_sex,$w_cl,$w_no,$w_endtime,$w_att,$w_def,$w_hit,$w_mhit,$w_level,$w_exp,$w_sta,$w_wep,$w_watt,$w_wtai,$w_bou,$w_bdef,$w_btai,$w_bou_h,$w_bdef_h,$w_btai_h,$w_bou_f,$w_bdef_f,$w_btai_f,$w_bou_a,$w_bdef_a,$w_btai_a,$w_tactics,$w_death,$w_msg,$w_sts,$w_pls,$w_kill,$w_icon,$w_item[0],$w_eff[0],$w_itai[0],$w_item[1],$w_eff[1],$w_itai[1],$w_item[2],$w_eff[2],$w_itai[2],$w_item[3],$w_eff[3],$w_itai[3],$w_item[4],$w_eff[4],$w_itai[4],$w_item[5],$w_eff[5],$w_itai[5],$w_log,$w_dmes,$w_bid,$w_club,$w_wn,$w_wp,$w_wa,$w_wg,$w_we,$w_wc,$w_wd,$w_wb,$w_wf,$w_ws,$w_com,$w_inf) = split(/,/, $userlist);
        if (($c_id eq $w_id) && ($c_password eq $w_password) && ($w_sts ne "死亡")) {   #同一ID or 同姓同名?
            &ERROR("キャラクタの複数登録は禁止しています。管理人にお問い合わせください。") ;
        }
    }
}

