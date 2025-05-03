<script setup lang="ts">
import { SidebarTrigger } from '@/components/ui/sidebar'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-vue-next'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'

const data = {
  messages: [
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'Hello!',
      timestamp: '2023-10-01 10:00:00',
      is_sender: true,
    },
    {
      sender_id: 2,
      receiver_id: 1,
      content: 'Hi! How are you?',
      timestamp: '2023-10-01 10:01:00',
      is_sender: false,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content:
        'I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!I am good, thanks!',
      timestamp: '2023-10-01 10:02:00',
      is_sender: true,
    },
    {
      sender_id: 2,
      receiver_id: 1,
      content:
        'What about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?hat about you?',
      timestamp: '2023-10-01 10:03:00',
      is_sender: false,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
    {
      sender_id: 1,
      receiver_id: 2,
      content: 'I am doing well too!',
      timestamp: '2023-10-01 10:04:00',
      is_sender: true,
    },
  ],
  otherUser: {
    id: 2,
    name: 'John Doe',
    email: 'johndoe@gmail.com',
    avatar: 'https://via.placeholder.com/150',
  },
}
</script>

<template>
  <header class="sticky top-0 flex h-16 shrink-0 items-center gap-2 bg-background">
    <div class="flex items-center gap-2 px-4">
      <SidebarTrigger class="-ml-1" />
      <Separator orientation="vertical" class="mr-2 h-4" />
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem class="hidden md:block">
            <BreadcrumbPage>Percakapan</BreadcrumbPage>
          </BreadcrumbItem>
          <BreadcrumbSeparator class="hidden md:block" />
          <BreadcrumbItem>
            <BreadcrumbPage>Teman</BreadcrumbPage>
          </BreadcrumbItem>
          <BreadcrumbSeparator class="hidden md:block" />
          <BreadcrumbItem>
            <Avatar class="h-8 w-8 rounded-full">
              <AvatarImage :src="data.otherUser.avatar" alt="Avatar" class="h-8 rounded-full" />
              <AvatarFallback>
                {{
                  data.otherUser.name
                    .split(' ')
                    .map((n) => n[0])
                    .join('')
                }}
              </AvatarFallback>
            </Avatar>
            <BreadcrumbLink href="#">{{ data.otherUser.name }}</BreadcrumbLink>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  </header>
  <div class="flex flex-1 flex-col gap-4 p-4 pb-0 pt-0">
    <div class="flex flex-1 flex-col rounded-xl bg-muted p-4 pb-0 md:min-h-min">
      <div class="flex-1 overflow-auto">
        <!-- Chat bubbles -->
        <div class="flex flex-col gap-2">
          <div
            v-for="(message, index) in data.messages"
            :key="index"
            :class="{
              'flex items-start gap-2': !message.is_sender,
              'flex items-start justify-end gap-2': message.is_sender,
            }">
            <template v-if="!message.is_sender">
              <Avatar>
                <AvatarImage :src="data.otherUser.avatar" alt="Avatar" class="h-8 rounded-full" />
                <AvatarFallback>
                  {{
                    data.otherUser.name
                      .split(' ')
                      .map((n) => n[0])
                      .join('')
                  }}
                </AvatarFallback>
              </Avatar>
              <div class="flex max-w-[75%] flex-col">
                <span class="text-sm font-semibold">{{ data.otherUser.name }}</span>
                <span class="my-2 text-sm">{{ message.content }}</span>
                <span class="text-xs text-muted-foreground">{{ message.timestamp }}</span>
              </div>
            </template>
            <template v-else>
              <div class="flex max-w-[75%] flex-col items-end">
                <span class="rounded-lg bg-primary p-2 text-sm text-white">
                  {{ message.content }}
                </span>
                <span class="text-xs text-muted-foreground">{{ message.timestamp }}</span>
              </div>
            </template>
          </div>
        </div>
      </div>
      <div class="sticky bottom-0 bg-muted pb-8 pt-2">
        <div class="mt-auto flex items-center gap-2 rounded-lg">
          <Input type="text" placeholder="Ketik pesan Anda..." class="flex-1 bg-card" />
          <Button variant="ghost">
            <Send />
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
