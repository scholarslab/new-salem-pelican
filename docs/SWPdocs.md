# Basic Documentation for Salem Witchcraft Papers (New-Salem-Pelican)

## File locations

New-Salem-Pelican presents the Salem Witchcraft Papers through the Pelican Static Site generator. The SWP documents are encoded in the simple Markdown format. Pelican then builds these documents into interlinked static HTML files. By default, Pelican keeps all content files in the [content directory](https://github.com/scholarslab/new-salem-pelican/tree/master/content). The New Salem content directory contains three discrete sets of markdown files:

* [swp (Salem Witchcraft Papers)](https://github.com/scholarslab/new-salem-pelican/tree/master/content/swp)
* [salvrec (Salem Village Records)](https://github.com/scholarslab/new-salem-pelican/tree/master/content/salvrec)
* [upham (Upham's Salem Watchcraft)](https://github.com/scholarslab/new-salem-pelican/tree/master/content/upham)

It also contains one directory of non-markdown files:

* [search (SWP search index and corpus)](https://github.com/scholarslab/new-salem-pelican/tree/master/content/search)

Of these, the site is normally configured to only build content from swp and search. Since the other markdown sets (salvrec and upham) are not in regular development and isolated from the rest of the site's content, we keep their markdown sources here for archival purposes and simply load in pre-built static html content to make builds faster and simpler.

The [swp directory](https://github.com/scholarslab/new-salem-pelican/tree/master/content/swp) contains 140 markdown files. Each file contains all the documents in a specific SWP case. [Here is an example](https://raw.githubusercontent.com/scholarslab/new-salem-pelican/master/content/swp/n6.md).

Each document in the case can be displayed separately by the front-end, but are organized together in the repository.

## Front Matter

The section at the top of each file is the Markdown front matter, a list of metadata about the case.

We use five metadata entries for SWP, one to a line:
* title: The case title, in the format SWP No. ###: FIRST LAST (of the accused)
* date: In the format YYYY=MM-DD
* slug: The URL, which should be the same as the SWP case #.
* category: Used to distinguish between different markdown sets. For SWP cases, this should always be "swp"
* tags: We are using Pelican's tag mechanism to track the individuals who appear in a particular case.

The text below the front matter is the content, formatted in mixed Markdown and HTML.

## Markdown formating

Markdown is a simple rich text format designed for easy human readibility so that documents should intuitively convey the meaning of its markup without complicated tagging or need for references. It is often used as an easy-to-read and easy-to-write method for producing more complex formats like HTML. This documentation was written in Markdown.

Here is a [good reference document](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) covering Markdown syntax.

Because the SWP markdown files essentially serve as a bridge between the older Cocoon/TEI P4 framework and Pelican, they don't quite live up to Markdown's goals. Markdown allows for arbitrary HTML alongside its own syntax and we take advantage fo this for a variety of purposes. Markdown is very forgiving, but the HTML blocks we use must be very carefully formatted.

Each document is wrapped within an HTML div tag:

`<div markdown class="doc" id="n6.1">`

This formatting must be exactly reproduced in order for the keyword search to function.

Figures use the markdown syntax to reference image locations, but are wrapped in HTML span tags for styling reasons:

`<span markdown class="figure">[![Figure ecca2107r](archives/ecca/thumb/ecca2107r.jpg)](archives/ecca/large/ecca2107r.jpg)</span>`

There is some latitude to the formating of the definitive, bracketed dates for each document. However, that format must still be machine-readable as a full date. Archaic spelling or formatting, extraneous or missing characters or punctuation, two-digit years, and the such will all confuse the software designed to parse modern date strings.

This is an example of a good date:

`[+ May 3, 1693 ]`

These are bad dates:

`[+ January 13, 1693 `
`[this 28 of June An'o 1692 ]`
`[MAy 13, 1692]`
`[May the 23, 1692 ]`
`[September 9, 92 ]`
`[10 August 1692. ]`
`[2. May 2, 1692]`
`[Passed November 2.]`

Bad dates will not show up on the search, but will not otherwise break the site. The search generator produces a list of bracketed entries that look like dates but that it can't understand and also a list of documents that are missing dates entirely, so bad dates should be easy to discover.

## Name Index

New Salem Pelican uses a tagging system to track which people appear in which cases. This is the tag metadata field in the front matter. To account for people with the same name or one person with many different names, titles, and addresses, we use a unique Id for each person. In order to display a single, canonical name to the user, New Salem uses a [json file as a mapping between ID and name](https://github.com/scholarslab/new-salem-pelican/blob/master/tags.json).

This file must be updated to alter a person's ID or canonical name. If an entry is not found, no text will be displayed. This won't totally break the site, but will result in some links that can no longer be seen or clicked.

## Keyword Search

NSP uses the [Lunr.js](https://github.com/olivernn/lunr.js) client-side search library to perform searches. For this to work, a corpus and index must be generated from the source documents ahead of time. If documents do not appear in the keyword/date search, it is likely because this has not yet been done (or there is a bug in the corpus/index generation).

## Build/Deployment

TBD
