---
title: "Open Source Database vs. Server Side Public License SSPL With Peter Zaitsev - Percona Podcast 01"
description: "On this episode of the HOSS (Head of open Source Strategy) talks FOSS (Free and Open Source Software), we talk with Peter Zaitsev CEO of Percona."
short_text: "On this episode of the HOSS (Head of open Source Strategy) talks FOSS (Free and Open Source Software), we talk with Peter Zaitsev CEO of Percona. We explore the changing landscape of the open source space including recent increases in the use of SSPL licenses by database providers like Elastic. We explore the trends driving the open source business in 2021. 


Last week Elastic announced that they were “Doubling Down” on open source by changing their licensing to a non-open license - MongoDB’s Server Side Public License or SSPL. Let me clarify in my opinion this is not doubling down - unless, as our good friend @gabidavila highlighted, that maybe the thinking was a double negative makes a positive? VM Brasseur posted on her blog that he feels Elastic and Kibana are now a business risk for enterprises. Peter Zaitsev has penned why he felt SSPL was bad for you before this announcement, and then sat down with me to discuss his thoughts last week as well. 


Elastic was the most recent company to change licenses away from a more permissive and open license following in the footsteps of other vendors like MongoDB. Is SSPL (Server Side Public) License good or bad? What is the impact on open source? Why the change?"
date: "2021-02-15"
podbean_link: "https://percona.podbean.com/e/the-hoss-talks-foss-ep01-talking-with-percona-ceo-peter-zaitsev-about-sspl-open-source-elastic-and-the-cloud/"
youtube_id: "KkFajzrF61s"
speakers:
  - peter_zaitsev
aliases:
    - "/podcasts/1/"
url: "/podcasts/1-open-source-database-vs-server-side-public-license-sspl"
---

## Transcript

**Matt Yonkovit:**  
I guess the big news of the week for us is that Elastic has decided to kick open to the curb despite saying they've doubled down on open, which is kind of silly because I have always thought doubling down meant you were going to do more of it, not less of it. But as someone pointed out on Twitter, maybe they're looking at doubling down as two negatives make a positive. So it looks like they're going to SSPL because they don't want to be open anymore.

**Peter Zaitsev:**  
Oh, no. I mean, I think that is a very tricky word. Right? They're not doubling down on open source, doubling down on open. 

**Matt Yonkovit:**  
Oh, open.

**Peter Zaitsev:**  
Oh, that's right. That's right.

**Matt Yonkovit:**  
So what does that mean, when they say that?

**Peter Zaitsev:**  
Well, I think that means what? No, I assume that means that they will be able to have more stuff to be open. But under the SSPL license, then they could have a departure license. But it's not going to be open source. So that is how I read that kind of announcement

**Matt Yonkovit:**  
Okay, but does that mean do you think that that means they're going to take things that are in their enterprise version and make them available to everyone through SSPL?

**Peter Zaitsev:**  
Maybe not. Right. Like, one thing to remember is what that is a second time. Elastic changes license? Yes, Right. So they had done one iteration of license change to see if I remembered things correctly. Amazon responded by opening these triggers for ElasticSearch very things which were not released in the budget to license got equivalents written by the Amazon team. Right. And now everything goes in SSPL. So now Amazon, yeah, can't touch it. Right. And I assume that will allow you to have more features to be released under SSPL than before. So that is possible.

**Matt Yonkovit:**  
So do you think that this is purely because of Amazon that they're doing this?

**Peter Zaitsev:**  
Well, uh, uh, not essentially, Amazon, but the cloud vendors? In general. Right? I see. I think that Amazon is like in the cloud, like McDonald's is in fast food. Right. So they are not the only vendors around right. But then you want to talk about an example of eel in the cloud. Amazon does it!

**Matt Yonkovit:**  
Oh, yes. Well, so. But I mean because I've seen this also as more of a revenue play. And I don't know if it's purely cloudy, right. So if you look at it we've got four major publicly traded open source database companies that are out there, and none of them are turning a profit. In fact, they've never turned a profit. And actually, they're, I can't think of any other pure, even just database companies that are kind of standalone that are still out there. Because I mean, the Oracle, I mean, they were a giant, but they sell more non-database stuff than they do database stuff. Now. so for me, I look at this, and I go, this is really about focusing more on the people that they're, they're focused on trying to get more shareholder value at the expense of that community. And I think that's the mantra of a lot of publicly traded companies, his shareholder first, how do we accelerate revenue? And I'm a bit interested in your thoughts like do open source databases work in the public traded space? I mean, I haven't seen it. Right. It's not something that I've seen turn a profit or anything?

