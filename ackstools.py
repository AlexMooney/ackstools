#!/usr/bin/python2

from flask import Flask
import libhenches
import libspellbook
import tables
from flask import render_template
from flask import request

app = Flask(__name__)

classfile = './classes'
spellsfile = './spells'
profsfile = './genprofs'
namefile = './germans'

classes = libhenches.parseClasses(classfile)
spells = libspellbook.parseSpells(spellsfile)
names = libhenches.parseNames(namefile)
profs = libhenches.parseProfs(profsfile)
marketvals = libhenches.marketClasses

@app.route('/')
def halp():
  return "halp hao do wobsit"

@app.route('/hench')
@app.route('/hench/')
@app.route('/hench/<int:market>')
def genrandom(market=None):
  if 'market' in request.form:
    market = int(request.form['market'])
  if not market or 1 > market or 6 < market:
    market = 4
  ol = []
  for level in range(0,5):
    numhenches = libhenches.rollMarket(marketvals[market-1][level])
    ol.append(libhenches.genHenches(numhenches, level, classes, market, 
      True, spells, names, profs, False))

  ol = [[s.replace('\n','. ') for s in l] for l in ol]
  return render_template('random.html',levels=ol) 

if __name__ == "__main__":
  app.debug = True
  app.run()
