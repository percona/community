---
title: "How To Optimize the Structure of a Simple PHP Application as Your Project Grows"
date: "2023-03-28T00:00:00+00:00"
draft: false
tags: ["Databases", "Percona", "PHP", "Docker"]
authors:
  - daniil_bazhenov
images:
  - blog/2023/03/php-3-structure-cover.jpg
---

Let's discuss the structure of our simple PHP application, folders, files, and functions and transform the project to grow it. 

You and I have developed a small PHP application that makes an HTTP request to the GitHub API and stores the result in the database.

* Step 1 - [How to Develop a Simple Web Application Using Docker-compose, Nginx, PHP 8, and MongoDB 6](https://dev.to/dbazhenov/how-to-develop-a-simple-web-application-using-docker-compose-nginx-php-8-and-mongodb-6-nhi).
* Step 2 - [How to Make HTTP Requests to API in PHP App Using GitHub API Example and Write to Percona Server for MongoDB](https://dev.to/dbazhenov/how-to-make-http-requests-to-api-in-php-app-using-github-api-example-and-write-to-percona-server-for-mongodb-3gi3).

Our code already performs different functions: 

1. Reading environment variables.
2. Connecting to the database.
3. Running API queries.
4. Looping and writing to the database.

The code is already hard to fit on the screen, and it's time to think about dividing the code into files, folders, and functions.

Frameworks are usually responsible for separating code into folders and files. But we don't use frameworks, so we'll do it ourselves. At this stage, we will not make the structure too complicated. Our task is to learn how to change it so that we can change it at any time in the future.

I prefer to change the structure of files and folders as the project grows, grouping files according to meaning and logic. In this article, we'll make the first change, and we'll do them more times in the future.

Let's start optimizing our application.

## Initializing and configuring the application

Usually, PHP scripts are executed sequentially starting with index.php, as in our case. 

At the beginning of index.php, we connect the composer libraries, read environment variables, create a database connection, and create an object for HTTP requests. This will be required for each script. I propose to put this in a separate init.php file.

Create an app/init.php file and move the initialization to it. We simply move the code from the index.php file, leaving only the logic of the script.

_app/init.php_
```
<?php

// Enabling Composer Packages
require __DIR__ . '/vendor/autoload.php';

// Get environment variables
$local_conf = getenv();
define('DB_USERNAME', $local_conf['DB_USERNAME']);
define('DB_PASSWORD', $local_conf['DB_PASSWORD']);
define('DB_HOST', $local_conf['DB_HOST']);

// Connect to MongoDB
$db_client = new \MongoDB\Client('mongodb://'. DB_USERNAME .':' . DB_PASSWORD . '@'. DB_HOST . ':27017/');

$app['db'] = $db_client->selectDatabase('tutorial');

$app['http'] = new \GuzzleHttp\Client();

```

You may also notice that I created an array or `$app` object, and added HTTP and db as array elements. That way I can use `$app` anywhere to pass to functions and have HTTP queries and database handling there.

And in the index.php file itself, we simply include our init.php

_app/index.php
```
<?php

require __DIR__ . '/init.php';

dd($app);

```

And print $db and $http with dd() to make sure they work and are available in index.php.

Leave the rest of the code in index.php unchanged for now and run `localhost` in the browser.

![PHP Structure - App Init](/blog/2023/03/php-3-structure-1.jpg)

So we split index.php into two files: init.php and index.php

When we start localhost, our nginx web server launches index.php, init.php connects there, does initialization and environment variables reading, and then the rest of the index.php code continues.

## Let's get to the functions 

Functions are needed to group code that is executed multiple times. 
Functions can be initialized either in the executable PHP file itself, next to the code, or in a separate file that includes, such as composer libraries.

For example, we make a GET HTTP request to the GitHub API at a certain URL. We will probably need to make another type of request to another URL, but it will still be an HTTP request using guzzle.

I assume in advance that I will have many different functions: general, for GitHub, for the database. So let's create a func folder in the app folder.

And in the `app/func` folder, create a github.php file. Create our first function there that will request the GitHub API.

_app/func/github.php_
```
<?php

function fn_github_get_repositories($app) 
{

    $http = $app['http'];
    
    $url = 'https://api.github.com/search/repositories';

    $params = [
        'q' => 'topic:mongodb',
        'sort' => 'help-wanted-issues'
    ];

    try {
        $response = $http->request('GET', $url , [
            'query' => $params
        ]);              

        $result = $response->getBody();

        $result = json_decode($result, true);

    } catch (GuzzleHttp\Exception\ClientException $e) {
        $response = $e->getResponse();
        $responseBodyAsString = $response->getBody()->getContents();
        echo $responseBodyAsString;
    }  

    return $result;
}
```

A little clarification, we will modify this file in the future, the first function is not the best. You should understand that you will need to change frequently, changing parameters and variables within functions.

Now go back to the index.php, and connect our first function file and run the function.

_app/index.php_
```
<?php

require __DIR__ . '/init.php';
require __DIR__ . '/func/github.php';

$repositories = fn_github_get_repositories($app);

dd($repositories);

```

Run `localhost` and see the same result. Our request was executed, and we got the list of repositories.

![PHP Structure - Functions](/blog/2023/03/php-3-structure-2.jpg)

So we cut our index.php file by more than half. All we have left in there is the database query. At the moment it doesn't look too complicated to put it in a separate function, but. We need to change it because the $db object, we now have $app['db']. 

In addition, the response from the API we have in the variable $repositories, which means that all loops and all operations must be done with it. 

So far, my `index.php` file is like this.

```
<?php

// Enabling Composer Packages
require __DIR__ . '/init.php';
require __DIR__ . '/func/github.php';

$repositories = fn_github_get_repositories($app);

$app['db']->repositories->createIndex(['id' => 1]);

if (!empty($repositories['items'])) {
    foreach($repositories['items'] as $key => $repository) {

        $updateResult = $db->repositories->updateOne(
            [
                'id' => $repository['id'] // query 
            ],
            ['$set' => $repository],
            ['upsert' => true]
        );

    }
}

dd($repositories['items']);
```

_app/_
```
.
├── func
│   └── github.php
├── vendor
├── composer.json
├── index.php
└── init.php
```

The result of running `localhost` in the browser will be the same, we will print the repositories that will be stored in the database.

![PHP Structure - Result](/blog/2023/03/php-3-structure-3.jpg)

I think we should stop for now and continue in the next article.

## Conclusion

As a result of this modification, we learned how to split one script into several scripts and create functions.

You can divide it into files and folders and functions as you like, as it is convenient to you now or will be convenient in the future. It's okay to change the structure as your project grows.

You can check and run the source code in [the repository](https://github.com/dbazhenov/nginx-php-mongodb-docker-compose/tree/tutorial_2_structure).

In the next post, we will continue to modify and improve our application. We will add new functions and features. I'm sure we'll end up with a very useful app, and you'll learn how to develop it.

Ask me questions, I'll be happy to answer them.


