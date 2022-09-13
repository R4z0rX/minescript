// SPDX-FileCopyrightText: © 2022 Greg Christiana <maxuser@minescript.net>
// SPDX-License-Identifier: GPL-3.0-only

package net.minescript.forge;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraftforge.client.event.ClientChatEvent;
import net.minecraftforge.client.event.InputEvent;
import net.minecraftforge.client.event.ScreenEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.world.ChunkEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minescript.common.Minescript;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@Mod("minescript")
public class MinescriptForgeMod {
  private static final Logger LOGGER = LogManager.getLogger();

  public MinescriptForgeMod() {
    LOGGER.info("(minescript) Minescript mod starting...");
    MinecraftForge.EVENT_BUS.register(this);

    Minescript.init();
  }

  @SubscribeEvent
  public void onKeyboardKeyPressedEvent(ScreenEvent.KeyboardKeyPressedEvent event) {
    if (Minescript.onKeyboardKeyPressed(event.getScreen(), event.getKeyCode())) {
      event.setCanceled(true);
    }
  }

  @SubscribeEvent
  public void onKeyInputEvent(InputEvent.KeyInputEvent event) {
    Minescript.onKeyInput(event.getKey());
  }

  @SubscribeEvent
  public void onChunkLoadEvent(ChunkEvent.Load event) {
    if (event.getWorld() instanceof ClientLevel) {
      Minescript.onChunkLoad(event.getWorld(), event.getChunk());
    }
  }

  @SubscribeEvent
  public void onChunkUnloadEvent(ChunkEvent.Unload event) {
    if (event.getWorld() instanceof ClientLevel) {
      Minescript.onChunkUnload(event.getWorld(), event.getChunk());
    }
  }

  @SubscribeEvent
  public void onClientChatEvent(ClientChatEvent event) {
    if (Minescript.onClientChat(event.getMessage())) {
      event.setCanceled(true);
    }
  }

  @SubscribeEvent
  public void onPlayerTick(TickEvent.PlayerTickEvent event) {
    Minescript.onPlayerTick();
  }
}
