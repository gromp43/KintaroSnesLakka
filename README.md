### NO LONGER SUPPORTED ###

Im not working for Kintaro. This software is maintained in my freetime. So please help me out when you find problems and open pull requests

## Installing on Lakka raspberry pi image

I'm not fluent in linux so there is probably a better way to do this, but I enabled ssh from lakka's Settings>Services menu
Then went to the Main Menu>Information>Network Information to find the IP address assigned to my pi
I then ssh'd into the pi using putty default user/pass is root/root

Once ssh'd in you should be at the default $HOME directory of /storage if not then type cd /storage

then type mkdir kintaro

1. then touch kintaro-service

2. then nano kintaro-service

3. and copy/paste the code.  ctrl+x to exit, Y to save, then enter.

4. type chmod +x ./kintaro-service 

repeat those 4 commands for pcb.py

type cp kintaro-service /storage/.config/system.d/

then finally sysctl enable kintaro-service

## Authors

* **Michael Kirsch** - *Initial work*

See also the list of [contributors](https://github.com/michaelkirsch/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

