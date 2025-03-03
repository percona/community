---
title: "How to Make HTTP Requests to API in PHP App Using GitHub API Example and Write to Percona Server for MongoDB"
date: "2023-03-20T00:00:00+00:00"
draft: false
tags: ["MongoDB", "Databases", "PHP", "Docker"]
categories: ["Community", "MongoDB"]
authors:
  - daniil_bazhenov
images:
  - blog/2023/03/PHP-API-2-cover.jpg
---

We learn how to work with HTTP requests in PHP and make API requests using the GitHub API as an example. We'll get the data from the API and save it to the database.

In [the previous article](https://percona.community/blog/2023/03/17/how-to-develop-a-simple-web-application-using-docker-nginx-php-and-mongodb/), we developed a simple application that connects to the MongoDB database ([Percona Server for MongoDB](https://www.percona.com/software/mongodb/percona-server-for-mongodb?utm_source=percona-community&utm_medium=blog&utm_campaign=daniil)) and writes documents in a loop. We only used [Composer](https://getcomposer.org/) packages to work with MongoDB. We have set up the Docker-compose environment and have the app/ directory where the application code is located. We can edit the code and check the result in the browser without restarting the Docker containers.

We plan to make HTTP requests to GitHub API. I prefer using the popular PHP HTTP client library [guzzlehttp/guzzle](https://packagist.org/packages/guzzlehttp/guzzle).

Here we go!  

## 1. Preparation

Open the project folder in the console or git clone the repository, and open the folder.

Start Docker-compose

```
docker-compose up -d
```

This will start the containers, and you can run `localhost` in the browser.

## 2. Connect PHP libraries using Composer

[Composer](https://getcomposer.org/) is a package manager for PHP. You can find out-of-the-box libraries and functions for almost any task. I prefer to use something other than Frameworks for small projects, but just plug-in packages.

Open the `app/composer.json` file in the code editor.

Add two new packages, guzzle, and dd.

```
{
    "require": {
        "guzzlehttp/guzzle": "^7.0", // Guzzle for HTTP
        "larapack/dd": "1.*", // dd for debug
        "mongodb/mongodb": "^1.6",
        "ext-mongodb": "^1.6"
    }
}
```

Connect to the container with php-fpm

```
docker exec -it [php-fpm-container-name] bash
```

Update the packages with the command.
```
composer update
```

That's it, we have the packages installed, more about Composer is [here](https://getcomposer.org/doc/01-basic-usage.md).

## 3. Let's choose an API and read the rules of use.

I chose [the GitHub API](https://docs.github.com/en/rest/search?apiVersion=2022-11-28#search-repositories) as an example because it is available with and without authorization and has good documentation. 

First, we will get a list of repositories. We will use the repository search API for all repositories containing the topic mongodb.

I opened [the REST API](https://docs.github.com/en/rest/search?apiVersion=2022-11-28#search-repositories) documentation and found the method, parameters, and examples I needed.

![the GitHub REST API](/blog/2023/03/PHP-API-1.jpg)

## 4. Let's make the first request to the API.

Open the index.php file in the app folder and add the following code somewhere at the beginning, after the inclusion of `vendor/autoload.php`

```
$http = new \GuzzleHttp\Client();

$url = 'https://api.github.com/search/repositories';

$params = [
    'q' => 'topic:mongodb'
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

dd($result);
```

To summarize, here is what we did:  

1. Initiated the HTTP client Guzzle.
2. Created a variable with a URL from GitHub API.
3. Created array with query parameters, in our case q search string.
4. Executed request in Try-Catch construct; if a request has errors, an exception will be thrown, and we can read the error. 
5. Received response results from API into variable $result.
6. Converted the response from JSON to an array.
7. Printed out the array in a convenient form using dd($result).

Run `localhost` in the browser and see the result. 

![the GitHub REST API - first request to the API](/blog/2023/03/PHP-API-2.jpg)

## 5. Exploring the result

`dd()` is a function that helps print any variable, array, or object. Just list them separated by commas.

You have printed the response from the API and see the array:

* total_count - says that there are 72945 repositories for our query. This looks like an excellent dataset for our experiments with analytics and the database

* items - contains an array of 30 other arrays with repository data.

I suggest modifying our API query to get a slightly different result. We'll add sorting to the query.

Change the $params array in the index.php file.

Let's add sorting by the count of `help-wanted-issues`.

_app/index.php_
```
$params = [
    'q' => 'topic:mongodb+language:php',
    'sort' => 'help-wanted-issues'
];
```

Run localhost in your browser, and you will see a different set of items in the API response.

## 6. Let's save the data to the database

Instead of dd(), we add a foreach loop over items and print one repository data.

_app/index.php_
```
if (!empty($result['items'])) {
    foreach($result['items'] as $key => $repository) {

        dd($repository);

    }
}
```

Great, we see the data. This will be our document in the collection of repositories. 

![the GitHub REST API - save the data to the database](/blog/2023/03/PHP-API-3.jpg)

Replace `dd($repository)` with an insert query to the MongoDB database.

Remember to move the client db initialization, database connection, and read environment variables.

_app/index.php_
```
if (!empty($result['items'])) {
    foreach($result['items'] as $key => $repository) {

        $updateResult = $db->repositories->updateOne(
            [
                'id' => $repository['id'] // query 
            ],
            ['$set' => $repository],
            ['upsert' => true]
        );

    }
}

dd($result);
```

Run `localhost` in your browser. I usually always type dd() at the end, since it stops the script and displays something like dd('finish').

You may notice that making a updateOne request to the repositories collection, with the parameter upsert. This means that if such a document with an id ('id' => $repository['id']) already exists in the database, it will be updated. If not, it will be inserted. This allows me to avoid duplicate data with multiple test queries.

## 7. Connecting to a database using MongoDB Compass.

We must see that we did everything correctly and the data appeared in the database.

Besides, we can play with them.

Open our new collection and check it out. We can also create an index by the id key in the Indexes tab. If you did not make the index with a PHP query.

Download and install MongoDB Compass [here](https://www.mongodb.com/products/compass)

![the GitHub REST API - MongoDB Compass](/blog/2023/03/PHP-API-4.jpg)

![the GitHub REST API - MongoDB Compass](/blog/2023/03/PHP-API-5.jpg)

## Conclusion

The code of the application at the current stage can be obtained from [the repository](https://github.com/dbazhenov/nginx-php-mongodb-docker-compose/tree/tutorial_step_1_api).

We did a great job and figured out how to make requests to the API, as you can make any HTTP requests.

In my next posts, we'll figure out how to add authorization and work with API limits. The point is that GitHub lets unauthorized users make a few requests. We aim to get a lot of valuable data from the API and will do that soon.

We will also devote some time to the structure of the files and folders of our application. It's already getting big, and we must make it more convenient.