**Peter Zaitsev:**  
Well, let's get a few things you mentioned, like at first, yes. Indeed, Elastic public companies return as do many other companies out there in the database space. I know, I think we live in an age where it looks like their logical approach to your losses are, the higher is your valuation, right. It's not just in a database company. In general, a lot of companies in a SaaS space would play by, by the same rules. Right? But if you look at shareholder value, right, it's not just revenue-related. It's also a related kind of offer, right? And if you look at how companies are valued. Their cloud revenue, subscription, cloud revenue is valued the highest, right? A snowflake is a great example of it, right? They have a huge, huge multiple in revenue, because you guess what the cloud revenue is the only type, and God they don't have that kind of legacy enterprise license in revenue, right? Stuff like that. Right? And if and as I talk to folks in the VC industry, right, everybody tells you, hey what? Their database of history as service revenue, cloud revenue, right, is the only thing that matters, right, as they see value companies? Right? And I would imagine in the public markets, it's very similar, right?

**Matt Yonkovit:**  
And is that why Mongo is focused very, very heavily on Atlas at the expense of everything else?

**Peter Zaitsev:**  
Oh, of course, of course. Right. I mean, they do that. Yeah. Oracle has been pushing the cloud very, very aggressively, right? Because, again, especially from their valuation standpoint, right, that is a market, which is seen as growing rapidly. And remember, your valuation as a public company is not about now. It's about a vision of a future you can sell. Right? So it's to sell a future that has less flow,

**Matt Yonkovit:**  
you're banking on eventually breaking even and making a profit. And what's, what's interesting is a lot of these models are predicated on continual expansion, which means you have to spend the customer has to spend more and more money in order to make.

**Peter Zaitsev:**  
Right and I think this is the interesting thing with the many companies out there, right? Not only in database space, right? If their idea is, hey, you give away a lot of stuff for free, you try to acquire as much dominance as possible. And then pardon my French, your generosity, your customer and right, you that is when you make a profit?

**Matt Yonkovit:**  
Well, I think this is like I see some different evolutions in that space, right, like, so when I see people who start out open there are the true open source believers. But then there are these companies that look like MySQL and they go, we want to copy that model. And then they now they're saying, we want to copy the Mongo model. So they get into the business because open source is a way to drive valuation. Not because they believe anything about open source, it's just hey, I can get more money if I go open source.

**Peter Zaitsev:**  
Well, that's right. And I think it's not only how companies are started, but also how companies are evolved, because in many venture-funded public companies, right, people who originally founded a company, often do not have control anymore. And in some cases, they leave in some cases, they decide to stick it out dry because there is a guess who to dollar check attached to them doing so. But this should not mean that founders in those companies often would completely share a vision? And that's right, where are those things off? Right. And you're right, as I think that's a general idea is hey what, open source is great for getting adoption, right? That's not dissimilar from Uber, for example, subsidizing your every ride, right to get to market dominance, and then you figure out how you can monetize your, your position.

**Matt Yonkovit:**  
Okay, so back to the specific change, what does this mean for Elastic open source users? Like what are they going to see that's going to be difficult?

**Peter Zaitsev:**  
I think it is very interesting, I think Elastic is in a different place, compared to MongoDB which did it early because there is a thing called Open distro for Elastic or create Amazon exists. And they have been quiet for the last 24 hours. So as this news broke, right, so it is not very clear, wherever they will sort of wave I'd flag and say, Hey, you know what we tried but you don't really want to really fork it and carry on the torch of open source Elastic equivalent, right? or they will do that. Right? I think if they will do that, then they'll get a lot more validity in the market space and, and the user base, you'll be fusion to that much more than it has been. It has been before. Right. 

**Matt Yonkovit:**  
So, could this could actually hurt Elastic in the long run if people start flipping to open Distro?

**Peter Zaitsev:**  
 Yes, absolutely. Right. I mean, if we openDistro for ElasticSearch, we'll continue carrying on the open source door trick and acquire a lot of users. Right. And, frankly, I believe that's a great opportunity for Amazon, to show that they are in the open source for real, right, and really be the champions in that in that project space right now just free riders, as they open it.

