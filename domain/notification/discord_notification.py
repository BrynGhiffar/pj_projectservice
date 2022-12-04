from adapter.discord.api import DiscordApi

class DiscordNotification:

    def __init__(self, api: DiscordApi):
        self.api = api
    
    def project_created_notification(self,project_id:str,project_members) -> None:

        title = "Project Uploaded!"
        message = "A new was Project has been uploaded."
        body = "```\n" \
            + "project_id: " + project_id + "\n" \
            + "Members: "
        for names in project_members:
            body += names + ' '
        body += "\n```\n"
        self.send_message(title, message, body)
