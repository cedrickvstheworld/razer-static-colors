# Razer Keyboard Static Colors

1. install openrazer. Go to this page for more info about openrazer https://openrazer.github.io/ including setup for different linux distributions.
openrazer python3 package will automatically install afterwards
2. clone this repository, cd into the directory and type the following commands:
    ```bash
        $ sudo chmod u+x razer-static-colors
    ```
3. add this line to your user's crontab:
    @reboot ./path/to/razer-static-colors
4. reboot your pc  or run main manually
### note:
    In case some of your keys (usually the right most keys) are not colorized. Manually set your Razer keyboard dimensions by editing this file:
    /usr/lib/python3/dist-packages/openrazer/client/devices/__init__.py
    find this line and set based to your custom razer dimension if not working otherwise leave it as is.
    self._matrix_dimensions = (row, col)

