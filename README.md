
This is my Shed Server Science Preject
hows spose to do alot of things 

this program offer a web ui for accessing the shed server API

Website includes
    The Shed Video Game DATABase 
        including an SQLlite for the catolog of games and there locations
        and the NAS with all the games

    Playerbase
        including member of the shed and there corrsponding stats
        and SHED COINS the shed crypto currency which is tied to the blockchain
        infact the entire playbase is writen to the shed blockchaion so no adommies can tammer with the results
    
    Consoles,
        detail describion of my consoles and controllers as well as the games that i have for that console 

    SHEDS radio
        a 24/7 webstream of the hickeys shed offical soundtrack that in theoy can be played from anywhere just like a radio station

    Shed media player, 
    my jellyfin server

    Shed weather station
        to send weather updates from the shed to discord and my phone with higher accuracy then eddie sheer

    qbittorent webui

    download files from the shed library using the shed API

i have built this program entirely in python for ease of development

flask for displaying the data on a webpage 
positioned in a docker container that will in thoery work
on all mac os windows and ubuntu, being developed now on macos and send to run in the cloud or shed server


docker run -p 5045:5045 shedapp
