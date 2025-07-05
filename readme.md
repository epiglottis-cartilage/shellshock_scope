# ShellShock Live Trainer
A simple (non intrusive) trainer for [ShellShock Live](http://www.shellshocklive.com)

**The project is only for exercise purposes and should not be used for cheating.**

# Usage

0. Find out scale on your screen:
   1. Run `./record.py` and game.
   2. Start a `firing range` in **Maximize Window / Full Screen** mode (that is at width as your screen) and shoot at **speed 100 angle 45**. 
   3. Put your mouse on the center of your tank and press `\`.
   4. Key `\` where your bullet pass through for as many times as you want.
   5. Key `q` to end recording.
   6. run `./curve_fit.py` and get the scale.
1. Execute the trainer (installation see below).
2. Start "Shellshock Live" (the trainer automatically detects a running instance of "Shellshock Live").
3. There are four hardcoded keys
    * Key `[` where are you
    * Key `\` where is the `x2` bounds or anything you want your bullet pass through (optional)
    * Key `]` where are your enemies
    * No more
