# Markdown Glossary for SWP Files

This document is a quick reference glossary of the markdown syntax and HTML tags used in the SWP files on the Salem Witchcraft Trials site.

* `<div>`
	
	The `<div>` tag is an HTML tag used to wrap contents of case documents in SWP files and the case document title. The contents of this tag drive keyword searching, and the tag must be formatted exactly as in these examples
	
	ex. Case Document 
		
		<div markdown class="doc" id="n6.1">
			Text of case document
		</div>
		
	Note that the closing `</div>` tag is placed at the end of the section of text comprising the case document.
	
	ex. Title of A Case Document
		
		<div class="doc_id">SWP No. 6.1</div>
		
	Note that this tag is closed after the text of the document title.

* Front Matter
	
	The front matter is markdown style metadata about the case transcribed in the markdown file. These fields are required, and must be the top five lines of the file, formatted exactly as shown in the example. Each label described below should be separated from the contents of the label by a colon.
	
	```
	title: The title of the case, in the format _SWP No. ###: FIRST LAST_ (of the accused)
	date: The date of the case, in the format YYYY-MM-DD
	slug: The SWP case number
	category: Used to distinguish between different markdown sets. For SWP documents, this should always be 'swp'	
	tags: Used to track all individuals named in a case. The person ids should be separated by a comma.
	```
	
	ex. 
	
	```
	title: SWP No. 006: John Alden
	date: 1692-05-31
	slug: n6
	category: swp
	tags: aldjoh, wilabi, warmar, hilzeb, noynic, carmar1, ricsar, ricnic, chesam1, hawjoh, walmar, ricjoh, corjoh, wilnat, booeli, putann2, arnjoh, stough, lewmer, gidbar
	```

* Heading
	
	The `#` character followed by a space creates a level 1 heading. This is used for the titles in case documents.
	
	ex.
	
	`# (Complaint v. [Joan Peney](/tag/penjoa.html) & Statement of Bond to Prosecute )`

* Image Link
	
	To include a link to the page image of a case document, use the following code
	
	`<span markdown class="figure">[![Figure name for display on web page](url for small inline image)](url for full size document)</span>`
	
	ex.
	
	`<span markdown class="figure">[![Figure B29r](archives/BPL/gifs/B29A.gif)](archives/BPL/LARGE/B29A.jpg)</span>`

* Name Link
	
	To make proper names from the case documents searchable, they must be linked to the official tag list of person ids using the following code
	
	`[First Last](/tag/personid.html)`
	
	ex.
	
	`[Zebulon Hill](/tag/hilzeb.html)`

* `<span>`
	
	The HTML `<span>` tag is used to style image figures included in the document. See Image Link entry above.

