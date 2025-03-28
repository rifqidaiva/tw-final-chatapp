<script setup lang="ts">
import ChatSidebar from '@/components/pages/Chats/ChatsSidebar.vue'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-vue-next'
</script>

<template>
  <SidebarProvider
    class=""
    :style="{
      '--sidebar-width': '380px',
    }">
    <ChatSidebar />
    <SidebarInset>
      <header class="sticky top-0 flex h-16 shrink-0 items-center gap-2 bg-background">
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1" />
          <Separator orientation="vertical" class="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem class="hidden md:block">
                <BreadcrumbLink href="#">Percakapan</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator class="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Teman</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
      </header>
      <div class="flex flex-1 flex-col gap-4 p-4 pb-0 pt-0">
        <div class="flex flex-1 flex-col rounded-xl bg-muted p-4 pb-0 md:min-h-min">
          <div class="flex-1 overflow-auto">
            <!-- Chat messages or content can go here -->
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...</p>
            <p>Chat content...1</p>
          </div>
          <div class="sticky bottom-0 bg-muted pb-8">
            <div class="mt-auto flex items-center gap-2 rounded-lg">
              <Input type="text" placeholder="Ketik pesan Anda..." class="flex-1 bg-card" />
              <Button variant="ghost">
                <Send />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
