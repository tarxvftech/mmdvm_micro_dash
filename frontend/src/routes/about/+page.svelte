<h1>mmdvm_micro_dash</h1>

<h3>Where</h3>
<p>Visit 
<!--<a target="about:blank" href="https://git.sr.ht/~tarxvf/mmdvm_micro_dash">the repo</a>-->
<a target=_blank href="https://git.mmcginty.me/mike/mmdvm_micro_dash">the mmdvm_micro_dash repo</a>
to read the code and documentation for the project responsible for this page.</p>
<h3>What</h3>
<p>
This micro dashboard is a portion of the 
<a href="https://porkalpine.org" target=_blank >PorkAlpine</a>
project - an 
<a href="https://alpinelinux.org/about/" target=_blank >Alpine Linux</a>
<a href="https://en.wikipedia.org/wiki/Linux_distribution" target=_blank>distribution</a>
for the 
<a href="https://www.raspberrypi.com/products/" target=_blank>raspberry pi</a>
and related packages (for all 
<a href="https://wiki.alpinelinux.org/wiki/Architecture" target=_blank>Alpine-supported architectures</a>
) 
focused on radios and 
Amateur radio
in particular. 
</p>
<p>
This software is a dashboard for `hotspots`, short-range access points for land mobile
radios to work with larger networked radio systems. These hotspots are
almost always built on 
<a href="https://mmdvm.com" target=_blank>MMDVM (Multi-Mode Digital Voice Modem)</a>
software. Thanks to efforts like 
<a href="https://www.pistar.uk/" target=_blank>Pi-Star</a>
and 
<a href="https://w0chp.radio/wpsd/" target=_blank>WPSD</a>
running a hotspot has been very easy - get a modem or radio board, slap
it on a raspberry pi of some sort, write the disk image to an sd card,
plug the card in, apply power, and away you go.
</p>
<p>
These are excellent, but as a Linux user I never felt fully comfortable using them.
</p>
<p>
Which brings us back to PorkAlpine: Instead of specifically building a hotspot disk image, I build my image and packages with the standard tools.
Building packages means standard tools work, and updates are easy. It
also means you can convert normal Alpine Linux to PorkAlpine with almost
no effort - just add the 
<a href="https://porkalpine.org/repos" target=_blank>PorkAlpine package repos </a>
and install the packages like normal. You can run a hotspot or repeater on an x86
machine, an old laptop, or anything to which you can attach a modem and
run Alpine Linux, and then you can attach a modem board with a simple TTL
serial adapter.
</p>
<h3>Why</h3>
<p>
Your Linux experience will be
useful here, and if you don't have much experience with Linux or the
standard tooling, PorkAlpine is a place to learn things that will easily
transfer to other systems.
</p>
<p>
Overall, these projects represent my rebuttal to claims
<!-- 
-->


that the raspberry pi0w is "too slow" for any modern uses. 
</p>
<blockquote><strong>retrieved by tarxvf from <a href="https://w0chp.radio/wpsd/#fn:2" target=_blank>w0chp.radio/wpsd (footnote 2)</a> on Dec 6, 2024</strong><br>
WPSD was not created for single-core and low-powered hardware; such as the first generation RPi Zero, etc. (armv6l). The dashboard will run slowly on under-powered hardware at times. Please consider yourself warned. Also, please ignore all of the hams on various support mediums saying, “anything more than a Pi Zero is overkill”. These ignoramuses have no idea what goes on under the hood in order to display meaningful info on the dashboard. Hint: it’s a lot, and it’s very resource-intensive. Ignore them…they have no idea what they are talking about. ⤴
</blockquote>
<p>
Chip was not writing this footnote about me, but I will chime in now with working code.
</p>
<p>
These systems are hilariously overpowered for the hotspot purpose itself -
and a dashboard need not take much more processor time.
Designing the architecture of the application is important to getting
performance, and Chip is working from a different kind of design where
it really <i>is</i> difficult to do performance - and to do performance
tuning.  He (and pi-star's authors before him) have done incredible
work to advance the state of the hobby, building on foundational work
released for free by people like G4KLX and <i>many</i> others.
</p>
<p>
All this to say that I do *not* say Chip is wrong; for his codebase and
architecture, I believe he is absolutely right. Chip can't simply re-write
his entire codebase, and he can't just drop features back to where it
was performant, but maybe we can yet save the pi0ws from the landfill.
</p>
<p>
(Chip, for his part, sent me several pi0ws with which I developed this
system. (Thank you!))
</p>
<p>
We're not crunching numbers here, and LMR hotspots aren't even moving
megabits back and forth. The web frontend usually only has to handle
one client. This is not exactly a planet-scale multi-tenant cloud on a
kubernetes cluster. My AWS bill is $0 a month and will stay that way. 
</p>
<p>
In short, I believe that these claims that the pi0 is slow are
not calibrated to the scale of compute truly required for the features
provided in a simplex multi-mode radio hotspot. 
</p>
<p>
But rather than argue - and if I successfully did convince my friends,
all I've really done is make more work for them - I figured actions
speak louder than words.
</p>
<p>
This project represents my own interests. It's simple,
lightweight, and powerful for users that want that power. 
It's built with, deployed on, and otherwise supports standardized tooling and
technologies everywhere possible. 
</p>
<p>
You will notice "convenient" is not on that list - it's a thing I value,
but my convenience is not your convenience.  "User-friendly" is similar:
it depends on the user.
</p>
<p>
My idea of convenient and user-friendly is:
</p>
<ul>
    <li>preferring abstraction over boilerplate, and configuration over mandate</li>
    <li>preferring direct access over abstractions when doing so retains power or flexibility</li>
    <li>including sane defaults and example configs</li>
    <li>trusting that you will read documentation (and including links to the relevant docs)</li>
    <li>and not doing anything automatically unless the *user* requests it. </li>
</ul>
<p>
The user is in charge. Software freedom is about the freedom of the user - user agency is paramount.
</p>
<p>

This philosophy is also why
PorkAlpine is built on Alpine Linux - you are provided a set of tools
and a kit of known-good parts, but ultimately the final product is due
to <i>your</i> actions.
</p>
<p>
One final thought on the differences between Pi-Star, WPSD, and PorkAlpine:
Any packaging I do is trivial to repackage for WPSD. This is not
a zero-sum-game. We mutually benefit from sharing our work. That's what open source is about. This is my contribution.
</p>
<p>

Please use this software in good health, be excellent to others and yourself, and have fun.  
</p>
<p style="margin-left: auto; margin-right: auto; width: 100%; border: 1px solid red;text-align:center; display:none;">
don't @ me
</p>

<div style="float:right; margin-bottom: 5em;">
    with love,
    <br>
    tarxvf
</div>