**Matt Yonkovit:**  
Well, it but I gotta be honest, lately, Amazon has done more for open source than a lot of the open source companies have it seems like as they like, age, they're going out, we're going to get more open. And then as Mongo and Elastic and others come of age, they're like, oh, we need to be more proprietary.

**Peter Zaitsev:**  
Yeah, I mean, well, I think perception is what matters, right? Think about how long it took Microsoft, for example, to get some open source reputation. After we started to really aggressively pursue open source. Right. And yes, I think Amazon has been doing a lot in the open source market recently. It is still a selective, right, the right, I think Amazon selectively has certain things open certain things not like for, for various reasons, right. Like, for example, it's very interesting for me to see what they plan to open source with Microsoft compatibility level for Postgres, right. But at the same time, they're a document DB, which is, I, at least I heard, is essentially their MongoDB compatibility level or Postgres, right? They keep it in-house, not open source, right, for one reason, or another.

**Matt Yonkovit:**  
Well, and now that we've got like, these, these companies trying to protect their IP more. What are the dangers around  SSPL? Or, as I like to call it half-assed open source licenses, like, what do you see are the big drawbacks, and the dangers as we go forward?

**Peter Zaitsev:**  
Well, I think it's important to look at a few groups right out first, first, there is this kind of claim, oh what, if you are just using this software, you can see to continue using that for free, right. But this is kind of really not what open source is about, right? You can also say, hey what, you can use Facebook for free, right, either for free or 100 have on your mobile phone for free, and it's as good as open source? Well, we all know, right, especially with some recent scandals, right, it's not quite having that workout right. And so, there so, I would say there is a lot of additional value in open source beyond free as in free as a beer, right. So what does SSPL mean for you, if you are wanting to just use software first, then they start speaking about using the day databases, right the database as a service is the only model which is really valued by investor and that is for a good reason because that is a model which is really likely to dominate in the future for user, right? So if you want to use your favorite database in database as a service model What are your choices? Right? And folks who push SSPL for you, want to say, hey, the only valuable way the only way which will make sense in the future to deploy and use a Database-as-a-Service. We want to be a monopoly. We want to have a monopoly for that, right? And write and even ex-Oracle? Well, if you have been an Oracle customer, you know what it is to be an Oracle customer. Right? And chances are, you don't want that to happen to you again. Right. In that normal open source, there is a competition. Right? And the competition drives innovation. It has a more balanced relationship between vendors, and customers, right? And yet a lot of great stuff for customers and for the University of Lodge. Well, not so much. Maybe for the company shareholders, right? Because monopoly is a great thing. For business, right? If you're that monopoly.

**Matt Yonkovit:**  
Monopoly is a fun game, but I don't want to play it in real life.

**Peter Zaitsev:**  
Well, it's a fun game, right? It's not fun dealing with monopoly, right? Does a so-called customer.

**Matt Yonkovit:**  
So Peter, then your final word on this? Why choose open? Why choose Open Source? Why choose a more less restrictive license?

**Peter Zaitsev:**  
Well, I never want to use a case, right? So if you just look to use the software or open source, truly open source software that really gives you that freedom from locking and you are going to get more value, or in the end, right? We have more choices. I think what is also important is their innovation, right, which happens in open source software and not the MongoDB famously said, right, what we did not open source MongoDB to get help, right? We did that as a freemium model. And if you look at that MongoDB is not known for having a lot of contributors, right or CO creators. Yeah, it's a very closed ecosystem, right, right there. If you look at other successful projects, like Kubernetes, Linux, right, which have a that a lot of contributors and Elastic ecosystem was somewhere in between, for example, the core component of Elastic Lucene is on the right or governed by Apache Foundation has a lot of contributors, right. But where it makes sense to contribute to especially permissive open source, right, is because everybody benefits in the same way, right? It's a level playing field. And I think about giving ranges. For example, lots of companies give their name to contribute to that, and everybody benefits from the fruits of their labor. Now, if you want to contribute to MongoDB, for example, right now, what are you going to do? Well, MongoDB is going to say thank you, and you know what, they can sell it as an enterprise. They can monetize that and a cloud and you can do nothing of that. Now think if you want to be a contributor, would you contribute? Probably not right, SSPL and similar licenses, kill contribution, and that kills innovation slows innovation down, right? And that means what, from now on Elastic will essentially have to keep carrying on Elastic on their own shoulders.

**Matt Yonkovit:**  
All right. Thanks, Peter, for chatting with us and giving us your thoughts on SSPL and open source. 

**Peter Zaitsev:**  
Okay, thank you.
