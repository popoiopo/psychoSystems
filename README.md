# CHATEL
## Complexity HTTP Automated Teammate Experimentation Lab

#### A high level python based website meant for conducting qualitative expert interview facilitating a complexity approach

This project is meant for making it easier to construct qualitative models from qualitative knowledge through structured interviews and collaborative work. The website guides a researcher in a coherent and incremental process of defining a complex problem by providing a multi-phase structure. This structure first lets the researcher define the problem in a concise manner and work out several variable values concerning the problem statement. These steps can be found in section [Step- by- step conceptualization of your project](#Step-by-step-conceptualization-of-your-project). The website will require the researcher to answer most of these questions in the dashboard page to configure the rest of the application. 

This README will explain how to configure a VPS (Virtual Private Server) to act as a web server, serve the website and configure its settings. This way, a researcher with a complex system problem can worry over the hard questions regarding the problem statement instead of dealing with issues of visualization and ways of data gathering. For more information, please read [my report](bas_chatel_internship2019.pdf).

# Step by step conceptualization of your project

1. Define the Problem
    * Meta-analysis 
      * What can be found in literature, what do we know?
      * What don't we know

    * By providing the web-structure, we force ourselves to structure problems as we write it for a broad audience. Even as its intended target group might not need a step by step introduction of the problem and its importance, it does help to think about what we are actually trying to accomplish. Upon writing the content of the introduction page we define what it is that we don't know, and what it is that we do know. 
2. Defining parameters
    * What type of factors are we dealing with?
      * Variable, Stock, Constant, etc.
    * At what spatial or temporal scale do these factors exist?
      * Spatial: Biology, Psychological, Interpersonal .. Global etc
      * Temporal: Milliseconds, Seconds, Minutes .. Years, Lifetime etc
    * At what scale do their interactions take place?
3. Interactions
    * What factors interact with each other?
    * What is the nature of the interaction?
      * If one increases does the other also increase or decrease?
      * How strong are these interactions?
      * How sensitive are the nodes to change?
    * At what point in the process of the problem are the factors and their interactions of importance?
      * Onset, Maintenance, relapse in a disease process
    * Do the interactions need operators?
      * A leads to B but only IF C is also active
      * IF, OR, XOR, AND
4. Experts
    * In order to obtain a data set beyond the scope of literature by merging quantitative knowledge found in literature and qualitative knowledge obtained from experts, we need to have expert knowledge representing all fields relating to the problem set. It is important to think about the different perspectives needed to form a complete overview of the problem statement and identify key figures that are linked to the field scientifically, experience based, policy wise etc.
    * For this we need some information of each expert:
      * What is their affiliation with the problem statement? (Experience Expert, Researcher, Policy maker, etc.)
      * In discipline are their working? (Biology, public health, physics, etc.)
      * What is their specialization? (epidemiology, genetics, methodology, social media, etc)
    * Also ask the experts whether they would be open for further feedback moments in unclear situations and whether they want to be named as a participant. As it might affect transparency and reliability of the qualitative data, a default term of conditions would be to state that any participant needs to agree with their name being associated with the expert list.

# Configuring a Virtual Private Server (VPS)

Though this might seem daunting, and perhaps for some technologically challenging, we provide a step by step tutorial of how to configure and publish the website. A VPS was chosen in order to cut budget costs and retain a lot of freedom to play around and alter anything you want.

### Choosing and configuring VPS service
As our web application will attract only few users (namely being your expert pool) we don't need a lot of RAM, Disk space, CPU etc. For our purposes a 2 GB RAM with 20 GB Disk space, 1 CPU and 20 TB traffic is more than enough. [Greenhost](https://greenhost.net/), [DigitalOcean](https://www.digitalocean.com/) or [Hetzner](https://www.hetzner.com/cloud) for example provide fine VPS services that let you do whatever you want with them for a small price. Out of these three, [Hetzner](https://www.hetzner.com/cloud) is the cheapest, so throughout this tutorial we will use this VPS provider.

#### Creating a VPS
1. At the Hetzner website make an account, don't forget to verify via your email.
2. Now that we have an account we first need to create an SSH key in order to be able to safely log in to the server we're about to create.
	1. Upon using a Windows' computer I would recommend using [PUTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). After installing this press the windows button and type "puttygen" and press enter. 
	2. When the PUTTY key generator has been opened, press the "generate" button and move your mouse around within the PUTTY window. The program uses your mouse movements to generate a random key (as it is very hard to figure out what movements someone made during the creation of this key it is very safe). *PICTURE*
	3. Press the "Safe private key" button and safe this somewhere on your computer where you can find it (you'll need this later to log into your VPS!).
	4. Copy the text within the box underneath "Public key for pasting into OpenSSH authorized_keys file:", the text should look a bit like this: *PICTURE*
	
    ```
      ssh-rsa
      AAAAB3NzaC1yc2EAAAABJQAAAQEAiFSzrOGXlpxdhDinznQyha5
      IZJ1DjtKGVu/woBnYw+OK0EzSj3pmmld233hetCekqCCGPpLG4X
      /rdy1e2shPXlBjvAzb8seMoF+YU+tVWtVfjm/kUQyu5WFRBNf5x
      NReFFfmko064OavJZmXARFTMQkZRqUnOhrkhK+brubModRyQn6g
      vpewDLfORcgyPCC4SNmFCyI9c3Dvfvs1rcdqy673COc81lwpIgC
      k4lEByZLJ0Cx20e5gCerm/KoM0M8opeKmd9mnRbArXaTmSe4zE7
      5AoDtvZiVtVyXeXlnnsKbthTQdN0ETO3Q2hiJJU/Pxr2FQn1FmA
      qQGZ919bu8fOw
      == rsa-key-20190330
    ```
3. Now that we have our SSH key and a Hetzner account has been created, go to the Hetzner website, log in, and click on the servers tab. Here click "ADD SERVER".
4. Here we see some choices given to us regarding the configuration of the server. Pick a location, Ubuntu 16.04 and the 3.01/mo payment plan with 1vCPU, 2 GB RAM, 20 GB SSD and 20 TB Traffic. Leave the rest blank, except point 6 where we click on **"Add SSH key" and paste our public SSH key** and 7 in which you can give your server a name. This can be any name, as long as you can remember it.
5. Click create and buy, and you'll have your very own VPS in a matter of seconds!
6. Now that we have our VPS set up, we still need to access and configure it! To do this, we'll need to access the VPS for which we can also use PUTTY, but I personally think it is a bit easier to use winSCP for this as it also provides a folder structure instead of just a terminal. You can download winSCP [here](https://winscp.net/eng/download.php).

#### Accessing the VPS
7. Once winSCP is installed, we can access the new VPS.
	1. Go to your Hetzner server and copy the IP address (if you look at the overview page, you should be able to see you IP address next to IPv4 on top of the page). **PICTURE**
	2. Press the Windows button and type "winSCP" and press enter.
	3. Now that winSCP is opened you should see something like: **PICTURE**
	4. Keep "File protocol"(1) on SFTP, paste your IP address in "Address targetcomputer" (2) , as "Username" (3) type root.
	5. Click on "Advanced" (4).
	6. To the left under the SSH tab, you can see "Authentication" (5), press here and then you'll be able to browse (click on the button with three dots (6)) to your private key that we saved in step 2.3.
	7. Press "OK" (7), then "Save" (8) where you can enter a name. I recommend it being called the same as your server name (step 2.4).
	8. Finally, press "Log in" (9)  and we can access our VPS! 
	9. As you can see, there are lots of buttons visible and a file structure as you are used to seeing using windows. We will first just use the terminal to do some configurations. Press the "Open Session in PUTTY" (10), its that small button looking like two computers with a lightning strike in between, just to the right of "synchronize".
	10. If all went well, you should be able to see a terminal opening looking like this: **PICTURE** 
	11. As of this moment, we will work a lot in the terminal which might seem a bit intimidating if you're not used to working with this, but I'll guide you every step of the way!

#### Configuring your VPS as a webserver

To be able to host your own web server, we need to install some things to be able to make your VPS visible to the internet, and therefore your experts and other people! We're about to install LAMP, which is an abbreviation for [Linux](https://en.wikipedia.org/wiki/Linux "Linux")  [operating system](https://en.wikipedia.org/wiki/Operating_system "Operating system"), the [Apache HTTP Server](https://en.wikipedia.org/wiki/Apache_HTTP_Server "Apache HTTP Server"), the [MySQL](https://en.wikipedia.org/wiki/MySQL "MySQL")  [relational database management system](https://en.wikipedia.org/wiki/Relational_database_management_system "Relational database management system") (RDBMS), and the [PHP](https://en.wikipedia.org/wiki/PHP "PHP")  [programming language](https://en.wikipedia.org/wiki/Programming_language "Programming language").   For this part I will follow another tutorial which you can find [here]([https://www.rosehosting.com/blog/how-to-install-wordpress-with-lamp-stack-on-ubuntu-16-04/](https://www.rosehosting.com/blog/how-to-install-wordpress-with-lamp-stack-on-ubuntu-16-04/)) but for our purposes it will be tweaked here and there as we don't need WordPress.

8. First we need to make sure that our server is up-to-date by running the following commands:
```
apt-get update && apt-get upgrade -y
```
9. Now that our server is up-to-date, we'll move on by installing Apache2 which is one of the most popular and widely used web servers as it is both fast and secure. Run the following command:
```
apt-get install apache2 -y
systemctl start apache2
systemctl enable apache2
``` 
To check whether this has worked, you can go open your web browser and enter your server IP address (same one as in step 7.1!). If Apache has successfully been installed, you should see the default Apache welcome page.

10. After Apache, we come to the next letter in the LAMP abbreviation, the M that stands for MySQL Database server. Here we will eventually store all information regarding the website, our factors, relations, expert profiles and even the contents of the website itself! To install MySQL type the following command:
```
apt-get install mysql-server -y
```
During the installation you will be prompted to enter a password for the MySQL root user (which is you!), so make sure it's a strong password nobody else could guess, press enter and re-enter the same password.

11. For security reasons lets configure the MySQL database by typing the following:
```
mysql_secure_installation
```
Now the program will ask your password again, following some other questions.
	1. It asks to install a password validation plugin so users are required to enter strong passwords. Let's answer yes!
	2. You can choose how picky the validation system is going to be, lets pick the safest so two.
	3. It'll prompt you if you want to change your root password by giving its security score.
	4. Remove anonymous users? Yes
	5. Disallow root login remotely? No
	6. Remove test database and access to it? As we don't need it, Yes.
	7. Reload privilege tables now? Yes, and that's it!

12. Now that we answered all the questions, we will enable the database to start automatically upon startup of the server by giving the following command:
```
systemctl start mysql
systemctl enable mysql
```
13. Now that MySQL has been installed, we can go ahead with installing PHP by typing the following command:
```
apt-get install php7.0 libapache2-mod-php7.0 php7.0-mysql php7.0-curl php7.0-mbstring php7.0-gd php7.0-xml php7.0-xmlrpc php7.0-intl php7.0-soap php7.0-zip
```
To test if PHP has been installed successfully we can create a file with the nano text editor:

```
nano /var/www/html/info.php
```
Enter the following content inside the file: 
```
<?php
phpinfo();
?>
```

and save it by pressing "ctrl+x" then "y" and lastly press "enter" and restart the server:
```
systemctl restart apache2
```
If all went well, you can again go to your IP address in the browser as in step 9, but this time followed by "/info.php". Like so, **http://your_ip_address/info.php** which will show you the following page: **PICTURE**

As this file is of no further use to our website, we can safely remove it by typing the following:
```
rm /var/www/html/info.php
```
If you now revisit **http://your_ip_address/info.php**, you'll see that it will return a Not Found error.

14. Now that we've installed the LAMP software, we would like to have some user interface to eventually work with regarding the database. This will make loading some defaults and debugging if a problem occurs easier. For this we will use phpMyAdmin by entering the following command:
```
apt-get install phpmyadmin
```
By doing this you will be prompted to select a web server to configure, hit the **space bar** to select Apache2 and Enter to confirm and continue (don't forget the space bar to actually select the apache2 option or else it won’t work). On the next screen, select YES to configure a database for phpMyAdmin with dbconfig-common. And finally set your password for phpMyAdmin.

15. To check whether installing phpMyAdmin has worked, go to **http://your_ip_address/phpmyadmin** and you should see the following page: **FIGURE**

Your Username is "root", and the password is the password you've set in the previous step.

#### Bringing in the website!

16. Now that we've downloaded pretty much all the essentials for running a web server, it's time to download the actual website onto the server. We are going to do this by cloning the CHATEL git repository to the file that Apache2 looks to for its website. This can be done by entering the following into the terminal:

```
cd /var/www/html
git clone https://github.com/popoiopo/psychoSystems.git
```
If you now type in "ls" than you should see an "index.html" and the psychoSystems folder.

17. Next we will download Python onto the server as the backbone of the website is written with the Python Flask library. For this we first need to install all required dependencies:
```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Then we will download Python itself:
```
cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz
```

And extract and compile the downloaded package,:

```
sudo tar xzf Python-2.7.15.tgz
cd Python-2.7.15
sudo ./configure --enable-optimizations
sudo make altinstall
```
Now that we have Python up and running, we'll want the pip package installation software by typing:
```
apt install python-pip
```
So far so good! Now that we can install python stuff, lets make a virtual environment in which our website will function (virtual environments are used so we can kind of have all our code run neatly within a single box instead of it being installed globally). 
```
pip install setuptools
pip install virtualenv
pip install virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv CHATEL
workon CHATEL
```
You should now see that (CHATEL) is displayed on the left side of your terminal as we are now working in the virtual environment called CHATEL. Now any dependencies within the website we will install inside this virtual environment. Whenever you want to work on the project from within the VPS, you can type **workon CHATEL** and you can access the environment again. So now that we have our virtual environment going we will perform a small magic trick and download all website requirements at once!

```
cd /var/www/html/psychoSystems
pip install -r requirements.txt
```

































