Installation
------------

1. Install and configure the CasparCG server; wire it up to your mixer.

   NOTE: CasparCG server version 2.1.0beta2 is required. This is because
   we use JSON format data, which doesn't work properly in 2.0.7.

   Before continuing, be sure it is working correctly - double check
   the output resolution, frame rate and interlacing.

2. Copy the 'mediary' template directory into the template directory
   in your CasparCG server.

3. Install Python 2.7 and wxPython 3.0 on the system which is to run the
   client.
   - On Windows, see README.Windows.txt.
   - On Linux, these can usually be found pre-packaged.  On Ubuntu and Debian
     systems, 'apt-get install python-wxgtk3.0' will likely do the trick.


Launching the client
--------------------

To run the client, run the appropriate Python script for what you want to do
(list below).

This is much easier if you have set up file associations to run .py files
with Python, as it means you can just double click.

Alternatively, you can set up desktop shortcuts (etc.) to run "python
basketball.py".

    generic.py      The generic 'kitchen sink' client which can do
                    everything. (You can switch widgets on or off via the
                    configuration dialog.)

    scorebug.py     Just the team scoring panel with generic +1/-1
                    buttons. See 'Sports scores' below for details.
    history.py      A derivative of the score bug, showing a 'main' score
                    and up to five 'past' scores. This is for sports
                    which keep score at two levels.

    basketball.py   For basketball. Team scores, +1/+2/+3 actions,
                    along with the timer and other useful widgets.
    bowls.py        Lawn bowls. This is the History widget, set up to show
                    a main score (number of sets) and one extra (current
                    set score). You might want to show the current
                    Set and End numbers in the Extra widget.
    rugby.py        The score widget with one-touch buttons for Try,
                    Converted try, Penalty, Drop goal. Also includes
                    timer and other widgets.

    lowerthird.py   Just simple lower thirds.


Understanding the client
------------------------

The client interface contains a number of indepenedent widgets.
The same widget may appear in multiple clients.

Each widget has its own configuration (template to use, Caspar CG layer,
whether it is Visible in the generic client, and other items as necessary).
Press the Configuration button to open up the config panel.

The configuration, and the last team colours set by each widget, are written
out to a file config.ini.


Operation
---------

Each widget has the following controls:
    'TAKE' causes the template to animate on.
    'ANIM OFF' animates the template off.
    'CUT OFF' cuts the template offline immediately.
    'UPDATE' sends updated data to the template (for example, to fix a name,
    or if you have typed in an updated score).

There is also a single global 'ALL GFX OFF' button. As the name suggests, this
kills the entire graphics channel with one click.

The bottom bar of the client window shows the status.  Most of the time this
reports on commands sent and any errors returned by the server.

If the network connection to the server is interrupted, the client may appear
to hang for a few seconds, then report a timeout in the status bar.

The 'Ping server' button can be used to test that the server connection is
alive and well. It reports to the status bar.


Special characters
------------------

Text fields are interpreted by the server as HTML. This means you can use
special characters, or the standard HTML entity codes for those characters.

You can use any HTML character - fractions, macrons, other accents, even
characters from other writing systems and emoji if the font supports it.

For example:
            &frac12;    The one-half fraction (½)
            &amacr;     Lower-case 'a' with macron (ā)
            &Amacr;     Capital 'a' with macron (Ā)
            &eacute;    Lower-case 'e' with acute accent (é)
            &#9835;     Musical notes symbol (♫)

For a list of HTML entity codes, refer to
https://www.w3schools.com/charsets/ref_utf_latin1_supplement.asp
(other extended character sets are listed in the sidebar).
You need to enter the code from the 'Entity' column.

BEWARE: There is no preview function!
Be sure to test out any special characters before show time, or with
graphics off-line.
If a font doesn't support a character, it will usually appear as a box.


Sports scores
-------------

These widgets have two template configurations - one for the score bug, one
for the banner. The drop-down between the team names selects which to take to
screen.

NOTE: the selection of Bug or Banner only has an effect when you
press Take. In other words, to switch from one to the other, you have to
press Take (or, if you prefer, Anim Off then Take).

We recommend setting the team name text and background colours to match their
respective uniforms.

The 'Extra' box is for additional information to go with the scores and timer.
Some sports will find this useful to report the number of the current period
or round.

The convenience buttons (+1, TRY, etc.) are 'one-click operation'. They
automatically send changes to the server; there is no need to press Update.


Rugby configuration
-------------------

Select the code (Union or League) in the configuration.

Should you need to change the points scores for the convenience buttons,
you can find these in rugby.py - look for ScoresByCode near the top.
You will need to close and reopen the client for the change to take effect.
(Beware, the client does not remember the score if you close and relaunch it!)


Countdown timer configuration
-----------------------------

The countdown starts immediately after it has animated on.

You can enter the time in MM:SS or HH:MM:SS format.

Counter direction (up/down) is set in the configuration.

If 'Clear on zero' is ticked, and the counter is counting down,
the counter will automatically animate off when it reaches zero.


Editing the client
------------------

The client is written in Python.

After making any changes you must close and reopen the client for them to take
effect.

If you find any bugs we'd appreciate a note.
Even better, if you fix any bugs we'd love to receive a patch!

You are welcome to create your own clients. The existing clients use the
Python inheritance mechanism to reuse code.  Basketball is a good example of a
simple customisation of the generic scores widget; rugby is a little more
complex.


Editing templates
-----------------

Any changes made in the live directory on the server take effect the next
time that template is taken to line. Pressing Update does _not_ reload it!


Editing the countdown timer
---------------------------

This template (mediary/timer) is quite complicated.
Don't try to edit it in place - it's compiled.
Instead, get the source code from
https://github.com/crazyscot/casparcg-countdown-timer

It has its own README.
Copy the compiled output from casparcg_output to templates/mediary/timer in
your CasparCG server directory.
