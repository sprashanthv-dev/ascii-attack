from command import Command


class HandleCommands():
  def execute(self, command: Command) -> None:
    command.execute()
    