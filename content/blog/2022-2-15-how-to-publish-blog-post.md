---
title: "How to publish a blog post"
date: "2022-02-10T00:00:00+00:00"
draft: false
tags: ['blog', 'PMM']
images:
  - blog/2022/2/0-How-To-Post-Cover.png
authors:
  - daniil_bazhenov
slug: 'how-to-publish-blog-post'
---

## Preparing the environment and tools for publishing a post. 

This step is optional, If you want to check your post or changes before publishing, you will need to make some adjustments on your computer. 

We use the Hugo website engine, which turns Markdown pages into HTML very quickly and easily. We also use GitHub and GitHub Pages for free website hosting. So by following the steps below you will learn how to use the Hugo engine and possibly build your own site using it in the future.

I will briefly describe the steps for the professional:
- Fork our repository ["percona/community"](https://github.com/percona/community/).
- Make a Git Clone fork on your computer
- Install [Hugo engine](https://gohugo.io/getting-started/installing/)
- Run the Hugo server in the source code folder of the site with the command `hugo server -D` and open a local copy of the site in your browser at `localhost:1313`
- That's it, you can change the texts and see the result immediately.
- You can move on to the next step, "How to add a post".

Now let's discuss these steps in detail.

1. You need to make a fork of our ["percona/community"](https://github.com/percona/community/) repository with the source code of the site. Just open our repository and click the "Fork" button and follow the suggested steps. As a result, you will have a copy of our repository. 

![Fork](/blog/2022/2/1-Forking-Percona-Community.png)

2. Git Clone your fork to your computer. Click Code and get the address to clone the repository.  

![Clone](/blog/2022/2/2-Git-Clone-Button.png)

Open the console on your computer and type the command:

`git clone git@github.com:dbazhenov/community.git percona-community` 

It is important to clone your fork and not the main repository. Yes, you will probably need to install Git on your computer if it hasn't been done before.

When cloned, all of the Git repository code will be downloaded to your computer so you can modify it and run it locally.

You will see in the console:
```
Daniils-MacBook-Pro:Sites daniilbazhenov$ git clone git@github.com:dbazhenov/community.git percona-community
Cloning into 'percona-community'...
remote: Enumerating objects: 67797, done.
remote: Counting objects: 100% (5879/5879), done.
remote: Compressing objects: 100% (1346/1346), done.
remote: Total 67797 (delta 3005), reused 5847 (delta 2988), pack-reused 61918
Receiving objects: 100% (67797/67797), 399.02 MiB | 843.00 KiB/s, done.
Resolving deltas: 100% (33607/33607), done.
Updating files: 100% (1387/1387), done.
```

3. Install the Hugo website engine: [Install Hugo](https://gohugo.io/getting-started/installing/). The installation is not difficult, I recommend choosing the right step for your operating system and watch the official installation video. Hugo is a lightweight static website generator, it is free and open-source software. You do not need to install a web server, programming language and database. I hope you installed it successfully.

4. Open the directory with the site code in the console, in my case it is: `cd percona-community`

5. Launch the Hugo server with the command 'hugo server -D'. When you start the server, the Hugo engine scans the structure of the project, generates the site on the fly and makes it available in the browser. You will see the URL as a result in the console.

```
Daniils-MacBook-Pro:percona-community daniilbazhenov$ hugo server -D
Start building sites …

                   |  EN
-------------------+-------
  Pages            | 1107
  Paginator pages  |   23
  Non-page files   |    0
  Static files     |    2
  Processed images | 1316
  Aliases          |   64
  Sitemaps         |    1
  Cleaned          |    0

Built in 99883 ms
Watching for changes in /percona-community/{archetypes,assets,content,layouts,static}
Watching for config changes in /percona-community/config.yaml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

6. Launch the website in your browser `http://localhost:1313/`. When you are done with the site, you can stop the server with the buttons in the console, in my case Ctrl+C

Everything is great, now you can edit the site, add new posts and immediately see the result in your browser.

![Browser](/blog/2022/2/3-Website-Browser.png)


## How to publish a post 

I hope you have successfully made a fork and clone of the repository, let's start publishing your post.

Our website works with text and posts marked up in [Markdown](https://www.markdownguide.org/basic-syntax/) syntax. You will probably need to edit the text a bit when you publish it.

1. Open the folder with the project source code. 

2. Create a separate git branch for your post

`git checkout -b "dbazhenov_post"` 

3. Create an author card in the `content/authors/` folder. You need to create a folder with your name and an index.md file. You can find many examples, such as `/percona-community/content/authors/jeff_gagne/index.md` ([GitHub link](https://raw.githubusercontent.com/percona/community/main/content/authors/jeff_gagne/index.md))

4. Add your photo to the folder `assets/blog/authors`. This is your avatar, its address will be used in your author profile file in the images field.

![Author Profile](/blog/2022/2/4-Author-Profile.png)

5. If your post contains images. Load the pre-made images into the `assets/blog/[YEAR]/[month]` directory. If there is no directory, create one. 

6. Now add the post in Markdown format to the `content/blog` directory. Important, get the name of your file right: "Date-name-in-style-URL". In my case, it is '2022-02-12-how-to-post.md'. If you are not familiar with markdown, just look at the examples in our blog, there are examples for code blocks, headers, pictures and lists. 

7. It is important that each post at the beginning must have special parameters in YAML format, the so-called [Front Matter](https://gohugo.io/content-management/front-matter/). You can see an example in any of our 100+ blog posts. You will need to specify in these parameters:

- Title
- Date
- Draft status
- Tags 
- Images - A special image that will be displayed in the list of posts and on social networks. If you're having trouble, write community-team@percona.com
- Authors - your name as you listed on the author card
- Slug - not necessary, only if you want to have a special URL.

7. If you ran the Hugo server, you can open your post in your browser. If you have difficulties or problems, email us or open Issues on GitHub.





