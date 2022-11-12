#!/bin/perl

# 電子掲示板 -Trees- v2.11 FreeSoft
# (c)1999-2009 by CGI-RESCUE
#
# for UNIX/SJIS
#
# [設置構成例] 詳しくはreadme.txtを参照してください。
#
# ┣━/data/ <777>
# ┃
# ┣ jcode.pl <644>
# ┣ trees.cgi <755>
# ┣ password.cgi <666>
#
# [履歴]
# v 1.00 07/MAY/1999 初版
# v 1.01 08/MAY/1999 一覧の表示題名文字数設定
# v 1.02 17/JUN/1999 タグ有効時は<br>コードを出力しないように修正
# v 1.03 09/JUL/1999 タグ処理の変数ミスを修正
# ------- ここを境にデータの完全互換はありませんが、重大な支障なくデータは後継できます.
# v 2.00 10/JUL/1999 コメントメール機能,プレビュー機能,半角カナ対策,New!画像に縦横サイズ設定,コメント有り記事の削除を制限する機能
# v 2.01 11/JUL/1999 削除関係のバグを修正
# v 2.02 15/JUL/1999 意味不明のバグの修正
# v 2.03 30/APR/2000 MAC版IE5対応のためにインデントタグの修正、クッキーのURLコンコード化
# v 2.04 17/AUG/2002 Mozilla1.0においてスレッドの深さが正しく表示できない不具合の修正
# v 2.10 06/JUN/2006 削除された投稿を表示しない・投稿時に確認ダイアログを表示させる
# v 2.11 12/MAY/2009 クロスサイト・スクリプティング対処

#-- 必須設定 ------------------------------------------------------------------

#●管理者のメールアドレス(半角で正しく)
$administrator = 'あなたのＥメールアドレス';

#●画面の「終了」リンク先(URL)
$bye = 'http://ホームページなどのＵＲＬ/';

#●タイトルなどの冒頭メッセージ(HTML書式)
$title = <<'EOF';
<h1>＊＊掲示板</h1>
EOF

# $.... = <<'EOF';
# この間に記述します.
# 複数行可能.
# EOF

#●ブラウザのタイトルバーの名称(１行のみ)
$title_bar = <<'EOF';
＊＊掲示板
EOF

#-- 任意設定 ------------------------------------------------------------------

#●画面の色や背景の設定 (HTML書式)
$body = '<body bgcolor=#FFFFFF text=#000000>';

#●バーの色
$cellcolor = '#ffeedd';

#●ホスト名の表示 1:する 0:しない
$view_host = 1;

#●タグの許可(運用途中で変更しないこと) 1:する(自動URLリンク無効) 0:しない
$allow_html = 0;

#●１画面に表示する行数(デフォルト値)
$def = 20;

#● 記録モードのデフォルトチェック値 0:改行無効 1:図表モード 2:改行有効
$chk = 2;

#●時刻設定
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('日','月','火','水','木','金','土');

#●このプログラムの場所をＵＲＬで設定(設定しなければ自動検出)
$reload = '';

#●$reloadで設定した設置ＵＲＬ以外のフォームからの投稿を禁止する処置 する:1 しない:0
$ref_axs = 0;

#●日本語コード変換ライブラリ(パス値) .. 2.0以上のバージョンのもの
require './jcode.pl';

#●データディレクトリの場所(パス値)
$data_dir = './data/';

#●管理者用パスワードファイル(パス値)
$pwd_file = './password.cgi';

#●コメントがある記事を管理者以外が削除できないように 1:する 0:しない
$delsave = 1;

#●コメントお知らせ機能を 1:使う 0:使わない
#  (使う状態でコメント機能を利用している記事であっても、この設定が0になればメールしません)
$resmail = 0;

#○コメントお知らせ機能を使う場合に設定する --------↓

#○sendmailの設定(パス値)
$sendmail = '/usr/lib/sendmail';

#○メールの題名
$mail_subject = '＊＊掲示板からのお知らせ';

#○メール本文の冒頭に入れる文章($mail_val = <<'EOF';とEOFの間に記述する)
$mail_val = <<'EOF';
「わたしのホームページ」 http://www.foo.bar/~user/ の
「＊＊掲示板」へお越しください。
EOF

#○メール本文の終わりに入れる文章(シグネチャ/署名)
$mail_val2 = <<'EOF';
---------------------------------------------
MyHomePage http://www.foo.bar/ user@mail.host
EOF

#---------------------------------------------------↑

#●コメントに階層番号を 0:つけない 1:付ける
$attnum = 1;

#●ツリー構成用罫線
$keisen = '┣';

#●番号を囲む括弧(左)
$kakko_l = '【';

#●番号を囲む括弧(右)
$kakko_r = '】';

#●クリックポイント印
$point = '≪';

#●クリックポイント印の色
$pointc = '#ff3333';

#●一覧時の題名文字数制限(byte)
$subject_max_length = 100;

#-- 過去ログ設定 --------------------------------------------------------------

#●過去ログ機能を 1:使う 0:使わない
$log = 0;

#●過去ログの場所(パス値)と名称
%LOG = (
	'' , '',

);

#-- 高度な設定 ----------------------------------------------------------------

#●手順
$prot = 'http';

#●クッキーを認識する範囲(通常はこのままでよい)
#  詳しいことは http://www.netscape.com/newsref/std/cookie_spec.html のpathの項目をご覧ください.
$path = '';

#------------------------------------------------------------------------------

if ($jcode'version < 2) { &error('ライブラリ異常','jcode.plは2.0以降のバージョンを設置してください.'); }
if ($reload ne '') { $SCRIPT_NAME = $reload; } # プログラム名の指定設定
else { $SCRIPT_NAME = $ENV{'SCRIPT_NAME'}; } # 自動設定
if ($SCRIPT_NAME eq '') { &error("設定エラー",'(E1)'); } # $SCRIPT_NAMEはクッキー名にも使う

$wcheck = 'wwwbbs.wck'; # 同内容連続投稿防止ファイル名
$lockfile = 'wwwbbs.lock'; # ロックファイル名
$date_now = sprintf("%04d/%01d/%01d(%s)%02d:%02d",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min); # 時刻構成

&decode_cookie($SCRIPT_NAME); # クッキー取得
$cname = $SCRIPT_NAME . '2'; &decode_cookie($cname); # 既読位置取得
$cname = $SCRIPT_NAME . '3'; &decode_cookie($cname); # 一覧数取得

if ($COOKIE{'list'} > 0) { $def = $COOKIE{'list'}; } # 行数設定
if ($COOKIE{'mode'} eq '') { $COOKIE{'mode'} = 't'; } # 一覧モード設定

$cmd = $ENV{'QUERY_STRING'}; # クエリー入力
@pairs = split(/&/,$cmd);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	$value =~ s/&/&amp;/g;
	$value =~ s/"/&quot;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;

	$CMD{$name} = $value; # クエリーデータはコマンド用連想配列へ
}

read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'}); # 標準入力

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($key,$val) = split(/=/,$pair);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	&jcode'h2z_sjis(*val); # 半角カナ→全角(SJIS)変換
	&jcode'convert(*val,'sjis'); # SJIS変換

	if ($key eq 'preview') { $preview = 1; } # プレビュー処理の検知

	$val =~ s/\t//g; # タブコードを無効化
	$val =~ s/\r\n/\n/g; # Win → Unix
	$val =~ s/\r/\n/g; # Mac → Unix

	unless ($key eq 'value') { # 内容文以外はタグを無視

		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
	}

	$in{$key} = $val;
}

if ($preview) { &prev; exit; } # プレビュー処理へ

if (!-e $pwd_file) { &error("エラー","(E2)"); }
if ($in{'action'} eq 'setpwd') { &setpwd; }
if (-z $pwd_file || $CMD{'action'} eq 'resetpwd') { &setpwd_form; }

($admin) = &master_check; # 管理者権限確認(管理パスワードなら$admin値は1)

# 過去ログ選択
if (!$log) { $in{'log'} = $CMD{'log'} = ''; }
if ($CMD{'log'} ne '') { $in{'log'} = $CMD{'log'}; }
if ($in{'log'} ne '') {

	$data_dir = $in{'log'};
	if (!-d $data_dir) { &error("過去ログが見つかりません","(E18)"); }

	$LOG_NAME = $LOG{$data_dir};
	$CMD{'log'} = $in{'log'};
	$title_bar .= " - $LOG_NAME";
	$newms = '一覧';
}
else { $newms = '最新の一覧'; }

