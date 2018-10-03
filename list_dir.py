import os

print("<html><body><ul>")

for f in sorted(os.listdir('.')):
  print('<li><a href="%s">%s</a></li>' % (f,f))

print("</ul></body></html>")