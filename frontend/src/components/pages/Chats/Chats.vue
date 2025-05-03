<script setup lang="ts">
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import ChatSidebar from '@/components/pages/Chats/ChatsSidebar.vue'
import ChatsConv from '@/components/pages/Chats/ChatsConv.vue'
</script>

<template>
  <SidebarProvider
    :style="{
      '--sidebar-width': '380px',
    }">
    <ChatSidebar />
    <SidebarInset>
      <ChatsConv />
    </SidebarInset>
  </SidebarProvider>
</template>
