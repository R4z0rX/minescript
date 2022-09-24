# SPDX-FileCopyrightText: © 2022 Greg Christiana <maxuser@minescript.net>
# SPDX-License-Identifier: GPL-3.0-only

# WARNING: This file is generated from the Minescript jar file. This file will
# be overwritten automatically when Minescript updates to a new version. If you
# make edits to this file, make sure to save a backup copy when upgrading to a
# new version of Minescript.

"""minescript v2.1 distributed via Minescript jar file

Usage: import minescript  # from Python script

User-friendly API for scripts to make function calls into the
Minescript mod.  This module should be imported by other
scripts and not run directly.
"""

import os
import sys
from minescript_runtime import CallScriptFunction, CallAsyncScriptFunction
from typing import Any, List, Set, Dict, Tuple, Optional, Callable


def execute(command: str):
  """Executes the given command.

  If command doesn't already start with a slash or backslash, automatically
  prepends a slash. Ignores leading and trailing whitespace, and ignores empty
  commands.
  """
  command = command.strip()
  if not command:
    return
  if command[0] not in ("/", "\\"):
    command = "/" + command
  print(command)


# Alias the built-in exec as pyexec because exec gets redefined below.
# TODO(maxuser): Remove this in minescript v3.0.
pyexec = exec


# TODO(maxuser): Remove this in minescript v3.0.
def exec(command: str):
  """Executes the given command.

  @deprecated: Use minescript.execute to avoid conflict with built-in exec.

  If command doesn't already start with a slash or backslash, automatically
  prepends a slash. Ignores leading and trailing whitespace, and ignores empty
  commands.
  """
  return execute(command)


def echo(message: Any):
  """Echoes message to the chat.

  The echoed message is visible only to the local player.
  """
  print(message, file=sys.stderr)


def chat(message: str):
  """Sends the given message to the chat.

  If message starts with a slash or backslash, automatically prepends a space
  so that the message is sent as a chat and not executed as a command.  Ignores
  empty messages.
  """
  if not message:
    return
  # If the message starts with a slash or backslash, prepend a space so that
  # the message is printed and not executed as a command.
  if message[0] in ("/", "\\"):
    message = " " + message
  print(message)


def screenshot(filename=None):
  """Takes a screenshot, similar to pressing the F2 key.

  Args:
    filename: if specified, screenshot filename relative to the screenshots directory; ".png"
      extension is added to the screenshot file if it doesn't already have a png extension.

  Returns:
    True is successful
  """
  if filename is None:
    return CallScriptFunction("screenshot")
  else:
    if os.path.sep in filename:
      echo(f'Error: `screenshot` does not support filenames with "{os.path.sep}" character.')
      return False
    else:
      if not filename.lower().endswith(".png"):
        filename += ".png"
      return CallScriptFunction("screenshot", filename)


def flush():
  """Wait for all previously issued script commands from this job to complete."""
  return CallScriptFunction("flush")


def player_name():
  """Gets the local player's name."""
  return CallScriptFunction("player_name")


def player_position(done_callback=None):
  """Gets the local player's position.

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    if done_callback is None, returns player's position as [x, y, z]
  """
  if done_callback is None:
    return CallScriptFunction("player_position")
  else:
    CallAsyncScriptFunction("player_position", done_callback)


def player_hand_items(done_callback=None):
  """Gets the items in the local player's hands.

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    If done_callback is None, returns items in player's inventory as list of
    items where each item is a dict: {"item": str, "count": int, "nbt": str}
  """
  if done_callback is None:
    return CallScriptFunction("player_hand_items")
  else:
    CallAsyncScriptFunction("player_hand_items", done_callback)


def player_inventory(done_callback=None):
  """Gets the items in the local player's inventory.

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    If done_callback is None, returns items in player's inventory as list of
    items where each item is a dict: {"item": str, "count": int, "nbt": str}
  """
  if done_callback is None:
    return CallScriptFunction("player_inventory")
  else:
    CallAsyncScriptFunction("player_inventory", done_callback)


def player_press_forward(pressed: bool):
  """Starts/stops moving the local player forward, simulating press/release of the 'w' key.

  Args:
    pressed: if True, go forward, otherwise stop doing so
  """
  return CallScriptFunction("player_press_forward", pressed)


def player_press_backward(pressed: bool):
  """Starts/stops moving the local player backward, simulating press/release of the 's' key.

  Args:
    pressed: if True, go backward, otherwise stop doing so
  """
  return CallScriptFunction("player_press_backward", pressed)


def player_press_left(pressed: bool):
  """Starts/stops moving the local player to the left, simulating press/release of the 'a' key.

  Args:
    pressed: if True, move to the left, otherwise stop doing so
  """
  return CallScriptFunction("player_press_left", pressed)


def player_press_right(pressed: bool):
  """Starts/stops moving the local player to the right, simulating press/release of the 'd' key.

  Args:
    pressed: if True, move to the right, otherwise stop doing so
  """
  return CallScriptFunction("player_press_right", pressed)


def player_press_jump(pressed: bool):
  """Starts/stops the local player jumping, simulating press/release of the space key.

  Args:
    pressed: if True, jump, otherwise stop doing so
  """
  return CallScriptFunction("player_press_jump", pressed)


