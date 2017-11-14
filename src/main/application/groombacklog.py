# Use Case: groom backlog

from datetime import datetime
import networkx as nx

from main.application.authority import get_action_authorized
from main.data.commands import GROOMBACKLOG
from main.service.rally import get_ungroomed_stories


class GroomBacklog:
    def __init__(self):
        self.date = datetime.today()
        self.command = GROOMBACKLOG
        self.RESPONSE_HEADER = "Tentatively Groomed Backlog:"
        self.INVALID_RESPONSE = "\nNo stories in backlog to groom."
        self.PER_USER_QUOTA = 13
        self.STORY_BASE_POINTS = 5
        self.TASK_BASE_POINTS = 3

    def get_response(self, user, all_users, request, rally):
        if request:
            date = request[0]
            try:
                self.date = datetime.strptime(date, "%m/%d/%Y")
            except Exception as e:
                self.date = datetime.today()

        response = self.RESPONSE_HEADER
        backlog = get_ungroomed_stories(self.date)
        perform_action = get_action_authorized(self, self.groom)

        if backlog:
            stories = [story for story in backlog]
            sprint_quota = len(all_users) * self.PER_USER_QUOTA
            perform_action(stories, sprint_quota)
            response += '\n' + '\n'.join(
                ['Story #' + story.FormattedID + ': ' + story.Name +
                 ' (Points: ' + str(story.PlanEstimate) + ')'
                 for story in stories])
        else:
            response += self.INVALID_RESPONSE
        return response


    def groom(self, stories, quota_left):

        ordering_criteria = [
            'Expedite',
            'whenCreated'
        ]

        chainedStories = [story for story in stories
                          if story.Predecessors or story.Successors]
        self.sort_stories(chainedStories)

        independentStories = list(set(stories) - set(chainedStories))
        for criterion in reversed(ordering_criteria):
            self.sort_stories(independentStories, criterion=criterion)

        tp_sorted_stories = self.sort_topological(chainedStories)

        # self.print_stories(tp_sorted_stories)
        # self.print_stories(independentStories)

        quota_left = self.assign_points_wrapper(quota_left, tp_sorted_stories)
        quota_left = self.assign_points_wrapper(quota_left, independentStories)


    def assign_points_wrapper(self, quota_left, sorted_stories):
        for sorted_story in sorted_stories:
            if quota_left < 1:
                break
            quota_left = self.assign_points(sorted_story, quota_left)
        return quota_left

    def print_stories(self, stories):
        print([story.Name + " | " + ("Expedite" if story.Expedite else "")
               for story in stories])


    def sort_topological(self, chainedStories):
        G = nx.DiGraph()
        for story in chainedStories:
            # print(story.Predecessors)
            if not G.has_node(story.FormattedID):
                G.add_node(story.FormattedID, story=story)
            else:
                G.nodes[story.FormattedID]['story'] = story

            if story.Predecessors:
                [G.add_edge(dependent.FormattedID, story.FormattedID)
                 for dependent in story.Predecessors]

        sorted_stories = [G.nodes[key]['story'] for key in nx.topological_sort(G)]

        return sorted_stories


    def get_count(self, obj):
        return (len(obj) if obj else 0)


    def sort_stories(self, list, criterion='Expedite'):
        if criterion is 'Expedite':
            list.sort(key=lambda x: (0 if x.Expedite else 1))
        if criterion is 'whenCreated':
            list.sort(key=lambda x: datetime.strptime(x.CreationDate, '%Y-%m-%dT%H:%M:%S.%fZ'))

    def assign_points(self, story, quota_left):
        estimated_points = self.STORY_BASE_POINTS \
                           + self.get_count(story.Successors) \
                           + (self.get_count(story.Tasks) * self.TASK_BASE_POINTS)

        if quota_left >= estimated_points:
            story.PlanEstimate = estimated_points
            quota_left -= estimated_points

        return quota_left
