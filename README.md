# inky-calendar
Calendar on PIMORONI's inky impression ePaper display.

![lib directory contents](/images/sample.jpg)

You can get it from here.
https://shop.pimoroni.com/products/inky-impression

# Installation
1.Run this command to install libs provided by Pimoroni.

```bash
curl https://get.pimoroni.com/inky | bash
```

2.Clone this repo on your Raspberry Pi.

```bash
git clone https://github.com/kotamorishi/inky-calendar
```

3.Run the script
```bash
cd inky-calendar
python3 inky-calendar.py
```

# Background image
Program automatically load ```images/background.jpg``` for the background.
if you wish to change, update the image.

# Day of the picture
Create image at least 85 x 85 in png format and place it under ```images/special_days``` folder.
Script will load your picture of the day.

![lib directory contents](/images/special_days/example.png)

### Every month of the day.
For every month 1st day, file name should be "01.png"(DD)

### Specific month of the day.
For Jan 24, file name should be "0124.png".(MMDD)

### Specific year and month of the day.
For Jan 1st, 2022, file name should be "20220101.png"(YYYYMMDD)

# Fonts and images
This project use Roboto font under Apache v2 license.
https://fonts.google.com/specimen/Roboto?query=robo#standard-styles

Example image for Nov 1st(CC0 License)
https://www.svgrepo.com/svg/75632/mountain
Also most of ```special_days``` images too.

Background image
https://www.pexels.com/photo/green-leaf-plant-on-pot-824572/
