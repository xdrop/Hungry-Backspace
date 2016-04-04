Hungry Backspace for Sublime Text
------------------------------------

### Overview

This small plugin brings to Sublime Text the "hungry backspace" feature from IntelliJ. The hungry backspace retains the scope (indentation) when the backspace key is pressed on an empty line. 

### Live demo

![](http://i.imgur.com/Ayw6jgA.gif)

### Warning

This plugin is **NOT** meant to replace backspace entirely, it is meant to be used in conjunction with the original backspace function which is now accessed by **Shift+Backspace**

### Version

1.0.0

### Installation


1. Having installed [Package Control](https://packagecontrol.io/installation) access the `Command Pallete` (`Ctrl+Shift+P`), select `Install package` and then select `Java Bytecode`.

2. Try it by pressing backspace on some empty lines!

3. You can change the key bindings by going to `Preferences` then `Package Settings` then `Hungry Backspace`, and select they keymap option

### Key bindings
By default this plugin overrides your backspace with the "hungry" one however, as mentioned previously the plugin is meant to be used in conjunction with the default backspace which is now accessible via `SHIFT+BACKSPACE`

```
[
  // the hungry backspace
  { "keys": ["backspace"], "command": "hungry_backspace" },
  // the default backspace
  { "keys": ["shift+backspace"], "command": "left_delete"}
]
```


### License

Copyright (c) 2016 xdrop


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

