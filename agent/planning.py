class Planning:
    def __init__(self):
        """
        Initializes an empty list to store action plans.
        """
        self.action_plans = []

    def create_plan(self, reflection, memory_stream):
        """
        Creates high-level action plans based on the conclusions drawn from reflection and the current 
        environment. Each plan includes a location, a starting time, and a duration.

        Args:
            reflection (Reflection): an instance of the Reflection class.
            memory_stream (MemoryStream): an instance of the MemoryStream class.
        """
        pass

    def implement_plan(self):
        """
        Converts the high-level action plans into detailed behaviors for action and reaction.
        """
        pass

    def change_plan(self, new_plan):
        """
        Changes the current plan midstream if needed.

        Args:
            new_plan (dict): a new plan to replace the current one.
        """
        pass