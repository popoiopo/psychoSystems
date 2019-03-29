# CHATEL
## Complexity HTTP Automized Teammate Experimentation Lab

#### A high level python based website meant for conducting qualitative expert interview fascilitating a complexity approach

This project is meant for making it easier to construct qualitative models from qualitative knowledge through structured interviews and collaboratative work. The website guides a researcher in a coherent and incremental process of defining a complex problem by providing a multi-phase structure. This structure first lets the researcher define the problem in a concise way and work out several variable values concerning the problem statement. These steps can be found in section [Step- by- step conceptualization of your project](#Step-by-step-conceptualization-of-your-project). The website will require the researcher to answer most of these questions in the dashboard page to configure the rest of the application. 

This README will explain how to configure a VPS (Virtual Private Server) to act as a webserver, serve the website and configure its settings. This way, a researcher with a complex systems problem can worry over the hard questions regarding the problem statement instead of dealing with issues of visualization and ways of data gathering. For more information, please read [my report](bas_chatel_internship2019.pdf).

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
      * Spatial: Biology, Psychological, Interpersonal .. global etc
      * Temporal: Miliseconds, Seconds, Minutes .. Years, Lifetime etc
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
    * In order to obtain a data set beyond the scope of literature by merging quantitative knowledge found in literature and qualitative knowledge obtained from experts, we need to have expert knowledge representing all fields relating to the problem set. It is important to think about the different perspectives needed to form a complete overview of the problem statement and identify key figures that are linked to the field scientifically, experience based, policywise etc.
    * For this we need some information of each expert:
      * What is their affiliation with the problem statement? (Experience Expert, Researcher, Policy maker, etc.)
      * In discipline are their working? (Biology, public health, physics, etc.)
      * What is their specialization? (epidemiology, genetics, methodology, social media, etc)
    * Also ask the experts whether or not they would be open for further feedback moments in unclear situations and whether or not they want to be named as a participant. As it might effect transparance and reliability of the qualitative data, a default term of conditions would be to state that any participant needs to agree with their name being associated with the expertlist.

# Configuring a Virtual Private Server (VPS)

Though this might seem daunting, and perhaps for some technologically challenging, we provide a step by step tutorial of how to configure and publish the website. A VPS was chosen in order to cut budget costs and retain a lot of freedom to play around and alter anything you want.

### Choosing VPS service
As our web application will attract only few users (namely being your expert pool) we don't need a whole lot of RAM, Disk space, CPU etc. For our purposes a 2GB RAM with 20GB Disk space, 1 CPU and 20TB traffic is more than enough. [Greenhost](https://greenhost.net/), [DigitalOcean](https://www.digitalocean.com/) or [Hetzner](https://www.hetzner.com/cloud) for example provide fine VPS services that let you do whatever you want with them for a small price. Out of these three, [Hetzner](https://www.hetzner.com/cloud) is the cheapest, so throughout this tutorial we will use this VPS provider.
















































