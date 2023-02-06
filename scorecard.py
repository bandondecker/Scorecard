import matplotlib.pyplot as plt
import numpy as np
import sys, os

# =============================================================================
# Functions for making the design of the individual cells
# =============================================================================
def makeDiamond(card,x,y,boxwdith,dashstyle,colour='r',linewidth=0.1):
    card.plot([x,x+0.5*boxwidth/2.0],[y-0.5*boxwidth/2.0,y],c=colour,dashes=dashstyle,lw=linewidth)
    card.plot([x+0.5*boxwidth/2.0,x],[y,y+0.5*boxwidth/2.0],c=colour,dashes=dashstyle,lw=linewidth)
    card.plot([x,x-0.5*boxwidth/2.0],[y+0.5*boxwidth/2.0,y],c=colour,dashes=dashstyle,lw=linewidth)
    card.plot([x-0.5*boxwidth/2.0,x],[y,y-0.5*boxwidth/2.0],c=colour,dashes=dashstyle,lw=linewidth)

def makeRBI(card,x,y,boxwdith,colour='r',linewidth=0.1):
    card.plot([x+0.6*0.5*boxwidth,x+0.6*0.5*boxwidth],[y+0.3*0.5*boxwidth,y+1*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    card.plot([x+0.6*0.5*boxwidth,x+1*0.5*boxwidth],[y+0.3*0.5*boxwidth,y+0.3*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)

def makeBallStrike(card,x,y,boxwdith,colour='r',linewidth=0.1):
    #Horizontal lines
    card.plot([x-1*0.5*boxwidth,x-0.4*0.5*boxwidth],[y-0.8*0.5*boxwidth,y-0.8*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    card.plot([x-1*0.5*boxwidth,x-0.6*0.5*boxwidth],[y-0.6*0.5*boxwidth,y-0.6*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    #Vertical lines
    card.plot([x-0.8*0.5*boxwidth,x-0.8*0.5*boxwidth],[y-1*0.5*boxwidth,y-0.6*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    card.plot([x-0.6*0.5*boxwidth,x-0.6*0.5*boxwidth],[y-1*0.5*boxwidth,y-0.6*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    card.plot([x-0.4*0.5*boxwidth,x-0.4*0.5*boxwidth],[y-1*0.5*boxwidth,y-0.8*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)

def makeFoulPitch(card,x,y,boxwdith,colour='r',linewidth=0.1):
    #Horizontal lines
    card.plot([x,x+0.6*0.5*boxwidth],[y-0.8*0.5*boxwidth,y-0.8*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    card.plot([x,x+1.0*0.5*boxwidth],[y-0.6*0.5*boxwidth,y-0.6*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)
    #Vertical lines
    for b in np.arange(0,0.8*0.5*boxwidth,0.2*0.5*boxwidth):
        card.plot([x+b,x+b],[y-1*0.5*boxwidth,y-0.6*0.5*boxwidth],c=colour,lw=linewidth)#,dashes=dashstyle)


# =============================================================================
# Function to read in the team/lineup data
# =============================================================================
def getData(fn,homeaway):
    lines = open(fn).readlines()
    date = lines[0][:-1]
    venue = lines[1][:-1]
    longnames = lines[2][:-1].split(' v ')
    shortnames = lines[3][:-1].split(' v ')
    if homeaway == 'Home':
        ind = 0
    elif homeaway == 'Away':
        ind = 1
    longname = longnames[ind].split('(')[0][:-1]
    record = longnames[ind].split('(')[1][:-1]
    
    lineup = []
    for i in range(5,14):
        entry = lines[i][:-1].split('\t')[ind]
        lineup.append(entry)
    pitcher = lines[15][:-1].split('\t')[ind]

    data = {'date':date,'venue':venue,'longname':longname,'record':record,'shortnames':shortnames,'lineup':lineup,'pitcher':pitcher}
    return data


# =============================================================================
# Code to build the full scorecard
# =============================================================================
scorecard_dir = os.getcwd()

totalxunits = 8.5*2.54 #Width in cm = 21.59
totalyunits = 11*2.54 #Height in cm = 27.94

boxwidth = 21.5/17.0 #Original boxwidth was 2, in arbitrary units. Now should be in cm, or so.
#Redefine everything else to be in units of this, then scale as needed
namewidth = 3*boxwidth
teamwidth = 4*boxwidth
boxheight = boxwidth #2 At least right now I think these should always be symmetric
pitchlineheight = boxheight*0.65 #Height of the boxes for pitching line and line score
lowmargin = 2.5*boxheight
highmargin = 3*boxheight #As written, I don't think this actually does anything
leftmargin = 0.01
rightmargin = 0 #I think this is also irrelevant now. They were just for scaling originally
pitchbase = lowmargin + 4*pitchlineheight
boxbase = pitchbase + 8*pitchlineheight

framecolour = 'red'
dashed_linewidth = 0.1
lineup_dashstyle = tuple(np.array((1.0,1.0))*25/(0.5*boxwidth))
diamond_dashstyle = tuple(np.array((1.5,1.5))*7.5/(0.35*boxwidth))
solid_linewdith = 0.5
textfontsize = 10

if len(sys.argv) > 1:
    homeaway = sys.argv[1]
else:
    homeaway = 'Test'

if len(sys.argv) > 2:
    gamedata = getData(sys.argv[2],homeaway)

totalpage,card = plt.subplots(nrows=1,subplot_kw={'aspect':'equal','ylim':(0,totalyunits),'xlim':(0,totalxunits)})
totalpage.set_size_inches(8.5*21.59/16.59,11.0*27.94/21.46) #See ruler.py for why this stupid hack seems to work
card.set_axis_off()
#card = plt.axes(aspect='equal',ylim=(0,totalyunits),xlim=(0,totalxunits))

#Make line score
for i in range(3):
    if i < 2:
        card.axhspan(ymin=lowmargin+i*pitchlineheight,ymax=lowmargin+(i+1)*pitchlineheight,xmin=leftmargin/totalxunits,xmax=(leftmargin+teamwidth)/totalxunits,ec=framecolour,fc='w',lw=0.5)
    for j in range(13):
        card.axhspan(ymin=lowmargin+i*pitchlineheight,ymax=lowmargin+(i+1)*pitchlineheight,xmin=(leftmargin+teamwidth+(j*boxwidth))/totalxunits,xmax=(leftmargin+teamwidth+((j+1)*boxwidth))/totalxunits,ec=framecolour,fc='w',lw=0.5)

#Make pitching stat box
for i in range(7):
    card.axhspan(ymin=pitchbase+i*pitchlineheight,ymax=pitchbase+(i+1)*pitchlineheight,xmin=leftmargin/totalxunits,xmax=(leftmargin+0.5*boxwidth)/totalxunits,ec=framecolour,fc='w',lw=0.5)
    card.axhspan(ymin=pitchbase+i*pitchlineheight,ymax=pitchbase+(i+1)*pitchlineheight,xmin=(leftmargin+0.5*boxwidth)/totalxunits,xmax=(leftmargin+0.5*boxwidth+(namewidth+0.5*boxwidth))/totalxunits,ec=framecolour,fc='w',lw=0.5)
    for j in range(8):
        card.axhspan(ymin=pitchbase+i*pitchlineheight,ymax=pitchbase+(i+1)*pitchlineheight,xmin=((leftmargin+0.5*boxwidth+(namewidth+0.5*boxwidth))+j*boxwidth)/totalxunits,xmax=((leftmargin+0.5*boxwidth+(namewidth+0.5*boxwidth))+(j+1)*boxwidth)/totalxunits,ec=framecolour,fc='w',lw=0.5)

#Make box score
#horizwidths = [1,namewidth,1,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,boxwidth,1,1,1,1,1,1]
horizwidths = np.array([0.5, 3, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])*boxwidth

for j in range(len(horizwidths)):
    #card.axhspan(ymin=boxbase+0,ymax=boxbase+0+1,xmin=(leftmargin+np.sum(horizwidths[:j+1])-horizwidths[j])/totalxunits,xmax=(leftmargin+np.sum(horizwidths[:j+1]))/totalxunits,ec=framecolour,fc='w',lw=0.5)
    card.axhspan(ymin=boxbase+0,ymax=boxbase+0+0.5*boxheight,xmin=(leftmargin+np.sum(horizwidths[:j+1])-horizwidths[j])/totalxunits,xmax=(leftmargin+np.sum(horizwidths[:j+1]))/totalxunits,ec=framecolour,fc='w',lw=0.5)
for i in np.arange(0.5,9,1):#boxheight*9,boxheight):
    for j in np.arange(len(horizwidths)):
        card.axhspan(ymin=boxbase+i*boxheight,ymax=boxbase+(i*boxheight)+(boxheight),xmin=(leftmargin+np.sum(horizwidths[:j+1])-horizwidths[j])/totalxunits,xmax=(leftmargin+np.sum(horizwidths[:j+1]))/totalxunits,ec=framecolour,fc='w',lw=0.5)
for j in range(len(horizwidths)):
    card.axhspan(ymin=boxbase+9.5*boxheight,ymax=boxbase+10*boxheight,xmin=(leftmargin+np.sum(horizwidths[:j+1])-horizwidths[j])/totalxunits,xmax=(leftmargin+np.sum(horizwidths[:j+1]))/totalxunits,ec=framecolour,fc='w',lw=0.5)

for i in np.arange(1,10):#*2:
    card.axhline(y=boxbase+i*boxheight,xmin=leftmargin/totalxunits,xmax=(leftmargin+np.sum(horizwidths[:3]))/totalxunits,c=framecolour,dashes=lineup_dashstyle,lw=dashed_linewidth)
    card.axhline(y=boxbase+i*boxheight,xmin=(leftmargin+np.sum(horizwidths[:13]))/totalxunits,xmax=(leftmargin+np.sum(horizwidths))/totalxunits,c=framecolour,dashes=lineup_dashstyle,lw=dashed_linewidth)

#Make diamonds
for i in range(1,10):
    for j in range(10):
        centrex = leftmargin+np.sum(horizwidths[:3])+(j+0.5)*boxwidth
        centrey = boxbase+i*boxheight
        makeDiamond(card,centrex,centrey,boxwidth,dashstyle=diamond_dashstyle,colour=framecolour,linewidth=dashed_linewidth)
        makeRBI(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)
        makeBallStrike(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)
        makeFoulPitch(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)

#Add text
#Numbers
for i in range(1,11):
    card.text(leftmargin+np.sum(horizwidths[:3])+(i-0.5)*boxwidth,lowmargin+2.5*pitchlineheight,str(i),fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')
    card.text(leftmargin+np.sum(horizwidths[:3])+(i-0.5)*boxwidth,boxbase+19.5*boxheight*0.5,str(i),fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#RHE
card.text(leftmargin+np.sum(horizwidths[:3])+(10.5)*boxwidth,lowmargin+2.5*pitchlineheight,'R',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')
card.text(leftmargin+np.sum(horizwidths[:3])+(11.5)*boxwidth,lowmargin+2.5*pitchlineheight,'H',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')
card.text(leftmargin+np.sum(horizwidths[:3])+(12.5)*boxwidth,lowmargin+2.5*pitchlineheight,'E',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#Box score headers
cols = ['AB','R','H','RBI','BB','SO']
for j in range(6):
    card.text((leftmargin+np.sum(horizwidths[:13])+(j+0.5)*boxwidth*0.5),boxbase+19.5*0.5*boxheight,cols[j],fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#Pitching headers
cols = ['IP','PC','H','R','ER','BB','SO','W/L']
for j in range(8):
    card.text((leftmargin+np.sum(horizwidths[:3])+(j+0.5)*boxwidth),pitchbase+6.5*(pitchlineheight),cols[j],fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#Name headers
for i in [pitchbase+6.5*(pitchlineheight),boxbase+19.5*0.5*boxheight]:
    card.text((leftmargin+0.25*boxwidth),i,'No.',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')
    
    card.text((leftmargin+0.75*boxwidth),i,'Name',fontsize=textfontsize,color=framecolour, horizontalalignment='left',verticalalignment='center')
    
card.text((leftmargin+np.sum(horizwidths[:2])+0.25*boxwidth),boxbase+19.5*0.5*boxheight,'Pos',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#Total line
card.text((leftmargin+np.sum(horizwidths[:1])+0.5*boxwidth),boxbase+0.25*boxheight,'Totals (R/H/LoB)',fontsize=textfontsize,color=framecolour, horizontalalignment='left',verticalalignment='center')
for j in range(3,13):
    card.text((leftmargin+np.sum(horizwidths[:j])+0.5*boxwidth),boxbase+0.25*boxheight,'/   /',fontsize=textfontsize,color=framecolour, horizontalalignment='center',verticalalignment='center')

#Header
lowhead = 'Venue:{0: <60}Date:{0: <40}Attendance:{0: <25}Time:'.format('')
card.text(leftmargin,boxbase+20.5*0.5*boxheight,lowhead,fontsize=textfontsize,color=framecolour, horizontalalignment='left',verticalalignment='center')

card.text(leftmargin,boxbase+22.5*0.5*boxheight,homeaway+' Team (Record):',fontsize=textfontsize,color=framecolour, horizontalalignment='left',verticalalignment='center')

if len(sys.argv) <= 2:
    plt.savefig(os.path.join(scorecard_dir, 'scorecard_'+homeaway.lower()+'.pdf'),bbox_inches='tight')

else:
    ## Teams
    for i in range(2):
        card.text(leftmargin+0.25*boxwidth, lowmargin+(0.5+i)*pitchlineheight, gamedata['shortnames'][i], fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')

    ## Pitcher info
    pitchno, pitchname = gamedata['pitcher'].split(':')
    # Number
    card.text(leftmargin+0.25*boxwidth,pitchbase+5.5*(pitchlineheight),pitchno,fontsize=textfontsize,color='k', horizontalalignment='center',verticalalignment='center')
    # Name
    card.text(leftmargin+0.75*boxwidth,pitchbase+5.5*(pitchlineheight),pitchname,fontsize=textfontsize,color='k', horizontalalignment='left',verticalalignment='center')

    ## Linuep
    for i in range(9):
        number,name,pos = gamedata['lineup'][i].split(':')
        # Number
        card.text(leftmargin+0.25*boxwidth,boxbase+(18.5-i*2)*0.5*boxheight,number,fontsize=textfontsize,color='k', horizontalalignment='center',verticalalignment='center')
        # Name
        card.text(leftmargin+0.75*boxwidth,boxbase+(18.5-i*2)*0.5*boxheight,name,fontsize=textfontsize,color='k', horizontalalignment='left',verticalalignment='center')
        # Position
        card.text(leftmargin+np.sum(horizwidths[:2])+0.25*boxwidth,boxbase+(18.5-i*2)*0.5*boxheight,pos,fontsize=textfontsize,color='k', horizontalalignment='center',verticalalignment='center')
    
    ## Team/game info
    card.text(leftmargin+1.25*boxwidth, boxbase+20.5*0.5*boxheight, gamedata['venue'],fontsize=textfontsize,color='k', horizontalalignment='left',verticalalignment='center') # The reason for the double multiplication is for ease of comparison to the iterative lineup add
    
    card.text(leftmargin+np.sum(horizwidths[:6])+0.25*boxwidth, boxbase+20.5*0.5*boxheight, gamedata['date'],fontsize=textfontsize,color='k', horizontalalignment='left',verticalalignment='center')
    
    highheadadd = '{1} ({2})'.format('',gamedata['longname'],gamedata['record'])
    card.text(leftmargin+np.sum(horizwidths[:2])-0.25*boxwidth, boxbase+22.5*0.5*boxheight, highheadadd,fontsize=textfontsize,color='k', horizontalalignment='left',verticalalignment='center')
    
    #Save
    plt.savefig(os.path.join(scorecard_dir, 'scorecard_'+homeaway.lower()+'_'+sys.argv[2][:-4]+'.pdf'),bbox_inches='tight')
