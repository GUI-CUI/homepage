#!/usr/local/bin/perl

# �d�q�f���� -Trees- v2.11 FreeSoft
# (c)1999-2009 by CGI-RESCUE
#
# for UNIX/SJIS
#
# [�ݒu�\����] �ڂ�����readme.txt���Q�Ƃ��Ă��������B
#
# ����/data/ <777>
# ��
# �� jcode.pl <644>
# �� trees.cgi <755>
# �� password.cgi <666>
#
# [����]
# v 1.00 07/MAY/1999 ����
# v 1.01 08/MAY/1999 �ꗗ�̕\���薼�������ݒ�
# v 1.02 17/JUN/1999 �^�O�L������<br>�R�[�h���o�͂��Ȃ��悤�ɏC��
# v 1.03 09/JUL/1999 �^�O�����̕ϐ��~�X���C��
# ------- ���������Ƀf�[�^�̊��S�݊��͂���܂��񂪁A�d��Ȏx��Ȃ��f�[�^�͌�p�ł��܂�.
# v 2.00 10/JUL/1999 �R�����g���[���@�\,�v���r���[�@�\,���p�J�i�΍�,New!�摜�ɏc���T�C�Y�ݒ�,�R�����g�L��L���̍폜�𐧌�����@�\
# v 2.01 11/JUL/1999 �폜�֌W�̃o�O���C��
# v 2.02 15/JUL/1999 �Ӗ��s���̃o�O�̏C��
# v 2.03 30/APR/2000 MAC��IE5�Ή��̂��߂ɃC���f���g�^�O�̏C���A�N�b�L�[��URL�R���R�[�h��
# v 2.04 17/AUG/2002 Mozilla1.0�ɂ����ăX���b�h�̐[�����������\���ł��Ȃ��s��̏C��
# v 2.10 06/JUN/2006 �폜���ꂽ���e��\�����Ȃ��E���e���Ɋm�F�_�C�A���O��\��������
# v 2.11 12/MAY/2009 �N���X�T�C�g�E�X�N���v�e�B���O�Ώ�

#-- �K�{�ݒ� ------------------------------------------------------------------

#���Ǘ��҂̃��[���A�h���X(���p�Ő�����)
$administrator = '���Ȃ��̂d���[���A�h���X';

#����ʂ́u�I���v�����N��(URL)
$bye = 'http://�z�[���y�[�W�Ȃǂ̂t�q�k/';

#���^�C�g���Ȃǂ̖`�����b�Z�[�W(HTML����)
$title = <<'EOF';
<h1>�����f����</h1>
EOF

# $.... = <<'EOF';
# ���̊ԂɋL�q���܂�.
# �����s�\.
# EOF

#���u���E�U�̃^�C�g���o�[�̖���(�P�s�̂�)
$title_bar = <<'EOF';
�����f����
EOF

#-- �C�Ӑݒ� ------------------------------------------------------------------

#����ʂ̐F��w�i�̐ݒ� (HTML����)
$body = '<body bgcolor=#FFFFFF text=#000000>';

#���o�[�̐F
$cellcolor = '#ffeedd';

#���z�X�g���̕\�� 1:���� 0:���Ȃ�
$view_host = 1;

#���^�O�̋���(�^�p�r���ŕύX���Ȃ�����) 1:����(����URL�����N����) 0:���Ȃ�
$allow_html = 0;

#���P��ʂɕ\������s��(�f�t�H���g�l)
$def = 20;

#�� �L�^���[�h�̃f�t�H���g�`�F�b�N�l 0:���s���� 1:�}�\���[�h 2:���s�L��
$chk = 2;

#�������ݒ�
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('��','��','��','��','��','��','�y');

#�����̃v���O�����̏ꏊ���t�q�k�Őݒ�(�ݒ肵�Ȃ���Ύ������o)
$reload = '';

#��$reload�Őݒ肵���ݒu�t�q�k�ȊO�̃t�H�[������̓��e���֎~���鏈�u ����:1 ���Ȃ�:0
$ref_axs = 0;

#�����{��R�[�h�ϊ����C�u����(�p�X�l) .. 2.0�ȏ�̃o�[�W�����̂���
require './jcode.pl';

#���f�[�^�f�B���N�g���̏ꏊ(�p�X�l)
$data_dir = './data/';

#���Ǘ��җp�p�X���[�h�t�@�C��(�p�X�l)
$pwd_file = './password.cgi';

#���R�����g������L�����Ǘ��҈ȊO���폜�ł��Ȃ��悤�� 1:���� 0:���Ȃ�
$delsave = 1;

#���R�����g���m�点�@�\�� 1:�g�� 0:�g��Ȃ�
#  (�g����ԂŃR�����g�@�\�𗘗p���Ă���L���ł����Ă��A���̐ݒ肪0�ɂȂ�΃��[�����܂���)
$resmail = 0;

#���R�����g���m�点�@�\���g���ꍇ�ɐݒ肷�� --------��

#��sendmail�̐ݒ�(�p�X�l)
$sendmail = '/usr/lib/sendmail';

#�����[���̑薼
$mail_subject = '�����f������̂��m�点';

