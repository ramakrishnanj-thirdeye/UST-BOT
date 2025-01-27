import requests
from botbuilder.core import TurnContext
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogSet, OAuthPrompt, OAuthPromptSettings
from botbuilder.dialogs.prompts import PromptOptions
from botbuilder.schema import Activity

from bot.config import Config


class MainDialog(DialogSet):
    def __init__(self):
        super().__init__()
        self.add(OAuthPrompt("OAuthPrompt", OAuthPromptSettings(
            connection_name=Config.AAD_CONNECTION_NAME,
            text="Please sign in to proceed.",
            title="Sign In"
        )))
        self.add(WaterfallDialog("MainDialog", [self.prompt_for_login, self.call_prompt_flow]))

    async def prompt_for_login(self, step_context: WaterfallStepContext):
        # Prompt the user to log in using Azure AD OAuth
        return await step_context.begin_dialog("OAuthPrompt")

    async def call_prompt_flow(self, step_context: WaterfallStepContext):
        # Retrieve OAuth token and fetch user email
        token_response = step_context.result
        if token_response:
            headers = {"Authorization": f"Bearer {token_response.token}"}
            user_profile = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
            user_email = user_profile.get("mail") or user_profile.get("userPrincipalName")

            # Call Prompt Flow with user query and email
            user_query = step_context.context.activity.text  # Get user query from Teams
            payload = {
                "inputs": {
                    "chat_history": [],
                    "question": user_query,
                    "user_email": user_email
                }
            }
            prompt_flow_headers = {
                "Authorization": f"Bearer {Config.PROMPT_FLOW_API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(Config.PROMPT_FLOW_URL, headers=prompt_flow_headers, json=payload)

            if response.status_code == 200:
                result = response.json().get("outputs", {}).get("response_text", "No response from Prompt Flow.")
                await step_context.context.send_activity(f"Prompt Flow Response: {result}")
            else:
                await step_context.context.send_activity(f"Failed to call Prompt Flow: {response.status_code}")
        else:
            await step_context.context.send_activity("Unable to retrieve user email.")
        return await step_context.end_dialog()
