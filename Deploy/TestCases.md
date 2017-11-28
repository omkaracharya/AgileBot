### Things to know before testing

1. __Rally__: To verify the changes made, you can use Rally credentials mentioned in [WORKSHEET.md](../Bot/WORKSHEET.md#rally-credential-for-instructors) 
2. __Slack__: Invitations have been sent out to TAs for joining `milestone-deployment` slack channel that has fully functioning @AgileBot included
3. __GitHub__: TAs have been added as collaborators to the GitHub repo `AgileBotTest` interfaced with our version of AgileBot. They are free to commit any code to execute last two test cases



## Acceptance Test cases


| Test Case | Current State | Input | Expected Result
| -------- | -------- | - | -------- |
| *Groom backlog success*     | <ol><li> There are stories in Rally with no points/estimates and no owner </li>                                  <li> These stories are in the sprint that falls over today's date </li><li> There is enough engineer quota to assign points to atleast one story </li></ol> | User mentions `@AgileBot groombacklog` (either in DM with @AgileBot or in any Slack channel with @AgileBot as a member) </td>| <ol><li> User should be shown with a tentative point assignment to all the stories. <li> If chosen `Yes`, AgileBot should write back the points/estimate to Rally  </li></ol>
| *Groom backlog failure*     | <ol><li> There are **NO** stories in Rally with no points/estimates and no owner </ol> | User mentions `@AgileBot groombacklog` (either in DM with @AgileBot or in any Slack channel with @AgileBot as a member) </td>| <ol><li> User should be shown a message `No stories in backlog to groom` </li></ol>
| *Plan Sprint success*     | <ol><li> There are stories in Rally with some points/estimates but **no** owner </li><li> These stories are present in the sprint that falls over today's date </li><li> There is enough engineer quota to assign points to atleast one story </li></ol> | User mentions `@AgileBot plansprint` (either in DM with @AgileBot or in any Slack channel with @AgileBot as a member) </td>| <ol><li> User should be shown with a tentative assignment of stories to engineers. <li> If chosen `Yes`, AgileBot should write back the owner(s) to these stories in Rally </li></ol>
| *Plan Sprint failure*     | <ol><li> There are **NO** stories without owners in the current sprint </ol> | User mentions `@AgileBot plansprint` (either in DM with @AgileBot or in any Slack channel with @AgileBot as a member) </td>| <ol><li> User should be shown a message `No stories in sprint to plan` </li></ol>|
| *Give My Status success*     | <ol><li> There is atleast one Git commit in team GitHub in past 36 Hours</li>                                 </ol> | User mentions `@AgileBot givemystatus` (preferrably in team's Slack channel having @AgileBot as a member) | <ol><li> An `emphemeral` message visible only to the user should be shown. This message should contain list of GitHub commit along with some useful info <li> If chosen `Yes` to submit, AgileBot should post this message in the channel and it should be visible to other members  </li></ol>
| *Give My Status failure*     | <ol><li> There are **NO** GitHub commits for the user in last 36 Hours</ol> | User mentions `@AgileBot givemystatus` (preferrably in team's Slack channel having @AgileBot as a member) | <ol><li> User should be shown a message `Currently you have no commits` </li></ol>
