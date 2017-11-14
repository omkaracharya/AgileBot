# Service that interacts with Rally.

from main.application.agilefactory import get_instance
from main.application.authority import is_authorized_date


def get_projects():
    rally = get_instance()
    for workspace in rally.getWorkspaces():
        print("Workspace: " + workspace.Name)
        projects = rally.getProjects(workspace=workspace.Name)
        for project in projects:
            print(project.oid, project.Name)


def get_iterations():
    rally = get_instance()
    iterations = rally.get('Iteration')
    return iterations


# Gets the active sprint at given date
def get_iteration_by_date(date):
    rally = get_instance()
    query = 'StartDate <= ' + date.strftime("%Y-%m-%d") + ' and EndDate >= ' + date.strftime("%Y-%m-%d")
    iterations = [it for it in rally.get('Iteration', query=query)]
    # for iteration in iterations:
    #     print(iteration.details())
    if iterations and len(iterations) > 0:
        return iterations[0]
    return None


def get_users():
    rally = get_instance()
    return rally.getAllUsers()


def get_user_info(user_oid):
    rally = get_instance()
    return rally.getUserInfo(user_oid)


def get_ungroomed_stories(start_date):
    if start_date and is_authorized_date(start_date):
        rally = get_instance()
        # Get the pending stories without any points assigned
        fields = "FormattedID,Name,PlanEstimate"
        criterion = "Owner = null and PlanEstimate = null or PlanEstimate = 0"
        stories = rally.get('UserStory', fetch=True, query=criterion)
        return stories
    return None


# Gets the stories for given sprint that are groomed but unassigned
def get_stories_for_sprint(iteration_oid):
    rally = get_instance()
    fields = "FormattedID,Name,PlanEstimate,Owner,Iteration"
    criterion = "PlanEstimate != null and Owner = null and Iteration.oid = " + str(iteration_oid)
    stories = rally.get('UserStory', fetch=fields, query=criterion)
    return stories


def get_user_capacities_for_iteration(iteration_oid):
    rally = get_instance()
    fields = "Capacity,User,Iteration,TaskEstimates"
    query = "Iteration.oid = " + str(iteration_oid)
    capacities = rally.get('UserIterationCapacity', query=query, fetch=fields)
    return capacities


def update_story_assignment(stories):
    rally = get_instance()
    for story in stories:
        if story.Owner:
            rally.post('UserStory', {'ObjectID': story.oid, 'Owner': story.Owner.oid})
