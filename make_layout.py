"""One-time helper: derive src/layout.html from a page of the al-folio site (same head, nav, footer, scripts).

Run once with the path of a built page; the result is committed. Placeholders:
  {{root}} path prefix to the site root ("" or "../"), {{title}}, {{description}}, {{nav}}, {{content}}
"""
import re
import sys

src = sys.argv[1]
t = open(src).read()
a = t.index("<article>")
b = t.index("</article>")
head, tail = t[:a], t[b + len("</article>"):]

# page title / description
head = re.sub(r"<title>.*?</title>", "<title>{{title}}</title>", head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*(")', r"\1{{description}}\2", head)

# brand: "Max Rommel" -> "Aevia"
head = re.sub(r'(<a class="navbar-brand[^>]*>)\s*<span class="font-weight-bold">Max</span>\s*Rommel\s*(</a>)',
              r'\1 <span class="font-weight-bold">Aev</span>ia \2', head)
head = head.replace('href="../index.html"><span', 'href="{{root}}index.html"><span')

# nav list -> placeholder
head = re.sub(r'<ul class="navbar-nav ml-auto flex-nowrap">.*?</ul>', '<ul class="navbar-nav ml-auto flex-nowrap">{{nav}}</ul>', head, flags=re.S)

# favicon + relative asset paths
head = head.replace("../assets/img/favicon.svg", "{{root}}assets/img/favicon.svg")
head = head.replace("../assets/", "{{root}}assets/")
head = head.replace('href="../index.html"', 'href="{{root}}index.html"')
tail = tail.replace("../assets/", "{{root}}assets/")

# footer: Impressum and privacy live on the main site (one legal notice for all of maxrommel.de)
tail = tail.replace('href="../impressum/index.html"', 'href="https://maxrommel.de/impressum/index.html"')
tail = tail.replace('href="../privacy/index.html"', 'href="https://maxrommel.de/privacy/index.html"')
tail = tail.replace("Questions or feedback? I'd love an email.", 'Part of <a href="https://maxrommel.de">maxrommel.de</a>.')

head = re.sub(r'<header class="post-header">\s*<h1 class="post-title">[^<]*</h1>\s*</header>', '', head)
layout = head + '<article>{{content}}</article>' + tail
leftovers = re.findall(r'(?:href|src)="\.\./[^"]*"', layout)
print("leftover ../ refs:", leftovers)
open("src/layout.html", "w").write(layout)
print("layout bytes:", len(layout))
