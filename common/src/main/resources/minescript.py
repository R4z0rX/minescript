# SPDX-FileCopyrightText: © 2022-2024 Greg Christiana <maxuser@minescript.net>
# SPDX-License-Identifier: GPL-3.0-only

# WARNING: This file is generated from the Minescript jar file. This file will
# be overwritten automatically when Minescript updates to a new version. If you
# make edits to this file, make sure to save a backup copy when upgrading to a
# new version of Minescript.

"""minescript v4.0 distributed via Minescript jar file

Usage: import minescript  # from Python script

User-friendly API for scripts to make function calls into the
Minescript mod.  This module should be imported by other
scripts and not run directly.
"""

import base64
import json
import os
import queue
import sys
import minescript_runtime

from array import array
from dataclasses import dataclass, asdict
from minescript_runtime import (
    await_script_function, call_async_script_function, send_script_function_request,
    tick_loop, render_loop, script_loop,
    Task, run_tasks, schedule_tick_tasks, schedule_render_tasks,
    ScriptFunction, NoReturnScriptFunction,
    ExceptionHandler)
from typing import Any, List, Set, Dict, Tuple, Optional, Callable


BlockPos = Tuple[int, int, int]
"""Tuple representing `(x: int, y: int, z: int)` position in block space."""

Vector3f = Tuple[float, float, float]
"""Tuple representing `(x: float, y: float, z: float)` position or offset in 3D space."""


@dataclass
class MinescriptRuntimeOptions:
  legacy_dict_return_values: bool = False  # set to `True` to emulate behavior before v4.0

options = MinescriptRuntimeOptions()


def execute(command: str, _as_task=False):
  """Executes the given command.

  If `command` is prefixed by a backslash, it's treated as Minescript command,
  otherwise it's treated as a Minecraft command (the slash prefix is optional).

  *Note: This was named `exec` in Minescript 2.0. The old name is no longer
  available in v3.0.*

  Since: v2.1
  """
  if not _as_task and not isinstance(command, str):
    raise TypeError("Argument must be a string.")
  return (command,)

execute = NoReturnScriptFunction("execute", execute, conditional_task_arg=True)


def echo(*messages, _as_task=False):
  """Echoes plain-text messages to the chat.

  Echoed messages are visible only to the local player.

  If multiple args are given, join messages with a space separating them.

  Update in v4.0:
    Support multiple plain-text messages.

  Since: v2.0
  """
  if _as_task:
    return messages
  else:
    return (" ".join([str(m) for m in messages]),)

echo = NoReturnScriptFunction("echo", echo, conditional_task_arg=True)


def echo_json(json_text):
  """Echoes JSON-formatted text to the chat.

  Echoed text is visible only to the local player.

  `json_text` may be a string representing JSON text, or a list or dict. If it's a list or dict,
  convert it to a JSON string using the standard `json` module.

  Since: v4.0
  """
  if type(json_text) in (dict, list):
    json_text = json.dumps(json_text)

  return (json_text,)

echo_json = NoReturnScriptFunction("echo_json", echo_json)


def chat(*messages, _as_task=False):
  """Sends messages to the chat.

  If `messages[0]` is a str starting with a slash or backslash, automatically
  prepends a space so that the messages are sent as a chat and not executed as
  a command. If `len(messages)` is greater than 1, join messages with a space
  separating them.  Ignores empty `messages`.

  Update in v4.0:
    Support multiple messages.

  Since: v2.0
  """
  if _as_task:
    return messages
  else:
    return (" ".join([str(m) for m in messages]),)

chat = NoReturnScriptFunction("chat", chat, conditional_task_arg=True)


def log(*messages, _as_task=False):
  """Sends messages to latest.log.

  Update in v4.0:
    Support multiple messages of any type. Auto-convert messages to `str`.

  Since: v3.0
  """
  if _as_task:
    return messages
  else:
    return (" ".join([str(m) for m in messages]),)

log = NoReturnScriptFunction("log", log, conditional_task_arg=True)


def screenshot(filename=None):
  """Takes a screenshot, similar to pressing the F2 key.

  Args:
    filename: if specified, screenshot filename relative to the screenshots directory; ".png"
      extension is added to the screenshot file if it doesn't already have a png extension.

  Since: v2.1
  """
  return (filename,)

screenshot = ScriptFunction("screenshot", screenshot)


@dataclass
class JobInfo:
  job_id: int
  command: List[str]
  source: str
  status: str
  self: bool = False

def job_info() -> List[JobInfo]:
  """Return info about active Minescript jobs.

  Returns:
    `JobInfo`.  For the  enclosing job, `JobInfo.self` is `True`.

  Since: v4.0
  """
  return ()

def _job_info_result_transform(jobs):
  """(__internal__)"""
  return [JobInfo(**job) for job in jobs]

job_info = ScriptFunction("job_info", job_info, _job_info_result_transform)


def flush():
  """Wait for all previously issued script commands from this job to complete.

  Since: v2.1
  """
  return ()

flush = ScriptFunction("flush", flush)


def player_name() -> str:
  """Gets the local player's name.

  Since: v2.1
  """
  return ()

player_name = ScriptFunction("player_name", player_name)


def player_position() -> List[float]:
  """Gets the local player's position.

  Returns:
    player's position as [x: float, y: float, z: float]

  Update in v4.0:
    Removed `done_callback` arg. Use `async_player_position()` for async execution.
  """
  return ()

player_position = ScriptFunction("player_position", player_position)


@dataclass
class ItemStack:
  item: str
  count: int
  nbt: str = None
  slot: int = None
  selected: bool = None

@dataclass
class HandItems:
  main_hand: ItemStack
  off_hand: ItemStack

def player_hand_items() -> HandItems:
  """Gets the items in the local player's hands.

  Returns:
    Items in player's hands.
    (Legacy-style return value can be restored with `options.legacy_dict_return_values = True`)

  Update in v4.0:
    Return `HandItems` instead of `List[Dict[str, Any]]` by default.
    Removed `done_callback` arg. Use `async_player_hand_items()` for async execution.

  Since: v2.0
  """
  return ()

def _player_hand_items_result_transform(items):
  """(__internal__)"""
  if options.legacy_dict_return_values:
    return items
  main, off = items
  return HandItems(
      main_hand=None if main is None else ItemStack(**main),
      off_hand=None if off is None else ItemStack(**off))

player_hand_items = ScriptFunction(
    "player_hand_items", player_hand_items, _player_hand_items_result_transform)


def player_inventory() -> List[ItemStack]:
  """Gets the items in the local player's inventory.

  Returns:
    Items in player's inventory.
    (Legacy-style return value can be restored with `options.legacy_dict_return_values = True`)

  Update in v4.0:
    Return `List[ItemStack]` instead of `List[Dict[str, Any]]` by default.
    Removed `done_callback` arg. Use `async_player_inventory()` for async execution.

  Update in v3.0:
    Introduced `"slot"` and `"selected"` attributes in the returned
    dict, and `"nbt"` is populated only when NBT data is present. (In prior
    versions, `"nbt"` was always populated, with a value of `null` when NBT data
    was absent.)

  Since: v2.0
  """
  return ()

def _player_inventory_result_transform(items):
  """(__internal__)"""
  if options.legacy_dict_return_values:
    return items
  return [ItemStack(**item) for item in items]

player_inventory = ScriptFunction(
    "player_inventory", player_inventory, _player_inventory_result_transform)


