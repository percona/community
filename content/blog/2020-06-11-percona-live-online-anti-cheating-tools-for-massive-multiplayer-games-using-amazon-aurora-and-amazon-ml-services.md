---
title: 'Percona Live ONLINE: Anti-cheating tools for massive multiplayer games using Amazon Aurora and Amazon ML services'
date: Thu, 11 Jun 2020 14:21:08 +0000
draft: false
tags: ['author_lawrence', 'Amazon', 'Amazon RDS', 'AWS', 'aws', 'ML', 'MySQL', 'mysql-and-variants', 'PostgreSQL', 'SQL', 'Tools']
images:
  - blog/2020/06/image4.jpg
authors:
  - cate_lawrence
slug: percona-live-online-anti-cheating-tools-for-massive-multiplayer-games-using-amazon-aurora-and-amazon-ml-services
---

Would you play a multiplayer game if you discovered other people are cheating? According to a survey by Irdeto, 60% of online games were negatively impacted by cheaters, and 77% of players said they would stop playing a multiplayer game if they think opponents are cheating. Player churn grows as cheating grows.

Stopping this is therefore essential if you want to build and develop your community, which is essential to success for today’s gaming companies. This session at [Percona Live ONLINE](https://www.percona.com/live/conferences) was presented by Yahav Biran, specialist solutions architect, gaming technologies at Amazon Web Services, and Yoav Eilat, Senior Product Manager at Amazon Web Services, presented a talk and demonstration about anti-cheating tools in gaming based on using automation and machine learning (ML). 

Yoav notes that while people might think of ML in terms of text or images, but: "There's a considerable percentage of the world's data sitting in relational databases. How can your application use it to get results and make predictions?”

Six steps for adding Machine Learning to an Application
-------------------------------------------------------

Traditionally there are a lot of steps for adding ML to an application with considerable expertise required and manual work, with the efforts of an application developer, database user and some help from a machine learning database scientist:

1.  Select and train database models
2.  Write application code to read data from the database
3.  Format the data for the ML model
4.  Call a machine learning service to run the ML model on the formatted data
5.  Format the output for the application
6.  Load the results to the application

The result is most machine learning is done offline by a data scientist in a desktop tool. "We would like to be able to add some code to your game and use the models directly from there," explained Yahav. 

With multiple databases such as the customer service database or order management system, or in the instance of gaming, this would all be a lot of work to do manually. "So, we want to see how we can do that in an easier and automated way," continued Yahav.

Examples where cheating can occur
---------------------------------

The duo provided some examples of common cheating behaviour that can occur in games:

*   Authentication: player authentication in the game, to prove they are who they say they are and that they have the right account
*   Transactional data: what the players purchase inside the game, so they either don’t spend funds they don’t have or don’t lose items they purchased legitimately
*   Player moves: for example where players in cahoots are walking in front of each other like a human shield

"Where you have a player that's walking in one direction, shooting in the other direction and doing five other things at the same time, then it's probably a bot," said Yahav.

Demonstrating ML in action
--------------------------

The demo was built on Amazon Aurora, a relational database offered by AWS and that is compatible with MySQL and PostgreSQL. The database includes some optimizations and performance improvements, plus a few additional features. It has pay as you go pricing. 

As Yahav explains: "The machine learning capabilities added in 2019 allow you to do a query in your Aurora database and then transfer it to a machine learning service for making a prediction. There's integration with Amazon SageMaker and Amazon Comprehend, which are two machine learning services offered by AWS. The whole thing was done using SQL queries. 

Thus, you don't need to call API's; there's no need to write additional code, you're doing a step, you can just write a statement where you're selecting from the results of the machine learning call. You can just use the results like you would use any other data from your database."

Shortening the process from six steps to three
----------------------------------------------

Using this approach, the process is now made much simpler:

*   (Optional) select and configure the ML model with Amazon SageMaker Autopilot
*   Run a SQL query to invoke the ML service
*   Use the results in the application

This article focuses on gaming; however, the presentation also provides details about fraud detection in financial transactions, sentiment analysis in the text (such a customer review written on a website), and a classification example to sort customers by predicted spend.

ML queries in gaming scenarios
------------------------------

Yahav and Yoav trained a SageMaker model to recognize anomalous user authentication activities such as the wrong password. You can dig deep into the code for the demonstration over at [GitHub](https://github.com/aws-samples/amazon-aurora-call-to-amazon-sagemaker-sample), so we'll only walk through some of the code. 

![](blog/2020/06/image6.jpg) 

The model can also use the function auth\_cheat\_score to find players with a significant cheat score during authentication.

Introducing EmuStarOne
----------------------

The game was developed initially in 2018 and is a massively multiplayer online (MMO) game that enables players to fight, build, explore and trade goods with each other. 

![](blog/2020/06/image4.jpg) 

The game can be viewed [https://yahavb.s3-us-west-2.amazonaws.com/EmuStarOne.mp4](https://yahavb.s3-us-west-2.amazonaws.com/EmuStarOne.mp4) 

Players authenticate from supporting clients, suc as a PC or game console. 

Five personality traits and game events define Emulants: they can move, forge, dodge, etc. and they can transact with virtual goods.

What does cheating look like in the data?
-----------------------------------------

To understand what cheating looks like within games, we have to understand what good and bad behaviour looks like in our game data over time:

*   Players can cheat as they make illegal trades or run bots that manipulate game moves on behalf of other players.
*   Cheating can manifest in different ways, such as player move anomalies and consecutive failed login attempts from two different sources.

In general, ML solutions work very well with problems that are evolving and are not static.

How can we stop cheating in the game?
-------------------------------------

To stop cheating requires a plan and some decisions to be made before creating the data model or ML approach:

*   We can form an anti-cheat team.
*   Take action against cheaters e.g., force logout with a hard captcha as a warning.
*   Escalate the anti-cheating actions as needed.
*   Eventually, cheaters learn the system behavior, so there is also the consideration of false positives.
*   Continuously redefine our cheating algorithms.

What we want to enable by forming this anti-cheat team is to stop those that cheat and continuously refine the algorithm.

EmuStar One game data authentication
------------------------------------

![](blog/2020/06/image3.jpg) 

Yoav explained: 

"In the first data set, we have the player authentication; this is the authentication transaction. There is a timestamp that the player came, and in this case, the authentication method was the Xbox Live token."

It means that the user logged through to the Xbox Authentication Service. It includes the playerGuid, the user agent, which in this case, is an Xbox device. You can see the source IP and the cidir and the geo-location.

Player transaction
------------------

![](blog/2020/06/image7.jpg)

The player moves
----------------

![](blog/2020/06/image2.jpg) 

The player moves (in this case is the X and Z coordination) include the timestamp and the player. There are three more properties - the quadrant, the sector, and the events can be traversing, user traversing from one place to another, or forging or dodging or other events that the game allowed.

The three ML models used for game data
--------------------------------------

*   For authentication: IP insights is an unsupervised learning algorithm for detecting anomalous behavior and usage patterns of IP addresses
*   For transactions: Supervised linear regression - this is because most transactions are already classified by Customer care and player surveys
*   For player moves: "Random cut forest (RCF), assuming most player moves are legit so anomalous moves indicate potential cheaters," explained Yoav.

Data preparation
----------------

The game involves a mammoth amount of data. Yoav shared: "We have 700,000 authentication events, 1 million transactions and 65 million player moves. For the supervised data, we classified data between 0.1 to 3% to allow the model to distinguish between legit transactions. Move authentication and other Models were built using Jupyter notebooks hosted by SageMaker. Data was stored on s3. 

"Once that we were able to distill the data and train the model, we deployed the model with hosted inference endpoints using SageMaker as the service. We used Aurora to invoke the endpoints.”

Data encoding and transformation
--------------------------------

In general, ML models like numbers - interest, doubles, or floats. So the String attributes were encoded. The same encoding was on the Aurora side, covering for example player move events such as TraverseSector or Travel.Explore 

The notebook is open source so you can see how encoding strings of the player moves was achieved. 

Yoav explained: " I took the quadrant, encoded the sector. encoded the event, and encoded it using the pandas, in the end, and the OneHot encoder." 

The code for an alternative method for achieving this was also shared:

 ![](blog/2020/06/image5.jpg)

The demo
--------

Based on the characteristics of cheating in our game, cheaters are found via:

*   Looking for suspicious transactions
*   Looking for suspicious authentication by the players who executed these transactions
*   Then seeing if the player moves were suspicious

Yahav shared code for the materialized view for authentication, querying the parameters and filtering only the suspicious ones that are mentioned as cls>zero classified as fraudulent. 

An anomaly score cls>2 indicates a suspicious move - the tools are very flexible! 

Yahav then executed a query for "the timestamp and the player Guids that are basically are suspicious." 

The live demo presented worked to filter suspicious transactions. Then the authentication cheat was joined with the transaction cheat. Subsequently, 13 suspicious cases were revealed based on timestamps. The suspicious moves were then queried based on the timestamps. 

![](blog/2020/06/image1.jpg) 

The demo included lots of movements, and transactions from all directions. 

Through exploring the player timestamp, playerGuid, quadrant, and sector of all the suspicious cases, it revealed where suspicious behavior occurred so that monitoring could occur in that specific area.

Resources from the presentation
-------------------------------

Examples on [Github:](https://github.com/aws-samples/amazon-aurora-call-to-amazon-sagemaker-sample)

*   [Amazon Aurora](https://aws.amazon.com/rds/aurora/)
*   [Aurora machine learning](https://aws.amazon.com/rds/aurora/machine-learning/)
*   [Amazon SageMaker](https://aws.amazon.com/sagemaker)

You can also [watch a video of the recording](https://www.percona.com/resources/videos/anti-cheating-tool-massive-multiplayer-games-using-amazon-aurora-and-ml-services).