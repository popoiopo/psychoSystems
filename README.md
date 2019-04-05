# CHATEL
## Complexity HTTP Automated Teammate Experimentation Lab

#### A high level python based website to facilitate conducting qualitative expert interviews regarding a Complex  System problem

This project is meant for making it easier to construct qualitative models from qualitative knowledge through structured interviews and collaborative work. The website guides a researcher in a coherent and incremental process of defining a complex problem by providing a multi-phase structure. This structure first lets the researcher concisely define the problem and work out several variable values concerning the problem statement. These steps can be found in section [Step- by- step conceptualization of your project](#Step-by-step-conceptualization-of-your-project). Eventually the website will require the researcher to answer most of these questions in the dashboard page to configure the rest of the application as these are used throughout the application. 

This README will explain how to configure a VPS (Virtual Private Server) to act as a web server, serve the website and configure its settings (see section [Configuring a Virtual Private Server (VPS)](#Configuring-a-Virtual-Private-Server-(VPS))). As setting up the VPS itself will take about an hour and the costs are 3 euros a month for hosting, a researcher investigating a complex system problem can worry over substantive questions regarding the problem statement instead of dealing with issues of visualization, ways of data gathering and structuring and overall structuring of the experimental layout. This Application is, as the name suggests, a web based tool designed for experimenting with qualitative views of different experts regarding a complex systems problem. For more information about how we applied this methodology to the complex systems problem statement of Major Depression, please read [my Master Thesis](bas_chatel_internship2019.pdf).

# Step by step conceptualization of your project

1. **Define the Problem**
    * Prior to all research it is off course necessary to get a grasp of what the current scope of knowledge is surrounding the problem statement. To achieve this perhaps some kind of **Meta-analysis** can help with these questions:
	  * What don't we know?
      * And maybe more importantly, what can be found in literature (i.e. what do we know)?

    * By providing a web-structure, we force ourselves to structure problems as we write it for a broad audience. Even as its intended target group might not need a step by step introduction of the problem and its importance, it does help to think about what we are actually trying to accomplish. Upon writing the content of the introduction page we define what it is that we don't know, and what it is that we do know. 
 
2. **Defining parameters**
    * What type of factors are we dealing with?
      * Variable, Stock, Constant, etc.
    * At what spatial or temporal scale do these factors exist?
      * Spatial: Biology, Psychological, Interpersonal .. Global etc
      * Temporal: Milliseconds, Seconds, Minutes .. Years, Lifetime etc
    * At what scale do their interactions take place?
 
3. **Interactions**
    * What factors interact with each other?
    * What is the nature of the interaction?
      * If one increases does the other also increase or decrease?
      * How strong are these interactions?
      * How sensitive are the nodes to change?
    * At what point in the process of the problem are the factors and their interactions of importance?
      * Onset, Maintenance, relapse in a disease process
    * Do the interactions need operators?
      * A leads to B but only IF C is also active
      * Operators like: <b>IF, IFF, OR, XOR, AND</b>

4. **Experts**
    * In order to obtain a data set beyond the scope of literature by merging quantitative knowledge found in literature and qualitative knowledge obtained from experts, we need to have expert knowledge representing all fields relating to the problem set. It is important to think about the different perspectives needed to form a complete overview of the problem statement and identify key figures that are linked to the field scientifically, experience based, policy wise etc.
    * For this we need some information of each expert:
      * What is their affiliation with the problem statement? (Experience Expert, Researcher, Policy maker, etc.)
      * In discipline are their working? (Biology, public health, physics, etc.)
      * What is their specialization? (epidemiology, genetics, methodology, social media, etc)
    * Also ask the experts whether they would be open for further feedback moments in unclear situations and whether they want to be named as a participant. As it might affect transparency and reliability of the qualitative data, a default term of conditions would be to state that any participant needs to agree with their name being associated with the expert list.

# Configuring a Virtual Private Server (VPS)

Though this might seem daunting, and perhaps for some technologically challenging, we provide a step by step tutorial of how to configure and publish the website within the hour and for a cost of about 3 euros per month hosting costs (if Hetzner is chosen as VPS host). A VPS was chosen in order to cut budget costs and retain a lot of freedom to personalize, play around and alter anything you want. This tutorial consists of several parts guiding you from start (reading this README!) to finish (a fully functional website).

### Choosing and configuring VPS service
As our web application will attract only few users (mostly being your expert pool) we don't need a lot of RAM, Disk space, CPU etc. For our purposes a 2 GB RAM with 20 GB Disk space, 1 CPU and 20 TB traffic is more than enough. [Greenhost](https://greenhost.net/), [DigitalOcean](https://www.digitalocean.com/) or [Hetzner](https://www.hetzner.com/cloud) for example provide fine VPS services that let you do whatever you want with them for a small price. Out of these three, [Hetzner](https://www.hetzner.com/cloud) is the cheapest with good reviews, so throughout this tutorial we will use this VPS provider. Throughout this tutorial three different notation styles will be used in order to clarify what needs to be typed in where.  Upon talking about buttons that need to be clicked and text outside the Linux terminal it will be presented between "quotations marks". Within the Linux terminal we will continuously use the following box:
```
Code that is in here is meant as a terminal command!
```

#### Creating a VPS
1. At the [Hetzner](https://www.hetzner.com/cloud) website make an account, don't forget to verify via your email.
2. Now that we have an account we first need to create an SSH key in order to be able to safely log in to the server we're about to create.
	1. Upon using a Windows' computer I would recommend using [PUTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). After installing this press the windows button on your keyboard, type **"puttygen"** and press enter. 
	2. When the PUTTY key generator has been opened, press the **"generate"** button and move your mouse around within the PUTTY window. The program uses your mouse movements to generate a random key (as it is very hard to figure out what movements someone made during the creation of this key it is very safe). 
  ![Putty Example](readmeIMG/putty.PNG)
	3. Press the **"Safe private key"** button and safe this somewhere on your computer where you can find it (you'll need this later to log into your VPS!).
	4. Copy the text within the box underneath "Public key for pasting into OpenSSH authorized_keys file:", the text should look a bit like this: 
	
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
3. Now that we have our SSH key and a Hetzner account has been created, go to the Hetzner website, log in, and click on the servers tab. Here click **"ADD SERVER"**.
4. Here we see some choices given to us regarding the configuration of the server. Pick a location, Ubuntu 16.04 and the 3.01/mo payment plan with 1vCPU, 2 GB RAM, 20 GB SSD and 20 TB Traffic. Leave the rest blank, except point 6 where we click on **"Add SSH key" and paste our public SSH key** and 7 in which you can give your server a name. This can be any name, as long as you can remember it.
5. Click create and buy, and you'll have your very own VPS in a matter of seconds!
6. Now that we have our VPS set up, we still need to access and configure it! To do this, we'll need to access the VPS for which we can also use PUTTY, but I personally think it is a bit easier to use winSCP for this as it also provides a folder structure instead of just a terminal. You can download winSCP [here](https://winscp.net/eng/download.php).

#### Accessing the VPS

7. Once winSCP is installed, we can access the new VPS.
	1. Go to your Hetzner server and copy the IP address (if you look at the overview page, you should be able to see your IP address next to IPv4 on top of the page). The IP address looks like 116.203.137.34 but with some different numbers. From now on if I talk about IP address or your_ip_address, this is what I'm talking about.
  ![Hetzner Website example](readmeIMG/Hetzner.PNG)
	2. Press the Windows button and type **"winSCP"** and press enter.
	3. Now that winSCP is opened you should see something like: 
  ![WinSCP example](readmeIMG/winSCP.PNG)
	4. Keep "File protocol" (1) on SFTP, paste your IP address in "Address targetcomputer" (2) , as "Username" (3) type root.
	5. Click on **"Advanced"** (4).
	6. To the left under the SSH tab, you can see **"Authentication"** (5), press here and then you'll be able to browse (click on the button with three dots (6)) to your private key that we saved in step 2.3.
	7. Press **"OK"** (7), then **"Save"** (8) where you can enter a name. I recommend it being called the same as your server name (step 2.4).
	8. Finally, press **"Log in"** (9)  and we can access our VPS! 
	8. As you can see, there are lots of buttons visible and a file structure as you are used to seeing using windows. We will first just use the terminal to do some configurations. Press the **"Open Session in PUTTY"** (10), it's that small button looking like two computers with a lightning strike in between, just to the right of "synchronize".
	10. If all went well, you should be able to see a terminal opening looking like this:
  ![teminal](readmeIMG/CHATELterminal.PNG)
	11. As of this moment, we will work a lot in the terminal which might seem a bit intimidating if you're not used to working with this, but I'll guide you every step of the way so it'll be fine!

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
	1. It asks to install a password validation plugin so users are required to enter strong passwords. Let's answer `y`!
	2. You can choose how picky the validation system is going to be, lets pick the safest so `2`.
	3. It'll prompt you if you want to change your root password by giving its security score. If you are happy with this score type: `n`
	4. Remove anonymous users? `y`
	5. Disallow root login remotely? As we later want to use phpMyAdmin, this is an `n`. 
	6. Remove test database and access to it? As we don't need it, `y`.
	7. Reload privilege tables now? `y`, and that's it!

12. Now that we answered all the questions, we will enable the database to start automatically upon startup of the server by giving the following command:
```
systemctl start mysql
systemctl enable mysql
```
14. Now that MySQL has been installed, we can go ahead with installing PHP by typing the following command:
```
apt-get install php7.0 libapache2-mod-php7.0 php7.0-mysql php7.0-curl php7.0-mbstring php7.0-gd php7.0-xml php7.0-xmlrpc php7.0-intl php7.0-soap php7.0-zip -y
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

and save it by pressing "ctrl+x" then `y` and lastly press "enter" and restart the server:
```
systemctl restart apache2
```
If all went well, you can again go to your IP address in the browser as in step 9, but this time followed by "/info.php". Like so, **http://your_ip_address/info.php** which will show you the following page: 

![Successfull PHP](readmeIMG/php.PNG)

As this file is of no further use to our website, we can safely remove it by typing the following:
```
rm /var/www/html/info.php
```
If you now revisit **http://your_ip_address/info.php**, you'll see that it will return a Not Found error.

14. Now that we've installed the LAMP software, we would like to have a user interface to eventually work with regarding the database. This will make loading some defaults and debugging if a problem occurs easier. For this we will use phpMyAdmin by entering the following command:
```
apt-get install phpmyadmin -y
```
By doing this you will be prompted to select a web server to configure (like in the figure underneath), hit the **"space bar"** to select Apache2 and Enter to confirm and continue (don't forget the space bar to actually select the apache2 option or else it won’t work). On the next screen, select YES to configure a database for phpMyAdmin with dbconfig-common. And finally set your password for phpMyAdmin.

![phpMyAdmin Prompt](readmeIMG/phpMyAdmin.PNG)

15. To check whether installing phpMyAdmin has worked, go to **http://your_ip_address/phpmyadmin** and you should see the following page: 

![Example PHPMyAdmin](readmeIMG/phpMyAdminLogin.PNG)

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
sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
```

18. Then we will download Python itself:
```
cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
```

And extract and compile the downloaded package:

```
sudo tar xzf Python-2.7.12.tgz
cd Python-2.7.12
sudo ./configure --enable-optimizations
sudo make altinstall
```
19. Now that we have Python up and running, we'll want the pip package manager installation software by typing:
```
apt install python-pip -y
```
So far so good! Now that we can install python stuff, lets make a virtual environment in which our website will function (virtual environments are used, so we can kind of have all our code run neatly within a single box instead of it being installed globally). 
```
pip install setuptools
pip install virtualenv
pip install virtualenvwrapper
```
20. Now that we have the necessary libraries to make a virtual environment paste these to lines at the bottom of the basrc file. We can open this file with:
```
sudo nano ~/.bashrc
```
And then scroll down using your down arrow to the bottom of the file and paste in the next two commands:
```
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
```
Then press "ctrl-x", type "y" and enter to safe this file. After the next two commands, every time you open a terminal you can return to the CHATEL project by typing "workon CHATEL".
```
mkvirtualenv CHATEL
deactivate
```
21. You should now see that (CHATEL) is displayed on the left side of your terminal as we are now working in the virtual environment called CHATEL. Now any dependencies within the website we will install inside this virtual environment. Whenever you want to work on the project from within the VPS, you can type **workon CHATEL** and you can access the environment again. So now that we have our virtual environment going we will perform a small magic trick and download all website requirements at once!

```
cd /var/www/html/psychoSystems
sudo apt-get install libmysqlclient-dev -y
sudo apt-get install python-dev -y
pip install wheel
pip install -r requirements.txt
```

22. And we have all our dependencies up and running! Now we can start configuring the flask backbone of the website:
```
export FLASK_CONFIG=production
export FLASK_APP=run.py
```
And set up the database by opening MySQL via the terminal by typing:
```
mysql -u root -p
```
After entering your MySQL password (given during step 10), you now type "show databases;" which gives a list showing all databases that is inside your MySQL database. You can also check this by logging into **http://your_ip_address/phpmyadmin**. 

23. Now we will move creating a database and a user that receives all rights: 

```
CREATE DATABASE psychoSystems;
CREATE USER 'psychoSystems_admin'@'localhost' IDENTIFIED BY  'Psycho1!';
GRANT ALL PRIVILEGES ON psychoSystems . * TO 'psychoSystems_admin'@'localhost';
quit
```
Then link our python environment with the database by the following:
```
export SQLALCHEMY_DATABASE_URI='mysql://psychoSystems_admin:Psycho1!@localhost/psychoSystems'
```
24. Then setup the website database and migrate it to MySQL by:
```
rm -r migrations
flask db init
flask db migrate
flask db upgrade
```
You can check if this worked by logging into **http://your_ip_address/phpmyadmin** where you can see a database called psychoSystems with multiple tables in there.

25. Now that we have our database installed like we need it, we can continue to paste in the default. These defaults can later be changed within the website itself on the dashboard page when logged in as administrator. We do this by clicking on the psychoSystems database (1), then clicking on the SQL tab (2) and pasting the content of the following file:
 [https://raw.githubusercontent.com/popoiopo/psychoSystems/master/instance/db_standards.sql](https://raw.githubusercontent.com/popoiopo/psychoSystems/master/instance/db_standards.sql)
 Now we can run the code by pressing "Go" (3). Afterwards, you can check if it worked by looking in the tables if you'd like.
26. As the database is now filled, and the website is ready to go (yay!) we need to make it visible to the world. In order to accomplish this, we need to tell Apache that it needs to search its root file (beginning of the website) elsewhere (i.e. instead of the index.html we need it to look at our run.py file). This can be accomplished by putting a configuration file as follows: 
```
cd /etc/apache2/sites-available
sudo nano CHATEL.conf
```
And paste the following code within this file:
```
<VirtualHost *:80>
		ServerName 116.203.137.34
		ServerAdmin root@116.203.137.34

		WSGIDaemonProcess CHATEL python-home=/root/Envs/CHATEL
		WSGIProcessGroup CHATEL
	
		WSGIScriptAlias / /var/www/html/psychoSystems/CHATEL.wsgi

		<Directory /var/www/html/psychoSystems/app/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/html/psychoSystems/app/static
		<Directory /var/www/html/psychoSystems/app/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
You can save the file by pressing "ctrl-x" followed by `y` and an "enter". Now that apache is looking at the right files, we still need one last dependency download and a restart:
```
apt-get install libapache2-mod-wsgi
systemctl restart apache2
```
And we are open for business! Please open the website at **"http://your_ip_address"** and enjoy the website! If you'd like a more professional look and have the URL be like a normal website instead of an IP address, you could go to [godaddy.com](https://sso.godaddy.com/login?realm=idp&app=dcc&path=%2fdefault.aspx%3fisc%3dgdbb2228f%26utm_source%3dgdocp%26utm_medium%3demail%26utm_campaign%3dnl-NL_other_email-nonrevenue_base_gd&ISC=gdbb2228f) and buy a domain name. If you have one and are logged in, you can click on your domain name followed by "Manage DNS" and configure it as follows:

![Domain Settings](readmeIMG/domain_name.PNG)




























