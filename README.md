Mediary's Caspar Client
=======================

## About

This is a lightweight broadcast graphics package for the [CasparCG](http://casparcg.com/) playout engine. It was created with live sports in mind but could be useful in many situations as a low cost option to create on-screen graphics in real time.

If you like this and find it useful, please consider buying me a coffee - hit the Sponsor button at the top of the page.

If you need support or customisations, get in touch with my company [Mediary](https://mediary.nz/) to discuss a commercial engagement.

**NOTE:** Experimental Python3 support is present on the [python3 branch](https://github.com/crazyscot/casparcg-client/tree/python3).

### Features

* Generic lower thirds - one line, two lines, and extended two line banner
* Score bug covers most sports
    - Operator-controlled team colours
    - Optional field for extra information (period number, stoppage, etc.)
    - Customised control panels for **rugby** _(both league and union)_ and **basketball**
    - Ability to generate a lower third from the current score data
* Score bug "with history", for sports with two levels of scoring
    - Customised panel for **lawn bowls**
* On-screen clock
    - Count-up and count-down modes
* Highly customisable, can be extended to other sports


[![Demo video (YouTube)](http://img.youtube.com/vi/JVwmA_sfuOE/0.jpg)](https://www.youtube.com/watch?v=JVwmA_sfuOE "Demo video (YouTube)")

## Installation

1. Install and configure the CasparCG server.  
   **NOTE:** CasparCG server version 2.1.0beta2 is required. This is because
we use JSON format data, which doesn't work properly in 2.0.7.
1. Wire the server up to your mixer in whatever way makes sense for your systems.  
   Before continuing, be sure it is working correctly - double check the output resolution, frame rate and interlacing.
1. Copy the `mediary` template directory into `CasparCG Server\template` .
1. On the system which is to run the client, install Python 2.7 and wxPython 3.0.

### Software prerequisites for the client

**NOTE:** Experimental Python3 support is present on the [python3 branch](https://github.com/crazyscot/casparcg-client/tree/python3).

**Python 2.7**

<https://www.python.org/downloads/release/python-2714/>

Look for "Windows x86 or Windows x86-64 MSI installer".

  When installing, you probably want to enable the option to associate 
  `.py` files with Python. That makes it much easier to launch the client:
  you can double click, easily set up a shortcut, etc.

**wxPython**

<https://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/>

Look for one of:

  - wxPython3.0-win**32**-3.0.2.0-py27.exe
  - wxPython3.0-win**64**-3.0.2.0-py27.exe

If you're running 64-bit windows, you can install either the 32-bit or 64-bit
versions of Python and wxPython BUT you must use the same for both packages.

**On Linux, these can usually be found pre-packaged.**  On Ubuntu and Debian systems, `apt-get install python-wxgtk3.0` will likely do the trick.

---

## Launching the client

The client is actually a collection of related Python scripts. Just run the appropriate one (list below).

This is much easier if you have set up file associations to open `.py` files
with Python, as it means you can just double click. Alternatively, you can set up desktop shortcuts to run the clients, e.g. `python basketball.py`

This is the current list of clients:

* generic.py  
  The generic 'kitchen sink' client which can do everything. (You can switch widgets on or off via the configuration dialog.)

* scorebug.py  
Just the team scoring panel with generic +1/-1 buttons. See 'Sports scores' below for details.

* history.py  
A derivative of the score bug, showing a 'main' score and up to five 'past' scores. This is for sports which keep score at two levels. See _bowls.py_ for a more concrete example.


* basketball.py  
For basketball. Team scores, +1/+2/+3 actions, along with the timer and other useful widgets.

* bowls.py  
Lawn bowls. This is the History widget, set up to show a main score (number of sets) and one extra (current set score). You might want to show the current Set and End numbers in the Extra widget.

* rugby.py  
The score widget with one-touch buttons for Try, Converted try, Penalty, Drop goal. Also includes timer and other widgets.

* lowerthird.py  
Just simple lower thirds.

---

## Understanding the client

The client interface contains a number of independent widgets.
The same widget may appear in multiple clients.

Each widget has its own configuration (template to use, CasparCG layer,
whether it is Visible in the generic client, and other items as necessary).
Press the Configuration button to open up the config panel.

The configuration, and the last team colours set by each widget, are written
out to a file `config.ini`


### Operation

Each widget has the following controls:

*    **TAKE** causes the template to animate on.
*    **ANIM OFF** animates the template off.
*    **CUT OFF** cuts the template offline immediately.
*    **UPDATE** sends updated data to the template (for example, to fix a name,
    or if you have typed in an updated score).

There is also a single global **ALL GFX OFF** button. As the name suggests, this
kills the entire graphics channel with one click.

The bottom bar of the client window shows the status of the last command sent.  Most of the time this
reports on commands sent and any errors returned by the server.

If the network connection to the server is interrupted, the client may appear
to hang for a few seconds, then report a timeout in the status bar.

The **Ping server** button can be used to test that the server connection is
alive and well. It reports to the status bar.


### Special characters

Text fields are interpreted by the server as HTML. This means you can use
special characters, or the standard HTML entity codes for those characters.

You can use any HTML character - fractions (&frac12;), macrons (&amacr; &Amacr;), other accents (&eacute; &ccedil; &agrave;), symbols (&#9835), even characters from other writing systems and emoji if the font supports it.

For a list of HTML entity codes, refer to
<https://www.w3schools.com/charsets/ref_utf_latin1_supplement.asp>
(other extended character sets are listed in the sidebar).
You need to enter the code from the 'Entity' column for the symbol you want.

**BEWARE:** There is no preview function!
Be sure to test out any special characters before show time, or with
graphics off-line.
If a font doesn't support a character, it will usually appear as a box.

---

## Sports scores

These widgets have two template configurations - one for the score bug, one
for the banner. The drop-down between the team names selects which to take to
screen.

**NOTE:** the selection of Bug or Banner only has an effect when you
press Take. In other words, to switch from one to the other, you have to
press Take (or, if you prefer, Anim Off then Take).

We recommend setting the team name text and background colours to match their
respective uniforms.

The 'Extra' box is for additional information to go with the scores and timer.
Some sports will find this useful to report the number of the current period
or round.

The convenience buttons (+1, TRY, etc.) are 'one-click operation'. They
automatically send changes to the server; there is no need to press Update.


### Rugby configuration

Select the code (Union or League) in the configuration.

Should you need to change the points scores for the convenience buttons,
you can find these in rugby.py - look for ScoresByCode near the top.
You will need to close and reopen the client for the change to take effect.
(Beware, the client does not remember the score if you close and relaunch it!)


### Countdown timer configuration

The countdown starts immediately after it has animated on.

You can enter the time in MM:SS or HH:MM:SS format.

Counter direction (up/down) is set in the configuration.

If 'Clear on zero' is ticked, and the counter is counting down,
the counter will automatically animate off when it reaches zero.


---

## Editing the client

The client is written in Python.

After making any changes to the code, you must close and reopen the client for them to take
effect.

If you find any bugs we'd appreciate a note. Please raise an issue via <https://github.com/crazyscot/casparcg-client/issues>.

Even better, if you fix any bugs we'd love to receive a patch or a pull request!

You are welcome to create your own clients. The existing clients use the
Python inheritance mechanism to reuse code.  Basketball is a good example of a
simple customisation of the generic scores widget; rugby is a little more
complex.


### Editing templates

Any changes made in the live directory on the server take effect the next
time that template is taken to line. Pressing Update does _not_ reload it!


### Editing the countdown timer

This template (mediary/timer) is quite complicated.
Don't try to edit it in place - it's compiled.
Instead, get the source code from
<https://github.com/crazyscot/casparcg-countdown-timer>

It has its own README.
Copy the compiled output from `casparcg_output` to `templates/mediary/timer` in
your CasparCG server directory.
