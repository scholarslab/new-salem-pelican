import os
import sys

APPEND = """
<!-- Matomo -->
<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://analytics.lib.virginia.edu/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '48']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<!-- End Matomo Code -->
"""

import os
output_dir = sys.argv[1]
files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(output_dir) for f in filenames if os.path.splitext(f)[1] == '.html' or os.path.splitext(f)[1] == '.htm']
for file in files:
    with open(file, 'r') as fin:
        html = fin.read()
    if "</HEAD>" not in html and "</head>" not in html:
        print(file.replace("output","old-salem"))
        continue
    if "</HEAD>" in html: 
        split = html.split("</HEAD>",1)
        appended = "".join([split[0],APPEND,"</HEAD>",split[1]])
    elif "</head>" in html: 
        split = html.split("</head>",1)
        appended = "".join([split[0],APPEND,"</head>",split[1]])
    with open(file, 'w') as fout:
        fout.write(appended)