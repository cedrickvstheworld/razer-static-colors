# Razer Keyboard Static Colors

## Get it up running

1. install openrazer. Go to this page for more info about openrazer https://openrazer.github.io/ including setup for different linux distributions.
openrazer python3 package will automatically install afterwards
2. clone this repository, cd into the directory and type the following commands:
    ```bash
    $ sudo chmod u+x exec
    ```
3. to run:
    ```bash
    $ ./exec
    ```

## options
(modify the run command on exec file)
map single color:
    ```bash
    $ /usr/bin/python3 ~/$path/razer-static-colors.py --s single --h #76b900
    ```

to map custom colors per key, check out samples on schemes folder and I think you probably would know what to do:
    ```bash
    $ /usr/bin/python3 ~/$path/razer-static-colors.py --s area51
    ```

## notes:
In case some of your keys (it happens on laptops, usually the right most keys) are not colorized. Manually set your Razer keyboard dimensions by editing this file:
/usr/lib/python3/dist-packages/openrazer/client/devices/__init__.py
find this line and set based to your custom razer dimension if not working otherwise leave it as is.
self._matrix_dimensions = (row, col)

You can enable this on startup i many ways (e.g crontab, systemd, rc.local). Thus I am using KDE, I just navigated to system settings > startup and shutdown > and that's it.

The project is open for contributors :D. Email me at cedrickdomingo048@gmail.com if you are interested.