chdir($data_dir); # ディレクトリ移動

if (!$CMD{'log'}) { &lock; } # ファイルロック

if ($CMD{'st'}) { $in{'start'} = $CMD{'st'} - 1; } # リスト位置
if ($in{'action'} ne '') { $CMD{'action'} = $in{'action'}; } # アクション値をコマンドにもコピー
if ($CMD{'search'} ne '') { $in{'search'} = $CMD{'search'}; }
if ($CMD{'mode'} ne '') { $in{'mode'} = $CMD{'mode'}; }

if ($CMD{'t'}) { # クリックポイント処理

	if ($in{'v'} =~ /\D/) { &error("エラー","数字は半角文字で入力してください."); }
	if (-e "$in{'v'}\.msg") { $CMD{'e'} = 'msg'; }
	elsif (-e "$in{'v'}\.res") { $CMD{'e'} = 'res'; }
	else { &error("File Not Found","$numberは削除されています."); }

	$CMD{'lp'} = $CMD{'v'} = $in{'v'};
}
elsif ($CMD{'tw'} ne '') { $CMD{'t'} = $CMD{'tw'}; }

if ($CMD{'v'} =~ /(\d+)/ && $CMD{'e'} =~ /(msg|res)/) { &view($CMD{'v'},$CMD{'e'}); } # 記事表示
elsif ($CMD{'image'} eq 'new') { &image($CMD{'image'}); }
elsif ($CMD{'image'} eq 'copyright') { &image($CMD{'image'}); }
elsif ($CMD{'bye'} ne '') { &bye; }
elsif ($CMD{'mc'}) {

	# リストモード変更
	$cook="uname\:$COOKIE{'uname'}\,email\:$COOKIE{'email'}\,pwd\:$COOKIE{'pwd'}\,mode\:$CMD{'mc'}";
	$cook =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URLエンコード
	$cook =~ tr/ /+/;
	print "Set-Cookie: $SCRIPT_NAME=$cook; path=$path; expires=$date_gmt\n";
	$COOKIE{'mode'} = $CMD{'mc'};
	&list;
}
else {
	if ($in{'start'} eq '') { $start = 0; } # リスト開始位置
	else { $start = $in{'start'} + 1; }

	if ($CMD{'action'} eq 'post' && !$CMD{'log'}) { &post; } # 投稿画面へ
	elsif ($in{'action'} eq 'write' && !$CMD{'log'}) { &write; } # 記録処理へ
	elsif ($in{'action'} eq 'remove' && !$CMD{'log'}) { # 削除処理へ

		($result) = &remove;
		if (!$result) { $alldel = 1; }

		if ($in{'search'} ne '') { &search; }
		else { &list; }
	}
	elsif ($in{'search'} ne '') { &search; } # 検索リスト
	else { &list; } # 通常リスト
}

if (-e $lockfile) { unlink $lockfile; } # ロック解除
exit;

sub getdir {

	local($type) = @_;

	$od_check = (eval { opendir(DIR,'.'); }, $@ eq "");
	if (!$od_check) {&error("エラー","(E3)"); }

	@newls = ();
	@list = readdir(DIR); # ファイル名の抽出

	foreach $file (@list) {

		next if -d $file;

		if ($type eq 'n') {

			# 番号順一覧
			if ($file =~ /(\d+)\.tre/) { next; }
			if ($file =~ /(\d+)\.(msg|res)/) { push(@newls,"$1\.$2"); }
		}
		else {
			# ツリー一覧
			if ($file =~ /(\d+)\.tre/) { push(@newls,"$1\.tre"); }
		}
	}

	close(DIR);

	@newls = sort { $b <=> $a; } @newls;
	$all = @newls;
}

sub getlast {

	$od_check = (eval { opendir(DIR,'.'); }, $@ eq "");
	if (!$od_check) {&error("エラー","(E3)"); }

	@newls2 = ();
	@list = readdir(DIR);

	foreach $file (@list) {

		next if -d $file;

		if ($file =~ /(\d+)\.tre/) { next; }
		if ($file =~ /(\d+)\.(msg|res)/) { push(@newls2,"$1\.$2"); }
	}

	close(DIR);

	@newls2 = sort { $b <=> $a; } @newls2;
	return($newls2[0]); # 最高番号検出
}

