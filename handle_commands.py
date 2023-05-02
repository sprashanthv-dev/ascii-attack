from command import Command


# The HandleCommands class servers as the 
# single point of entry for all command
# implementations within the game.
class HandleCommands():
  # Delegates the responsibility by invoking the 
  # execute() method of the passed in command class.
  def execute(self, command: Command) -> None:
    command.execute()
    