#!/usr/bin/perl

open(FILE, "/web/data/salem/witchcraft/Essex/vol7/introfiles/name") || die "Couldn't open file for reading\n";
while(<FILE>) {
   push(@files,"$_");
}
close(FILE);

####################################
# CHANGE THIS
$index=0;
####################################

$cnt=@files;
for($i=$index; $i<$cnt; $i++) {
   
   $gif=$files[$i];
   chop $gif;
   
   $file=$gif;
   $file=~s/\.gif$//;
   $file=~/(\d{3})/;
   my $num=$1;
   $num=$num-$index;
   my $result = sprintf("%03d",$num);
   $file=~s/\d{3}/$result/;

   open(OUT, "> /web/data/salem/witchcraft/Essex/vol7/introfiles/$file.html") || die "Cannot open $file.html for writing\n";
   if (defined($files[$i+1])) { 
      $nextfile=$files[$i+1];
      chop $nextfile;
      $nextfile=~s/\.gif$//;
      $nextfile=~/(\d{3})/;
      my $nnum=$1;
      $nnum=$nnum-$index;
      my $nresult = sprintf("%03d",$nnum);
      $nextfile=~s/\d{3}/$nresult/;

   }
   if (defined($files[$i-1])) {
      $lastfile=$files[$i-1];
      chop $lastfile;
      $lastfile=~s/\.gif$//;
      $lastfile=~/(\d{3})/;
      my $lnum=$1;
      $lnum=$lnum-$index;
      my $lresult = sprintf("%03d",$lnum);
      if ($lresult =~ /000/) {
         $lresult = "001";
      }
      $lastfile=~s/\d{3}/$lresult/;
   }
   &PrintHead;
   close(OUT);
}

sub PrintHead {
print OUT <<"EndofHeader";
<html>
<head>
<title>Records and Files of the Quarterly Courts of Essex County</title>
<meta name="generator" content="iView Multimedia">
</head>

<body TEXT="#000000" BGCOLOR="#FFFFFF" LINK="#0000FF" VLINK="#0000FF">

<center><font size="+1">Records and Files of the Quarterly Courts of Essex County</font><br>
<br><br>
<br>
<br>
<hr width="35">
Volume VII<br>
<br>
<br>
<br>
<center>
<table border="1" cellspacing="0" cellpadding="4" width="100%">
<tr>
<td width="20"><p><center><a href="../table/index.html">&lt;&lt;</a></center></td>
<td><p></td>
<td width="20"><p><center><a href="$lastfile.html">&lt;</a></center></td>
<td width="20"><p><center><a href="$nextfile.html">&gt;</a></center></td>
</tr>
</table>
</center></p>

<p><center>
<img src="../gifs/$gif" alt="$gif" align="bottom">
</center></p>

<center>
<table border="1" cellspacing="0" cellpadding="4" width="100%">
<tr>
<td width="20"><p><center><a href="../table/index.html">&lt;&lt;</a></center></td>
<td><p></td>
<td width="20"><p><center><a href="$lastfile.html">&lt;</a></center></td>
<td width="20"><p><center><a href="$nextfile.html">&gt;</a></center></td>
</tr>
</table>
</center>

</body>
</html>
EndofHeader
}
