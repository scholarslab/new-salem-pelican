#!/usr/bin/perl

open(FILE, "/web/data/salem/witchcraft/Perley/vol3/jpgs/name") || die "Couldn't open file for reading\n";
while(<FILE>) {
   push(@files,"$_");
}
close(FILE);

$cnt=@files;
for($i=0; $i<$cnt; $i++) {
   $jpg=$files[$i];
   chop $jpg;
   $file=$jpg;
   $file=~s/\.jpg$//;
   open(OUT, "> /web/data/salem/witchcraft/Perley/vol3/images/$file.html") || die "Cannot open $file.html for writing\n";
   if (defined($files[$i+1])) { 
      $nextfile=$files[$i+1];
      chop $nextfile;
      $nextfile=~s/\.jpg$//;
   }
   if (defined($files[$i-1])) {
      $lastfile=$files[$i-1];
      chop $lastfile;
      $lastfile=~s/\.jpg$//;
   }
&PrintHead;
close(OUT);
}

sub PrintHead {
print OUT <<"EndofHeader";
<html>
<head>
<title>History of Salem</title>
<meta name="generator" content="iView Multimedia">
</head>

<body TEXT="#000000" BGCOLOR="#FFFFFF" LINK="#0000FF" VLINK="#0000FF">

<center><font size="+1">A History of Salem Massachusetts</font><br>
<br>
By Sidney Perley
<br>
<hr width="35">
Volume III<br>
1671-1716
<br>
<hr width="35">
Salem, Mass.<br>
Sidney Perley<br>
1928
<br>
<br>
<center>
<table border="1" cellspacing="0" cellpadding="4" width="100%">
<tr>
<td width="20"><p><center><a href="../table/index.html">&lt;&lt;</a></center></td>
<td><p><center><b>$file</b></center></td>
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
<td><p><center><b>$file</b></center></td>
<td width="20"><p><center><a href="$lastfile.html">&lt;</a></center></td>
<td width="20"><p><center><a href="$nextfile.html">&gt;</a></center></td>
</tr>
</table>
</center>

</body>
</html>
EndofHeader
}