sub list {

	if ($in{'search'} ne '') {

		if ($in{'search'} =~ /[&"<>]/) { &error("入力文字制限","検索文字列に記号の入力はできません."); }

		$keys = $target = $in{'search'};
		$keys =~ s/　/ /g;
		$target =~ s/　/ /g;
		$target =~ s/(\W)/\\$1/g;
		@keys = split(/\\\s+/,$target);
	}

	&getdir($COOKIE{'mode'});

	if ($in{'cls'}) { # 行数変更

		$def = $in{'ls'};
		print "Set-Cookie: $SCRIPT_NAME" . '3' . "=list:$def; path=$path; expires=$date_gmt\n";
	}

	# 一覧行の検討
	if ($all <= ($start + $def - 1)) { $end = $all - 1; }
	else { $end = $start + $def - 1; }

	if ($COOKIE{'mode'} eq 'n') { $mc = 't'; $mc2 = 'ツリー一覧'; }
	else { $mc = 'n'; $mc2 = '番号順一覧'; }

	&html_head;

	print "$body\n";
	print "$title<p>\n";

	if ($all != 0) {

		print "<font size=-1>\n";
		if ($start != 0 || $cmd ne '' || $CMD{'log'}) { print "〔<a href=\"JavaScript:history.back()\">前の画面</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?action=post\">新しい話題</a>〕"; }
		print "〔<a href=\"#search\" onClick=\"document.SearchForm.search.focus();\">検索</a>〕";
		print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>〕";
		print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>〕";
		if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>全て読んだことにする</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>全て読んだことにして終了</a>〕"; }
		print "〔<a href=\"$bye\" target=_top>終了</a>〕";
		print "</font><p>\n";

		if ($CMD{'log'}) { $COOKIE{'rp'} = ''; }
		elsif ($COOKIE{'rp'} ne '' && $start == 0) {

			($lastf) = &getlast;
			($lastnum,$ext) = split(/\./,$lastf,2);
			$rp2 = $COOKIE{'rp'} + 1;

			if ($COOKIE{'rp'} > $lastnum) { $COOKIE{'rp'} = $lastnum; }
			else {

				print "<font size=-1>《 あなたの最終アクセス日 $COOKIE{'lastlogin'} 既読番号 ～No.$COOKIE{'rp'} 》</font>\n";
				print "<ul>\n";
				if ($COOKIE{'rp'} < $lastnum) {

					if ($rp2 == $lastnum) { $msg = $rp2; } else { $msg = "$rp2～$lastnum"; }
					print "<li>前回より、$msgが<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>新規投稿されています.\n";
					if ($COOKIE{'mode'} ne 'n') { print "<li>まとめて見るには〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>〕にすると便利です.\n"; }
				}
				print "</ul>\n";
			}
		}

		if ($alldel) { print "<a name=\"$number\"></a>\n"; }

		if ($LOG_NAME ne '') { print "<h3>$LOG_NAME</h3>\n"; }
		print "<DL>\n";
		if ($start != 0) { print "<DT><font size=-1>↑</font></dt>\n"; }

		foreach $num ($start .. $end) {

			$k = ''; # 罫線クリア

			if ($COOKIE{'mode'} eq 'n') {

				# 時系列形式
				($file,$ext) = split(/\./,$newls[$num],2); # ファイル名と拡張子に分ける
				if ($ext eq 'msg') { $cell = " bgcolor=$cellcolor"; } else { $cell = ''; }
				if ($CMD{'bk'} == $file || $res_bk == $file) { $file2 = "<blink><font color=$pointc class=\"blink\">$file</font></blink>"; } else { $file2 = $file; }

				if (-s $newls[$num] == 0) { next; }
				($result) = &gethead($newls[$num],0); # 記事ヘッダの取得(第２引数が0でヘッダのみ、1で@VALに内容文を取得)
				if (!$result) { print "<DT>$kakko_l$file$kakko_r" . "Read Error E10($newls[$num])</dt>\n"; next; }

				if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }

				if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }
				if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }
				$line = "<a name=\"$file\">$kakko_l$file2$kakko_r\</a>$new <a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&v=$file&e=$ext&lp=$file&st=$start\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'})</font>";

				$line = "<table cellpadding=0 cellspacing=1 border=0 width=100%><tr><td$cell>$line</td></tr></table>";
				print "<DT>$line</dt>\n";
			}
			else {
				# スレッド形式
				if (open(TREE,"$newls[$num]")) {

					@trees = <TREE>;
					close(TREE);
				}
				else { print "<DT>$kakko_l$file$kakko_r" . "Read Error E11($HD{'tree'}\.tre)</dt>\n"; next; }

				foreach $line (@trees) {

					$line =~ s/\n//g;

					if ($line =~ /<DD>/) { next; }
					elsif ($line =~ /<DL>/) { print "<DD><DL>\n"; next; }
					elsif ($line =~ /<\/DL>/) { print "</DL></dd>\n"; next; }
					elsif ($line =~ /<DT>\!(\d+)\.(msg|res)/) {

						$num = $1;
						$ext = $2;

						if ($CMD{'bk'} == $num || $res_bk == $num) { $num2 = "<blink><font color=$pointc class=\"blink\">$num</font></blink>"; } else { $num2 = $num; }
						if ($ext eq 'res') { $k = $keisen; }

						next;
					}
					elsif ($line =~ /<DT>\D*(\d+)\.(msg|res)/) {

						$num = $1;
						$ext = $2;
						$file = "$num\.$ext";
						if ($CMD{'bk'} == $num || $res_bk == $num) { $num2 = "<blink><font color=$pointc class=\"blink\">$num</font></blink>"; } else { $num2 = $num; }

						if (-s $file == 0) { next; }

						($result) = &gethead($file,0);
						if (!$result) {

							if ($ext eq 'res') { $k = $keisen; }
							print "$k$kakko_l$num2$kakko_r" . "Read Error E10($file)\n";
							next;
						}

						if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }
						if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }
						if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }
						$change = "<a name=\"$num\">$kakko_l$num2$kakko_r\</a>$new <a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&v=$num&e=$ext&lp=$num&st=$start\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'}) </font>";
						$line =~ s/$file/$change/;
						$line =~ s/<DT>//;

						if ($ext eq 'msg') { $line = "<table border=0 cellpadding=0 cellspacing=1 width=100%><tr><td bgcolor=$cellcolor>$line</td></tr></table>"; }
						else { $k = $keisen; }
					}
					print "<DT>$k$line</dt>\n";
				}
			}
		}
		print "</DL></dd>\n";
	}
	else {
		print "<font size=-1>\n";
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?action=post\">新しい話題</a>〕"; }
		print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>〕";
		if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
		print "〔<a href=\"$bye\" target=_top>終了</a>〕";
		print "</font><p>\n";

		print "メッセージはありません.<p>\n";
	}

	print "<hr size=1>\n";

	if ($all != 0) {

		print "<font size=-1>\n";
		if ($start != 0 || $cmd ne '' || $CMD{'log'}) { print "〔<a href=\"JavaScript:history.back()\">前の画面</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?action=post\">新しい話題</a>〕"; }
		print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>〕";
		print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>〕";
		if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>全て読んだことにする</a>〕"; }
		if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>全て読んだことにして終了</a>〕"; }
		print "〔<a href=\"$bye\" target=_top>終了</a>〕";
		print "</font><p>\n";
	}

	print "<table border=0><tr>\n";

	$i = $all - 1;
	if ($end < $i) {

		print "<form method=post action=\"$SCRIPT_NAME\?log=$CMD{'log'}\">\n";
		print "<input type=hidden name=\"start\" value=\"$end\">\n";
		print "<td><input type=submit value=\"↓次のページ\"></td></form>\n";
	}

	if ($all != 0) {

		print <<"EOF";
		</tr>
		<tr><td></td></tr>
		<tr>
		<form method=POST action="$SCRIPT_NAME\?log=$CMD{'log'}" name="SearchForm">
		<td colspan=2 bgcolor=$cellcolor>
		<a name="search"></a>
		検索文字列 <input type=text name="search" value="$keys" size=15>
		<input type=submit value="検索"><font size=-1>
		<input type=radio name="mode" value="and" checked>AND <input type=radio name="mode" value="or">OR<br>
		</font>
		<font size=-1>(空白で区切って複合検索可/題名,名前,Eメールによる)</font></td></form>
EOF
		if ($start == 0) { # 最初の画面だけ表示する

			print <<"EOF";
			<form method=POST action="$SCRIPT_NAME\?t=1">
			<input type=hidden name="log" value="$CMD{'log'}">
			<input type=hidden name="st" value="$start">
			<td bgcolor=$cellcolor align=right>
			番号 <input type=text name="v" value="" size=5>
			<input type=submit value="閲覧"></td>
			</tr></form>
EOF
		}
	}

	if ($start == 0 && $all != 0) {

		if ($COOKIE{'mode'} ne 'n') { $mes = '<font size=-1>↑コメント記事はカウントされません.</font>'; }

		print <<"EOF";
		<tr><td></td></tr>
		<form method=post action="$SCRIPT_NAME\?log=$CMD{'log'}">
		<input type=hidden name="cls" value="1">
		<tr><td bgcolor=$cellcolor align=center><input type=text name="ls" value="$def" size=5>行<input type=submit value="設定"></td>
		</form>
EOF
		if ($COOKIE{'rp'} ne '' && !$CMD{'log'}) {

			print <<"EOF";
			<form method=post action="$SCRIPT_NAME\?bye=crd">
			<td bgcolor=$cellcolor align=center>既読位置<input type=text name="rd" value="$COOKIE{'rp'}" size=5><input type=submit value="変更"></td>
			</form>
EOF
		}
	}

	if ($log && $start == 0) { # 最初の画面だけ表示する

		# 過去ログ一覧
		print "<form method=post action=\"$SCRIPT_NAME\">\n";
		print "<td bgcolor=$cellcolor align=center><select name=\"log\" size=1>\n";
		print "<option value=\"\">最新のログ</option>\n";

		$selected_log{$CMD{'log'}} = "selected";

		foreach $key (sort keys(%LOG)) {

			print "<option value=\"$key\" $selected_log{$key}>$LOG{$key}</option>\n";
		}

		print "</select><input type=submit value=\"閲覧\"></td></form>\n";
	}

	print "</tr></table> $mes<p>\n";

	# 必ず表示してくださいね
	print "<p align=right><a href=\"http://www.rescue.ne.jp/\" target=\"_top\"><img src=\"$SCRIPT_NAME\?image=copyright\" border=0 alt=\"Trees\"></a></p>\n";

	if (!$CMD{'log'}) { print "<font size=-1>"; }
	print "〔<a href=\"mailto:$administrator\">管理者への問合せ</a>〕\n"; # 管理に関して当サイトに問合せが来ることがある為
	print " ( )内は記事サイズ</font><p></body></html>\n";
}

