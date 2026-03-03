#!/usr/bin/perl

open(FILE, "/web/data/salem/witchcraft/Essex/vol2/gifs/intro/names") || die "Couldn't open file for reading\n";
while(<FILE>) {
   push(@files,"$_");
}
close(FILE);

$cnt=@files;
for($i=0; $i<$cnt; $i++) {
   $gif=$files[$i];
   chop $gif;
   $file=$gif;
   $file=~s/\.gif$//;
   open(OUT, "> /web/data/salem/witchcraft/Essex/vol2/images/intro/$file.html") || die "Cannot open $file.html for writing\n";
   if (defined($files[$i+1])) { 
      $nextfile=$files[$i+1];
      chop $nextfile;
      $nextfile=~s/\.gif$//;
   }
   if (defined($files[$i-1])) {
      $lastfile=$files[$i-1];
      chop $lastfile;
      $lastfile=~s/\.gif$//;
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
<hr width="35">
Volume II<br>
1656-1662<br>
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
<img src="../../gifs/intro/$gif" alt="$gif" align="bottom">
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
