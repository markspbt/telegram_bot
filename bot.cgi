#!/opt/local/bin/perl
# 	This software is free under AL/GPL, copyright (c) 2021 CodeMacs.com
# 	You can redistribute it and/or modify it under the same terms as the Perl 5 programming language system itself.
# 	Use it at your own risk!
# Prerequisites: curl
# Refer to Telegram website for bot creation steps:
# https://core.telegram.org/bots
# This bot settings:
# 	Privacy: disabled
# 	Administrative privileges: administrator
# 	Bot mode: webhook
# More info:
# https://www.codemacs.com/coding/perl/simple-telegram-chat-bot.5291981.htm

use strict;
use warnings;
# If needed set/update proper program environment and variables
#$ENV{'PATH'} = '/bin:/sbin:/usr/bin:/usr/sbin:/opt/local/bin';
	my $domain_root = '/path_to_data/folder';	# Folder where chat data stored
	my $temp_dir = '/path_to_temp_folder';		# Temporary folder
	my $your_userid_for_testing='1234567890';	# Telegram User ID for testing this bot
	my $growl_ip = '192.168.1.99';			# LAN IP to send Growl message. Empty IP - No Growl message.
## Get Telegram Token from remote machine using passwordless access - secure
#  as long as passwordless access granted to a special user and token file
#  has limiting access mode set to the user read only
#my $tagis = `ssh user@server_IP '/bin/cat /path_to_file/token.cgi'`;
## Get Telegram Token from local file - not very secure
#my $tagis = `/bin/cat /path_to_file/token.cgi`;
## Embed Telegram Token into the program - unsecure
my $tagis='1234567890:CGF90DaKIud4lk1eOElEchi3TEBppCDddrb';
	print "Content-type: text/txt\n\n";	# Throw the text MIME
	my($datacr,$origstr,$buffer,$tdata);
	my $write=time;

