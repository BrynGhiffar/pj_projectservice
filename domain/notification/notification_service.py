from adapter.discord.api import DiscordApi

class NotificationService:

    def __init__(self, api: DiscordApi):
        self.api = api

    def send_message(self, title: str, message: str, body: str) -> None:
        to_be_sent = message + "\n"
        to_be_sent += f"> **{title}**\n"
        for line in body.splitlines():
            to_be_sent += f"> {line}\n"
        self.api.send_message(to_be_sent)
    
    def send_project_created_notification(self, project_id: str, project_title: str, project_short_description: str, project_member_ids: list[str]) -> None:

        title = "Project Uploaded!"
        message = "A new Project has been created."
        body = "```\n" \
            + "project id: " + project_id + "\n" \
            + "project title: " + project_title + "\n" \
            + "project short description: " + project_short_description + "\n" \
            + "member id: " + "\n"
        for ids in project_member_ids:
            body += "* " + ids + '\n'
        body += "\n```\n"
        self.send_message(title, message, body)
