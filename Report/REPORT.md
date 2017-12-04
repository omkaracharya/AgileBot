## Presentation

## Report

### 1. The problem your bot solved

Agile is the most widely used methodology in software development. Standups, grooming, backlog, scrum practices form the core essence of Agile. There are various tools that help in tracking/managing these processes but not automate them.  

This issue is very cruical in the software development company to improve the overall team effiiciency because A huge chunk of time is spent every day in menial agile processes. For instance, tasks like Sprint planning, triaging a bug, assigning a user story to an engineer are the tasks that can be automated to a major extent.   

We have proposed a AgileBot as a solution to solve this problem. AgileBot is a SlackBot that interfaces with Project planning tool Rally and GitHub. AgileBot solves three major use cases:  

* Auto assigns the unassigned bugs to the best engineer based on his workload.  

* Auto assigns the point to the user stories and assigns the user stories to the 'best' engineer after taking into consideration various heuristics.  

* User can request for his status. AgileBot will process the user's commit logs and returns his current status. 

### 2. Primary features and screenshots

AgileBot provides 3 major features
1. Story Assignment
2. Status Updating
3. Backlog Grooming

**1. Story Assignment:** The team lead will request for a sprint plan and provide a list of team members and stories. The bot will provide possible story assignments and team lead confirms it. Bot creates sprint plan and posts link.


**2. Status Updating:** The user will request for a status update and provide the standup/team id/date. The bot will provide possible status updates based on commit logs. The user updated and/or confirms it. Bot posts user's status update to standup/team channel.

![givemystatus](https://media.github.ncsu.edu/user/6216/files/2719700c-d84f-11e7-840e-5f066cf90bf0)

**3. Backlog Grooming:**  The scrum master will request for backlog grooming. The bot will provide possible point allocation to stories and scrum master confirms it. Bot assigns the points and posts the link.

![groombacklog](https://media.github.ncsu.edu/user/6216/files/4409ca40-d84f-11e7-880f-71d29c8adf6c)

### 3. Your reflection on the development process and project.

### 4. Any limitations and future work.

There is always a chance of improvement in everything. Here is the list of enhancement which we can do:

* Currently AgileBot will works with only fixed third party softwares like rally, github, trello because we have not exposed a generic interface to intergrate any kind of software management tools. This will make the AgileBot more useable becuase different companies uses differenet software management tools. For ex: mercurial instead of github.

* We can enhance the givemystatus logic. Currently AgileBot reports the user status only based on the number of github commits but if we standardised the github commit message like 
  
  ```
  Bug Id: <XYZ>
  Reviewer: <jsingh8 -- XYZ>
  ```

Then we can find out that this commit belongs to which Bug Id or Feature Id and based on this, we can report user status by mentioning, list of bugs reolved, lines of code checked in. 

* Similarly we can improve the story assignment task. Now AgileBoot calculate the workload of the each user based on the list of assigned task and then it will get to know the avilable quota for the user. And based on the Quota, it will assgin the task to a particular user.

But logically user might be busy in meeting or reviewing code of other people. so 
* we should look into the calender and take the meeting time as well into consideration while calculating user avilable time Quota. 
* we should check for the list of code reviews for that person and take corresponding time into consideration while calcualting user aviable time quota before assigning the story to him.
