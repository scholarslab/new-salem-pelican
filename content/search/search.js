    idxFile = '/search/idx.json';
    corpusFile = '/search/corpus.json';
    
    if (search) {
        var searchVars = search.split('&');
        for (var i=0;i<searchVars.length;i++) {
            var pair = searchVars[i].split("=");
            $('#'+pair[0]).val(pair[1]);
        }
    }
    $("#search_form").hide();
    $.when(
        $.getJSON(idxFile, function(data) {
            window.idx = data;
        }),
        $.getJSON(corpusFile, function(data) {
            window.documents = [];
            Object.entries(data).forEach(function(key, value) {
                var doc = {
                    'id': key[1].id,
                    'content': key[1].content,
                    'title': key[1].title,
                    'slug': key[1].slug,
                    'date': key[1].date,
                    'year': key[1].year,
                    'month': key[1].month,
                    'day': key[1].day,
                    'case_id': key[1].case_id,
                    'case_title': key[1].case_title
                };
                window.documents.push(doc);
            });
        })
    ).done(function() {
        $("#search_loading").hide();
        $("#search_form").show();
        if (search) {
            displaySearchResults(search);
        }
    });

    function returnQueryArray(query_string) {
        var query_array = new Array();
        var searchVars = query_string.split('&');
        if (searchVars) {
            for (var i=0; i<searchVars.length;i++) {
                var pair = searchVars[i].split("=");
                query_array[pair[0]] = pair[1];
            }
        }
        return query_array;
    }

    console.log(returnQueryArray(search));

    function buildLunrQueryString(query) {
        var queryArray = new Array(),
            queryString = '',
            vars = returnQueryArray(query);
        if (vars) {
            for (var key in vars) {
                value = vars[key];
                console.log(value);
                if (value != '') {
                    if (key == 'terms') {
                        termsArray = value.split(' ');
                        queryVariable = '+'+termsArray.join(' +');
                    } else {
                        queryVariable = "+"+key+":"+value;
                    }
                    queryArray.push(queryVariable);
                }
            }
            queryString = queryArray.join(" ");
        }
        return queryString;
    }

    function getSearchResults(query) {
        idx = lunr.Index.load(window.idx);
        results = buildLunrQueryString(query)
        return idx.search(results);
    }

    function displaySearchResults(query) {
        var results = getSearchResults(query),
            search_list = $("#search-list"),
            case_list = $("#case-list"),
            results_cases = [],
            results_docs = [],
            results_docs_undated = [],
            lookup = {};

        var noCaseIds = [];

        if (results.length) {
            search_list.empty(); // Clear any old results
            case_list.empty();            
            results.forEach(function(result) {
                var item = window.documents.filter(doc => doc.id === result.ref);
                if (item[0].date == undefined){
                    results_docs_undated.push(item)
                }
                else{
                    results_docs.push(item)
                }

                var case_id = item[0].case_id;
                
                if (case_id !== null) {
                    var case_title = item[0].case_title;
                        
                    if (!(case_id in lookup)) {
                        lookup[case_id] = 1;
                        documentCase = new Object();
                        documentCase.case_id = case_id;
                        documentCase.case_title = case_title;
                        documentCase.document_count = 1;
                        results_cases.push(documentCase);
                    } else {
                        case_result = results_cases.find( casefile => casefile.case_id === case_id)
                        case_result.document_count += 1;
                    }
                }
            });

            results_docs.sort(function(a,b){
                if (a[0].date == b[0].date){
                    return 0
                }
                else if (a[0].date > b[0].date) {
                    return 1
                }
                else{
                    return -1
                }
            });


            results_docs.forEach(function(doc){
                var li = buildSearchResult(doc[0]) // Build a snippet of HTML for this result
                search_list.append(li);
            });
            results_docs_undated.forEach(function (doc) {
                var li = buildSearchResult(doc[0]) // Build a snippet of HTML for this result
                search_list.append(li);
            });

            results_cases.sort(function (a, b) {
                return b.document_count - a.document_count;
            });
            results_cases.forEach(function(casefile) {
                var li = buildCaseResult(casefile);
                case_list.append(li);
            });
        } else {
            // If there are no results, let the user know.
            search_results.html('<li>No results found.<br/>Please check spelling, spacing, yada...</li>');
        }
    }

    // HTML snippet for individual search result.
    function buildSearchResult(doc) {
        var div = document.createElement('div'),
            article = document.createElement('article'),
            header = document.createElement('header'),
            section = document.createElement('section'),
            em = document.createElement('em'),
            h2 = document.createElement('h2'),
            courtcase = document.createElement('p'),
            a = document.createElement('a');
        
        em.textContent = doc.date;
        a.dataset.field = 'name';
        a.href += '/' + doc.slug + '.html#'+doc.id;
        a.textContent = doc.title.toUpperCase();
        courtcase.textContent = 'Case: ' + doc.case_title;

        div.class = 'doc';
        div.appendChild(article);
        article.appendChild(header);
        article.appendChild(section);
        header.appendChild(em);
        header.appendChild(h2);
        header.appendChild(courtcase);
        h2.appendChild(a);

        return div;
    }

    function buildCaseResult(casefile) {
        var case_item = document.createElement('li'),
            case_link = document.createElement('a'),
            case_text = document.createElement('div'),
            case_num = document.createElement('div'),
            queryString = '',
            queryArray = new Array(),
            vars = returnQueryArray(search);
        
        vars['case_id'] = casefile.case_id;

        for (var key in vars) {
            var value = vars[key];
            string = key+'='+value;
            queryArray.push(string);
        }

        queryString = queryArray.join("&");
        $(case_text).addClass('facet_text');
        $(case_num).addClass('facet_num');
        case_link.href += '/search/?'+queryString;
        console.log(case_link.href);
        case_link.textContent = ''+casefile.case_title;
        case_text.appendChild(case_link);
        case_item.appendChild(case_text);
        case_num.textContent = ''+casefile.document_count;
        case_item.appendChild(case_num);

        return case_item;
    }

    // Wraps matching search terms with mark element.
    function wrapTerms(element, matches) {
        var nodeFilter = {
            acceptNode: function(node) {
                if (/^[\t\n\r ]*$/.test(node.nodeValue)) {
                    return NodeFilter.FILTER_SKIP
                }
                return NodeFilter.FILTER_ACCEPT
            }
        }
        var index = 0,
            matches = matches.sort(function(a, b) {
                return a[0] - b[0]
            }).slice(),
            previousMatch = [-2, - 2],
            match = matches.shift(),
            walker
        if (element instanceof Element) {
            walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            nodeFilter,
            false)
        } else {
            return 'not an element';
        }
        while (node = walker.nextNode()) {
            if (match == undefined) break
            if (match[0] == previousMatch[0]) continue
            var text = node.textContent,
                nodeEndIndex = index + node.length;
            if (match[0] < nodeEndIndex) {
                var range = document.createRange(),
                    tag = document.createElement('mark'),
                    rangeStart = match[0] - index,
                    rangeEnd = rangeStart + match[1];
                tag.dataset.rangeStart = rangeStart
                tag.dataset.rangeEnd = rangeEnd
                range.setStart(node, rangeStart)
                range.setEnd(node, rangeEnd)
                range.surroundContents(tag)
                index = match[0] + match[1]
                // the next node will now actually be the text we just wrapped, so
                // we need to skip it
                walker.nextNode()
                previousMatch = match
                match = matches.shift()
            } else {
                index = nodeEndIndex
            }
        }
    }

    function clear_form(){
        $("#search_form")[0].reset();
        $("#search-list").empty();
        $("#case-list").empty();
    }

