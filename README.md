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

# Day of the picture
Create image at least 85 x 85 in png format and place it under images/special_days folder.
Script will load your picture of the day.

![lib directory contents](/images/special_days/example.png)

The file name should be MMDD.png
If the file for Jan 24, file name should be "0124.png".

# Fonts and images
This project use Roboto font under Apache v2 license.
https://fonts.google.com/specimen/Roboto?query=robo#standard-styles

Example image for Nov 1st(CC0 License)
https://www.svgrepo.com/svg/75632/mountain

Background image
https://www.pexels.com/photo/green-leaf-plant-on-pot-824572/
