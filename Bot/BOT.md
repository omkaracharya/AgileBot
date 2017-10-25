# Bot Milestone

## 1. Use Cases
Feedback from the initial [Design Proposal](../Design/Design.md):
* Refocus [Use Case 3](../Design/Design.md#use-case-3-backlog-grooming):
* Text-only output would get very long, consider more concise output + action buttons:

The updated [Design Proposal](../Design/Design.md) includes the above modifications.

## 2. Mocking
<!-- Authority pattern -->
## 3. Bot Implementation
### Bot Platform:
We have used `SlackClient` in `Python` to create a slack bot called `AgileBot`. We have created a slack channel [#agilebot-test](https://csc510project.slack.com/messages/agilebot-test/) and have added `AgileBot` to the channel. Now, whenever a user wants to use the bot, he has to call the bot using `@AgileBot` followed by a proper command. Also, direct messages to the bot is also allowed using the same bot tag.

### Bot Integration:
We have a fully operational `Slack bot` that responds to the commands `plansprint`, `givemystatus`, and `groombacklog`. If the user enters an invalid command or argument, the bot replies with the `Usage` containing the following commands:

**Commands:**
  * `plansprint`: Using this command, stories are assigned to the team members. To do this, the user needs to provide the date of the sprint to be planned along with the command. If the date is not provided, then the bot takes the current date as the default date.
  * `givemystatus`: Using this command, a team member is able to provide his/her status. The status contains user's `GitHub` commits for the given date. The current date is taken if no date parameter is passed.
  * `groombacklog`: Using this command, the `Scrum Master` is able to assign points to the stories in the backlog. 
  
  Here is how the channel looks like:  
    
  ![Bot Platform](../Bot/bot_platform.PNG)
  

## 4. Selenium testing of each use case
Currently, we have implemented 6 selenium tests, 2 for each use case for `happy` and `alternate` paths respectively.

### Overview for each test:
* Selenium Test runs the bot application on a daemon thread so a separate invocation is not required.
* Selenium also setups the required mock environment so that they can be executed independently.
* Selenium logs in as 'Tester' user in the slack project.
* It invokes each use case twice (happy and alternate)
* Currently, the happy and alternate paths are distinguished by a mock decision on the date. Odd date invokes the happy path and an even date invokes the alternate path.
* The test first asserts that a successful message has been sent to the slack channel. Then it checks the following messages for AgileBot's response for up to 5 seconds (customizable). This makes sure that a stale response doesn't pass the test and only a new response is valid. The test fails if it doesn't get a response in time or the response doesn't match the expected response. All of these are executed by xpath queries.

## 5. Task Tracking
All iterations and the associated tasks are included in this [Worksheet](WORKSHEET.md)

## 6. Screencast
The screencast for this milestone can be found [here]()