sub search {

	if ($in{'search'} =~ /[&"<>]/) { &error("入力文字制限","記号の入力はできません."); }

	if ($in{'mode'} eq 'or') { $OR = 'checked'; $MODE = ' <sup>または</sup> '; }
	elsif ($in{'mode'} eq 'and' || $in{'mode'} eq '') { $AND = 'checked'; $MODE = ' <sup>かつ</sup> '; }

	$keys = $target = $in{'search'}; # 検索文字列
	$keys =~ s/　/ /g;
	$target =~ s/　/ /g;
	$target =~ s/(\W)/\\$1/g; # メタ処理
	@keys = split(/\\\s+/,$target);
	unless ($keys =~ / /) { $MODE = ''; }
	$keys2 = $keys;
	$keys2 =~ s/ /$MODE/g;

	&getdir('n');

	$next_num = '';
	$hit = 0;

	foreach $num ($start .. $#newls) {

		if (-s $newls[$num] == 0) { next; }
		($result) = &gethead($newls[$num],0);
		if (!$result) { next; }

		$string = "$HD{'uname'} $HD{'email'} $HD{'subject'}";

		if ($in{'mode'} eq 'or') { # 論理和検索

			$match = 1;
			foreach $term (@keys) { if ($string =~ /$term/i) { $match = 0; }}
		}
		else { # 論理積検索

			$match = 0;
			foreach $term (@keys) {	if (!($string =~ /$term/i)) { $match = 1; }}
		}

		if ($match) { next; }

		if ($hit == $def) { $next_num = $num; last; }
		else { push(@PICKUP,$newls[$num]); $hit++; }
	}

	&html_head;

	print "$body\n";
	print "$title<p>\n";

	print "<font size=-1>\n";
	if (!@PICKUP) { $msg = "<blink>前の画面</blink>"; } else { $msg = "前の画面"; }
	print "〔<a href=\"JavaScript:history.back()\">$msg</a>〕";
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?action=post\">新しい話題</a>〕"; }
	print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">検索モード解除</a>〕";
	if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>全て読んだことにする</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>全て読んだことにして終了</a>〕"; }
	print "〔<a href=\"$bye\" target=_top>終了</a>〕";
	print "</font><p>\n";

	print <<"EOF";
	<h3>《<blink>検索モード</blink>》$LOG_NAME</h3>
	検索条件 → $keys2<p>
EOF
	if (@PICKUP) {

		if ($alldel) { print "<a name=\"$number\"></a>\n"; }
		if ($CMD{'log'}) { $COOKIE{'rp'} = ''; }

		print "<DL>\n";
		if ($start != 0) { print "<DT><font size=-1>↑</font></dt>\n"; }

		foreach $filename (@PICKUP) {

			$k = '';

			# 時系列形式のみ
			($file,$ext) = split(/\./,$filename,2);
			if ($ext eq 'msg') { $cell = " bgcolor=$cellcolor"; } else { $cell = ''; }

			if (-s $filename == 0) { next; }
			($result) = &gethead($filename,0);
			if (!$result) { print "<DT>$kakko_l$file$kakko_r" . "Read Error E10($filename)</dt>\n"; next; }

			if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }

			if ($CMD{'bk'} == $file || $res_bk == $file) { $file2 = "<blink><font color=$pointc class=\"blink\">$file</font></blink>"; } else { $file2 = $file; }
			if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }

			$ukeys = $keys;
			$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URLエンコード
    			$ukeys =~ tr/ /+/;

			if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }
			$line = "<a name=\"$file\">$kakko_l$file2$kakko_r\</a>$new <a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&v=$file&e=$ext&lp=$file&st=$start\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'})</font>";

			$line = "<table cellpadding=0 cellspacing=1 border=0 width=100%><tr><td$cell>$line</td></tr></table>";
			print "<DT>$line</dt>\n";
		}
		print "</DL>\n";
	}
	else { print "抽出されませんでした.<p>\n"; }

	print "<hr size=1><table border=0>\n";

	if ($next_num ne '') {

		$next_num--;
		print "<form method=post action=\"$SCRIPT_NAME\?log=$CMD{'log'}\">\n";
		print "<input type=hidden name=\"start\" value=\"$next_num\">\n";
		print "<input type=hidden name=\"mode\" value=\"$in{'mode'}\">\n";
		print "<input type=hidden name=\"search\" value=\"$in{'search'}\">\n";
		print "<tr><td><input type=submit value=\"↓次のページ\"></td></tr></form>\n";
		print "<tr><td></td></tr>\n";
	}

	print <<"EOF";
	<tr>
	<form method=POST action="$SCRIPT_NAME\?log=$CMD{'log'}">
	<td  bgcolor=$cellcolor>
	検索文字列 <input type=text name="search" value="$keys" size=15>
	<input type=submit value="検索"><font size=-1>
	<input type=radio name="mode" value="and" $AND>AND <input type=radio name="mode" value="or" $OR>OR<br>
	</font></td></tr></table></form>
EOF
	# 必ず表示してくださいね
	print "<p align=right><a href=\"http://www.rescue.ne.jp/\" target=\"_top\"><img src=\"$SCRIPT_NAME\?image=copyright\" border=0 alt=\"Trees v1.01\"></a></p>\n";

	print "<font size=-1>\n";
	print "〔<a href=\"mailto:$administrator\">管理者への問合せ</a>〕\n"; # 管理に関して当サイトに問合せが来ることがある為
	print " ( )内は記事サイズ</font><p></body></html>\n";
}

sub gethead {

	local($file,$vv) = @_;
	@VAL = (); # 本文クリア

	if (!open(HEAD,$file)) { return(0); }
	while (<HEAD>) {

		if (/^$/) { last; } # 空行でヘッダ終了

		($key,$value) = split(/\t/);
		$value =~ s/\n//g;
		$HD{$key} = $value;
	}
	if ($vv) { while (<HEAD>) { push(@VAL,$_); }} # 本文
	close(HEAD);

	return(1);
}

sub view {

	local($number,$ext) = @_;

	if (-s "$number\.$ext" == 0) { &error("File Not Found","$numberは削除されています."); }
	($result) = &gethead("$number\.$ext",1);
	if (!$result) { &error("エラー","Read Error E10($number\.$ext)"); }

	#参照数処理
	if ($CMD{'log'}) { $no_count = 1; }
	if (!$no_count) {

		$HD{'rc'}++;

		if (open(OUT,"> $number\.$ext")) {

			print OUT "pwd\t$HD{'pwd'}\n";
			print OUT "rc\t$HD{'rc'}\n"; # カウント数を更新
			print OUT "date\t$HD{'date'}\n";
			print OUT "uname\t$HD{'uname'}\n";
			print OUT "email\t$HD{'email'}\n";
			print OUT "host\t$HD{'host'}\n";
			print OUT "subject\t$HD{'subject'}\n";
			print OUT "size\t$HD{'size'}\n";
			print OUT "how\t$HD{'how'}\n";
			print OUT "link\t$HD{'link'}\n";
			print OUT "resp\t$HD{'resp'}\n";
			print OUT "tree\t$HD{'tree'}\n";
			print OUT "psemail\t$HD{'psemail'}\n";
			print OUT "res\t$HD{'res'}\n";
			print OUT "\n";
			print OUT @VAL;
			close(OUT);
		}
	}

	if ($res_bk ne '') { $CMD{'lp'} = $CMD{'bk'} = $res_bk; }

	$ukeys = $in{'search'};
	$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URLエンコード
    	$ukeys =~ tr/ /+/;

	&html_head;

	print "$body\n";

	print <<"EOF";
	<font size=-1>
	〔<a href="JavaScript:history.back()">前の画面</a>〕
EOF
	if (!$CMD{'t'}) { print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$CMD{'lp'}\#$CMD{'lp'}\">クリックポイント</a>〕"; }

	print <<"EOF";
	〔<a href="$SCRIPT_NAME\?log=$CMD{'log'}">$newms</a>〕
EOF
	if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>全て読んだことにする</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>全て読んだことにして終了</a>〕"; }

	print <<"EOF";
	〔<a href="$bye" target=_top>終了</a>〕
	</font><p>
	<table cellpadding=3 cellspacing=0 border=0 width=100%><tr>
	<td bgcolor=$cellcolor><font size=+1><strong>$number $HD{'subject'}</strong></font></td>
	</tr></table>
EOF
	if ($view_host) { $host = "- <font size=-1>$HD{'host'}</font>"; } else { $host = ""; }
	print " <font size=-1>$HD{'date'}</font> ";
	if ($HD{'email'} ne '') { print "- <a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a> "; }
	else { print "- $HD{'uname'} "; }
	print "$host";

	if ($HD{'psemail'}) { $Pse = '- ResMail'; } else { $Pse = ''; }
	if (!$CMD{'log'}) { print " - <font size=-1>$HD{'rc'} hit(s) $Pse"; }
	print "</font><p>\n";

	if (!$CMD{'log'}) {

		print "<table border=1 cellpadding=1 cellspacing=0 align=right><tr>\n";
		print "<form method=post action=\"$SCRIPT_NAME\?tw=$CMD{'t'}&search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$CMD{'lp'}&lp=$CMD{'lp'}\">\n";
		print "<input type=hidden name=\"action\" value=\"post\">\n";
		print "<input type=hidden name=\"resp_number\" value=\"$number\.$ext\">\n";
		print "<input type=hidden name=\"resp_subject\" value=\"$HD{'subject'}\">\n";
		print "<input type=hidden name=\"resp_base\" value=\"$HD{'tree'}\">\n";
		print "<td><input type=submit value=\"   返信   \"><font size=-1><input type=checkbox name=\"inyou\" value=\"1\">引用する</font></td></form>\n";

		if ($in{'search'} ne '') { $lp = $CMD{'lp'}; } else { $lp = $number; }

		print "<form method=post action=\"$SCRIPT_NAME\?search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$number\#$number\">\n";
		print "<input type=hidden name=\"action\" value=\"remove\">\n";
		print "<input type=hidden name=\"remove_number\" value=\"$number\.$ext\">\n";
		print "<td><font size=-1>現在のパスワード</font><input type=password name=\"pwd\" value=\"$COOKIE{'pwd'}\" size=10>";
		print "<input type=submit value=\"削除\"></td></form>\n";
		print "</tr></table></form>\n";
	}

	print "<p><hr size=1><p>\n";

	if ($HD{'how'} == 1) { print "<pre><tt>"; } # 図/表モード

	@VAL2 = @VAL;
	foreach $value (@VAL2) {

		if (($HD{'link'} != 2 && $allow_html) || !$allow_html) { # タグ不許可またはタグを使わない場合

			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
		}

		if ($allow_html) { # タグ許可の場合はtarget属性を追加する

			$value =~ s/<a href=/<a target="_blank" href=/ig;
		}

		if ($HD{'link'} == 1 && !$allow_html) { # タグ不許可でURLリンクする場合

			$value =~ s/&gt;/\t/g;
			$value =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig;
			$value =~ s/\t/&gt;/g;
		}

		if ($HD{'link'} == 2 && $allow_html) { print $value; } # HTML有効時
		elsif ($HD{'how'} == 1) { print $value; } # 図/表モード
		elsif ($HD{'how'} == -1) { $value =~ s/\n/<br>\n/g; print $value; } # 改行有効
		else { $value =~ s/\n//g; print $value; } # 改行無効
	}

	if ($HD{'how'} == 1) { print "</tt></pre><p>\n"; } # 図/表モード

	#スレッド
	print "<p><hr size=1><a name=\"tree\"></a><p>\n";
	print "〔ツリー構\成〕<p>\n";
	print "<DL>\n";

	if ($ext eq 'msg') { $tree = $number; }
	else { $tree = $HD{'tree'}; }

	if (open(TREE,"$tree\.tre")) {

		@trees = <TREE>;
		close(TREE);

		foreach $line (@trees) {

			$line =~ s/\n//g;

			if ($line =~ /<DD>/) { next; }
			elsif ($line =~ /<DL>/) { print "<DD><DL>\n"; next; }
			elsif ($line =~ /<\/DL>/) { print "</DL></dd>\n"; next; }
			elsif ($line =~ /<DT>\!(\d+)\.(msg|res)/) {

				$num = $1;
				$ext = $2;

				if ($ext eq 'res') { $k = $keisen; }
				next;
			}
			elsif ($line =~ /<DT>\D*(\d+)\.(msg|res)/) {

				$num = $1;
				$ext = $2;
				$file = "$num\.$ext";

				if ($ext eq 'res') { $k = $keisen; } # レスに罫線をつける
				if ($CMD{'lp'} == $num && !$CMD{'t'}) { $p = "<blink><font color=$pointc class=\"blink\">$point</font></blink>"; } else { $p = ""; } # クリックポイント印
				if ($basenum == $num) { $num2 = "<blink><font color=$pointc class=\"blink\">$num</font></blink>"; } else { $num2 = $num; }

				if (-s $file == 0) { next; }
				($result) = &gethead($file,0);
				if (!$result) {

					print "$k$kakko_l$num2$kakko_r" . "Read Error E10($file)\n";
					next;
				}

				if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }
				if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }
				if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }

				$change = "$kakko_l$num2$kakko_r$new <a href=\"$SCRIPT_NAME\?tw=$CMD{'t'}&log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&v=$num&e=$ext&lp=$CMD{'lp'}&st=$CMD{'st'}\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'}) </font>";
				$change2 = "$kakko_l$num2$kakko_r$new $HD{'subject'} <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'}) </font>";
				$line =~ s/<DT>//;

				if ($number == $num) { $line = "<table border=0 cellpadding=0 cellspacing=0><tr><td bgcolor=$cellcolor>$k$change2 $p</td></tr></table>"; }
				else { $line = "<table border=0 cellpadding=0 cellspacing=0><tr><td>$k$change $p</td></tr></table>"; }
			}
			print "<DT><a name=\"$num\"></a>$line</dt>\n";
		}
	}
	else { print "<DT>Read Error E11($tree\.tre)</dt>\n"; }

	print "</DL>\n";

	print <<"EOF";
	<hr size=1>
	<font size=-1>
	〔<a href="JavaScript:history.back()">前の画面</a>〕
