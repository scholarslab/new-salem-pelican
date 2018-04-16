#!/usr/bin/perl

open(FILE, "/web/data/salem/witchcraft/speccol/cmather/jpgs/name") || die "Couldn't open file for reading\n";
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
   
   $jpg=$files[$i];
   chop $jpg;
   
   $file=$jpg;
   $file=~s/\.jpg$//;
   $file=~/(\d{3})/;
   my $num=$1;
   $num=$num-$index;
   my $result = sprintf("%03d",$num);
   $file=~s/\d{3}/$result/;

   open(OUT, "> /web/data/salem/witchcraft/speccol/cmather/images/$file.html") || die "Cannot open $file.html for writing\n";
   if (defined($files[$i+1])) { 
      $nextfile=$files[$i+1];
      chop $nextfile;
      $nextfile=~s/\.jpg$//;
      $nextfile=~/(\d{3})/;
      my $nnum=$1;
      $nnum=$nnum-$index;
      my $nresult = sprintf("%03d",$nnum);
      $nextfile=~s/\d{3}/$nresult/;

   }
   if (defined($files[$i-1])) {
      $lastfile=$files[$i-1];
      chop $lastfile;
      $lastfile=~s/\.jpg$//;
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
<title>The Wonders of the Invisible World</title>
<meta name="generator" content="iView Multimedia">
</head>

<body TEXT="#000000" BGCOLOR="#FFFFFF" LINK="#0000FF" VLINK="#0000FF">

<center><font size="+1">The Wonders of the Invisible World</font><br>
<br><br>
<br>
<hr width="35">
<br>
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
<img src="../jpgs/$jpg" alt="$jpg" align="bottom">
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