def player_inventory_slot_to_hotbar(slot: int) -> int:
  """Swaps an inventory item into the hotbar.

  Args:
    slot: inventory slot (9 or higher) to swap into the hotbar

  Returns:
    hotbar slot (0-8) into which the inventory item was swapped

  Update in v4.0:
    Removed `done_callback` arg. Use `async_player_inventory_slot_to_hotbar(...)
    for async execution.

  Since: v3.0
  """
  return (slot,)

player_inventory_slot_to_hotbar = ScriptFunction(
    "player_inventory_slot_to_hotbar", player_inventory_slot_to_hotbar)


def player_inventory_select_slot(slot: int) -> int:
  """Selects the given slot within the player's hotbar.

  Args:
    slot: hotbar slot (0-8) to select in the player's hand

  Returns:
    previously selected hotbar slot

  Update in v4.0:
    Removed `done_callback` arg. Use `async_player_inventory_select_slot(...)` for async execution.

  Since: v3.0
  """
  return (slot,)

player_inventory_select_slot = ScriptFunction(
    "player_inventory_select_slot", player_inventory_select_slot)


def press_key_bind(key_mapping_name: str, pressed: bool):
  """Presses/unpresses a mapped key binding.

  Valid values of `key_mapping_name` include: "key.advancements", "key.attack", "key.back",
  "key.chat", "key.command", "key.drop", "key.forward", "key.fullscreen", "key.hotbar.1",
  "key.hotbar.2", "key.hotbar.3", "key.hotbar.4", "key.hotbar.5", "key.hotbar.6", "key.hotbar.7",
  "key.hotbar.8", "key.hotbar.9", "key.inventory", "key.jump", "key.left",
  "key.loadToolbarActivator", "key.pickItem", "key.playerlist", "key.right",
  "key.saveToolbarActivator", "key.screenshot", "key.smoothCamera", "key.sneak",
  "key.socialInteractions", "key.spectatorOutlines", "key.sprint", "key.swapOffhand",
  "key.togglePerspective", "key.use"

  Args:
    key_mapping_name: name of key binding
    pressed: if `True`, press the bound key, otherwise unpress it

  Since: v4.0
  """
  return (key_mapping_name, pressed)

press_key_bind = ScriptFunction("press_key_bind", press_key_bind)


def player_press_forward(pressed: bool):
  """Starts/stops moving the local player forward, simulating press/release of the 'w' key.

  Args:
    pressed: if `True`, go forward, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_forward = ScriptFunction("player_press_forward", player_press_forward)


def player_press_backward(pressed: bool):
  """Starts/stops moving the local player backward, simulating press/release of the 's' key.

  Args:
    pressed: if `True`, go backward, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_backward = ScriptFunction("player_press_backward", player_press_backward)


def player_press_left(pressed: bool):
  """Starts/stops moving the local player to the left, simulating press/release of the 'a' key.

  Args:
    pressed: if `True`, move to the left, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_left = ScriptFunction("player_press_left", player_press_left)


def player_press_right(pressed: bool):
  """Starts/stops moving the local player to the right, simulating press/release of the 'd' key.

  Args:
    pressed: if `True`, move to the right, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_right = ScriptFunction("player_press_right", player_press_right)


def player_press_jump(pressed: bool):
  """Starts/stops the local player jumping, simulating press/release of the space key.

  Args:
    pressed: if `True`, jump, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_jump = ScriptFunction("player_press_jump", player_press_jump)


def player_press_sprint(pressed: bool):
  """Starts/stops the local player sprinting, simulating press/release of the left control key.

  Args:
    pressed: if `True`, sprint, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_sprint = ScriptFunction("player_press_sprint", player_press_sprint)


def player_press_sneak(pressed: bool):
  """Starts/stops the local player sneaking, simulating press/release of the left shift key.

  Args:
    pressed: if `True`, sneak, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_sneak = ScriptFunction("player_press_sneak", player_press_sneak)


def player_press_pick_item(pressed: bool):
  """Starts/stops the local player picking an item, simulating press/release of the middle mouse button.

  Args:
    pressed: if `True`, pick an item, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_pick_item = ScriptFunction("player_press_pick_item", player_press_pick_item)


def player_press_use(pressed: bool):
  """Starts/stops the local player using an item or selecting a block, simulating press/release of the right mouse button.

  Args:
    pressed: if `True`, use an item, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_use = ScriptFunction("player_press_use", player_press_use)


def player_press_attack(pressed: bool):
  """Starts/stops the local player attacking or breaking a block, simulating press/release of the left mouse button.

  Args:
    pressed: if `True`, press attack, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_attack = ScriptFunction("player_press_attack", player_press_attack)


