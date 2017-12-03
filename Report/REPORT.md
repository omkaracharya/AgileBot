## Presentation

## Report

#### 1. The problem your bot solved

Agile is the most widely used methodology in software development. Standups, grooming, backlog, scrum practices form the core essence of Agile. There are various tools that help in tracking/managing these processes but not automate them.  

This issue is very cruical in the software development company to improve the overall team effiiciency because A huge chunk of time is spent every day in menial agile processes. For instance, tasks like Sprint planning, triaging a bug, assigning a user story to an engineer are the tasks that can be automated to a major extent.   

We have proposed a AgileBot as a solution to solve this problem. AgileBot is a SlackBot that interfaces with Project planning tool Rally and GitHub. AgileBot solves three major use cases:  

* Auto assigns the unassigned bugs to the best engineer based on his workload.  

* Auto assigns the point to the user stories and assigns the user stories to the 'best' engineer after taking into consideration various heuristics.  

* User can request for his status. AgileBot will process the user's commit logs and returns his current status. 

#### 2. Primary features and screenshots

AgileBot provides 3 major features
1. Story Assignment
2. Status Updating
3. Backlog Grooming

**1. Story Assignment:** The team lead will request for a sprint plan and provide a list of team members and stories. The bot will provide possible story assignments and team lead confirms it. Bot creates sprint plan and posts link.

**2. Status Updating:** The user will request for a status update and provide the standup/team id/date. The bot will provide possible status updates based on commit logs. The user updated and/or confirms it. Bot posts user's status update to standup/team channel.

**3. Backlog Grooming:**  The scrum master will request for backlog grooming. The bot will provide possible point allocation to stories and scrum master confirms it. Bot assigns the points and posts the link.