def player_press_sprint(pressed: bool):
  """Starts/stops the local player sprinting, simulating press/release of the left control key.

  Args:
    pressed: if True, sprint, otherwise stop doing so
  """
  return CallScriptFunction("player_press_sprint", pressed)


def player_press_sneak(pressed: bool):
  """Starts/stops the local player sneaking, simulating press/release of the left shift key.

  Args:
    pressed: if True, sneak, otherwise stop doing so
  """
  return CallScriptFunction("player_press_sneak", pressed)


def player_press_pick_item(pressed: bool):
  """Starts/stops the local player picking an item, simulating press/release of the middle mouse button.

  Args:
    pressed: if True, pick an item, otherwise stop doing so
  """
  return CallScriptFunction("player_press_pick_item", pressed)


def player_press_use(pressed: bool):
  """Starts/stops the local player using an item or selecting a block, simulating press/release of the right mouse button.

  Args:
    pressed: if True, use an item, otherwise stop doing so
  """
  return CallScriptFunction("player_press_use", pressed)


def player_press_attack(pressed: bool):
  """Starts/stops the local player attacking or breaking a block, simulating press/release of the left mouse button.

  Args:
    pressed: if True, press attack, otherwise stop doing so
  """
  return CallScriptFunction("player_press_attack", pressed)


def player_press_swap_hands(pressed: bool):
  """Starts/stops moving the local player swapping hands, simulating press/release of the 'f' key.

  Args:
    pressed: if True, swap hands, otherwise stop doing so
  """
  return CallScriptFunction("player_press_swap_hands", pressed)


def player_press_drop(pressed: bool):
  """Starts/stops the local player dropping an item, simulating press/release of the 'q' key.

  Args:
    pressed: if True, drop an item, otherwise stop doing so
  """
  return CallScriptFunction("player_press_drop", pressed)


def player_orientation():
  """Gets the local player's orientation.

  Returns:
    (yaw: float, pitch: float) as angles in degrees
  """
  return CallScriptFunction("player_orientation")


def player_set_orientation(yaw: float, pitch: float):
  """Sets the local player's orientation.

  Args:
    yaw: degrees rotation of the local player's orientation around the y axis
    pitch: degrees rotation of the local player's orientation from the x-z plane

  Returns:
    True if successful
  """
  return CallScriptFunction("player_set_orientation", yaw, pitch)


def players():
  """Gets a list of nearby players and their attributes: name, position, velocity, etc."""
  return CallScriptFunction("players")


def entities():
  """Gets a list of nearby entities and their attributes: name, position, velocity, etc."""
  return CallScriptFunction("entities")


def getblock(x: int, y: int, z: int, done_callback=None):
  """Gets the type of block at position (x, y, z).

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    if done_callback is None, returns the block type at (x, y, z) as a string
  """
  if done_callback is None:
    return CallScriptFunction("getblock", x, y, z)
  else:
    CallAsyncScriptFunction("getblock", (x, y, z), done_callback)


def getblocklist(positions: List[List[int]], done_callback=None):
  """Gets the types of block at the specified [x, y, z] positions.

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    if done_callback is None, returns the block types at given positions as list of strings
  """
  if done_callback is None:
    return CallScriptFunction("getblocklist", positions)
  else:
    CallAsyncScriptFunction("getblocklist", (positions,), done_callback)


def await_loaded_region(x1: int, z1: int, x2: int, z2: int, done_callback=None):
  """Notifies the caller when the region from (x1, z1) to (x2, z2) is loaded.

  Args:
    done_callback: if given, return immediately and call done_callback(return_value)
        asynchronously when return_value is ready

  Returns:
    if done_callback is None, returns True when the requested region is fully loaded.
  """
  if done_callback is None:
    return CallScriptFunction("await_loaded_region", x1, z1, x2, z2)
  else:
    CallAsyncScriptFunction(
        "await_loaded_region", (x1, z1, x2, z2), done_callback)


def register_chat_message_listener(listener: Callable[[str], None]):
  """Registers a listener for receiving chat messages. One listener allowed per job.

  Listener receives both incoming and outgoing chat messages.

  See also register_chat_message_interceptor() for swallowing outgoing chat
  messages.

  Args:
    listener: callable that repeatedly accepts a string representing chat messages
  """
  CallAsyncScriptFunction(
      "register_chat_message_listener", (), listener)


def unregister_chat_message_listener():
  """Unegisters a chat message listener, if any, for the currently running job.

  Returns:
    True if successfully unregistered a listener, False otherwise.
  """
  CallScriptFunction("unregister_chat_message_listener")


def register_chat_message_interceptor(interceptor: Callable[[str], None]):
  """Registers an interceptor for swallowing chat messages.

  An interceptor swallows outgoing chat messages, typically for use in
  rewriting outgoing chat messages by calling minecraft.chat(str), e.g. to
  decorate or post-process outgoing messages automatically before they're sent
  to the server.  Only one interceptor is allowed at a time within a Minecraft
  instance.

  See also register_chat_message_listener() for non-destructive listening of
  chat messages.

  Args:
    interceptor: callable that repeatedly accepts a string representing chat messages
  """
  CallAsyncScriptFunction(
      "register_chat_message_interceptor", (), interceptor)


def unregister_chat_message_interceptor():
  """Unegisters the chat message interceptor, if one is currently registered.

  Returns:
    True if successfully unregistered an interceptor, False otherwise.
  """
  CallScriptFunction("unregister_chat_message_interceptor")
