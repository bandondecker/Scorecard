import scorecard as page
# import numpy as np
import os, sys
from pypdf import PdfMerger

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = ''

# =============================================================================
# Set parameters
# =============================================================================
# Ideally these will can be overwritten by the user at the call
totalxunits = 21.6 #Width in cm = 21.59
totalyunits = 27.9 #Height in cm = 27.94

boxwidth = 21.5/17.0 #Original boxwidth was 2, in arbitrary units. Now should be in cm, or so.

top_margin = 2
left_margin_home = 1.25
left_margin_away = 0.1


# =============================================================================
# Buld home card
# =============================================================================
homepage, homecard = page.initialiseCard(totalxunits, totalyunits)
try:
    data = page.getData(fn+'.txt', home=True)
except IOError:
    data = None
page.makeBoxScore(homecard, top_margin, left_margin_home, boxwidth, data)
page.makePitcherStats(homecard, top_margin, left_margin_home, boxwidth, data)
page.makeLineScore(homecard, top_margin, left_margin_home, boxwidth, data)
page.addHeader(homecard, top_margin, left_margin_home, boxwidth, 'Home', data)
homefn = fn+'_home.pdf'
homepage.savefig(homefn, bbox_inches='tight')


# =============================================================================
# Buld away card
# =============================================================================
awaypage, awaycard = page.initialiseCard(totalxunits, totalyunits)
try:
    data = page.getData(fn+'.txt', home=False)
except IOError:
    data = None
page.makeBoxScore(awaycard, top_margin, left_margin_away, boxwidth, data)
page.makePitcherStats(awaycard, top_margin, left_margin_away, boxwidth, data)
page.makeLineScore(awaycard, top_margin, left_margin_away, boxwidth, data)
page.addHeader(awaycard, top_margin, left_margin_away, boxwidth, 'Away', data)
awayfn = fn+'_away.pdf'
awaypage.savefig(awayfn, bbox_inches='tight')


# =============================================================================
# Merge pdfs
# =============================================================================
scorecard = PdfMerger()
for pdf in [homefn, awayfn]:
    scorecard.append(pdf)

if fn == '':
    scorecardfn = 'scorecard.pdf'
else:
    scorecardfn = fn+'.pdf'
scorecard.write(scorecardfn)

os.remove(homefn)
os.remove(awayfn)