# Get JSON data and convert it to hash
if($ENV{'CONTENT_LENGTH'}) {read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
$datacr=$buffer;		$buffer =~ s/\'/\\\'/g;
$datacr =~ s/^\{+//;		$datacr =~ s/^(\n+|\r+)//;		$datacr =~ s/^\s+//;			$datacr =~ s/\s+$//;
$datacr =~ s/\}$//;		$datacr =~ s/\012/\n/g;			$datacr =~ s/\015/\n/g;			$datacr =~ s/\000/\n/g;
$datacr =~ tr/\n\n//s;		$datacr =~ s/\: /\:/g;			$datacr =~ s/(\n)(\s{2})/\n/g;		$datacr =~ s/(\n)(  )/$1\t/g;
$datacr =~ s/ /SP/g;		$datacr =~ s/(SPSP)/\t/g;		$datacr =~ s/(\:)(\{)/ \=\> $2/g;	$datacr =~ s/\:/\,/g;
$datacr =~ s/\s+$//;		$datacr =~ s/SP/ /g;			$datacr =~ s#(http|https)(\,)#$1\:#gi;
$datacr =~ s/\@/\\\@/g;		$datacr =~ s/\$/\\\$/g;			$datacr =~ s/\'/\\\'/g;			$datacr =~ s/\"/\'/g;
	if($datacr =~ m/\\u\w{4}/) { # Make foreign languages readable
	$origstr=$datacr;	$origstr =~ s#\\u(\w{4})#chr(hex $1)#eg;	$origstr =~ s/\'/\\\'/g;
	$origstr = "\n\n\$origstr='$origstr';";}
} ## END DATA PRESENT
else {print "Thank you!\n";	exit(0);} ## If no data - exit

our @initqu=();	our %subquestion = ();
gethashes();
	# Create buttons ######### >>
	my @resqu=@initqu;	my $questions='';	my $comma='';
	foreach my $q (@initqu) {$questions.= "$comma\[\"$q\"\]";	$comma=',';}
my $utime=time;			my $readtime = localtime($utime);	$readtime =~ tr/  //s;
#unless(-d "$domain_root/data") {`mkdir -p $domain_root/data`;	`chmod 777 $domain_root/data`;}
#unless(-d "$domain_root/chats") {`mkdir -p $domain_root/chats`;	`chmod 777 $domain_root/chats`;}
unless($datacr) {print "Thank you!\n";	exit(0);}
print "received\n";
# Write data to a file
open(MESS,">$domain_root/data/$utime.txt");	print MESS "\%messdata=($datacr);$origstr";	close(MESS);
	our %messdata=();
eval {require "$domain_root/data/$utime.txt"};		# Get data from newly created hash file
if($messdata{message}{from}{is_bot} eq 'false') {	# Read only user's data
	my $chatid = $messdata{message}{chat}{id};	# Chat ID
	my $messageid = $messdata{message}{message_id};	# Message ID
	my $nameid = $messdata{message}{from}{id};	# Name ID
	my $name = "$messdata{message}{from}{first_name} $messdata{message}{from}{last_name}";
	my $posted = $messdata{message}{date};
	my $message = $messdata{message}{text};		# Actual Message
	$messdata{message}{text} =~ s/\W//g;
	$messdata{message}{text} =~ tr/A-Z/a-z/;
	if($origstr && $message =~ m/\\u\w{4}/) {$message =~ s#\\u(\w{4})#chr(hex $1)#eg;}
		if($origstr && $messdata{message}{from}{first_name} =~ m/\\u\w{4}/) {
		$messdata{message}{from}{first_name} =~ s#\\u(\w{4})#chr(hex $1)#eg;
		$messdata{message}{from}{last_name} =~ s#\\u(\w{4})#chr(hex $1)#eg;
		$name =~ s#\\u(\w{4})#chr(hex $1)#eg;
		}
	if($messdata{message}{new_chat_participant}) { ## NEW USER JOINED THE CHAT #########################
	my $trepl = "$messdata{message}{from}{first_name}, Welcome to $messdata{message}{chat}{title}!\n";
	my $chatid = $messdata{message}{chat}{id};
	$trepl = "Type the word \"Help\" and send it at any point to get a quick answer.";
	$trepl =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
	`curl 'https://api.telegram.org/bot$tagis/sendMessage?chat_id=$chatid\&text=$trepl'`;
	sleep(2);
$tdata='{"text":"Please feel free to ask any questions or click on a button below.","chat_id":'.$chatid.',"reply_markup":{"keyboard":['.$questions.'],"one_time_keyboard":true,"resize_keyboard":true}}';
`curl -H 'content-type: application/json' -d '$tdata' 'https://api.telegram.org/bot$tagis/sendMessage'`;
# Send Growl message to a local workstation (optional)
sendgrowl($name,$messdata{message}{chat}{title},$posted,'joined');	exit(0);
	} ## END NEW USER JOINED THE CHAT ##################################################################
	elsif($messdata{message}{left_chat_member}) { ## USER LEFT CHAT #################################
# Nothing to do here except sending a Growl message (optional)
sendgrowl($name,$messdata{message}{chat}{title},$posted,'left');	exit(0);
	} ## END USER LEFT CHAT #########################################################################
	elsif($messdata{message}{reply_to_message}) { ## CLICK ON A BUTTON ####
		if($subquestion{$message}{1}) {
			doreplyqu($messdata{message}{from}{first_name},$messdata{message}{from}{last_name},$chatid,$message);
		} ## END PROPER QUESTION
		else { ## BAD QUESTION
unless(-f "$temp_dir/init.chat.answer.done.$nameid") { ##### Limit
`touch $temp_dir/init.chat.answer.done.$nameid`;
	my $trepl = "Unfortunately I don't have an answer to your question\n\"$message\"";
	$trepl =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
	`curl 'https://api.telegram.org/bot$tagis/sendMessage?chat_id=$chatid\&text=$trepl'`;
	exit(0);
} ## END UNLESS ALREADY ANSWERED ########################### Limit
		} ## END BAD QUESTION
	} ## END CLICK ON A BUTTON ############################################
	elsif($messdata{message}{text} eq 'help') {
# If "Help" requested - print quick keyboard buttons
my $tdatahlp='{"text":"Please click appropriate button below","chat_id":'.$chatid.',"reply_markup":{"keyboard":['.$questions.'],"one_time_keyboard":true,"resize_keyboard":true}}';
`curl -H 'content-type: application/json' -d '$tdatahlp' 'https://api.telegram.org/bot$tagis/sendMessage'`;
exit(0);
	} ## END HELP REQUESTED
		# If actual message sent by the user - send a reply
		if($messdata{message}{text}) {
		sendreply($chatid,$messageid,$nameid,$name,$posted,$message);
		} ## END IF MESSAGE PRESENT
} ## END NOT BOOT

exit(0);

sub sendreply {
my($chatid,$messageid,$nameid,$name,$posted,$message)=@_;	our %origchat=();	my $reply='';
if(-f "$domain_root/chats/$nameid.txt") {eval {require "$domain_root/chats/$nameid.txt"};} ## END CHAT WITH PERSON PRESENT
if($nameid eq $your_userid_for_testing) {## Comment this "if" before deploing, uncomment for testing
#	my $tekst = "\"$message\"\nReply";
#	$tekst =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
#	`curl 'https://api.telegram.org/bot$tagis/sendMessage?chat_id=$chatid\&text=$tekst'`;
#	exit(0);
} ## END END SENT FROM US
else {
## Throw immediate answer to the first message from the new user
unless(-f "$temp_dir/init.chat.done.$nameid") {`touch $temp_dir/init.chat.done.$nameid`;
my @initrpl = ('Just a moment..','One minute please','One moment','Be right back','Hold on please');
randomarrs ( \@initrpl );	$reply = shift(@initrpl);
$reply .= "\nWe will try to answer your question personally ASAP";
} ## END UNLESS ALREADY REPLIED
} ## END SENT FROM OTHER PERSON

if($reply) {
$origchat{$posted}{reply}=$reply;	$origchat{$posted}{reply} =~ s/\n/ /g;
$reply =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
`curl 'https://api.telegram.org/bot$tagis/sendMessage?chat_id=$chatid\&text=$reply'`;
}

# Write a chat log if needed
my $ptstime=localtime($posted);		$ptstime =~ tr/  //s;
$origchat{$posted}{postime}=$ptstime;
$origchat{$posted}{chatid}=$chatid;
$origchat{$posted}{messageid}=$messageid;
$origchat{$posted}{name}=$name;
$origchat{$posted}{posted}=$posted;
$origchat{$posted}{message}=$message;
open(TXS,">$domain_root/chats/$nameid.txt");	print TXS "\%origchat = (\n";	my $cma='';
foreach my $ut (sort numbr keys (%origchat)) {
print TXS "$cma'$ut'=>{\n";	$cma=",\n";	my $cma1="\t";
	foreach my $k (sort keys %{$origchat{$ut}}) {$origchat{$ut}{$k} =~ s/\'/\\\'/g;
	unless($origchat{$ut}{$k}) {next;}
	print TXS "$cma1'$k','$origchat{$ut}{$k}'";	$cma1=",\n\t";
	} ## FOREACH KEY END
print TXS "\n}";	
} ## FOREACH UNIX TIME END
print TXS "\n);\n";	close(TXS);
} ## END SEND REPLY SUB

sub numbr {$a <=> $b;}

sub randomarrs {
    my $array = shift;
    my $i;
    for ($i = @$array; --$i; ) {
        my $j = int rand ($i+1);
        next if $i == $j;
        @$array[$i,$j] = @$array[$j,$i];
    }
} ## RANDOMIZE ARRAYS END

sub sendgrowl {
unless($growl_ip) {return;}
my($name,$chatname,$posted,$did) = @_;	$posted = localtime($posted);	$posted =~ tr/  //s;
my $dcheck = `ping -q -c 1 -W 1 $growl_ip`;
	if($dcheck =~ m/1 packets received/) {
	my $data="$name\n\n$did Telegram chat\n\n\"$chatname\"\n\non: $posted";
	$data =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
	`curl http://$growl_ip/chat.cgi?data=$data`;
	} ## END GOOD PING
} ## END SEND GROWL MESSAGE

sub doreplyqu {
my($fname,$lname,$chatid,$message)=@_;	my $prtext='';
foreach my $answ (sort numbr keys %{$subquestion{$message}}) {
$prtext .= "$subquestion{$message}{$answ}\n";
} ## FOREACH ANSWER END
$prtext =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
`curl 'https://api.telegram.org/bot$tagis/sendMessage?chat_id=$chatid\&text=$prtext'`;
exit(0);
} ## END DO REPLY TO QUESTION

sub gethashes {# Create a keyboard buttons
@initqu=('Get Product information','Placing an Order','Contacting Us','Order issues');
$subquestion{'Get Product information'}{1}="Go to:\nhttps://www.example.com/";
$subquestion{'Get Product information'}{2}="Choose Category from the drop-down menu or use site search to locate the product.";
$subquestion{'Get Product information'}{3}="Click on the product link to see full product description";

$subquestion{'Placing an Order'}{1}="Locate the product and click on \"Buy it Now\" button.";
$subquestion{'Placing an Order'}{2}="Follow order instructions.";
$subquestion{'Placing an Order'}{3}="Once order received you will receive order confirmation email.";

$subquestion{'Contacting Us'}{1}="The easiest and most reliable way to get in-touch with us would be using our Contact form at:";
$subquestion{'Contacting Us'}{2}="https://www.example.com/contact/";

$subquestion{'Order issues'}{1}="Should any order issues arise, please do not hesitate to contact us.";
$subquestion{'Order issues'}{2}="We will try our best to work with you for your complete satisfaction.";
$subquestion{'Order issues'}{3}="We have 30-day money-back guarantee!";
} ## END SUB GET HASHES

