# Design Milestone

## 1. Problem Statement

### What is the problem?
Agile is the most widely used methodology in software development. Standups, grooming, backlog, scrum practices form the core essence of Agile. There are various tools that help in tracking/managing these processes but not automate them.


### Why is it a problem?
A huge chunk of time is spent every day in menial agile processes. For instance, tasks like Sprint planning, triaging a bug, assigning a user story to an engineer are the tasks that can be automated to a major extent.


## 2. Bot Description
<!--What does your bot do? -->
AgileBot is a [SlackBot](https://get.slack.help/hc/en-us/articles/202026038) that interfaces with Project planning tool (JIRA, Tiaga). When called for its services, it looks up for unassigned bugs and user stories. It minimizes the agile overhead by estimating time frame and assigning user stories to the 'best' engineer after taking into consideration various heuristics

<!--Why is a bot a good solution for the problem? -->
AgileBot's mission is to automate these repetitive tasks to a degree that will speed up the overall processes. With AgileBot, a significant amount of time can be saved.

<!-- Does your bot have a conversation with users (e.g. hubot), or does it just response to events (e.g., coveralls bot on GitHub)? -->

* @AgileBot can be added to the team's Slack Room. From sprint planning, a Scrum master can invoke AgileBot by mentioning it to `PlanSprint`.
* Engineers working as a part of the sprint can submit their standup contents by mentioning AgileBot with text `GiveMyStatus`.
* Scrum Master can view her entire team's status by calling `GetTeamStatus`

<!-- Does your bot fit in one of the categories we talked about in class? A code drone vs documentation bot? -->
> We think that our bot fits into **Space Reactor category**.

<!--
2.1 Input?
2.2 Workflow
2.3 Output/suggestions
-->

## 3. Use Cases

### Use case 1: Story Assignment

**1. Preconditions**  
* Agile platform with APIs available for automation.
* Stories with points assigned.
* Users with available quotas.
* Teams with user information and roles.
  
**2. Main Flow**
    The team lead will request for a `sprint plan` and provide a list of team members and stories [S1]. The bot will provide possible story assignments and team lead confirms [S2]. Bot creates sprint plan [S3] and posts link [S4].

**3. Subflows**

    [S1] Provide the list of team members and stories    
    [S2] Provide possible story assignments    
    [S3] Create a sprint plan    
    [S4] Post the link
    
**4. Alternative Flows**

    [E1] No team members are available.


### Use case 2: Status Updating

**1. Preconditions**
* User must have commits with the description in the system.
* Bot should have read access to user commits.
* Teams with user information and roles.  

**2. Main Flow**
   The user will request for a `status update` and provide the standup/team id [S1]. The bot will provide possible status updates based on commit logs and the user confirms [S2]. Bot posts user's status update to standup/team channel [S3].

**3. Subflows**

    [S1] Provide list of attendees    
    [S2] Provide possible meeting times    
    [S3] Create a meeting    
    [S4] Post the link
    
**4. Alternative Flows**

    [E1] No team members are available.


### Use case 3: Backlog Grooming

**1. Preconditions**
* Stories and bugs with assigned priorities.
* Users with available quotas.
* Teams with user information and roles.

**2. Main Flow**
    The scrum master will request `backlog grooming` and provide a list of team members, stories, and bugs [S1]. The bot will provide possible `point allocation` and scrum master confirms [S2]. Bot assigns the points [S3], creates the sprint plan [S4] and posts the link [S5].

**3. Subflows**

    [S1] Provide list of team members, stories, and bugs    
    [S2] Provide possible `point allocation`      
    [S3] Assign the points    
    [S4] Create the sprint plan    
    [S5] Post the link  

**4. Alternative Flows**

    [E1] No team members are available.
    

## 4. Design Sketches

### Wireframe
<!-- Create a wireframe mockup of your bot in action. -->

### Storyboard
<!-- Create a storyboard that illustrates the primary task that a user undergoes with bot. -->

## 5. Architecture Design + Additional Patterns

<!-- This section should be several diagrams + paragraphs of text. This is the opportunity to really think through how you might build your system. Consider all the criteria listed here in your description. Generic architectures that do not properly reflect a solution will receive low scores. -->

### Architectural Diagram
<!-- Create a diagram that illustrates the components of your bot, the platform it is embedded in, third-party services it may use, data storage it may require, etc. -->

### Architecture components
<!-- Describe the architecture components in text. -->

### Constraints/Guidelines
<!-- Describe any constraints or guidelines that should be established in building software for your architecture (e.g., a bot cannot send data from one user to another user). -->
Only Scrum master can call `PlanSprint`

### Additional Design Patterns
<!-- Describe any additional design patterns that may be relevant for your bot design. -->
