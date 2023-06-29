## Running

The main script in the module is `buildScorecard.py` and this is what
you will call to create a new blank scorecard.

`buildScorecard` can be run either with or without a game file passed
as an argument. If it is run by itself (ie, `$ python
buildScorecard.py` it will produce a totally blank template simply
called `scorecard.pdf`.

If a game file is given as an argument, it will create a .pdf with the
same name as the .txt file given. Eg, if you call
`$ python buildScorecard.py sample1`
it will read in the `sample1.txt` game file and produce a scorecard
called `sample1.pdf`.

### Game files

The syntax for the game files is very precise and unfortunately there
is not a lot of error handling yet. (I plan to build some in!) But
there are two sample files to use as templates.

The first two lines of the game file are general game information,
line 1 is the date and line 2 is the venue. These will go into the
appropriate areas on the scorecard and it's just string
printing---whatever goes in will be put in those spots.

All the remaining lines give information on the teams and the two
teams are separated by the string `' v '`. The spaces are important!
The home team is listed first (as games are supposed to be),
but I might switch it at some point to better align with how baseball
games are usually listed.

Lines 3 and 4 seem kind of redundant, with the first one specifying
the team region and the second one the team nickname. The reason they
are separate is that the line score just uses the region name, whereas
the header uses the full region + nickname. There's not a good regex
(that I can think of)
to split them, since regions and nicknames can both be arbitrary
numbers of words.

Line 5 is the team records, which I like to have printed after the
team names to provide some context. The code will automatically print
some brackets to surround this, but anything can go here.

The `sample2.txt` game file also gives an example of how to add a note
to the region name that will not appear in the full name. Simply
describing a team as 'New York' is obviously degenerate, so there is
the option to add an '(N)' (or '(M)', if you prefer) to break the
degeneracy in a way that does not show up in the full team
name. Anything in brackets will only appear in the line score, not the
header.

In a future version, I want to add an option for the user to select if
they want just the region name (as I do), just the nickname, or the
full name for the line score. But we're not there yet!

After a blank line (the blank line is important) the next nine lines
are the starting lineups for both teams. As with the team names, the
lineup spots for the two teams are separated by the ` v `
string. For each team, the batter's number, name (either last or full,
I prefer last, but there's plenty of room for either) and position are
separated by colons. Again, see the sample files for examples, but
note that even if you want to leave one part of the line blank, you
still need to include the colons so the code knows how to break up the
blanks. This is another aspect that really boils down to lack of error
handling, something that I'd like to fix in this or a future
offseason.

After another (important) blank line, the starting pitchers are
listed. In both of the sample files, this is a little redundant, as
the pitchers are both in the starting lineup. (Take a moment to savour
having the pitcher in the lineup.) But to accomodate the DH rule, it's
necessary to have a separate line for the pitching stats rather than
use string matching to identify the pitcher in the lineup.

All of this seems straightforward enough, but without any sort of
error handling it can be very finicky and has tripped me up a few
times. The important things are to make sure that even if a section
should be blank, it is still listed in the game file as though it were
not blank. There are several times I've only put in the date, venue
and teams, then several lines of `:: v ::` to make sure the code
doesn't throw an error.