#�����[���{���̖`���ɓ���镶��($mail_val = <<'EOF';��EOF�̊ԂɋL�q����)
$mail_val = <<'EOF';
�u�킽���̃z�[���y�[�W�v http://www.foo.bar/~user/ ��
�u�����f���v�ւ��z�����������B
EOF

#�����[���{���̏I���ɓ���镶��(�V�O�l�`��/����)
$mail_val2 = <<'EOF';
---------------------------------------------
MyHomePage http://www.foo.bar/ user@mail.host
EOF

#---------------------------------------------------��

#���R�����g�ɊK�w�ԍ��� 0:���Ȃ� 1:�t����
$attnum = 1;

#���c���[�\���p�r��
$keisen = '��';

#���ԍ����͂ފ���(��)
$kakko_l = '�y';

#���ԍ����͂ފ���(�E)
$kakko_r = '�z';

#���N���b�N�|�C���g��
$point = '��';

#���N���b�N�|�C���g��̐F
$pointc = '#ff3333';

#���ꗗ���̑薼����������(byte)
$subject_max_length = 100;

#-- �ߋ����O�ݒ� --------------------------------------------------------------

#���ߋ����O�@�\�� 1:�g�� 0:�g��Ȃ�
$log = 0;

#���ߋ����O�̏ꏊ(�p�X�l)�Ɩ���
%LOG = (
	'' , '',

);

#-- ���x�Ȑݒ� ----------------------------------------------------------------

#���菇
$prot = 'http';

#���N�b�L�[��F������͈�(�ʏ�͂��̂܂܂ł悢)
#  �ڂ������Ƃ� http://www.netscape.com/newsref/std/cookie_spec.html ��path�̍��ڂ�������������.
$path = '';

#------------------------------------------------------------------------------

if ($jcode'version < 2) { &error('���C�u�����ُ�','jcode.pl��2.0�ȍ~�̃o�[�W������ݒu���Ă�������.'); }
if ($reload ne '') { $SCRIPT_NAME = $reload; } # �v���O�������̎w��ݒ�
else { $SCRIPT_NAME = $ENV{'SCRIPT_NAME'}; } # �����ݒ�
if ($SCRIPT_NAME eq '') { &error("�ݒ�G���[",'(E1)'); } # $SCRIPT_NAME�̓N�b�L�[���ɂ��g��

$wcheck = 'wwwbbs.wck'; # �����e�A�����e�h�~�t�@�C����
$lockfile = 'wwwbbs.lock'; # ���b�N�t�@�C����
$date_now = sprintf("%04d/%01d/%01d(%s)%02d:%02d",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min); # �����\��

&decode_cookie($SCRIPT_NAME); # �N�b�L�[�擾
$cname = $SCRIPT_NAME . '2'; &decode_cookie($cname); # ���ǈʒu�擾
$cname = $SCRIPT_NAME . '3'; &decode_cookie($cname); # �ꗗ���擾

if ($COOKIE{'list'} > 0) { $def = $COOKIE{'list'}; } # �s���ݒ�
if ($COOKIE{'mode'} eq '') { $COOKIE{'mode'} = 't'; } # �ꗗ���[�h�ݒ�

$cmd = $ENV{'QUERY_STRING'}; # �N�G���[����
@pairs = split(/&/,$cmd);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	$value =~ s/&/&amp;/g;
	$value =~ s/"/&quot;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;

	$CMD{$name} = $value; # �N�G���[�f�[�^�̓R�}���h�p�A�z�z���
}

read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'}); # �W������

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($key,$val) = split(/=/,$pair);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	&jcode'h2z_sjis(*val); # ���p�J�i���S�p(SJIS)�ϊ�
	&jcode'convert(*val,'sjis'); # SJIS�ϊ�

	if ($key eq 'preview') { $preview = 1; } # �v���r���[�����̌��m

	$val =~ s/\t//g; # �^�u�R�[�h�𖳌���
	$val =~ s/\r\n/\n/g; # Win �� Unix
	$val =~ s/\r/\n/g; # Mac �� Unix

	unless ($key eq 'value') { # ���e���ȊO�̓^�O�𖳎�

		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
	}

	$in{$key} = $val;
}

if ($preview) { &prev; exit; } # �v���r���[������

if (!-e $pwd_file) { &error("�G���[","(E2)"); }
if ($in{'action'} eq 'setpwd') { &setpwd; }
if (-z $pwd_file || $CMD{'action'} eq 'resetpwd') { &setpwd_form; }

($admin) = &master_check; # �Ǘ��Ҍ����m�F(�Ǘ��p�X���[�h�Ȃ�$admin�l��1)

# �ߋ����O�I��
if (!$log) { $in{'log'} = $CMD{'log'} = ''; }
if ($CMD{'log'} ne '') { $in{'log'} = $CMD{'log'}; }
if ($in{'log'} ne '') {

	$data_dir = $in{'log'};
	if (!-d $data_dir) { &error("�ߋ����O��������܂���","(E18)"); }

	$LOG_NAME = $LOG{$data_dir};
	$CMD{'log'} = $in{'log'};
	$title_bar .= " - $LOG_NAME";
	$newms = '�ꗗ';
}
else { $newms = '�ŐV�̈ꗗ'; }

chdir($data_dir); # �f�B���N�g���ړ�

if (!$CMD{'log'}) { &lock; } # �t�@�C�����b�N

if ($CMD{'st'}) { $in{'start'} = $CMD{'st'} - 1; } # ���X�g�ʒu
if ($in{'action'} ne '') { $CMD{'action'} = $in{'action'}; } # �A�N�V�����l���R�}���h�ɂ��R�s�[
if ($CMD{'search'} ne '') { $in{'search'} = $CMD{'search'}; }
if ($CMD{'mode'} ne '') { $in{'mode'} = $CMD{'mode'}; }

if ($CMD{'t'}) { # �N���b�N�|�C���g����

	if ($in{'v'} =~ /\D/) { &error("�G���[","�����͔��p�����œ��͂��Ă�������."); }
	if (-e "$in{'v'}\.msg") { $CMD{'e'} = 'msg'; }
	elsif (-e "$in{'v'}\.res") { $CMD{'e'} = 'res'; }
	else { &error("File Not Found","$number�͍폜����Ă��܂�."); }

	$CMD{'lp'} = $CMD{'v'} = $in{'v'};
}
elsif ($CMD{'tw'} ne '') { $CMD{'t'} = $CMD{'tw'}; }

if ($CMD{'v'} =~ /(\d+)/ && $CMD{'e'} =~ /(msg|res)/) { &view($CMD{'v'},$CMD{'e'}); } # �L���\��
elsif ($CMD{'image'} eq 'new') { &image($CMD{'image'}); }
elsif ($CMD{'image'} eq 'copyright') { &image($CMD{'image'}); }
elsif ($CMD{'bye'} ne '') { &bye; }
elsif ($CMD{'mc'}) {

	# ���X�g���[�h�ύX
	$cook="uname\:$COOKIE{'uname'}\,email\:$COOKIE{'email'}\,pwd\:$COOKIE{'pwd'}\,mode\:$CMD{'mc'}";
	$cook =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URL�G���R�[�h
	$cook =~ tr/ /+/;
	print "Set-Cookie: $SCRIPT_NAME=$cook; path=$path; expires=$date_gmt\n";
	$COOKIE{'mode'} = $CMD{'mc'};
	&list;
}
else {
	if ($in{'start'} eq '') { $start = 0; } # ���X�g�J�n�ʒu
	else { $start = $in{'start'} + 1; }

	if ($CMD{'action'} eq 'post' && !$CMD{'log'}) { &post; } # ���e��ʂ�
	elsif ($in{'action'} eq 'write' && !$CMD{'log'}) { &write; } # �L�^������
	elsif ($in{'action'} eq 'remove' && !$CMD{'log'}) { # �폜������

		($result) = &remove;
		if (!$result) { $alldel = 1; }

		if ($in{'search'} ne '') { &search; }
		else { &list; }
	}
	elsif ($in{'search'} ne '') { &search; } # �������X�g
	else { &list; } # �ʏ탊�X�g
}

if (-e $lockfile) { unlink $lockfile; } # ���b�N����
exit;

sub getdir {

	local($type) = @_;

	$od_check = (eval { opendir(DIR,'.'); }, $@ eq "");
	if (!$od_check) {&error("�G���[","(E3)"); }

	@newls = ();
	@list = readdir(DIR); # �t�@�C�����̒��o

	foreach $file (@list) {

		next if -d $file;

		if ($type eq 'n') {

			# �ԍ����ꗗ
			if ($file =~ /(\d+)\.tre/) { next; }
			if ($file =~ /(\d+)\.(msg|res)/) { push(@newls,"$1\.$2"); }
		}
		else {
			# �c���[�ꗗ
			if ($file =~ /(\d+)\.tre/) { push(@newls,"$1\.tre"); }
		}
	}

	close(DIR);

	@newls = sort { $b <=> $a; } @newls;
	$all = @newls;
}

sub getlast {

	$od_check = (eval { opendir(DIR,'.'); }, $@ eq "");
	if (!$od_check) {&error("�G���[","(E3)"); }

	@newls2 = ();
	@list = readdir(DIR);

	foreach $file (@list) {

		next if -d $file;

		if ($file =~ /(\d+)\.tre/) { next; }
		if ($file =~ /(\d+)\.(msg|res)/) { push(@newls2,"$1\.$2"); }
	}

	close(DIR);

	@newls2 = sort { $b <=> $a; } @newls2;
	return($newls2[0]); # �ō��ԍ����o
}

sub list {

	if ($in{'search'} ne '') {

		if ($in{'search'} =~ /[&"<>]/) { &error("���͕�������","����������ɋL���̓��͂͂ł��܂���."); }

		$keys = $target = $in{'search'};
		$keys =~ s/�@/ /g;
		$target =~ s/�@/ /g;
		$target =~ s/(\W)/\\$1/g;
		@keys = split(/\\\s+/,$target);
	}

	&getdir($COOKIE{'mode'});

	if ($in{'cls'}) { # �s���ύX

		$def = $in{'ls'};
		print "Set-Cookie: $SCRIPT_NAME" . '3' . "=list:$def; path=$path; expires=$date_gmt\n";
	}

	# �ꗗ�s�̌���
	if ($all <= ($start + $def - 1)) { $end = $all - 1; }
	else { $end = $start + $def - 1; }

	if ($COOKIE{'mode'} eq 'n') { $mc = 't'; $mc2 = '�c���[�ꗗ'; }
	else { $mc = 'n'; $mc2 = '�ԍ����ꗗ'; }

	&html_head;

	print "$body\n";
	print "$title<p>\n";

	if ($all != 0) {

		print "<font size=-1>\n";
		if ($start != 0 || $cmd ne '' || $CMD{'log'}) { print "�k<a href=\"JavaScript:history.back()\">�O�̉��</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?action=post\">�V�����b��</a>�l"; }
		print "�k<a href=\"#search\" onClick=\"document.SearchForm.search.focus();\">����</a>�l";
		print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>�l";
		print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>�l";
		if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>�S�ēǂ񂾂��Ƃɂ���</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>�S�ēǂ񂾂��Ƃɂ��ďI��</a>�l"; }
		print "�k<a href=\"$bye\" target=_top>�I��</a>�l";
		print "</font><p>\n";

		if ($CMD{'log'}) { $COOKIE{'rp'} = ''; }
		elsif ($COOKIE{'rp'} ne '' && $start == 0) {

			($lastf) = &getlast;
			($lastnum,$ext) = split(/\./,$lastf,2);
			$rp2 = $COOKIE{'rp'} + 1;

			if ($COOKIE{'rp'} > $lastnum) { $COOKIE{'rp'} = $lastnum; }
			else {

				print "<font size=-1>�s ���Ȃ��̍ŏI�A�N�Z�X�� $COOKIE{'lastlogin'} ���ǔԍ� �`No.$COOKIE{'rp'} �t</font>\n";
				print "<ul>\n";
				if ($COOKIE{'rp'} < $lastnum) {

					if ($rp2 == $lastnum) { $msg = $rp2; } else { $msg = "$rp2�`$lastnum"; }
					print "<li>�O����A$msg��<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>�V�K���e����Ă��܂�.\n";
					if ($COOKIE{'mode'} ne 'n') { print "<li>�܂Ƃ߂Č���ɂ́k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>�l�ɂ���ƕ֗��ł�.\n"; }
				}
				print "</ul>\n";
			}
		}

		if ($alldel) { print "<a name=\"$number\"></a>\n"; }

		if ($LOG_NAME ne '') { print "<h3>$LOG_NAME</h3>\n"; }
		print "<DL>\n";
		if ($start != 0) { print "<DT><font size=-1>��</font></dt>\n"; }

		foreach $num ($start .. $end) {

			$k = ''; # �r���N���A

			if ($COOKIE{'mode'} eq 'n') {

				# ���n��`��
				($file,$ext) = split(/\./,$newls[$num],2); # �t�@�C�����Ɗg���q�ɕ�����
				if ($ext eq 'msg') { $cell = " bgcolor=$cellcolor"; } else { $cell = ''; }
				if ($CMD{'bk'} == $file || $res_bk == $file) { $file2 = "<blink><font color=$pointc class=\"blink\">$file</font></blink>"; } else { $file2 = $file; }

				if (-s $newls[$num] == 0) { next; }
				($result) = &gethead($newls[$num],0); # �L���w�b�_�̎擾(��Q������0�Ńw�b�_�̂݁A1��@VAL�ɓ��e�����擾)
				if (!$result) { print "<DT>$kakko_l$file$kakko_r" . "Read Error E10($newls[$num])</dt>\n"; next; }

				if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }

				if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }
				if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }
				$line = "<a name=\"$file\">$kakko_l$file2$kakko_r\</a>$new <a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&v=$file&e=$ext&lp=$file&st=$start\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'})</font>";

				$line = "<table cellpadding=0 cellspacing=1 border=0 width=100%><tr><td$cell>$line</td></tr></table>";
				print "<DT>$line</dt>\n";
			}
			else {
				# �X���b�h�`��
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
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?action=post\">�V�����b��</a>�l"; }
		print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>�l";
		if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
		print "�k<a href=\"$bye\" target=_top>�I��</a>�l";
		print "</font><p>\n";

		print "���b�Z�[�W�͂���܂���.<p>\n";
	}

	print "<hr size=1>\n";

	if ($all != 0) {

		print "<font size=-1>\n";
		if ($start != 0 || $cmd ne '' || $CMD{'log'}) { print "�k<a href=\"JavaScript:history.back()\">�O�̉��</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?action=post\">�V�����b��</a>�l"; }
		print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">$newms</a>�l";
		print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&mc=$mc\">$mc2</a>�l";
		if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>�S�ēǂ񂾂��Ƃɂ���</a>�l"; }
		if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>�S�ēǂ񂾂��Ƃɂ��ďI��</a>�l"; }
		print "�k<a href=\"$bye\" target=_top>�I��</a>�l";
		print "</font><p>\n";
	}

	print "<table border=0><tr>\n";

	$i = $all - 1;
	if ($end < $i) {

		print "<form method=post action=\"$SCRIPT_NAME\?log=$CMD{'log'}\">\n";
		print "<input type=hidden name=\"start\" value=\"$end\">\n";
		print "<td><input type=submit value=\"�����̃y�[�W\"></td></form>\n";
	}

	if ($all != 0) {

		print <<"EOF";
		</tr>
		<tr><td></td></tr>
		<tr>
		<form method=POST action="$SCRIPT_NAME\?log=$CMD{'log'}" name="SearchForm">
		<td colspan=2 bgcolor=$cellcolor>
		<a name="search"></a>
		���������� <input type=text name="search" value="$keys" size=15>
		<input type=submit value="����"><font size=-1>
		<input type=radio name="mode" value="and" checked>AND <input type=radio name="mode" value="or">OR<br>
		</font>
		<font size=-1>(�󔒂ŋ�؂��ĕ���������/�薼,���O,E���[���ɂ��)</font></td></form>
EOF
		if ($start == 0) { # �ŏ��̉�ʂ����\������

			print <<"EOF";
			<form method=POST action="$SCRIPT_NAME\?t=1">
			<input type=hidden name="log" value="$CMD{'log'}">
			<input type=hidden name="st" value="$start">
			<td bgcolor=$cellcolor align=right>
			�ԍ� <input type=text name="v" value="" size=5>
			<input type=submit value="�{��"></td>
			</tr></form>
EOF
		}
	}

	if ($start == 0 && $all != 0) {

		if ($COOKIE{'mode'} ne 'n') { $mes = '<font size=-1>���R�����g�L���̓J�E���g����܂���.</font>'; }

		print <<"EOF";
		<tr><td></td></tr>
		<form method=post action="$SCRIPT_NAME\?log=$CMD{'log'}">
		<input type=hidden name="cls" value="1">
		<tr><td bgcolor=$cellcolor align=center><input type=text name="ls" value="$def" size=5>�s<input type=submit value="�ݒ�"></td>
		</form>
EOF
		if ($COOKIE{'rp'} ne '' && !$CMD{'log'}) {

			print <<"EOF";
			<form method=post action="$SCRIPT_NAME\?bye=crd">
			<td bgcolor=$cellcolor align=center>���ǈʒu<input type=text name="rd" value="$COOKIE{'rp'}" size=5><input type=submit value="�ύX"></td>
			</form>
EOF
		}
	}

	if ($log && $start == 0) { # �ŏ��̉�ʂ����\������

		# �ߋ����O�ꗗ
		print "<form method=post action=\"$SCRIPT_NAME\">\n";
		print "<td bgcolor=$cellcolor align=center><select name=\"log\" size=1>\n";
		print "<option value=\"\">�ŐV�̃��O</option>\n";

		$selected_log{$CMD{'log'}} = "selected";

		foreach $key (sort keys(%LOG)) {

			print "<option value=\"$key\" $selected_log{$key}>$LOG{$key}</option>\n";
		}

		print "</select><input type=submit value=\"�{��\"></td></form>\n";
	}

	print "</tr></table> $mes<p>\n";

	# �K���\�����Ă���������
	print "<p align=right><a href=\"http://www.rescue.ne.jp/\" target=\"_top\"><img src=\"$SCRIPT_NAME\?image=copyright\" border=0 alt=\"Trees\"></a></p>\n";

	if (!$CMD{'log'}) { print "<font size=-1>"; }
	print "�k<a href=\"mailto:$administrator\">�Ǘ��҂ւ̖⍇��</a>�l\n"; # �Ǘ��Ɋւ��ē��T�C�g�ɖ⍇�������邱�Ƃ������
	print " ( )���͋L���T�C�Y</font><p></body></html>\n";
}

sub search {

	if ($in{'search'} =~ /[&"<>]/) { &error("���͕�������","�L���̓��͂͂ł��܂���."); }

	if ($in{'mode'} eq 'or') { $OR = 'checked'; $MODE = ' <sup>�܂���</sup> '; }
	elsif ($in{'mode'} eq 'and' || $in{'mode'} eq '') { $AND = 'checked'; $MODE = ' <sup>����</sup> '; }

	$keys = $target = $in{'search'}; # ����������
	$keys =~ s/�@/ /g;
	$target =~ s/�@/ /g;
	$target =~ s/(\W)/\\$1/g; # ���^����
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

		if ($in{'mode'} eq 'or') { # �_���a����

			$match = 1;
			foreach $term (@keys) { if ($string =~ /$term/i) { $match = 0; }}
		}
		else { # �_���ό���

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
	if (!@PICKUP) { $msg = "<blink>�O�̉��</blink>"; } else { $msg = "�O�̉��"; }
	print "�k<a href=\"JavaScript:history.back()\">$msg</a>�l";
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?action=post\">�V�����b��</a>�l"; }
	print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}\">�������[�h����</a>�l";
	if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>�S�ēǂ񂾂��Ƃɂ���</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>�S�ēǂ񂾂��Ƃɂ��ďI��</a>�l"; }
	print "�k<a href=\"$bye\" target=_top>�I��</a>�l";
	print "</font><p>\n";

	print <<"EOF";
	<h3>�s<blink>�������[�h</blink>�t$LOG_NAME</h3>
	�������� �� $keys2<p>
EOF
	if (@PICKUP) {

		if ($alldel) { print "<a name=\"$number\"></a>\n"; }
		if ($CMD{'log'}) { $COOKIE{'rp'} = ''; }

		print "<DL>\n";
		if ($start != 0) { print "<DT><font size=-1>��</font></dt>\n"; }

		foreach $filename (@PICKUP) {

			$k = '';

			# ���n��`���̂�
			($file,$ext) = split(/\./,$filename,2);
			if ($ext eq 'msg') { $cell = " bgcolor=$cellcolor"; } else { $cell = ''; }

			if (-s $filename == 0) { next; }
			($result) = &gethead($filename,0);
			if (!$result) { print "<DT>$kakko_l$file$kakko_r" . "Read Error E10($filename)</dt>\n"; next; }

			if ($HD{'email'} ne '') { $HD{'uname'} = "<a href=\"mailto:$HD{'email'}\">$HD{'uname'}</a>"; }

			if ($CMD{'bk'} == $file || $res_bk == $file) { $file2 = "<blink><font color=$pointc class=\"blink\">$file</font></blink>"; } else { $file2 = $file; }
			if ($file > $COOKIE{'rp'} && $COOKIE{'rp'} ne '') { $new = "<img src=\"$SCRIPT_NAME\?image=new\" border=0 alt=\"New!\" width=22 height=10>"; } else { $new = ''; }

			$ukeys = $keys;
			$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URL�G���R�[�h
    			$ukeys =~ tr/ /+/;

			if (length($HD{'subject'}) > $subject_max_length) { $HD{'subject'} = substr($HD{'subject'},0,$subject_max_length -1); $HD{'subject'} = $HD{'subject'} . '..'; }
			$line = "<a name=\"$file\">$kakko_l$file2$kakko_r\</a>$new <a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&v=$file&e=$ext&lp=$file&st=$start\">$HD{'subject'}</a> <font size=-1>$HD{'date'} $HD{'uname'} ($HD{'size'})</font>";

			$line = "<table cellpadding=0 cellspacing=1 border=0 width=100%><tr><td$cell>$line</td></tr></table>";
			print "<DT>$line</dt>\n";
		}
		print "</DL>\n";
	}
	else { print "���o����܂���ł���.<p>\n"; }

	print "<hr size=1><table border=0>\n";

	if ($next_num ne '') {

		$next_num--;
		print "<form method=post action=\"$SCRIPT_NAME\?log=$CMD{'log'}\">\n";
		print "<input type=hidden name=\"start\" value=\"$next_num\">\n";
		print "<input type=hidden name=\"mode\" value=\"$in{'mode'}\">\n";
		print "<input type=hidden name=\"search\" value=\"$in{'search'}\">\n";
		print "<tr><td><input type=submit value=\"�����̃y�[�W\"></td></tr></form>\n";
		print "<tr><td></td></tr>\n";
	}

	print <<"EOF";
	<tr>
	<form method=POST action="$SCRIPT_NAME\?log=$CMD{'log'}">
	<td  bgcolor=$cellcolor>
	���������� <input type=text name="search" value="$keys" size=15>
	<input type=submit value="����"><font size=-1>
	<input type=radio name="mode" value="and" $AND>AND <input type=radio name="mode" value="or" $OR>OR<br>
	</font></td></tr></table></form>
EOF
	# �K���\�����Ă���������
	print "<p align=right><a href=\"http://www.rescue.ne.jp/\" target=\"_top\"><img src=\"$SCRIPT_NAME\?image=copyright\" border=0 alt=\"Trees v1.01\"></a></p>\n";

	print "<font size=-1>\n";
	print "�k<a href=\"mailto:$administrator\">�Ǘ��҂ւ̖⍇��</a>�l\n"; # �Ǘ��Ɋւ��ē��T�C�g�ɖ⍇�������邱�Ƃ������
	print " ( )���͋L���T�C�Y</font><p></body></html>\n";
}

sub gethead {

	local($file,$vv) = @_;
	@VAL = (); # �{���N���A

	if (!open(HEAD,$file)) { return(0); }
	while (<HEAD>) {

		if (/^$/) { last; } # ��s�Ńw�b�_�I��

		($key,$value) = split(/\t/);
		$value =~ s/\n//g;
		$HD{$key} = $value;
	}
	if ($vv) { while (<HEAD>) { push(@VAL,$_); }} # �{��
	close(HEAD);

	return(1);
}

sub view {

	local($number,$ext) = @_;

	if (-s "$number\.$ext" == 0) { &error("File Not Found","$number�͍폜����Ă��܂�."); }
	($result) = &gethead("$number\.$ext",1);
	if (!$result) { &error("�G���[","Read Error E10($number\.$ext)"); }

	#�Q�Ɛ�����
	if ($CMD{'log'}) { $no_count = 1; }
	if (!$no_count) {

		$HD{'rc'}++;

		if (open(OUT,"> $number\.$ext")) {

			print OUT "pwd\t$HD{'pwd'}\n";
			print OUT "rc\t$HD{'rc'}\n"; # �J�E���g�����X�V
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
	$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URL�G���R�[�h
    	$ukeys =~ tr/ /+/;

	&html_head;

	print "$body\n";

	print <<"EOF";
	<font size=-1>
	�k<a href="JavaScript:history.back()">�O�̉��</a>�l
EOF
	if (!$CMD{'t'}) { print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$CMD{'lp'}\#$CMD{'lp'}\">�N���b�N�|�C���g</a>�l"; }

	print <<"EOF";
	�k<a href="$SCRIPT_NAME\?log=$CMD{'log'}">$newms</a>�l
EOF
	if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>�S�ēǂ񂾂��Ƃɂ���</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>�S�ēǂ񂾂��Ƃɂ��ďI��</a>�l"; }

	print <<"EOF";
	�k<a href="$bye" target=_top>�I��</a>�l
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
		print "<td><input type=submit value=\"   �ԐM   \"><font size=-1><input type=checkbox name=\"inyou\" value=\"1\">���p����</font></td></form>\n";

		if ($in{'search'} ne '') { $lp = $CMD{'lp'}; } else { $lp = $number; }

		print "<form method=post action=\"$SCRIPT_NAME\?search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$number\#$number\">\n";
		print "<input type=hidden name=\"action\" value=\"remove\">\n";
		print "<input type=hidden name=\"remove_number\" value=\"$number\.$ext\">\n";
		print "<td><font size=-1>���݂̃p�X���[�h</font><input type=password name=\"pwd\" value=\"$COOKIE{'pwd'}\" size=10>";
		print "<input type=submit value=\"�폜\"></td></form>\n";
		print "</tr></table></form>\n";
	}

	print "<p><hr size=1><p>\n";

	if ($HD{'how'} == 1) { print "<pre><tt>"; } # �}/�\���[�h

	@VAL2 = @VAL;
	foreach $value (@VAL2) {

		if (($HD{'link'} != 2 && $allow_html) || !$allow_html) { # �^�O�s���܂��̓^�O���g��Ȃ��ꍇ

			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
		}

		if ($allow_html) { # �^�O���̏ꍇ��target������ǉ�����

			$value =~ s/<a href=/<a target="_blank" href=/ig;
		}

		if ($HD{'link'} == 1 && !$allow_html) { # �^�O�s����URL�����N����ꍇ

			$value =~ s/&gt;/\t/g;
			$value =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig;
			$value =~ s/\t/&gt;/g;
		}

		if ($HD{'link'} == 2 && $allow_html) { print $value; } # HTML�L����
		elsif ($HD{'how'} == 1) { print $value; } # �}/�\���[�h
		elsif ($HD{'how'} == -1) { $value =~ s/\n/<br>\n/g; print $value; } # ���s�L��
		else { $value =~ s/\n//g; print $value; } # ���s����
	}

	if ($HD{'how'} == 1) { print "</tt></pre><p>\n"; } # �}/�\���[�h

	#�X���b�h
	print "<p><hr size=1><a name=\"tree\"></a><p>\n";
	print "�k�c���[�\\���l<p>\n";
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

				if ($ext eq 'res') { $k = $keisen; } # ���X�Ɍr��������
				if ($CMD{'lp'} == $num && !$CMD{'t'}) { $p = "<blink><font color=$pointc class=\"blink\">$point</font></blink>"; } else { $p = ""; } # �N���b�N�|�C���g��
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
	�k<a href="JavaScript:history.back()">�O�̉��</a>�l
EOF
	if (!$CMD{'t'}) { print "�k<a href=\"$SCRIPT_NAME\?log=$CMD{'log'}&search=$ukeys&mode=$in{'mode'}&st=$CMD{'st'}&bk=$CMD{'lp'}\#$CMD{'lp'}\">�N���b�N�|�C���g</a>�l"; }

	print <<"EOF";
	�k<a href="$SCRIPT_NAME\?log=$CMD{'log'}">$newms</a>�l
EOF
	if ($CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\" target=_top>�ŐV�̃��O</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=reset\" target=_top>�S�ēǂ񂾂��Ƃɂ���</a>�l"; }
	if (!$CMD{'log'}) { print "�k<a href=\"$SCRIPT_NAME\?bye=bye\" target=_top>�S�ēǂ񂾂��Ƃɂ��ďI��</a>�l"; }

	print <<"EOF";
	�k<a href="$bye" target=_top>�I��</a>�l
EOF
	if (!$CMD{'t'}) {

		print <<"EOF";
		<p>�� �w�N���b�N�|�C���g<blink><font color=$pointc class=\"blink\">$point</font></blink>�x�Ƃ͈ꗗ�ォ��ǂݎn�߂��n�_���w���A�c���[��̋L�������񂵂Ă��A���̈ʒu�ɖ߂邱�Ƃ��ł��܂�.
EOF
	}
	print "<p></body></html>\n";
}

sub prev { # �v���r���[����

	&html_head;
	&gethost;

	print "$body\n";

	print <<"EOF";
	<table cellpadding=3 cellspacing=0 border=0 width=100%><tr>
	<td bgcolor=$cellcolor><font size=+1>�s�\\���m�F�t <strong>$in{'subject'}</strong></font></td>
	</tr></table>
EOF

	if ($in{'email'} ne '') { print "by <a href=\"mailto:$in{'email'}\">$in{'uname'}</a> "; }
	else { print "by $in{'uname'} "; }

	if ($view_host) { print "- <font size=-1>$host</font>"; }

	if ($in{'psemail'}) { print " - <font size=-1>ResMail</font>"; }

	print "<hr size=1><p>\n";

	if ($in{'how'} == 1) { print "<pre><tt>"; } # �}/�\���[�h

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

	if ($in{'link'} == 2 && $allow_html) { print $value; } # HTML�L����
	elsif ($in{'how'} == 1) { print $value; } # �}/�\���[�h
	elsif ($in{'how'} == -1) { $value =~ s/\n/<br>\n/g; print $value; } # ���s�L��
	else { $value =~ s/\n//g; print $value; } # ���s����
	if ($in{'how'} == 1) { print "</tt></pre><p>\n"; } # �}/�\���[�h

	print <<"EOF";
	<p>
	<hr size=1>
	<h3>
	�k<a href="JavaScript:history.back()">���e��ʂɖ߂�</a>�l
	</h3></body></html>
EOF

}

sub bye {

	($lastf) = &getlast;
	($lastnum,$ext) = split(/\./,$lastf,2);

	if ($in{'rd'} ne '') { # �C�ӂ̊��ǈʒu�ݒ�

		if ($in{'rd'} > $lastnum) { $in{'rd'} = $lastnum; }
		print "Set-Cookie: $SCRIPT_NAME" . '2' . "=rp:$in{'rd'}\,lastlogin:$COOKIE{'lastlogin'}; path=$path; expires=$date_gmt\n";
	}
	else {
		# �S�ēǂ񂾂��Ƃɂ���(�ŏI�ԍ������ǈʒu�Ƃ��Đݒ�)
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
		$ukeys =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URL�G���R�[�h
    		$ukeys =~ tr/ /+/;
	}

	if ($chk < 0 || $chk > 2) { $chk = 0; }
	$howc[$chk] = "checked";

	if ($in{'resp_number'} ne '') {

		($respnum,$ext) = split(/\./,$in{'resp_number'},2);
		if (-s "$respnum\.$ext" == 0) { &error("File Not Found","$respnum�͍폜����Ă��܂��̂ŁA�R�����g�ł��܂���."); }

		if ($in{'inyou'}) { $get_val = 1; } else { $get_val = 0; }
		($result) = &gethead("$respnum\.$ext",$get_val);
		if (!$result) {	@VAL = (); }

		if ($HD{'how'} == 1 && $in{'inyou'}) {

			$howc[$chk] = "";
			$howc[1] = "checked";
			$com = '(���I���p���͐}/�\���[�h�ŋL�^����Ă��܂�)';
		}
		if ($in{'inyou'}) { $caution = "�� ���p�����͕K�v�Œ���ɂ��܂��傤. �T�[�o�����̐ߖ�ɂ����͂�������.<p>\n"; }

		$write_title = "$respnum�ւ̃R�����g";
		$ichi = "#tree";
	}
	else { $write_title = "�V�����b��"; $ichi = ""; }

	#�薼����
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

	# �J�[�\���t�H�[�J�X�ʒu
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
	<tr><th align=right>���e��</th>
	<td><input type=text name="uname" size=20 value="$COOKIE{'uname'}"></td></tr>
	<tr><th align=right>�d���[��</th>
	<td><input type=text name="email" size=40 value="$COOKIE{'email'}"></td></tr>
	<tr><th align=right>�p�X���[�h</th>
	<td><input type=password name="pwd" size=10 value="$COOKIE{'pwd'}"> <font size=-1>�����̋L�����폜���邽�߂̃p�X���[�h�ł�.</font></td></tr>
	<tr><th align=right>�薼</th>
	<td><input type=text name="subject" value="$subject" size=60></td></tr>
	<tr><th align=right>���e</th>
	<td><font size=-1>
	<input type=radio name="how" value="0" $howc[0]>���s����
	<input type=radio name="how" value="-1" $howc[2]>���s�L��
	<input type=radio name="how" value="1" $howc[1]>�}/�\\���[�h $com</font><br>
EOF
	print "<textarea name=\"value\" rows=15 cols=80 wrap=off>";

	if ($in{'inyou'}) {

		foreach $value (@VAL) {	print "$HD{'uname'}&gt; $value"; }
		print "\n</textarea>";
	}
	else { print "</textarea>"; }

	if (!$allow_html) { print "<br>\n<font size=-1><input type=checkbox name=\"link\" value=\"1\" checked>���e��URL������΃����N������</font></td>"; }
	else { print "<br>\n<font size=-1><input type=checkbox name=\"link\" value=\"2\">�g�s�l�k��L���ɂ���</font></td>"; }

	print <<"EOF";
	</tr>
	<tr><td></td>
	<td align=center><input type=checkbox name="cookie" value="1" checked><font size=-1>���e�҂ƃ��[���ƃp�X���[�h��ۑ�</font>
EOF
	if ($resmail) { print "<input type=checkbox name=\"psemail\" value=\"1\"> <font size=-1>�R�����g�������烁�[���A�����~����</font></td></tr>\n"; }

	print <<"EOF";
	<tr><td></td>
	<td align=center><input type=submit name="preview" value="�H�v���r���[">�@�@<input type=submit value="  �� ���e  " onClick="f=confirm('���e���܂����H');return f"> <input type=reset value="�~ ���Z�b�g"></td></tr>
	</table></form>
	<p>
	�k<a href="JavaScript:history.back()">�O�̉��</a>�l<p>
	<font size=-1>
	<ul>
	<li>���p���͍Œ���ɂ��܂��傤.
EOF
	if ($resmail) { print "<li>�R�����g�������烁�[���A������@�\\�́A���ȃ��X�ɂ͓K�p����܂���.<p>\n"; }

	print <<"EOF";
	<li>[���s����] ���s�ƘA���������p�󔒂���������܂�.
	<li>[���s�L��] ���s����ꂽ�ʒu�Ő܂�Ԃ���܂����A�A���������p�󔒂���������܂�.
	<li>[�}/�\\���[�h] �L�����ꂽ�ʂ�ɋL�^���܂�.
EOF
	if ($allow_html) { print "<li>�g�s�l�k��L���ɂ���ꍇ�́A�}/�\\���[�h�ȊO�͖����ɂȂ�܂�.\n"; }

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

	if ($ENV{'REQUEST_METHOD'} ne "POST") { &error('�G���[','(E4)'); }

	if ($ref_axs) {

		$ref = $ENV{'HTTP_REFERER'};
		if (!($ref =~ /$SCRIPT_NAME/i)) { &error('���e�s��',"�u$SCRIPT_NAME�v�ȊO����̓��e�����m���܂���. (E5)<br>$ref<br>$SCRIPT_NAME"); }
	}

	($lastf) = &getlast;
	($num,$ext) = split(/\./,$lastf,2);
	$basenum = $num + 1;

	($respnum,$ext) = split(/\./,$in{'resp_number'},2);
	if ($in{'resp_number'} ne '' && !-e "$respnum\.$ext") { &error('�ԐM�G���[',"�ԐM���ƂȂ�$respnum�Ԃ̋L���͍폜����Ă��܂��̂ŁA�R�����g�ł��܂���."); }

	if ($in{'resp_base'} eq '') { $in{'resp_base'} = $basenum; }

	if ($in{'uname'} eq '') { &error('���͕s��','���O��������Ă��܂���.'); }
	if ($in{'email'} eq '' && $in{'psemail'}) { &error('���͕s��','�R�����g���������ɘA�����~�����ꍇ�͂d���[������͂��Ă�������.','�Ȃ��A���[�����͂��Ȃ���ȗ��R�͋L���~�X�ł��̂ŁA�����ӂ�������.'); }

	if (length($in{'uname'}) > 20) { &error('���͕s��','���O��20�o�C�g�ȓ��ł��L����������.'); }
	if ($in{'subject'} eq '') { &error('���͕s��','�薼��������Ă��܂���.'); }
	if ($in{'pwd'} =~ /\W/ || $in{'pwd'} eq '') { &error('���͕s��','�p�X���[�h�𔼊p�p�����œ��͂��Ă�������.'); }
	if ($in{'value'} eq '') { &error('���͕s��','���e��������Ă��܂���.'); }

	$host = &gethost;

	($crypt_password) = &MakeCrypt($in{'pwd'});

	$MSGc = "$in{'uname'}\t$in{'email'}\t$in{'subject'}\t$in{'value'}";
	$MSGc =~ s/\n//g;

	# �����e�A�����e�h�~
	if (!-e $wcheck) {

		if (!open(CHECK,"> $wcheck")) { &error("�G���[","(E6)"); }
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

	if ($in{'resp_number'} ne '' && -s $in{'resp_number'} == 0) { &error("File Not Found","$in{'resp_number'}�͍폜����Ă��܂��̂ŁA�R�����g�̓��e�͂ł��܂���."); }

	# �g���q�̌���(�V�K�L����.mes �R�����g��.res ���Ȃ݂Ƀc���[�t�@�C����.tre)
	if ($basenum eq $in{'resp_base'}) { $ext = 'msg'; } else { $ext = 'res'; }

	if (!open(OUT,"> $basenum\.$ext")) { &error('�L�^�G���[',"�L���̋L�^���ł��܂���.(E7)"); }

	print OUT "pwd\t$crypt_password\n"; # �L���p�X���[�h
	print OUT "rc\t0\n"; # ���[�h�J�E���g
	print OUT "date\t$date_now\n"; # ����
	print OUT "uname\t$in{'uname'}\n"; # ���e��
	print OUT "email\t$in{'email'}\n"; # �d���[��
	print OUT "host\t$host\n"; # �z�X�g��
	print OUT "subject\t$in{'subject'}\n"; # �L���̃^�C�g��
	$size = length($in{'value'});
	print OUT "size\t$size\n"; # �L���̃T�C�Y
	print OUT "how\t$in{'how'}\n"; # �L�^���[�h(���s����:0 �L��:-1 �}�\:1)
	print OUT "link\t$in{'link'}\n"; # URL���������N�̗L��(����:1)
	print OUT "resp\t$in{'resp_number'}\n"; # ���ڂ̃R�����g���ƂȂ�L���ԍ�
	print OUT "tree\t$in{'resp_base'}\n"; # ���̋L����������c���[�t�@�C���̔ԍ�
	print OUT "psemail\t$in{'psemail'}\n"; # �R�������m�点���[�������邩�ǂ���(����:1)
	print OUT "res\t\n"; # ���̋L���ɃR�����g�����݂��邩�ǂ���(����:1)
	print OUT "\n"; # �w�b�_�Ɩ{���𕪂�����s
	print OUT $in{'value'}; # �{��
	close(OUT);
	chmod(0666,"$basenum\.$ext");

	&tree; # �c���[����

	# �R�����g���m�点���[������
	if ($in{'resp_number'} ne '.') { ($result) = &gethead($in{'resp_number'},0); }
	if ($resmail && $HD{'psemail'} && $in{'email'} ne $HD{'email'}) {

		$HD{'email'} =~ s/\n//g;
		$mail_subject =~ s/\n//g;

		if (!open(OUT,"| $sendmail -t")) { &error('�V�X�e���G���[','�V�X�e�������܂ł��҂���������.'); }
		print OUT "To: $HD{'email'}\n";
		print OUT "From: $administrator\n";
		print OUT "Errors-To: $administrator\n";
		print OUT &jis("Subject: $mail_subject\n"); # �S�p���܂ނ��̂�JIS�ϊ�
		print OUT "Content-Transfer-Encoding: 7bit\n";
		print OUT 'Content-Type: text/plain; charset=iso-2022-jp' . "\n\n";

		print OUT &jis("$mail_val\n");
		($num,$ext) = split(/\./,$in{'resp_number'},2);
		print OUT &jis("  (No.$num)$HD{'subject'} �ɁA\n");
		print OUT &jis("  �R�����g(No.$basenum)������܂���.\n");
		print OUT &jis("\n$mail_val2\n");

		close(OUT);
	}

	# �R�����g�̏ꍇ�͐e�L���ɃR�����g���t�������Ƃ��L�^����
	if ($in{'resp_number'} ne '') {

		($result) = &gethead($in{'resp_number'},1);
		if (!$result) { &error("�G���[","Read Error E10($in{'resp_number'})"); }

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
			print OUT "res\t1\n"; # ���̋L���ɃR�����g�����݂��邩�ǂ���(����:1)
			print OUT "\n";
			print OUT @VAL;
			close(OUT);
		}
	}

	if ($in{'cookie'}) { $cook="uname\:$in{'uname'}\,email\:$in{'email'}\,pwd\:$in{'pwd'}\,mode\:$COOKIE{'mode'}"; }
	else { $cook=""; $date_gmt = ""; }

	$cook =~ s/([^0-9A-Za-z_])/"%" . unpack("H2",$1)/ge; # URL�G���R�[�h
	$cook =~ tr/ /+/;

	print "Set-Cookie: $SCRIPT_NAME=$cook; path=$path; expires=$date_gmt\n";

	if ($COOKIE{'mode'} ne 't' && $ext ne 'msg') { $CMD{'st'}++; $start++; } # �߂�ʒu����
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

		if (!open(OUT,"> $basenum\.tre")) { &error('�L�^�G���[','�X���b�h�t�@�C���ɋL�^�ł��܂���.(E7)'); }
		print OUT "<DT>$basenum\.$ext\n";
		print OUT "<DD><!--$basenum-->\n"; # �R�����g�}���ʒu
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

	if (!-e "$number\.$ext") { return(0); } # ���ɕ����폜����Ă���
	if (-s "$number\.$ext" == 0) { return(0); } # ���ɘ_���폜����Ă���

	($result) = &gethead("$number\.$ext",1);
	if (!$result) { return(0); } # �t�@�C���ُ�

	if ($HD{'pwd'} eq '') { &error("�G���[","Read Error E10($number\.$ext)"); }
	if ($HD{'pwd'} =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }

	if (!$admin) {

		if (crypt($in{'pwd'},substr($HD{'pwd'},$salt,2)) ne $HD{'pwd'} && !$admin) { &error('�F�؃G���[',"�p�X���[�h�������܂���̂ō폜�ł��܂���.(E8)"); }
		if ($HD{'res'} && $delsave) { &error('�폜�s��',"���̋L���ɂ̓R�����g������̂ŁA�Ǘ��҈ȊO�͍폜�ł��܂���.","�����̓s����A�R�����g���폜����Ă����Ƃ��Ă����l�ł�."); }
	}

	if (open(DEL,"> $number\.$ext")) { print DEL ''; close(DEL); } # �_���폜
	else { push(@NOT_REMOVE,"$number\.$ext"); }

	#�c���[�t�@�C���̍X�V
	if (!open(IN,"$HD{'tree'}\.tre")) { return(0); }
	@tr_file = <IN>;
	close(IN);

	foreach $line (@tr_file) {

		# �_���폜
		$line =~ s/<DT>$number\.$ext/<DT>!$number\.$ext/;
		if ($line =~ /<DD><!--$number-->/) { next; }
		push(@new,$line);
	}

	# �c���[�X�V
	if (!open(OUT,"> $HD{'tree'}\.tre")) { return; }
	print OUT @new;
	close(OUT);

	if (@NOT_REMOVE) { &error('���s����',"���̃t�@�C���̍폜�Ɏ��s���܂���. �Ǘ��҂ɍ폜�˗����Ă�������.(E9) &gt; @NOT_REMOVE"); }

	if (open(CHECK,"> $wcheck")) {

		print CHECK '';
		close(CHECK);
	}

	return(1);
}

sub gethost {

	#�z�X�g���̎擾(�����l�b�g�Ȃ玟�̂S�s���w��̃v���O�����Ɠ���ւ���)

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

	if ($CMD{'log'}) { &error(); } # �ߋ����O���[�h���̓G���[
	if (-e $lockfile) { unlink $lockfile; }

	&html_head;

	print <<"EOF";
	$body
	<h1>�Ǘ��҃p�X���[�h�̐ݒ�/�ύX<hr size=1></h1>
	<form action=$SCRIPT_NAME method=POST>
	<input type=hidden name="action" value="setpwd">
EOF
	if (!-z $pwd_file) { print "���p�X���[�h <input type=password name=\"old_password\" size=10><br>\n"; }

	print <<"EOF";
	�V�p�X���[�h <input type=password name="new_password" size=10><br>
	�V�p�X���[�h <input type=password name="retype_password" size=10> (������x)<p>
	<input type=submit value="���s">
	</form><p><hr size=1>
EOF
	if (!-z $pwd_file) { print "[<A HREF=\"JavaScript:history.back()\">�߂�</A>]<p>\n"; }
	print "</body></html>\n";
	exit;
}

sub setpwd {

	if ($CMD{'log'}) { &error(); }

	if (!-z $pwd_file) {

		if (!open(READ,$pwd_file)) { &error('�G���[','�Ǘ��җp�p�X���[�h�t�@�C�����ǂݏo���܂���.(E12)'); }
		$master = <READ>;
		close(READ);

		chop($master) if $master =~ /\n/;
		if ($master =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
		if (crypt($in{'old_password'},substr($master,$salt,2)) ne $master) { &error("Authorization Required",'���p�X���[�h���F�؂���܂���ł���.(E13)'); }
	}

	if (length($in{'new_password'}) < 6 || $in{'new_password'} eq '') { &error('���̓~�X','6�����ȏ�̃p�X���[�h���w�肵�Ă�������.(E14)'); }
	if ($in{'new_password'} ne $in{'retype_password'}) { &error('���̓~�X','�Q����͂����p�X���[�h�������܂���.'); }

	($pwd) = &MakeCrypt($in{'new_password'});

	if (!open(WRITE,"> $pwd_file")) { &error('�G���[','�Ǘ��җp�p�X���[�h�t�@�C���ɋL�^�ł��܂���.(E15)'); }
	print WRITE $pwd;
	close(WRITE);
}

sub master_check {

	local($admin);
	$admin = 0;

	if (!open(READ,$pwd_file)) { &error('�G���[','�Ǘ��җp�p�X���[�h�t�@�C�����ǂݏo���܂���.(E12)'); }
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

	# ������30����ɐݒ�(GMT)
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

	# ���b�N�����̎������� symlink()�D��
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file��

			$c++;
			if ($c >= 3) { &error('���g���C�G���[','�������܍��G���Ă���܂�.<br>�߂��Ă�����x���s���Ă݂Ă�������.(E17)'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink��

			if (--$retry <= 0) { &error('���g���C�G���[','�������܍��G���Ă���܂�.<br>�߂��Ă�����x���s���Ă�������.(E17)'); }
			sleep(2);
		}
	}
}

sub image {

	local($image) = @_;

	if (-e $lockfile) { unlink $lockfile; }

	if ($image eq 'new') { # New!�摜�f�[�^

		@array = (
		"47","49","46","38","39","61","16","00","0a","00","b3","02","00","00","00","00","ff","d6","00","ff",
		"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff","ff",
		"ff","21","f9","04","01","00","00","02","00","2c","00","00","00","00","16","00","0a","00","40","04",
		"37","50","c8","29","02","ad","77","06","60","2b","0f","60","b8","71","00","e7","99","db","88","7e",
		"21","ab","81","65","1c","be","70","4d","8a","69","6e","66","38","98","49","29","e0","4d","b4","f3",
		"d8","8e","3e","c1","67","59","3b","a9","4a","47","54","12","c3","eb","09","22","00","3b");
	}
	elsif ($image eq 'copyright') { # ���S�摜�f�[�^

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
	<h3>[<A HREF="JavaScript:history.back()">�߂�</A>]</h3>
	</body></html>
EOF
	exit;
}
