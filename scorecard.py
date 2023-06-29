
import matplotlib.pyplot as plt
import numpy as np
import sys, os


# =============================================================================
# Set global defaults
# =============================================================================
totalxunits = 21.6 #Width in cm = 21.59
totalyunits = 27.9 #Height in cm = 27.94

boxwidth = 21.5/17.0 #Original boxwidth was 2, in arbitrary units. Now should be in cm, or so.

framecolour = 'red'
dashed_linewidth = 0.07
lineup_dashstyle = tuple(np.array((1.0,1.0))*25/(0.5*boxwidth))
diamond_dashstyle = tuple(np.array((1.5,1.5))*7.5/(0.35*boxwidth))
solid_linewidth = 0.5
textfontsize = 8


# =============================================================================
# Code to create the card and define the dimensions
# =============================================================================
def initialiseCard(totalxunits:float, totalyunits:float):
    totalpage = plt.figure()
    # For some reason this always produces unreasonable margins
    # totalpage.set_size_inches(8.5, 11.0)
    scale = 1.2
    totalpage.set_size_inches(8.5*scale, 11.0*scale)
    card = totalpage.add_subplot(111)
    card.set_xlim(0,totalxunits)
    card.set_ylim(0,totalyunits)
    card.set_axis_off()
    
    return totalpage, card


# =============================================================================
# Functions for making the design of the individual cells
# =============================================================================
def makeDiamond(card, x, y, boxwdith, dashstyle, colour='r', linewidth=dashed_linewidth):
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
def getData(fn:str,home:bool):
    idx = np.abs(home - 1)
    lines = open(fn).readlines()
    date = lines[0][:-1]
    venue = lines[1][:-1]
    home_region, away_region = lines[2][:-1].split(' v ')
    region_name = lines[2][:-1].split(' v ')[idx]
    nickname = lines[3][:-1].split(' v ')[idx]
    record = lines[4][:-1].split(' v ')[idx]
    
    lineup = []
    for i in range(6,15):
        entry = lines[i][:-1].split(' v ')[idx]
        lineup.append(entry)
    pitcher = lines[16][:-1].split(' v ')[idx]

    data = {'date':date,'venue':venue,'home':home_region,'away':away_region,'region':region_name,'nickname':nickname,'record':record,'lineup':lineup,'pitcher':pitcher}
    return data


