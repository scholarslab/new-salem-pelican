# new-salem-pelican
New Salem running on Pelican

## Initial Set Up

- Clone the repo.
- In the project directory, initialize the theme submodule: `git submodule init && git submodule update`
- Run `pipenv update` to grab dependencies.

## Running the Project.
- Open pipenv shell: `pipenv shell`
- Run the web server: `make devserver`

## Static files and make targets
The typical Pelican structure is complicated by the large number of legacy static files from the Old Salem site that have not been converted into Pelican markdown content as well as static HTML files that replace or link to these unmanaged static files. In order to limit the pollution of the content directory, these files reside inside a number of discrete subdirectories:

`old-salem` - Old Salem static web content, some changed minimally to conform to New Salem urls and content requirements
`static-salem` - New Salem static web content unmanaged by Pelican
`static-salvrec` and `static-uph1wit` - New Salem static content that was built once by Pelican from markdown files in the `content` directory, but made into static web content because we don't expect them to be modified going foward.

The order that these files should be loaded into the output directory is:
1. `old-salem`
2. Pelican-built content
3. `static-salem`, `static-salvrec`, `static-uph1wit` (implying that none of these files should conflict)

Because the old-salem directory contains many thousands of files, it can be slow to rsync over to the `output` directory. And because it is the first to be loaded and therefore the lowest priority when it comes to duplicate files, we should only need to copy it into `output` once every `clean`. 

`make html-old` performs steps 1, 2, and 3.
`make html` performs steps 2 and 3. 
`make html-static` performs only step 3
`make devserver` extends `make html`
`make publish` and its child targets clean the output directory and then perform steps 1, 2, and 3.

Clear as mud? You're probably safe doing `make html` every time. If none of the styling and images show up, do a `make html-old` once. Everything is terrible, I know.

## Documentation
[Documentation for the Salem Witchcraft Papers](docs/SWPdocs.md)