def player_press_swap_hands(pressed: bool):
  """Starts/stops moving the local player swapping hands, simulating press/release of the 'f' key.

  Args:
    pressed: if `True`, swap hands, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_swap_hands = ScriptFunction("player_press_swap_hands", player_press_swap_hands)


def player_press_drop(pressed: bool):
  """Starts/stops the local player dropping an item, simulating press/release of the 'q' key.

  Args:
    pressed: if `True`, drop an item, otherwise stop doing so

  Since: v2.1
  """
  return (pressed,)

player_press_drop = ScriptFunction("player_press_drop", player_press_drop)


def player_orientation():
  """Gets the local player's orientation.

  Returns:
    (yaw: float, pitch: float) as angles in degrees

  Since: v2.1
  """
  return ()

player_orientation = ScriptFunction("player_orientation", player_orientation)


def player_set_orientation(yaw: float, pitch: float):
  """Sets the local player's orientation.

  Args:
    yaw: degrees rotation of the local player's orientation around the y axis
    pitch: degrees rotation of the local player's orientation from the x-z plane

  Returns:
    True if successful

  Since: v2.1
  """
  return (yaw, pitch)

player_set_orientation = ScriptFunction("player_set_orientation", player_set_orientation)


@dataclass
class TargetedBlock:
  position: BlockPos
  distance: float
  side: str
  type: str

  # __getitem__ provided for backward compatibility with the list returned in prior versions.
  def __getitem__(self, i):
    if i == 0:
      return self.position
    elif i == 1:
      return self.distance
    elif i == 2:
      return self.side
    elif i == 3:
      return self.type
    else:
      raise ValueError("Expected integer from 0 to 3 but got " + repr(i))

def player_get_targeted_block(max_distance: float = 20):
  """Gets info about the nearest block, if any, in the local player's crosshairs.

  Args:
    max_distance: max distance from local player to look for blocks

  Returns:
    `TargetedBlock` for the block targeted by the player, or `None` if no block is targeted.

  Update in v4.0:
    Return value changed from `list` to `TargetedBlock`.

  Since: v3.0
  """
  return (max_distance,)

def _player_get_targeted_block_result_transform(targeted_block):
  return None if targeted_block is None else TargetedBlock(*targeted_block)

player_get_targeted_block = ScriptFunction(
    "player_get_targeted_block", player_get_targeted_block,
    _player_get_targeted_block_result_transform)


@dataclass
class EntityData:
  name: str
  type: str
  uuid: str
  id: int
  position: Vector3f
  yaw: float
  pitch: float
  velocity: Vector3f
  lerp_position: Vector3f = None
  health: float = None
  local: bool = None  # `True` if this the local player
  passengers: List[str] = None  # UUIDs of passengers as strings
  nbt: Dict[str, Any] = None


def player_get_targeted_entity(max_distance: float = 20, nbt: bool = False) -> EntityData:
  """Gets the entity targeted in the local player's crosshairs, if any.

  Args:
    max_distance: maximum distance to check for targeted entities
    nbt: if `True`, populate an `"nbt"` attribute for the player

  Returns:
    `EntityData` for the entity targeted by the player, or `None` if no entity is targeted.
    (Legacy-style returned dict can be restored with `options.legacy_dict_return_values = True`)

  Since: v4.0
  """
  return (max_distance, nbt)

def _player_get_targeted_entity_result_transform(entity):
  if options.legacy_dict_return_values:
    return entity
  return None if entity is None else EntityData(**entity)

player_get_targeted_entity = ScriptFunction(
    "player_get_targeted_entity", player_get_targeted_entity,
    _player_get_targeted_entity_result_transform)


def player_health() -> float:
  """Gets the local player's health.

  Since: v3.1
  """
  return ()

player_health = ScriptFunction("player_health", player_health)


def player(*, nbt: bool = False):
  """Gets attributes for the local player.

  Args:
    nbt: if `True`, populate the `nbt` field for the player

  Returns:
    `EntityData` representing a snapshot of values for the local player.
    (Legacy-style returned dict can be restored with `options.legacy_dict_return_values = True`)

  Since: v4.0
  """
  return (nbt,)

def _player_result_transform(entity):
  if options.legacy_dict_return_values:
    return entity
  return EntityData(**entity)

player = ScriptFunction("player", player, _player_result_transform)
get_player = player  # Alias for scripts with `player` variables.


def players(
    *, nbt: bool = False, uuid: str = None, name: str = None,
    position: Vector3f = None, offset: Vector3f = None, min_distance: float = None,
    max_distance: float = None, sort: str = None, limit: int = None):
  """Gets a list of nearby players and their attributes.

  Args:
    nbt: if `True`, populate an `"nbt"` attribute for each returned player
    uuid: regular expression for matching entities' UUIDs (optional)
    name: regular expression for matching entities' names (optional)
    position: position used with `offset`, `min_distance`, or `max_distance` to define a
        volume for filtering entities; default is the local player's position (optional)
    offset: offset relative to `position` for selecting entities (optional)
    min_distance: min distance relative to `position` for selecting entities (optional)
    max_distance: max distance relative to `position` for selecting entities (optional)
    sort: one of "nearest", "furthest", "random", or "arbitrary" (optional)
    limit: maximum number of entities to return (optional)

  Returns:
    `List[EntityData]` representing a snapshot of values for the selected players.
    (Legacy returned dicts can be restored with `options.legacy_dict_return_values = True`)

  Update in v4.0:
    Added args: uuid, name, type, position, offset, min_distance, max_distance, sort, limit.
    Return `List[EntityData]` instead of `List[Dict[str, Any]]` by default.
    Added `uuid` and `id` to returned players.

  Update in v3.1:
    Added `"health"` and `"local"` attributes, and `nbt` arg to output `"nbt"`
    attribute.

  Since: v2.1
  """
  return (nbt, uuid, name, position, offset, min_distance, max_distance, sort, limit)

def _players_result_transform(ents):
  if options.legacy_dict_return_values:
    return ents
  return [EntityData(**e) for e in ents]

players = ScriptFunction("players", players, _players_result_transform)
get_players = players  # Alias for scripts with `players` variables.


def entities(
    *, nbt: bool = False, uuid: str = None, name: str = None, type: str = None,
    position: Vector3f = None, offset: Vector3f = None, min_distance: float = None,
    max_distance: float = None, sort: str = None, limit: int = None):
  """Gets a list of nearby entities and their attributes.

  Args:
    nbt: if `True`, populate an `"nbt"` attribute for each returned entity (optional)
    uuid: regular expression for matching entities' UUIDs (optional)
    name: regular expression for matching entities' names (optional)
    type: regular expression for matching entities' types (optional)
    position: position used with `offset`, `min_distance`, or `max_distance` to define a
        volume for filtering entities; default is the local player's position (optional)
    offset: offset relative to `position` for selecting entities (optional)
    min_distance: min distance relative to `position` for selecting entities (optional)
    max_distance: max distance relative to `position` for selecting entities (optional)
    sort: one of "nearest", "furthest", "random", or "arbitrary" (optional)
    limit: maximum number of entities to return (optional)

  Returns:
    `List[EntityData]` representing a snapshot of values for the selected entities.
    (Legacy returned dicts can be restored with `options.legacy_dict_return_values = True`)

  Update in v4.0:
    Added args: uuid, name, type, position, offset, min_distance, max_distance, sort, limit.
    Return `List[EntityData]` instead of `List[Dict[str, Any]]` by default.
    Added `uuid`, `id`, and `passengers` (only for entities with passengers) to returned entities.

  Update in v3.1:
    Added `"health"` and `"local"` attributes, and `nbt` arg to output `"nbt"`
    attribute.

  Since: v2.1
  """
  return (nbt, uuid, name, type, position, offset, min_distance, max_distance, sort, limit)

def _entities_result_transform(ents):
  """(__internal__)"""
  if options.legacy_dict_return_values:
    return ents
  return [EntityData(**e) for e in ents]

entities = ScriptFunction("entities", entities, _entities_result_transform)
get_entities = entities  # Alias for scripts with `entities` variables.


@dataclass
class VersionInfo:
  minecraft: str
  minescript: str
  mod_loader: str
  launcher: str
  os_name: str
  os_version: str

def version_info() -> VersionInfo:
  """Gets version info for Minecraft, Minescript, mod loader, launcher, and OS.

  Returns:
    `VersionInfo`

  Since: v4.0
  """
  return ()

def _version_info_result_transform(info):
  return VersionInfo(**info)

version_info = ScriptFunction("version_info", version_info, _version_info_result_transform)


@dataclass
class WorldInfo:
  game_ticks: int
  day_ticks: int
  raining: bool
  thundering: bool
  spawn: BlockPos
  hardcore: bool
  difficulty: str
  name: str
  address: str

def world_info() -> WorldInfo:
  """Gets world properties.

  If the current world is a multiplayer world loaded from the server list, then
  the returned `name` and `address` attributes are the values as they appear in
  the server list; otherwise `name` is the name of the locally saved world and
  `address` is `localhost`.

  `day_ticks` are the ticks associated with the day-night cycle.

  Renamed from `world_properties()` from v3.1.

  Returns:
    `WorldInfo`

  Since: v4.0
  """
  return ()

def _world_info_result_transform(info):
  return WorldInfo(**info)

world_info = ScriptFunction("world_info", world_info, _world_info_result_transform)


def getblock(x: int, y: int, z: int) -> str:
  """Gets the type of block at position (x, y, z).

  Args:
    x, y, z: position of block to get

  Returns:
    block type at (x, y, z) as a string
  """
  return (x, y, z)

getblock = ScriptFunction("getblock", getblock)


def getblocklist(positions: List[List[int]]) -> List[str]:
  """Gets the types of block at the specified [x, y, z] positions.

  Args:
    list of positions as lists of x, y, z int coordinates, e.g. [[0, 0, 0], [0, 0, 1]]

  Returns:
    block types at given positions as list of strings

  Update in v4.0:
    Removed `done_callback` arg. Use `async_getblocklist(...)` for async execution.

  Since: v2.1
  """
  return (positions,)

getblocklist = ScriptFunction("getblocklist", getblocklist)


def await_loaded_region(x1: int, z1: int, x2: int, z2: int):
  """Waits for chunks to load in the region from (x1, z1) to (x2, z2).

  Args:
    x1, z1, x2, z2: bounds of the region for awaiting loaded chunks
    timeout: if specified, timeout in seconds to wait for the region to load

  Update in v4.0:
    Removed `done_callback` arg. Call now always blocks until region is loaded.
  """
  return (x1, z1, x2, z2)

await_loaded_region = ScriptFunction("await_loaded_region", await_loaded_region)


def register_key_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler for receiving keyboard events.

  For a more user-friendly API, use `EventQueue` instead. (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing key events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Returns:
    ID for the new handler.

  Update in v4.0:
    Added return value for identifying the newly registered handler.

  Since: v3.2
  """
  handler_id = await_script_function("register_key_listener", ())
  send_script_function_request(
      "start_key_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_mouse_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler for receiving mouse events.

  For a more user-friendly API, use `EventQueue` instead. (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing mouse events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Update in v4.0:
    Added return value for identifying the newly registered handler.

  Since: v4.0
  """
  handler_id = await_script_function("register_mouse_listener", ())
  send_script_function_request(
      "start_mouse_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_chat_message_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for chat messages.

  Handler receives both incoming and outgoing chat messages.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing chat message events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Update in v4.0:
    Added return value for identifying the newly registered handler.

  Update in v3.2:
    Added optional arg `exception_handler`.

  Since: v2.0

  See also:
    `register_chat_message_interceptor()` for swallowing outgoing chat messages
  """
  handler_id = await_script_function("register_chat_message_listener", ())
  send_script_function_request(
      "start_chat_message_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_chat_message_interceptor(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None,
    *, prefix: str = None, pattern: str = None) -> int:
  """Registers a handler for swallowing outgoing chat messages matching a prefix or pattern.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  The handler swallows outgoing chat messages, typically for use in
  rewriting outgoing chat messages by calling minecraft.chat(str), e.g. to
  decorate or post-process outgoing messages automatically before they're sent
  to the server.

  `prefix` or `pattern` can be specified, but not both. If neither `prefix` nor
  `pattern` is specified, all outgoing chat messages are intercepted.

  Args:
    handler: callable that repeatedly accepts chat message events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)
    prefix: if specified, intercept only the messages starting with this literal prefix
    pattern: if specified, intercept only the messages matching this regular expression

  Returns:
    ID for the new handler.

  Update in v4.0:
    Support filtering of intercepted messages via `prefix` and `pattern`.
    Added return value for identifying the newly registered listener.

  Since: v2.1

  See also:
    `register_chat_message_listener()` for non-destructive listening of chat messages
  """
  handler_id = await_script_function("register_chat_message_interceptor", (prefix, pattern))

  send_script_function_request(
      "start_chat_message_interceptor", (handler_id,), handler, exception_handler)

  return handler_id


def register_add_entity_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for entities being added.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing added entities
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_add_entity_listener", ())
  send_script_function_request(
      "start_add_entity_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_block_update_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for block update events.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing block updates
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_block_update_listener", ())
  send_script_function_request(
      "start_block_update_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_take_item_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for items being taken.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing a taken item
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_take_item_listener", ())
  send_script_function_request(
      "start_take_item_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_damage_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for damage events.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing damage events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_damage_listener", ())
  send_script_function_request(
      "start_damage_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_explosion_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for explosion events.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing explosion events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_explosion_listener", ())
  send_script_function_request(
      "start_explosion_listener", (handler_id,), handler, exception_handler)
  return handler_id


def register_chunk_listener(
    handler: Callable[[Dict[str, Any]], None], exception_handler: ExceptionHandler = None) -> int:
  """Registers a handler to listen for chunk load/unload events.

  For a more user-friendly API, use `EventQueue` instead.  (__internal__)

  Args:
    handler: callable that repeatedly accepts a dict representing chunk events
    exception_handler: callable for handling an `Exception` thrown from Java (optional)

  Since: v4.0
  """
  handler_id = await_script_function("register_chunk_listener", ())
  send_script_function_request(
      "start_chunk_listener", (handler_id,), handler, exception_handler)
  return handler_id


def unregister_event_handler(handler_id: int):
  """Unregisters an event handler, if any, for the currently running job. (__internal__)

  Args:
    handler_id: ID of an event handler returned from a `register_...()` function.

  Returns:
    `True` if `handler_id` was successfully cancelled, `False` otherwise.

  Since: v4.0
  """
  return await_script_function("unregister_event_handler", (handler_id,))


def cancel_scheduled_tasks(task_list_id: int):
  """Cancels a scheduled task list, if any, for the currently running job. (__internal__)

  Args:
    task_list_id: ID of task list returned from `schedule_tick_tasks()` or `schedule_render_tasks`.

  Returns:
    `True` if `task_list_id` was successfully cancelled, `False` otherwise.

  Since: v4.0
  """
  return await_script_function("cancel_scheduled_tasks", (task_list_id,))


@dataclass
class _EventType:
  KEY: str = "key"
  MOUSE: str = "mouse"
  CHAT: str = "chat"
  OUTGOING_CHAT_INTERCEPT: str = "outgoing_chat_intercept"
  ADD_ENTITY: str = "add_entity"
  BLOCK_UPDATE: str = "block_update"
  TAKE_ITEM: str = "take_item"
  DAMAGE: str = "damage"
  EXPLOSION: str = "explosion"
  CHUNK: str = "chunk"

EventType = _EventType()

@dataclass
class KeyEvent:
  """Key event data.

  For a list of key codes, see: https://www.glfw.org/docs/3.4/group__keys.html
  `action` is 0 for key up, 1 for key down, and 2 for key repeat.
  """
  type: str
  time: float
  key: int
  scan_code: int
  action: int
  modifiers: int
  screen: str

@dataclass
class MouseEvent:
  """Mouse event data.

  `action` is 0 for mouse up and 1 for mouse down.
  """
  type: str
  time: float
  button: int
  action: int
  modifiers: int
  x: float
  y: float
  screen: str = None

@dataclass
class ChatEvent:
  type: str
  time: float
  message: str

@dataclass
class AddEntityEvent:
  type: str
  time: float
  entity: EntityData

@dataclass
class BlockUpdateEvent:
  type: str
  time: float
  position: BlockPos
  old_state: str
  new_state: str

@dataclass
class TakeItemEvent:
  type: str
  time: float
  player_uuid: str
  item: EntityData
  amount: int

@dataclass
class DamageEvent:
  type: str
  time: float
  entity_uuid: str
  cause_uuid: str
  source: str

@dataclass
class ExplosionEvent:
  type: str
  time: float
  position: Vector3f
  blockpack_base64: str

@dataclass
class ChunkEvent:
  type: str
  time: float
  loaded: bool
  x_min: int
  z_min: int
  x_max: int
  z_max: int

def _create_add_entity_event(**kwargs):
  kwargs["entity"] = EntityData(**kwargs["entity"])
  return AddEntityEvent(**kwargs)

def _create_take_item_event(**kwargs):
  kwargs["item"] = EntityData(**kwargs["item"])
  return TakeItemEvent(**kwargs)

_EVENT_CONSTRUCTORS = {
  EventType.KEY: KeyEvent,
  EventType.MOUSE: MouseEvent,
  EventType.CHAT: ChatEvent,
  EventType.OUTGOING_CHAT_INTERCEPT: ChatEvent,
  EventType.ADD_ENTITY: _create_add_entity_event,
  EventType.BLOCK_UPDATE: BlockUpdateEvent,
  EventType.TAKE_ITEM: _create_take_item_event,
  EventType.DAMAGE: DamageEvent,
  EventType.EXPLOSION: ExplosionEvent,
  EventType.CHUNK: ChunkEvent,
}

class EventQueue:
  """Queue for managing events.

  Implements context management so that it can be used with a `with` expression
  to automatically unregister event listeners at the end of the block, e.g.

  ```
  with EventQueue() as event_queue:
    echo("Capturing key events...")
    event_queue.register_key_listener()
    while True:
      event = event_queue.get()
      if event.type == EventType.KEY:
        # Key code 93 is the `]` key.
        if event.key == 93:
          break
        echo(f"Captured key with code {event.key}.")

  echo("No longer capturing key events.")
  ```

  Since: v4.0
  """

  def __init__(self):
    """Creates an event registration handler."""
    self.queue = queue.Queue()
    self.event_handler_ids = []

  def register_key_listener(self):
    self._register(EventType.KEY, register_key_listener)

  def register_mouse_listener(self):
    self._register(EventType.MOUSE, register_mouse_listener)

  def register_chat_listener(self):
    self._register(EventType.CHAT, register_chat_message_listener)

  def register_outgoing_chat_interceptor(self, *, prefix: str = None, pattern: str = None):
    self._register(
        EventType.OUTGOING_CHAT_INTERCEPT,
        lambda handler, exception_handler: \
            register_chat_message_interceptor(
                handler, exception_handler, prefix=prefix, pattern=pattern))

  def register_add_entity_listener(self):
    self._register(EventType.ADD_ENTITY, register_add_entity_listener)

  def register_block_update_listener(self):
    self._register(EventType.BLOCK_UPDATE, register_block_update_listener)

  def register_take_item_listener(self):
    self._register(EventType.TAKE_ITEM, register_take_item_listener)

  def register_damage_listener(self):
    self._register(EventType.DAMAGE, register_damage_listener)

  def register_explosion_listener(self):
    self._register(EventType.EXPLOSION, register_explosion_listener)

  def register_chunk_listener(self):
    self._register(EventType.CHUNK, register_chunk_listener)

  def _register(self, event_type: str, registration_func):
    def put_typed_event(event):
      try:
        event["type"] = event_type
        self.queue.put(event)
      except Exception as e:
        exception_message = f"Exception in event handler for `{event_type}`: {e}"
        minescript_runtime.debug_log(exception_message)
        print(exception_message, file=sys.stderr)

    handler_id = registration_func(put_typed_event, self.queue.put)
    if type(handler_id) is not int:
      error_message = f"Expected registration function to return int but got `{self.handler_id}`"
      minescript_runtime.debug_log(error_message)
      raise ValueError(error_message)
    self.event_handler_ids.append(handler_id)

  def unregister_all(self):
    handler_ids = self.event_handler_ids
    self.event_handler_ids = []
    for handler_id in handler_ids:
      unregister_event_handler(handler_id)

  def get(self, block: bool = True, timeout: float = None) -> Any:
    """Gets the next event in the queue.

    Args:
      block: if `True`, block until an event fires
      timeout: timeout in seconds to wait for an event if `block` is `True`

    Returns:
      subclass-dependent event

    Raises:
      `queue.Empty` if `block` is `True` and `timeout` expires, or `block` is `False` and
      queue is empty.
    """
    value = self.queue.get(block, timeout)
    if isinstance(value, Exception):
      minescript_runtime.debug_log("Throwing exception from EventQueue.get:", value)
      raise value
    if type(value) is not dict or not "type" in value:
      error_message = f"Expected event dict with key `type` but got: {value}"
      minescript_runtime.debug_log(error_message)
      raise ValueError(error_message)
    return _EVENT_CONSTRUCTORS[value["type"]](**value)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.unregister_all()

  def __del__(self):
    self.unregister_all()


def KeyEventListener():
  """Deprecated listener for keyboard events. Use `EventQueue.register_key_listener` instead.

  Update in v4.0:
    Deprecated in favor of `EventQueue.register_key_listener`.

  Since: v3.2
  """
  print(
      "KeyEventListener is deprecated. Use `EventQueue.register_key_listener` instead.",
      file=sys.stderr)
  event_queue = EventQueue()
  event_queue.register_key_listener()
  return event_queue


def ChatEventListener():
  """Deprecated listener for chat message events.

  Use `EventQueue.register_chat_message_listener` instead.

  Update in v4.0:
    Deprecated in favor of `EventQueue.register_chat_message_listener`.

  Since: v3.2
  """
  print(
      "ChatEventListener is deprecated. "
      "Use `EventQueue.register_chat_listener()` instead.",
      file=sys.stderr)
  event_queue = EventQueue()
  event_queue.register_chat_listener()
  return event_queue


def screen_name() -> str:
  """Gets the current GUI screen name, if there is one.

  Returns:
    Name of current screen (str) or `None` if no GUI screen is being displayed.

  Since: v3.2
  """
  return ()

screen_name = ScriptFunction("screen_name", screen_name)


def show_chat_screen(show: bool, prompt: str = None) -> str:
  """Shows or hides the chat screen.

  Args:
    show: if `True`, show the chat screen; otherwise hide it
    prompt: if show is `True`, insert `prompt` into chat input box upon showing chat screen.

  Returns:
    `True` if chat screen was successfully shown (`show=True`) or hidden (`show=False`)

  Since: v4.0
  """
  return (show, prompt)

show_chat_screen = ScriptFunction("show_chat_screen", show_chat_screen)


def append_chat_history(message: str):
  """Appends `message` to chat history, available via up and down arrows in chat.

  Since: v4.0
  """
  return (message,)

append_chat_history = ScriptFunction("append_chat_history", append_chat_history)


def chat_input():
  """Gets state of chat input text.

  Returns:
    `[text, position]` where `text` is `str` and `position` is `int` cursor position within `text`

  Since: v4.0
  """
  return ()

chat_input = ScriptFunction("chat_input", chat_input)


def set_chat_input(text: str = None, position: int = None, color: int = None):
  """Sets state of chat input text.

  Args:
    text: if specified, replace chat input text
    position: if specified, move cursor to this position within the chat input box
    color: if specified, set input text color, formatted as 0xRRGGBB

  Since: v4.0
  """
  return (text, position, color)

set_chat_input = ScriptFunction("set_chat_input", set_chat_input)


def container_get_items() -> List[ItemStack]:
  """Gets all items in an open container (chest, furnace, etc. with slots).

  Returns:
    List of items if a container's contents are displayed; `None` otherwise.

  Since: v4.0
  """
  return ()

def _container_get_items_result_transform(items):
  if options.legacy_dict_return_values:
    return items
  return None if items is None else [ItemStack(**item) for item in items]

container_get_items = ScriptFunction(
    "container_get_items", container_get_items, _container_get_items_result_transform)


def player_look_at(x: float, y: float, z: float):
  """Rotates the camera to look at a position.

  Args:
    x: x position
    y: y position
    z: z position

  Since: v4.0
  """
  return (x, y, z)

player_look_at = ScriptFunction("player_look_at", player_look_at)


Rotation = Tuple[int, int, int, int, int, int, int, int, int]
"""Tuple of 9 `int` values representing a flattened, row-major 3x3 rotation matrix."""


class Rotations:
  """Common rotations for use with `BlockPack` and `BlockPacker` methods.

  Since: v3.0
  """

  IDENTITY: Rotation = (1, 0, 0, 0, 1, 0, 0, 0, 1)
  """Effectively no rotation."""

  X_90: Rotation = (1, 0, 0, 0, 0, 1, 0, -1, 0)
  """Rotate 90 degrees about the x axis."""

  X_180: Rotation = (1, 0, 0, 0, -1, 0, 0, 0, -1)
  """Rotate 180 degrees about the x axis."""

  X_270: Rotation = (1, 0, 0, 0, 0, -1, 0, 1, 0)
  """Rotate 270 degrees about the x axis."""

  Y_90: Rotation = (0, 0, 1, 0, 1, 0, -1, 0, 0)
  """Rotate 90 degrees about the y axis."""

  Y_180: Rotation = (-1, 0, 0, 0, 1, 0, 0, 0, -1)
  """Rotate 180 degrees about the y axis."""

  Y_270: Rotation = (0, 0, -1, 0, 1, 0, 1, 0, 0)
  """Rotate 270 degrees about the y axis."""

  Z_90: Rotation = (0, 1, 0, -1, 0, 0, 0, 0, 1)
  """Rotate 90 degrees about the z axis."""

  Z_180: Rotation = (-1, 0, 0, 0, -1, 0, 0, 0, 1)
  """Rotate 180 degrees about the z axis."""

  Z_270: Rotation = (0, -1, 0, 1, 0, 0, 0, 0, 1)
  """Rotate 270 degrees about the z axis."""

  INVERT_X: Rotation = (-1, 0, 0, 0, 1, 0, 0, 0, 1)
  """Invert the x coordinate (multiply by -1)."""

  INVERT_Y: Rotation = (1, 0, 0, 0, -1, 0, 0, 0, 1)
  """Invert the y coordinate (multiply by -1)."""

  INVERT_Z: Rotation = (1, 0, 0, 0, 1, 0, 0, 0, -1)
  """Invert the z coordinate (multiply by -1)."""


# TODO(maxuser): Move this into Rotations class and rename to compose(...).
def combine_rotations(rot1: Rotation, rot2: Rotation, /) -> Rotation:
  """Combines two rotation matrices into a single rotation matrix.

  Since: v3.0
  """
  return (
      rot1[0] * rot2[0] + rot1[1] * rot2[3] + rot1[2] * rot2[6],
      rot1[0] * rot2[1] + rot1[1] * rot2[4] + rot1[2] * rot2[7],
      rot1[0] * rot2[2] + rot1[1] * rot2[5] + rot1[2] * rot2[8],
      rot1[3] * rot2[0] + rot1[4] * rot2[3] + rot1[5] * rot2[6],
      rot1[3] * rot2[1] + rot1[4] * rot2[4] + rot1[5] * rot2[7],
      rot1[3] * rot2[2] + rot1[4] * rot2[5] + rot1[5] * rot2[8],
      rot1[6] * rot2[0] + rot1[7] * rot2[3] + rot1[8] * rot2[6],
      rot1[6] * rot2[1] + rot1[7] * rot2[4] + rot1[8] * rot2[7],
      rot1[6] * rot2[2] + rot1[7] * rot2[5] + rot1[8] * rot2[8])


def blockpack_read_world(
    pos1: BlockPos, pos2: BlockPos,
    rotation: Rotation = None, offset: BlockPos = None,
    comments: Dict[str, str] = {}, safety_limit: bool = True) -> int:
  """Creates a blockpack from blocks in the world within a rectangular volume.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    pos1, pos2: opposing corners of a rectangular volume from which to read world blocks
    rotation: rotation matrix to apply to block coordinates read from world
    offset: offset to apply to block coordiantes (applied after rotation)
    comments: key, value pairs to include in the new blockpack
    safety_limit: if `True`, fail if requested volume spans more than 1600 chunks

  Returns:
    an int id associated with a new blockpack upon success, `None` otherwise

  Since: v3.0
  """
  return (pos1, pos2, rotation, offset, comments, safety_limit)

blockpack_read_world = ScriptFunction("blockpack_read_world", blockpack_read_world)


def blockpack_read_file(filename: str) -> int:
  """Reads a blockpack from a file.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    filename: name of file to read; relative to Minecraft dir unless it's an absolute path
        (".zip" is automatically appended to filename if it does not end with that extension)

  Returns:
    an int id associated with a blockpack upon success

  Since: v3.0
  """
  return (filename,)

blockpack_read_file = ScriptFunction("blockpack_read_file", blockpack_read_file)


def blockpack_import_data(base64_data: str) -> int:
  """Creates a blockpack from base64-encoded serialized blockpack data.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    base64_data: base64-encoded string containing serialization of blockpack data.

  Returns:
    an int id associated with a blockpack upon success, `None` otherwise

  Since: v3.0
  """
  return (base64_data,)

blockpack_import_data = ScriptFunction("blockpack_import_data", blockpack_import_data)


def blockpack_block_bounds(blockpack_id: int) -> (BlockPos, BlockPos):
  """Returns bounding coordinates of blocks in the blockpack associated with blockpack_id.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Since: v3.0
  """
  return (blockpack_id,)

blockpack_block_bounds = ScriptFunction("blockpack_block_bounds", blockpack_block_bounds)


def blockpack_comments(blockpack_id: int) -> Dict[str, str]:
  """Returns comments stored in the blockpack associated with blockpack_id.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Since: v3.0
  """
  return (blockpack_id,)

blockpack_comments = ScriptFunction("blockpack_comments", blockpack_comments)


def blockpack_write_world(
    blockpack_id: int, rotation: Rotation = None, offset: BlockPos = None) -> bool:
  """Writes blocks from a blockpack into the current world. Requires setblock and fill commands.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    blockpack_id: id of a currently loaded blockpack
    rotation: rotation matrix to apply to block coordinates before writing to world
    offset: offset to apply to block coordiantes (applied after rotation)

  Returns:
    `True` upon success

  Since: v3.0
  """
  return (blockpack_id, rotation, offset)

blockpack_write_world = ScriptFunction("blockpack_write_world", blockpack_write_world)


def blockpack_write_file(blockpack_id: int, filename: str) -> bool:
  """Writes a blockpack to a file.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    blockpack_id: id of a currently loaded blockpack
    filename: name of file to write; relative to Minecraft dir unless it's an absolute path
        (".zip" is automatically appended to filename if it does not end with that extension)

  Returns:
    `True` upon success

  Since: v3.0
  """
  return (blockpack_id, filename)

blockpack_write_file = ScriptFunction("blockpack_write_file", blockpack_write_file)


def blockpack_export_data(blockpack_id: int) -> str:
  """Serializes a blockpack into a base64-encoded string.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    blockpack_id: id of a currently loaded blockpack

  Returns:
    a base64-encoded string containing a serialized blockpack

  Since: v3.0
  """
  return (blockpack_id,)

blockpack_export_data = ScriptFunction("blockpack_export_data", blockpack_export_data)


def blockpack_delete(blockpack_id: int) -> bool:
  """Frees a currently loaded blockpack to be garbage collected.

  For a more user-friendly API, use the `BlockPack` class instead. (__internal__)

  Args:
    blockpack_id: id of a currently loaded blockpack

  Returns:
    `True` upon success

  Since: v3.0
  """
  return (blockpack_id,)

blockpack_delete = ScriptFunction("blockpack_delete", blockpack_delete)


def blockpacker_create() -> int:
  """Creates a new, empty blockpacker.

  For a more user-friendly API, use the `BlockPacker` class instead. (__internal__)

  Returns:
    an int id associated with a new blockpacker

  Since: v3.0
  """
  return ()

blockpacker_create = ScriptFunction("blockpacker_create", blockpacker_create)


def blockpacker_add_blocks(
    blockpacker_id: int, offset: BlockPos,
    base64_setblocks: str, base64_fills: str, blocks: List[str]) -> bool:
  """Adds blocks from setblocks and fills arrays to a currently loaded blockpacker.

  For a more user-friendly API, use the `BlockPacker` class instead. (__internal__)

  Args:
    blockpacker_id: id of a currently loaded blockpacker
    offset: offset from 16-bit positions in `base64_setblocks` and `base64_fills`
    base64_setblocks: base64-encoded array of 16-bit signed ints where every 4 values are:
      x, y, z relative to `offset` and index into `blocks` list
    base64_fills: base64-encoded array of 16-bit signed ints where every 7 values are:
      x1, y1, z1, x2, y2, z2 relative to `offset` and index into `blocks` list
    blocks: types of blocks referenced from `base64_setblocks` and `base64_fills` arrays

  Returns:
    `True` upon success

  Since: v3.1
  """
  return (blockpacker_id, offset, base64_setblocks, base64_fills, blocks)

blockpacker_add_blocks = ScriptFunction("blockpacker_add_blocks", blockpacker_add_blocks)


def blockpacker_add_blockpack(
    blockpacker_id: int, blockpack_id: int,
    rotation: Rotation = None, offset: BlockPos = None) -> bool:
  """Adds the blocks within a currently loaded blockpack into a blockpacker.

  For a more user-friendly API, use the `BlockPacker` class instead. (__internal__)

  Args:
    blockpacker_id: id of a blockpacker to receive blocks
    blockpack_id: id of a blockpack from which to copy blocks
    rotation: rotation matrix to apply to block coordinates before adding to blockpacker
    offset: offset to apply to block coordiantes (applied after rotation)

  Returns:
    `True` upon success

  Since: v3.0
  """
  return (blockpacker_id, blockpack_id, rotation, offset)

blockpacker_add_blockpack = ScriptFunction("blockpacker_add_blockpack", blockpacker_add_blockpack)


def blockpacker_pack(blockpacker_id: int, comments: Dict[str, str]) -> int:
  """Packs blocks within a blockpacker into a new blockpack.

  For a more user-friendly API, use the `BlockPacker` class instead. (__internal__)

  Args:
    blockpacker_id: id of a currently loaded blockpacker
    comments: key, value pairs to include in the new blockpack

  Returns:
    int id for a new blockpack containing a snapshot of blocks from the blockpacker

  Since: v3.0
  """
  return (blockpacker_id, comments)

blockpacker_pack = ScriptFunction("blockpacker_pack", blockpacker_pack)


def blockpacker_delete(blockpacker_id: int) -> bool:
  """Frees a currently loaded blockpacker to be garbage collected.

  For a more user-friendly API, use the `BlockPacker` class instead. (__internal__)

  Args:
    blockpacker_id: id of a currently loaded blockpacker

  Returns:
    `True` upon success

  Since: v3.0
  """
  return (blockpacker_id,)

blockpacker_delete = ScriptFunction("blockpacker_delete", blockpacker_delete)


class BlockPack:
  """BlockPack is an immutable and serializable collection of blocks.

  A blockpack can be read from or written to worlds, files, and serialized
  bytes. Although blockpacks are immutable and preserve position and
  orientation of blocks, they can be rotated and offset when read from or
  written to worlds.

  For a mutable collection of blocks, see `BlockPacker`.

  Since: v3.0
  """

  def __init__(self, java_generated_id: int):
    """Do not call the constructor directly. Use factory classmethods instead.

    (__internal__)
    """
    self._id = java_generated_id

  @classmethod
  def read_world(
      cls,
      pos1: BlockPos, pos2: BlockPos, *,
      rotation: Rotation = None, offset: BlockPos = None,
      comments: Dict[str, str] = {}, safety_limit: bool = True) -> 'BlockPack':
    """Creates a blockpack from blocks in the world within a rectangular volume.

    Args:
      pos1, pos2: opposing corners of a rectangular volume from which to read world blocks
      rotation: rotation matrix to apply to block coordinates read from world
      offset: offset to apply to block coordiantes (applied after rotation)
      comments: key, value pairs to include in the new blockpack
      safety_limit: if `True`, fail if requested volume spans more than 1600 chunks

    Returns:
      a new BlockPack containing blocks read from the world
    """
    blockpack_id = blockpack_read_world(pos1, pos2, rotation, offset, comments, safety_limit)
    return BlockPack(blockpack_id)

  @classmethod
  def read_file(cls, filename: str, *, relative_to_cwd=False) -> 'BlockPack':
    """Reads a blockpack from a file.

    Args:
      filename: name of file relative to minescript/blockpacks dir unless it's an absolute path
        (".zip" is automatically appended to filename if it does not end with that extension)
      relative_to_cwd: if `True`, relative filename is taken to be relative to Minecraft dir

    Returns:
      a new BlockPack containing blocks read from the file
    """
    if not os.path.isabs(filename) and not relative_to_cwd:
      filename = os.path.join("minescript", "blockpacks", filename)
    return BlockPack(blockpack_read_file(filename))

  @classmethod
  def import_data(cls, base64_data: str) -> 'BlockPack':
    """Creates a blockpack from base64-encoded serialized blockpack data.

    Args:
      base64_data: base64-encoded string containing serialization of blockpack data.

    Returns:
      a new BlockPack containing blocks read from the base64-encoded data
    """
    return BlockPack(blockpack_import_data(base64_data))

  def block_bounds(self) -> (BlockPos, BlockPos):
    """Returns min and max bounding coordinates of blocks in this BlockPack."""
    return blockpack_block_bounds(self._id)

  def comments(self) -> Dict[str, str]:
    """Returns comments stored in this BlockPack."""
    return blockpack_comments(self._id)

  def write_world(self, *, rotation: Rotation = None, offset: BlockPos = None):
    """Writes blocks from this BlockPack into the current world. Requires setblock, fill commands.

    Args:
      rotation: rotation matrix to apply to block coordinates before writing to world
      offset: offset to apply to block coordiantes (applied after rotation)
    """
    blockpack_write_world(self._id, rotation, offset)

  def write_file(self, filename: str, *, relative_to_cwd=False):
    """Writes this BlockPack to a file.

    Args:
      filename: name of file relative to minescript/blockpacks dir unless it's an absolute path
        (".zip" is automatically appended to filename if it does not end with that extension)
      relative_to_cwd: if `True`, relative filename is taken to be relative to Minecraft dir
    """
    if not os.path.isabs(filename) and not relative_to_cwd:
      filename = os.path.join("minescript", "blockpacks", filename)
    blockpack_write_file(self._id, filename)

  def export_data(self) -> str:
    """Serializes this BlockPack into a base64-encoded string.

    Returns:
      a base64-encoded string containing this blockpack's data
    """
    return blockpack_export_data(self._id)

  def __del__(self):
    """Frees this BlockPack to be garbage collected."""
    blockpack_delete(self._id)


class BlockPackerException(Exception):
  pass


def _pos_subtract(pos1: BlockPos, pos2: BlockPos) -> BlockPos:
  """Returns pos1 minus pos2."""
  return (pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])


_SETBLOCKS_ARRAY_THRESHOLD = 4000
_FILLS_ARRAY_THRESHOLD = 7000
_BLOCKS_DICT_THRESHOLD = 1000

class BlockPacker:
  """BlockPacker is a mutable collection of blocks.

  Blocks can be added to a blockpacker by calling `setblock(...)`, `fill(...)`,
  and/or `add_blockpack(...)`.  To serialize blocks or write them to a world, a
  blockpacker can be "packed" by calling pack() to create a compact snapshot of
  the blocks contained in the blockpacker in the form of a new BlockPack. A
  blockpacker continues to store the same blocks it had before being packed,
  and more blocks can be added thereafter.

  For a collection of blocks that is immutable and serializable, see `BlockPack`.

  Since: v3.0
  """

  def __init__(self):
    """Creates a new, empty blockpacker."""

    self._id = blockpacker_create()
    self.offset = None # offset for 16-bit positions recorded in setblocks and fills
    self.setblocks = array("h")
    self.fills = array("h")
    self.blocks: Dict[str, int] = dict()

  def _get_block_id(self, block_type: str) -> int:
    return self.blocks.setdefault(block_type, len(self.blocks))

  def setblock(self, pos: BlockPos, block_type: str):
    """Sets a block within this BlockPacker.

    Args:
      pos: position of a block to set
      block_type: block descriptor to set

    Raises:
      `BlockPackerException` if blockpacker operation fails
    """
    if self.offset is None:
      self.offset = pos

    relative_pos = _pos_subtract(pos, self.offset)
    if max(relative_pos) > 32767 or min(relative_pos) < -32768:
      raise BlockPackerException(
          f"Blocks within a Python-generated BlockPacker cannot span more than 32,767 blocks: "
          f"{self.offset} -> {pos}")

    self.setblocks.extend(relative_pos)
    self.setblocks.append(self._get_block_id(block_type))

    if (len(self.setblocks) > _SETBLOCKS_ARRAY_THRESHOLD or
        len(self.blocks) > _BLOCKS_DICT_THRESHOLD):
      self._flush_blocks()

  def fill(self, pos1: BlockPos, pos2: BlockPos, block_type: str):
    """Fills blocks within this BlockPacker.

    Args:
      pos1, pos2: coordinates of opposing corners of a rectangular volume to fill
      block_type: block descriptor to fill

    Raises:
      `BlockPackerException` if blockpacker operation fails
    """
    if self.offset is None:
      self.offset = pos1

    relative_pos1 = _pos_subtract(pos1, self.offset)
    if max(relative_pos1) > 32767 or min(relative_pos1) < -32768:
      raise BlockPackerException(
          f"Blocks within a Python-generated BlockPacker cannot span more than 32,767 blocks: "
          f"{self.offset} -> {pos1}")

    relative_pos2 = _pos_subtract(pos2, self.offset)
    if max(relative_pos2) > 32767 or min(relative_pos2) < -32768:
      raise BlockPackerException(
          f"Blocks within a Python-generated BlockPacker cannot span more than 32,767 blocks: "
          f"{self.offset} -> {pos2}")

    self.fills.extend(relative_pos1)
    self.fills.extend(relative_pos2)
    self.fills.append(self._get_block_id(block_type))

    if (len(self.fills) > _FILLS_ARRAY_THRESHOLD or
        len(self.blocks) > _BLOCKS_DICT_THRESHOLD):
      self._flush_blocks()

  def _flush_blocks(self):
    if sys.byteorder != "big":
      # Swap to network (big-endian) byte order.
      self.setblocks.byteswap()
      self.fills.byteswap()

    blockpacker_add_blocks(
        self._id, self.offset,
        base64.b64encode(self.setblocks.tobytes()).decode("utf-8"),
        base64.b64encode(self.fills.tobytes()).decode("utf-8"),
        list(self.blocks.keys()))

    self.offset = None
    self.setblocks = array("h")
    self.fills = array("h")
    self.blocks = dict()

  def add_blockpack(
      self, blockpack: BlockPack, *, rotation: Rotation = None, offset: BlockPos = None):
    """Adds the blocks within a BlockPack into this BlockPacker.

    Args:
      blockpack: BlockPack from which to copy blocks
      rotation: rotation matrix to apply to block coordinates before adding to blockpacker
      offset: offset to apply to block coordiantes (applied after rotation)
    """
    blockpacker_add_blockpack(self._id, blockpack._id, rotation, offset)

  def pack(self, *, comments: Dict[str, str] = {}) -> BlockPack:
    """Packs blocks within this BlockPacker into a new BlockPack.

    Args:
      comments: key, value pairs to include in the new BlockPack

    Returns:
      a new BlockPack containing a snapshot of blocks from this BlockPacker
    """
    self._flush_blocks()
    return BlockPack(blockpacker_pack(self._id, comments))

  def __del__(self):
    """Frees this BlockPacker to be garbage collected."""
    blockpacker_delete(self._id)


def java_class(name: str):
  """Looks up Java class by fully qualified name. Returns handle to Java object."""
  return (name,)

java_class = ScriptFunction("java_class", java_class)

def java_string(s):
  """Creates Java String. Returns handle to Java object."""
  return (s,)

java_string = ScriptFunction("java_string", java_string)

def java_double(d):
  """Creates Java Double. Returns handle to Java object."""
  return (d,)

java_double = ScriptFunction("java_double", java_double)

def java_float(f):
  """Creates Java Float. Returns handle to Java object."""
  return (f,)

java_float = ScriptFunction("java_float", java_float)

def java_long(l):
  """Creates Java Long. Returns handle to Java object."""
  return (l,)

java_long = ScriptFunction("java_long", java_long)

def java_int(i):
  """Creates Java Integer. Returns handle to Java object."""
  return (i,)

java_int = ScriptFunction("java_int", java_int)

def java_bool(b):
  """Creates Java Boolean. Returns handle to Java object."""
  return (b,)

java_bool = ScriptFunction("java_bool", java_bool)

def java_ctor(clss):
  """Returns handle to constructor for `clss`."""
  return (clss,)

java_ctor = ScriptFunction("java_ctor", java_ctor)

def java_new_instance(ctor, *args):
  """Creates new Java instance. Returns handle to newly created Java object.

  Args:
    ctor: constructor set returned from `java_ctor`
    args: handles to Java objects to pass as constructor params
  """
  return (ctor, *args)

java_new_instance = ScriptFunction("java_new_instance", java_new_instance)

def java_member(clss, name: str):
  """Gets Java member(s) matching `name`. Returns handle to Java object."""
  return (clss, name)

java_member = ScriptFunction("java_member", java_member)

def java_access_field(target, field):
  """Accesses `field` on `target`. Returns handle to Java object, or `None` if `null`."""
  return (target, field)

java_access_field = ScriptFunction("java_access_field", java_access_field)

def java_call_method(target, method, *args):
  """Invokes method on target. Returns handle to Java object, or `None` if `null`.

  Args:
    args: handles to Java objects to pass as constructor params
  """
  return (target, method, *args)

java_call_method = ScriptFunction("java_call_method", java_call_method)

def java_array_length(array):
  """Returns length of array handle as `int`."""
  return (array,)

java_array_length = ScriptFunction("java_array_length", java_array_length)

def java_array_index(array, i):
  """Gets element `i` of array handle. Returns handle to Java object, or `None` if `null`."""
  return (array, i)

java_array_index = ScriptFunction("java_array_index", java_array_index)

def java_to_string(target):
  """Returns `str` from calling `target.toString()` in Java."""
  return (target,)

java_to_string = ScriptFunction("java_to_string", java_to_string)

def java_assign(dest, source):
  """Reassigns `dest` handle to reference the object referenced by `source` handle."""
  return (dest, source)

java_assign = ScriptFunction("java_assign", java_assign)

def java_release(*targets):
  """Releases the Java reference(s) associated with `targets`."""
  return targets

java_release = ScriptFunction("java_release", java_release)