# =============================================================================
# Code to build the large grid elements
# =============================================================================
vertical_locations = np.cumsum([0, 0.5, 3, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
def makeBoxScore(card, top_margin, left_margin, boxwidth, data=None):
    
    boxheight = boxwidth # The boxes in this section are symmetric
    
    # Define which of the vertical lines to use
    # For this, it's all 19 of them
    vertical_booleans = np.array([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True])
    vertlines = left_margin + (vertical_locations[vertical_booleans == True])*boxwidth

    # Solid row heights
    heights = np.array([0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5]) * boxheight
    horizsolidlines = np.concatenate([[totalyunits - top_margin], (totalyunits - top_margin) - heights.cumsum()])

    # Solid lines
    for vl in vertlines:
        card.plot([vl, vl], [horizsolidlines[-1], horizsolidlines[0]], ls='-', lw=solid_linewidth, c=framecolour)
    for hsl in horizsolidlines:
        card.plot([vertlines[0], vertlines[-1]], [hsl, hsl], ls='-', lw=solid_linewidth, c=framecolour)
    
    # Dashed lines
    horizdashedlines = []
    for i in range(9):
        # TODO: Define variable for how far down the frame to put the dashed line
        # And sync them to the names below
        horizdashedlines.append(totalyunits - top_margin - (0.5 + i+0.4)*boxheight)
        horizdashedlines.append(totalyunits - top_margin - (0.5 + i+0.7)*boxheight)

    for hdl in horizdashedlines:
        card.plot([vertlines[0], vertlines[3]], [hdl, hdl], dashes=lineup_dashstyle, lw=dashed_linewidth, c=framecolour)
        card.plot([vertlines[12], vertlines[-1]], [hdl, hdl], dashes=lineup_dashstyle, lw=dashed_linewidth, c=framecolour)

    #Make diamonds
    for i in range(3,12): # Horizontal values of innings
        centrex = (vertlines[i] + vertlines[i+1])/2.0
        for j in range(1,10): # Vertical values of batting order
            centrey = (horizsolidlines[j] + horizsolidlines[j+1])/2.0
            makeDiamond(card,centrex,centrey,boxwidth,dashstyle=diamond_dashstyle,colour=framecolour,linewidth=dashed_linewidth)
            makeRBI(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)
            makeBallStrike(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)
            makeFoulPitch(card,centrex,centrey,boxwidth,colour=framecolour,linewidth=dashed_linewidth)
    
    # Add column headers
    x_headers = vertlines[:-1] + (vertlines[1:] - vertlines[:-1])/2.0
    x_headers[1] = vertlines[1] + (vertlines[2] - vertlines[1])*0.1 # Left align
    y_headers = horizsolidlines[0] + (horizsolidlines[1] - horizsolidlines[0])/2.0
    
    boxcols = np.concatenate([['#', 'Batting', ''], range(1,10), ['AB','R','H','RBI','BB','SO']])
    for i in range(len(x_headers)):
        colname = boxcols[i]
        if i == 1:
            halign = 'left'
        else:
            halign = 'center'
        card.text(x_headers[i], y_headers, colname, fontsize=textfontsize, color=framecolour, horizontalalignment=halign, verticalalignment='center')
    
    # Add total line
    x_totals = x_headers[1:-6]
    y_totals = horizsolidlines[-1] - (horizsolidlines[-1] - horizsolidlines[-2])/2.0
    
    for i in range(len(x_totals)):
        if i == 0:
            totalstring = 'Totals (R/H/LoB)'
            halign = 'left'
        elif i == 1:
            totalstring = ''
            halign = 'center'
        else:
            totalstring = '/   /'
            halign = 'center'
        card.text(x_totals[i], y_totals, totalstring, fontsize=textfontsize, color=framecolour, horizontalalignment=halign, verticalalignment='center')
    
    # Add linup, if applicable
    if data != None:
        for i in range(9):
            player = data['lineup'][i]
            number, name, position = player.split(':')
            yloc = totalyunits - top_margin - (0.5 + i+0.4/2.0)*boxheight
            card.text(x_headers[0], yloc, number, fontsize=textfontsize, color='k', horizontalalignment='center', verticalalignment='center')
            card.text(x_headers[1], yloc, name, fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')
            card.text(x_headers[2], yloc, position, fontsize=textfontsize, color='k', horizontalalignment='center', verticalalignment='center')


def makePitcherStats(card, topbuffer, leftbuffer, boxwidth, data=None):
    
    boxheight = boxwidth * 0.65
    pitchtop = totalyunits - topbuffer - boxwidth*11 # Using width because it is the height of the box score boxes
    
    # Define which of the vertical lines to use
    vertical_booleans = np.array([True, True, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False])
    vertlines = leftbuffer + (vertical_locations[vertical_booleans == True])*boxwidth
    
    heights = np.array([0.5/0.65, 1, 1, 1, 1, 1, 1])*boxheight
    horizlines = np.concatenate([[pitchtop], pitchtop - heights.cumsum()])
    
    # Make seven total rows (eight lines)
    for hl in horizlines:
        card.plot([vertlines[0], vertlines[-1]], [hl, hl], ls='-', lw=solid_linewidth, c=framecolour)
    
    # Make columns
    for vl in vertlines:
        card.plot([vl, vl], [horizlines[0], horizlines[-1]], ls='-', lw=solid_linewidth, c=framecolour)
    
    # Make column header text
    x_headers = vertlines[:-1] + (vertlines[1:] - vertlines[:-1])/2.0
    x_headers[1] = vertlines[1] + (vertlines[2] - vertlines[1])*0.1 # Left align
    y_header = horizlines[0] + (horizlines[1] - horizlines[0])/2.0
    
    cols = ['#', 'Pitching', 'IP', 'BF', 'PC', 'H', 'R', 'ER', 'BB', 'SO', 'W/L']
    for i in range(len(x_headers)):
        colname = cols[i]
        if i == 1:
            halign = 'left'
        else:
            halign = 'center'
        card.text(x_headers[i], y_header, colname, fontsize=textfontsize, color=framecolour, horizontalalignment=halign, verticalalignment='center')
    
    # Add starting pitcher, if applicable
    if data != None:
        number, name = data['pitcher'].split(':')
        yloc = horizlines[1] + (horizlines[2] - horizlines[1])/2.0
        card.text(x_headers[0], yloc, number, fontsize=textfontsize, color='k', horizontalalignment='center', verticalalignment='center')
        card.text(x_headers[1], yloc, name, fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')
    

def makeLineScore(card, topbuffer, leftbuffer, boxwidth, data=None):
    
    boxheight = boxwidth * 0.65
    linetop = totalyunits - topbuffer - boxwidth*11 - boxwidth*5
    
    # Define which of the vertical lines to use
    vertical_booleans = np.array([True, False, False, True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, True])
    vertlines = leftbuffer + (vertical_locations[vertical_booleans == True])*boxwidth
    
    heights = np.array([0.5/0.65, 1, 1])*boxheight
    horizlines = np.concatenate([[linetop], linetop - heights.cumsum()])
    
    # Make horizontal lines
    ## Top one should be shorter
    for i in range(len(horizlines)):
        hl = horizlines[i]
        if i == 0:
            card.plot([vertlines[1], vertlines[-1]], [hl, hl], ls='-', lw=solid_linewidth, c=framecolour)
        else:
            card.plot([vertlines[0], vertlines[-1]], [hl, hl], ls='-', lw=solid_linewidth, c=framecolour)
    
    # Make vertical lines
    ## Again, first one should be shorter
    for i in range(len(vertlines)):
        vl = vertlines[i]
        if i == 0:
            card.plot([vl, vl], [horizlines[1], horizlines[-1]], ls='-', lw=solid_linewidth, c=framecolour)
        else:
            card.plot([vl, vl], [horizlines[0], horizlines[-1]], ls='-', lw=solid_linewidth, c=framecolour)
    
    # Make inning headers
    x_headers = vertlines[1:-1] + (vertlines[2:] - vertlines[1:-1])/2.0
    y_header = horizlines[0] + (horizlines[1] - horizlines[0])/2.0
    
    cols = np.concatenate([range(1,10), ['R', 'H', 'E']])
    for i in range(len(x_headers)):
        colname = cols[i]
        card.text(x_headers[i], y_header, colname, fontsize=textfontsize, color=framecolour, horizontalalignment='center', verticalalignment='center')
    
    # Add team data, if defined
    if data != None:
        card.text(vertlines[0]+boxwidth*0.25, y_header-boxheight, data['away'], fontsize=textfontsize, color='k')
        card.text(vertlines[0]+boxwidth*0.25, y_header-2*boxheight, data['home'], fontsize=textfontsize, color='k')
        
    
# =============================================================================
# Add Game Header
# =============================================================================
def addHeader(card, top_margin, left_margin, boxwidth, team, data=None):
    
    card.text(left_margin, totalyunits - top_margin + 1.25*boxwidth, f'{team} Team (Record):', fontsize=textfontsize, color=framecolour, horizontalalignment='left', verticalalignment='center')
    if data != None:
        
        try:
            region = data['region'].split(' (')[0]
        except IndexError:
            region = data['region']
    
        card.text(left_margin + 2.75*boxwidth, totalyunits - top_margin + 1.25*boxwidth, '{0} {1}   ({2})'.format(region,data['nickname'],data['record']), fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')
    
    card.text(left_margin, totalyunits - top_margin + 0.5*boxwidth, '{0: <55}{1: <35}{2: <35}{3: <35}'.format('Venue:','Date:','Attendance:','Time:'), fontsize=textfontsize, color=framecolour, horizontalalignment='left', verticalalignment='center')
    if data != None:
        card.text(left_margin + boxwidth, totalyunits - top_margin + 0.5*boxwidth, data['venue'], fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')
        card.text(left_margin + 5.3*boxwidth, totalyunits - top_margin + 0.5*boxwidth, data['date'], fontsize=textfontsize, color='k', horizontalalignment='left', verticalalignment='center')
    