EOF
	if (!$CMD{'t'}) { print "〔<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$CMD{'lp'}\#$CMD{'lp'}\">クリックポイント</a>〕"; }

	print <<"EOF";
	〔<a href="$SCRIPT_NAME\?log=$CMD{'log'}">$newms</a>〕
EOF
	if ($CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\" target=_top>最新のログ</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>全て読んだことにする</a>〕"; }
	if (!$CMD{'log'}) { print "〔<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>全て読んだことにして終了</a>〕"; }

	print <<"EOF";
	〔<a href="$bye" target=_top>終了</a>〕
EOF
	if (!$CMD{'t'}) {

		print <<"EOF";
		<p>※ 『クリックポイント<blink><font color=$pointc class=\"blink\">$point</font></blink>』とは一覧上から読み始めた地点を指し、ツリー上の記事を巡回しても、その位置に戻ることができます.
EOF
	}
	print "<p></body></html>\n";
}

sub prev { # プレビュー処理

	&html_head;
	&gethost;

	print "$body\n";

	print <<"EOF";
	<table cellpadding=3 cellspacing=0 border=0 width=100%><tr>
	<td bgcolor=$cellcolor><font size=+1>《表\示確認》 <strong>$in{'subject'}</strong></font></td>
	</tr></table>
EOF

	if ($in{'email'} ne '') { print "by <a href=\"mailto:$in{'email'}\">$in{'uname'}</a> "; }
	else { print "by $in{'uname'} "; }

	if ($view_host) { print "- <font size=-1>$host</font>"; }

	if ($in{'psemail'}) { print " - <font size=-1>ResMail</font>"; }

	print "<hr size=1><p>\n";

	if ($in{'how'} == 1) { print "<pre><tt>"; } # 図/表モード

	$value = $in{'value'};

	if (($in{'link'} != 2 && $allow_html) || !$allow_html) {

		$value =~ s/&/&amp;/g;
		$value =~ s/"/&quot;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
	}

	if ($allow_html) { $value =~ s/<a href=/<a target="_blank" href=/ig; }

	if ($in{'link'} == 1 && !$allow_html) {

		$value =~ s/&gt;/\t/g;
		$value =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig;
		$value =~ s/\t/&gt;/g;
	}

	if ($in{'link'} == 2 && $allow_html) { print $value; } # HTML有効時
	elsif ($in{'how'} == 1) { print $value; } # 図/表モード
	elsif ($in{'how'} == -1) { $value =~ s/\n/<br>\n/g; print $value; } # 改行有効
	else { $value =~ s/\n//g; print $value; } # 改行無効
	if ($in{'how'} == 1) { print "</tt></pre><p>\n"; } # 図/表モード

	print <<"EOF";
	<p>
	<hr size=1>
	<h3>
	〔<a href="JavaScript:history.back()">投稿画面に戻る</a>〕
	</h3></body></html>
EOF

}

sub bye {

	($lastf) = &getlast;
	($lastnum,$ext) = split(/\./,$lastf,2);

	if ($in{'rd'} ne '') { # 任意の既読位置設定

		if ($in{'rd'} > $lastnum) { $in{'rd'} = $lastnum; }
		print "Set-Cookie: $SCRIPT_NAME" . '2' . "=rp:$in{'rd'}\,lastlogin:$COOKIE{'lastlogin'}; path=$path; expires=$date_gmt\n";
	}
	else {
		# 全て読んだことにする(最終番号を既読位置として設定)
		print "Set-Cookie: $SCRIPT_NAME" . '2' . "=rp:$lastnum\,lastlogin:$date_now; path=$path; expires=$date_gmt\n";
	}

	if ($SCRIPT_NAME =~ /$prot/) { $prot = ''; }
	else { $prot = "$prot://$ENV{'SERVER_NAME'}"; }

	if ($CMD{'bye'} eq 'reset' || $CMD{'bye'} eq 'crd') { print "Location: $prot$SCRIPT_NAME\?log=$CMD{'log'}\n\n"; }
	else { print "Location: $bye\n\n"; }
}

sub post {

	if ($CMD{'log'}) { &error(); }

	if ($in{'search'} ne '') {

		$ukeys = $in{'search'};
		$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URLエンコード
    		$ukeys =~ tr/ /+/;
	}

	if ($chk < 0 || $chk > 2) { $chk = 0; }
	$howc[$chk] = "checked";

	if ($in{'resp_number'} ne '') {

		($respnum,$ext) = split(/\./,$in{'resp_number'},2);
		if (-s "$respnum\.$ext" == 0) { &error("File Not Found","$respnumは削除されていますので、コメントできません."); }

		if ($in{'inyou'}) { $get_val = 1; } else { $get_val = 0; }
		($result) = &gethead("$respnum\.$ext",$get_val);
		if (!$result) {	@VAL = (); }

		if ($HD{'how'} == 1 && $in{'inyou'}) {

			$howc[$chk] = "";
			$howc[1] = "checked";
			$com = '(注！引用文は図/表モードで記録されています)';
		}
		if ($in{'inyou'}) { $caution = "※ 引用部分は必要最低限にしましょう. サーバ資源の節約にご協力ください.<p>\n"; }

		$write_title = "$respnumへのコメント";
		$ichi = "#tree";
	}
	else { $write_title = "新しい話題"; $ichi = ""; }

	#題名処理
	if ($in{'resp_subject'} eq '') { $subject = ''; }
	elsif ($attnum) {

		if ($in{'resp_subject'} =~ /^re\((.*)\):(.*)/) {

			$title = $2;
			if ($1 =~ /(\d+)/) {

				$resnum = ($1 + 1);
				$subject = "re($resnum):$title";
			}
			else { $subject = "re:$in{'resp_subject'}"; }
		}
		else { $subject = "re(1):$in{'resp_subject'}"; }
	}
	else { $subject = "re:$in{'resp_subject'}"; }

	# カーソルフォーカス位置
	if ($COOKIE{'uname'} eq '') { $focus = 'onLoad="document.InputForm.uname.focus();"'; }
	elsif ($in{'resp_number'} eq '') { $focus = 'onLoad="document.InputForm.subject.focus();"'; }
	else { $focus = 'onLoad="document.InputForm.value.focus();"'; }

	if ($body =~ /<body([^<>]*)>/i) { $body = "<body$1 $focus>"; }

	&html_head;
	print "$body\n";

	print <<"EOF";
	<h3>$write_title</h3>
	$caution
	<form method=post action="$SCRIPT_NAME\?tw=$CMD{'tw'}&search=$ukeys&mode=$in{'mode'}&bk=$CMD{'bk'}&st=$CMD{'st'}$ichi" name="InputForm">
	<input type=hidden name="action" value="write">
	<input type=hidden name="resp_number" value="$respnum\.$ext">
	<input type=hidden name="resp_base" value="$in{'resp_base'}">
	<table border=3 cellpadding=1 cellspacing=2>
	<tr><th align=right>投稿者</th>
	<td><input type=text name="uname" size=20 value="$COOKIE{'uname'}"></td></tr>
	<tr><th align=right>Ｅメール</th>
	<td><input type=text name="email" size=40 value="$COOKIE{'email'}"></td></tr>
	<tr><th align=right>パスワード</th>
	<td><input type=password name="pwd" size=10 value="$COOKIE{'pwd'}"> <font size=-1>※この記事を削除するためのパスワードです.</font></td></tr>
	<tr><th align=right>題名</th>
	<td><input type=text name="subject" value="$subject" size=60></td></tr>
	<tr><th align=right>内容</th>
	<td><font size=-1>
	<input type=radio name="how" value="0" $howc[0]>改行無効
	<input type=radio name="how" value="-1" $howc[2]>改行有効
	<input type=radio name="how" value="1" $howc[1]>図/表\モード $com</font><br>
EOF
	print "<textarea name=\"value\" rows=15 cols=80 wrap=off>";

	if ($in{'inyou'}) {

		foreach $value (@VAL) {	print "$HD{'uname'}&gt; $value"; }
		print "\n</textarea>";
	}
	else { print "</textarea>"; }

	if (!$allow_html) { print "<br>\n<font size=-1><input type=checkbox name=\"link\" value=\"1\" checked>内容にURLがあればリンクさせる</font></td>"; }
	else { print "<br>\n<font size=-1><input type=checkbox name=\"link\" value=\"2\">ＨＴＭＬを有効にする</font></td>"; }

	print <<"EOF";
	</tr>
	<tr><td></td>
	<td align=center><input type=checkbox name="cookie" value="1" checked><font size=-1>投稿者とメールとパスワードを保存</font>
EOF
	if ($resmail) { print "<input type=checkbox name=\"psemail\" value=\"1\"> <font size=-1>コメントがついたらメール連絡が欲しい</font></td></tr>\n"; }

	print <<"EOF";
	<tr><td></td>
	<td align=center><input type=submit name="preview" value="？プレビュー">　　<input type=submit value="  ○ 投稿  " onClick="f=confirm('投稿しますか？');return f"> <input type=reset value="× リセット"></td></tr>
	</table></form>
	<p>
	〔<a href="JavaScript:history.back()">前の画面</a>〕<p>
	<font size=-1>
	<ul>
	<li>引用文は最低限にしましょう.
EOF
	if ($resmail) { print "<li>コメントがついたらメール連絡する機能\は、自己レスには適用されません.<p>\n"; }

	print <<"EOF";
	<li>[改行無効] 改行と連続した半角空白が無視されます.
	<li>[改行有効] 改行を入れた位置で折り返されますが、連続した半角空白が無視されます.
	<li>[図/表\モード] 記入された通りに記録します.
EOF
	if ($allow_html) { print "<li>ＨＴＭＬを有効にする場合は、図/表\モード以外は無効になります.\n"; }

	print <<"EOF";
	</ul>
	</font>
	<p>
	</body></html>
EOF

}

sub write {

	if ($CMD{'log'}) { &error(); }
	if (!$resmail) { $in{'psemail'} = ''; }

	if ($ENV{'REQUEST_METHOD'} ne "POST") { &error('エラー','(E4)'); }

	if ($ref_axs) {

		$ref = $ENV{'HTTP_REFERER'};
		if (!($ref =~ /$SCRIPT_NAME/i)) { &error('投稿不可',"「$SCRIPT_NAME」以外からの投稿を検知しました. (E5)<br>$ref<br>$SCRIPT_NAME"); }
	}

	($lastf) = &getlast;
	($num,$ext) = split(/\./,$lastf,2);
	$basenum = $num + 1;

	($respnum,$ext) = split(/\./,$in{'resp_number'},2);
	if ($in{'resp_number'} ne '' && !-e "$respnum\.$ext") { &error('返信エラー',"返信元となる$respnum番の記事は削除されていますので、コメントできません."); }

	if ($in{'resp_base'} eq '') { $in{'resp_base'} = $basenum; }

	if ($in{'uname'} eq '') { &error('入力不備','名前が書かれていません.'); }
	if ($in{'email'} eq '' && $in{'psemail'}) { &error('入力不備','コメントがついた時に連絡が欲しい場合はＥメールを入力してください.','なお、メールが届かない主な理由は記入ミスですので、ご注意ください.'); }

	if (length($in{'uname'}) > 20) { &error('入力不備','名前は20バイト以内でご記入ください.'); }
	if ($in{'subject'} eq '') { &error('入力不備','題名が書かれていません.'); }
	if ($in{'pwd'} =~ /\W/ || $in{'pwd'} eq '') { &error('入力不備','パスワードを半角英数字で入力してください.'); }
	if ($in{'value'} eq '') { &error('入力不備','内容が書かれていません.'); }

	$host = &gethost;

	($crypt_password) = &MakeCrypt($in{'pwd'});

	$MSGc = "$in{'uname'}\t$in{'email'}\t$in{'subject'}\t$in{'value'}";
	$MSGc =~ s/\n//g;

	# 同内容連続投稿防止
	if (!-e $wcheck) {

		if (!open(CHECK,"> $wcheck")) { &error("エラー","(E6)"); }
		close(CHECK);
	}

	if (open(CHECK,$wcheck)) {

		$cmsg = <CHECK>;
		close(CHECK);

		if ($cmsg eq $MSGc) {

			if ($in{'search'} eq '') { $i = $CMD{'bk'}; $CMD{'bk'} = $basenum; }
			$res_bk = $i;

			if ($basenum ne $in{'resp_base'}) {

				($respnum,$ext) = split(/\./,$in{'resp_number'},2);
				$no_count = 1;
				&view($respnum,$ext);
			}
			elsif ($in{'search'} ne '') { &search; }
			else { &list; }

			return;
		}
		else {
			if (!open(CHECK,"> $wcheck")) { &list; return; }
			print CHECK $MSGc;
			close(CHECK);
			chmod(0666,$wcheck);
		}
	}

	if ($in{'search'} eq '') { $i = $CMD{'bk'}; $CMD{'bk'} = $basenum; }
	else {  $i = $CMD{'bk'}; }
	$res_bk = $i;

	if ($in{'resp_number'} ne '' && -s $in{'resp_number'} == 0) { &error("File Not Found","$in{'resp_number'}は削除されていますので、コメントの投稿はできません."); }

	# 拡張子の決定(新規記事は.mes コメントは.res ちなみにツリーファイルは.tre)
	if ($basenum eq $in{'resp_base'}) { $ext = 'msg'; } else { $ext = 'res'; }

	if (!open(OUT,"> $basenum\.$ext")) { &error('記録エラー',"記事の記録ができません.(E7)"); }

	print OUT "pwd\t$crypt_password\n"; # 記事パスワード
	print OUT "rc\t0\n"; # リードカウント
	print OUT "date\t$date_now\n"; # 時刻
	print OUT "uname\t$in{'uname'}\n"; # 投稿者
	print OUT "email\t$in{'email'}\n"; # Ｅメール
	print OUT "host\t$host\n"; # ホスト名
	print OUT "subject\t$in{'subject'}\n"; # 記事のタイトル
	$size = length($in{'value'});
	print OUT "size\t$size\n"; # 記事のサイズ
	print OUT "how\t$in{'how'}\n"; # 記録モード(改行無効:0 有効:-1 図表:1)
	print OUT "link\t$in{'link'}\n"; # URL自動リンクの有無(する:1)
	print OUT "resp\t$in{'resp_number'}\n"; # 直接のコメント元となる記事番号
	print OUT "tree\t$in{'resp_base'}\n"; # この記事が属するツリーファイルの番号
	print OUT "psemail\t$in{'psemail'}\n"; # コメンお知らせメールをするかどうか(する:1)
	print OUT "res\t\n"; # この記事にコメントが存在するかどうか(する:1)
	print OUT "\n"; # ヘッダと本文を分ける改行
	print OUT $in{'value'}; # 本文
	close(OUT);
	chmod(0666,"$basenum\.$ext");

	&tree; # ツリー処理

	# コメントお知らせメール処理
	if ($in{'resp_number'} ne '.') { ($result) = &gethead($in{'resp_number'},0); }
	if ($resmail && $HD{'psemail'} && $in{'email'} ne $HD{'email'}) {

		$HD{'email'} =~ s/\n//g;
		$mail_subject =~ s/\n//g;

		if (!open(OUT,"| $sendmail -t")) { &error('システムエラー','システム復旧までお待ちください.'); }
		print OUT "To: $HD{'email'}\n";
		print OUT "From: $administrator\n";
		print OUT "Errors-To: $administrator\n";
		print OUT &jis("Subject: $mail_subject\n"); # 全角を含むものはJIS変換
		print OUT "Content-Transfer-Encoding: 7bit\n";
		print OUT 'Content-Type: text/plain; charset=iso-2022-jp' . "\n\n";

		print OUT &jis("$mail_val\n");
		($num,$ext) = split(/\./,$in{'resp_number'},2);
		print OUT &jis("  (No.$num)$HD{'subject'} に、\n");
		print OUT &jis("  コメント(No.$basenum)がありました.\n");
		print OUT &jis("\n$mail_val2\n");

		close(OUT);
	}

	# コメントの場合は親記事にコメントが付いたことを記録する
	if ($in{'resp_number'} ne '') {

		($result) = &gethead($in{'resp_number'},1);
		if (!$result) { &error("エラー","Read Error E10($in{'resp_number'})"); }

		if (open(OUT,"> $in{'resp_number'}")) {

			print OUT "pwd\t$HD{'pwd'}\n";
			print OUT "rc\t$HD{'rc'}\n";
			print OUT "date\t$HD{'date'}\n";
			print OUT "uname\t$HD{'uname'}\n";
			print OUT "email\t$HD{'email'}\n";
			print OUT "host\t$HD{'host'}\n";
			print OUT "subject\t$HD{'subject'}\n";
			print OUT "size\t$HD{'size'}\n";
			print OUT "how\t$HD{'how'}\n";
			print OUT "link\t$HD{'link'}\n";
			print OUT "resp\t$HD{'resp'}\n";
			print OUT "tree\t$HD{'tree'}\n";
			print OUT "psemail\t$HD{'psemail'}\n";
			print OUT "res\t1\n"; # この記事にコメントが存在するかどうか(する:1)
			print OUT "\n";
			print OUT @VAL;
			close(OUT);
		}
	}

	if ($in{'cookie'}) { $cook="uname\:$in{'uname'}\,email\:$in{'email'}\,pwd\:$in{'pwd'}\,mode\:$COOKIE{'mode'}"; }
	else { $cook=""; $date_gmt = ""; }

	$cook =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URLエンコード
	$cook =~ tr/ /+/;

	print "Set-Cookie: $SCRIPT_NAME=$cook; path=$path; expires=$date_gmt\n";

	if ($COOKIE{'mode'} ne 't' && $ext ne 'msg') { $CMD{'st'}++; $start++; } # 戻り位置調整
	if ($CMD{'tw'}) { $CMD{'t'} = 1; }

	if ($basenum ne $in{'resp_base'}) {

		($respnum,$ext) = split(/\./,$in{'resp_number'},2);
		$no_count = 1;
		&view($respnum,$ext);
	}
	elsif ($in{'search'} ne '') { &search; }
	else { &list; }
}

sub tree {

	if ($basenum eq $in{'resp_base'}) {

		if (!open(OUT,"> $basenum\.tre")) { &error('記録エラー','スレッドファイルに記録できません.(E7)'); }
		print OUT "<DT>$basenum\.$ext\n";
		print OUT "<DD><!--$basenum-->\n"; # コメント挿入位置
		close(OUT);
		chmod(0666,"$basenum\.tre");

		return;
	}
	else { if (!-e "$in{'resp_base'}\.tre") { return; }}

	if (!open(IN,"$in{'resp_base'}\.tre")) { return; }
	@tr_file = <IN>;
	close(IN);

	if (!open(OUT,"> $in{'resp_base'}\.tre")) { return; }

	foreach $line (@tr_file) {

		if ($line =~ /<DD><!--$respnum-->/) {

			print OUT "<DL>\n";
			print OUT "<DT>$basenum\.$ext\n";
			print OUT "<DD><!--$basenum-->\n";
			print OUT "</DL>\n";
			print OUT "<DD><!--$respnum-->\n";
	     	}
		else { print OUT $line; }
	}

	close(OUT);
	chmod(0666,"$in{'resp_base'}\.tre");
}

sub remove {

	if ($CMD{'log'}) { &error(); }

	($number,$ext) = split(/\./,$in{'remove_number'},2);

	if (!-e "$number\.$ext") { return(0); } # 既に物理削除されている
	if (-s "$number\.$ext" == 0) { return(0); } # 既に論理削除されている

	($result) = &gethead("$number\.$ext",1);
	if (!$result) { return(0); } # ファイル異常

	if ($HD{'pwd'} eq '') { &error("エラー","Read Error E10($number\.$ext)"); }
	if ($HD{'pwd'} =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }

	if (!$admin) {

		if (crypt($in{'pwd'},substr($HD{'pwd'},$salt,2)) ne $HD{'pwd'} && !$admin) { &error('認証エラー',"パスワードが合いませんので削除できません.(E8)"); }
		if ($HD{'res'} && $delsave) { &error('削除不可',"この記事にはコメントがあるので、管理者以外は削除できません.","処理の都合上、コメントが削除されていたとしても同様です."); }
	}

	if (open(DEL,"> $number\.$ext")) { print DEL ''; close(DEL); } # 論理削除
	else { push(@NOT_REMOVE,"$number\.$ext"); }

	#ツリーファイルの更新
	if (!open(IN,"$HD{'tree'}\.tre")) { return(0); }
	@tr_file = <IN>;
	close(IN);

	foreach $line (@tr_file) {

		# 論理削除
		$line =~ s/<DT>$number\.$ext/<DT>!$number\.$ext/;
		if ($line =~ /<DD><!--$number-->/) { next; }
		push(@new,$line);
	}

	# ツリー更新
	if (!open(OUT,"> $HD{'tree'}\.tre")) { return; }
	print OUT @new;
	close(OUT);

	if (@NOT_REMOVE) { &error('実行結果',"次のファイルの削除に失敗しました. 管理者に削除依頼してください.(E9) &gt; @NOT_REMOVE"); }

	if (open(CHECK,"> $wcheck")) {

		print CHECK '';
		close(CHECK);
	}

	return(1);
}

sub gethost {

	#ホスト名の取得(リムネットなら次の４行を指定のプログラムと入れ替える)

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq '') { $host = $addr; }
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	if ($host eq '') { $view_host = 0; }
	return $host;
}

