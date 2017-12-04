## Project Presentation


## Report

### 1. The problem your our solved

Agile is the most widely used methodology in software development. Standups, grooming, backlog, scrum practices form the core essence of Agile. There are various tools that help in tracking/managing these processes but not automate them.  

This issue is very crucial in the software development company to improve the overall team efficiency because a huge chunk of time is spent every day in menial agile processes. For instance, tasks like Daily standups, triaging a bug, assigning a user story to an engineer are the tasks that can be automated to a major extent.

We have proposed AgileBot as a solution to solve this problem. AgileBot is a SlackBot that interfaces with Project planning tool Rally and GitHub. AgileBot solves three major use cases:  


* Auto assigns the point to the user stories based on their dependencies and priorities
* Auto assigns the user stories to the 'best' engineer after taking into consideration various heuristics and the engineer's workload.  
* Auto submits engineer's daily status from git ommit logs and metadata

### 2. Primary features and screenshots

AgileBot provides 3 major features
1. Backlog Grooming
2. Story Assignment
3. Status Updating



**1. Backlog Grooming:**  The scrum master will request for backlog grooming. The bot will provide possible point allocation to stories and scrum master confirms it. Bot assigns the points and posts the link.

![groombacklog](https://media.github.ncsu.edu/user/6216/files/4409ca40-d84f-11e7-880f-71d29c8adf6c)

**2. Story Assignment:** The team lead will request assigning pending stories to his team members. The bot will provide possible story assignments and team lead confirms it. Bot posts the link.

![assignstories](https://media.github.ncsu.edu/user/6216/files/5fa2ba9a-d869-11e7-9d40-9f1a92a4015f)

**3. Status Updating:** The user will request a status update and provide the date. The bot will provide possible status updates based on commit logs. The user confirms it. Bot posts user's status update to standup/team channel.

![givemystatus](https://media.github.ncsu.edu/user/6216/files/2719700c-d84f-11e7-840e-5f066cf90bf0)

### 3. Your reflection on the development process and project.

### 4. Any limitations and future work.

There is always a chance of improvement in everything. Here is the list of enhancement which we can do:

* Currently AgileBot will work with only fixed third party softwares like Rally, GitHub, Trello because we have not exposed a generic interface to integrate any kind of software management tools. This will make the AgileBot more useable because different companies use different software management tools. For example: Mercurial instead of GitHub.

* We can enhance the `givemystatus` logic. Currently, AgileBot reports the user status only based on the number of GitHub commits but if we have standardized the GitHub commit message like 
  
  ```
  Bug Id: <XYZ>
  Reviewer: <jsingh8 -- XYZ>
  ```  
  Then AgileBot can find out that which commit the Bug Id or Feature Id belong to and thus it can report user status by mentioning, list of bugs resolved, lines of code checked in. 

* Similarly we can improve the story assignment task. Currently, AgileBoot calculates the workload of each user based on the list of assigned task and then it will get to know the available quota for the user. And based on the quota, it will assign the task to a particular user.

  But logically user might be busy in meetings or reviewing code of other people. so 
  1. we should look into the calendar and take the meeting time as well into consideration while calculating user available time quota. 
  2. we should check the list of code reviews for that person and take corresponding time into consideration while calculating user available time quota before assigning the story to him.
  3. Also, we can track the history of the bug fixes an engineer has done so as to label her as an 'expert' in that field so as to assign relevant stories to her.
