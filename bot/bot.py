from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.dialogs import DialogSet, Dialog

class TeamsBot(ActivityHandler):
    def __init__(self, dialog: Dialog):
        self.dialog = dialog
        self.dialog_set = DialogSet()

    async def on_message_activity(self, turn_context: TurnContext):
        # Run the dialog
        dialog_context = await self.dialog.create_context(turn_context)
        await dialog_context.continue_dialog()
        if not turn_context.responded:
            await dialog_context.begin_dialog("MainDialog")