sub jis { $msg = $_[0]; &jcode'convert(*msg,'jis'); return $msg; }

sub html_head {

	$title_bar =~ s/\n//g;

	print "Content-type: text/html\n\n";

	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML><HEAD>
	<TITLE>$title_bar</TITLE>
	<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
	<meta name="description" content="$title_bar">
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	<style type="text/css">
	<!--
	font.blink { text-decoration: blink }
	-->
	</style>
	</HEAD>
EOF
}

sub setpwd_form {

	if ($CMD{'log'}) { &error(); } # 過去ログモード時はエラー
	if (-e $lockfile) { unlink $lockfile; }

	&html_head;

	print <<"EOF";
	$body
	<h1>管理者パスワードの設定/変更<hr size=1></h1>
	<form action=$SCRIPT_NAME method=POST>
	<input type=hidden name="action" value="setpwd">
EOF
	if (!-z $pwd_file) { print "現パスワード <input type=password name=\"old_password\" size=10><br>\n"; }

	print <<"EOF";
	新パスワード <input type=password name="new_password" size=10><br>
	新パスワード <input type=password name="retype_password" size=10> (もう一度)<p>
	<input type=submit value="実行">
	</form><p><hr size=1>
EOF
	if (!-z $pwd_file) { print "[<A HREF=\"JavaScript:history.back()\">戻る</A>]<p>\n"; }
	print "</body></html>\n";
	exit;
}

sub setpwd {

	if ($CMD{'log'}) { &error(); }

	if (!-z $pwd_file) {

		if (!open(READ,$pwd_file)) { &error('エラー','管理者用パスワードファイルが読み出せません.(E12)'); }
		$master = <READ>;
		close(READ);

		chop($master) if $master =~ /\n/;
		if ($master =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
		if (crypt($in{'old_password'},substr($master,$salt,2)) ne $master) { &error("Authorization Required",'現パスワードが認証されませんでした.(E13)'); }
	}

	if (length($in{'new_password'}) < 6 || $in{'new_password'} eq '') { &error('入力ミス','6文字以上のパスワードを指定してください.(E14)'); }
	if ($in{'new_password'} ne $in{'retype_password'}) { &error('入力ミス','２回入力したパスワードが合いません.'); }

	($pwd) = &MakeCrypt($in{'new_password'});

	if (!open(WRITE,"> $pwd_file")) { &error('エラー','管理者用パスワードファイルに記録できません.(E15)'); }
	print WRITE $pwd;
	close(WRITE);
}

sub master_check {

	local($admin);
	$admin = 0;

	if (!open(READ,$pwd_file)) { &error('エラー','管理者用パスワードファイルが読み出せません.(E12)'); }
	$master = <READ>;
	close(READ);

	chop($master) if $master =~ /\n/;
	if ($master =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	if ($master eq '') { ; }
	elsif (crypt($in{'pwd'},substr($master,$salt,2)) eq $master) { $admin = 1; }

	return $admin;
}

sub MakeCrypt {

	my ($mypass) = $_[0];
	srand();
	my @saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	my $nsalt = $saltset[int(rand(64))] . $saltset[int(rand(64))];
	return crypt($mypass,$nsalt);
}

sub decode_cookie {

	local($name) = @_;
	local($cookies);

	# 期限を30日後に設定(GMT)
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + 30*24*60*60);
	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun"; $m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);
	@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);
	$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",$youbi[$wdayg],$mdayg,$monthg[$mong],$yearg +1900,$hourg,$ming,$secg);

	$cookies = $ENV{'HTTP_COOKIE'};

	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {

		($key,$val) = split(/=/,$pair,2);
		$key =~ s/ //g;

		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		if ($key eq $name) {

			@pairs = split(/,/,$val);
			foreach $pair (@pairs) {

				($key,$val) = split(/:/,$pair,2);
				$COOKIE{$key} = $val;
			}
			last;
		}
	}
}

sub lock {

	# ロック方式の自動判定 symlink()優先
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file式

			$c++;
			if ($c >= 3) { &error('リトライエラー','ただいま混雑しております.<br>戻ってもう一度実行してみてください.(E17)'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink式

			if (--$retry <= 0) { &error('リトライエラー','ただいま混雑しております.<br>戻ってもう一度実行してください.(E17)'); }
			sleep(2);
		}
	}
}

sub image {

	local($image) = @_;

	if (-e $lockfile) { unlink $lockfile; }

	if ($image eq 'new') { # New!画像データ

		@array = (
		"47","49","46","38","39","61","16","00","0a","00","b3","02","00","00","00","00","ff","d6","00","ff",
		"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","21","f9","04","01","00","00","02","00","2c","00","00","00","00","16","00","0a","00","40","04",
		"37","50","c8","29","02","ad","77","06","60","2b","0f","60","b8","71","00","e7","99","db","88","7e",
		"21","ab","81","65","1c","be","70","4d","8a","69","6e","66","38","98","49","29","e0","4d","b4","f3",
		"d8","8e","3e","c1","67","59","3b","a9","4a","47","54","12","c3","eb","09","22","00","3b");
	}
	elsif ($image eq 'copyright') { # ロゴ画像データ

		@array = (
		"47","49","46","38","39","61","30","00","20","00","b3","03","00","00","00","00","18","18","18","84",
		"84","84","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","21","f9","04","01","00","00","03","00","2c","00","00","00","00","30","00","20","00","40","04",
		"ff","70","c8","49","ab","bd","38","e3","00","40","10","c3","e7","0d","02","47","72","41","0a","90",
		"eb","19","48","a9","26","09","25","d7","dd","37","59","ba","fa","b7","83","af","12","e8","d4","91",
		"09","8a","b3","63","e7","38","58","2a","25","4e","64","54","66","51","bd","2a","d7","50","36","4b",
		"4d","d2","54","9d","20","e7","0b","20","13","59","b3","72","ad","74","4b","71","29","38","5c","77",
		"3e","a3","3e","27","77","56","ab","a9","9f","b4","d4","48","74","74","6f","82","17","56","36","69",
		"89","21","2d","31","30","84","19","4a","31","34","7a","71","6d","87","1e","36","98","57","5b","23",
		"30","96","14","6c","62","41","2d","47","1f","92","41","42","a3","26","1a","34","ad","ad","78","33",
		"a7","24","76","ab","16","43","4f","43","85","ba","b6","81","7d","69","71","94","39","34","39","76",
		"af","5e","b9","3a","93","78","c6","c9","c8","bb","cf","d0","73","57","3b","d1","86","72","30","b1",
		"69","9b","d5","60","3e","9d","ab","26","6c","3c","8b","14","8f","58","61","9e","a5","44","95","71",
		"6e","23","d4","e7","13","6e","99","a7","ed","2a","64","c3","ad","9a","9f","98","58","28","3e","b1",
		"3c","0c","d3","b1","62","a0","3a","26","6b","bc","b9","59","c6","c6","52","0a","5c","a7","44","d5",
		"38","11","eb","07","22","5b","ae","dc","b5","99","e5","63","9a","98","3a","b3","3b","96","f5","82",
		"a6","cc","19","2b","78","15","8e","0c","03","54","6d","57","9e","26","45","a4","10","83","32","13",
		"e6","48","0c","2f","71","f5","c1","55","84","e7","92","39","39","03","29","31","36","54","19","c1",
		"9b","17","ae","d9","24","a5","04","c9","4a","a7","4a","5b","4a","95","10","01","00","3b");
	}
	else { return; }

	print "Content-type: image/gif\n\n";
	foreach (@array) { $data = pack('C*',hex($_)); print $data; }
}

sub error {

	if (-e $lockfile) { unlink $lockfile; }

	local (@msg) = @_;
	local ($i);

	&html_head;

	print <<"EOF";
	$body
	<h1>$_[0]</h1>
EOF

	print "<ul>\n";
	foreach $i (1 .. $#msg) { print "<li>$msg[$i]\n"; }
	print "</ul>\n";

	print <<"EOF";
	<h3>[<A HREF="JavaScript:history.back()">戻る</A>]</h3>
	</body></html>
EOF
	exit;
}
