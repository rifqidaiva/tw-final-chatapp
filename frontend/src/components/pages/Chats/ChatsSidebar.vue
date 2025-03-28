<script setup lang="ts">
import ChatsSidebarUser from '@/components/pages/Chats/ChatsSidebarUser.vue'
import { Label } from '@/components/ui/label'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarInput,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  type SidebarProps,
  useSidebar,
} from '@/components/ui/sidebar'
import { Switch } from '@/components/ui/switch'
import { Command, Inbox, Search, Users } from 'lucide-vue-next'
import { h, ref } from 'vue'

const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: 'icon',
})

const data = {
  user: {
    name: 'shadcn',
    email: 'm@example.com',
    avatar: '/avatars/shadcn.jpg',
  },
  navMain: [
    {
      title: 'Teman',
      url: '#',
      icon: Users,
      isActive: true,
    },
    {
      title: 'Grup',
      url: '#',
      icon: Inbox,
      isActive: false,
    },
    {
      title: 'Cari orang',
      url: '#',
      icon: Search,
      isActive: false,
    },
  ],
  friends: [],
  friendMails: [
    {
      name: 'William Smith',
      email: 'williamsmith@example.com',
      date: '09:34',
      teaser:
        'Hi team, just a reminder about our meeting tomorrow at 10 AM.\nPlease come prepared with your project updates.',
    },
    {
      name: 'Alice Smith',
      email: 'alicesmith@example.com',
      date: 'Kemarin',
      teaser:
        "Thanks for the update. The progress looks great so far.\nLet's schedule a call to discuss the next steps.",
    },
  ],
  groups: [],
  groupMails: [
    {
      name: 'Project Team',
      userName: 'Alice Smith',
      email: 'projectteam@example.com',
      date: 'Hari ini',
      teaser:
        'Reminder: The project deadline is approaching. Please ensure all tasks are completed by the end of the week.',
    },
    {
      name: 'Family Group',
      userName: 'Alice Smith',
      email: 'familygroup@example.com',
      date: '2 hari yang lalu',
      teaser: "Don't forget about the family gathering this weekend. Let us know if you're coming!",
    },
    {
      name: 'Study Group',
      userName: 'Alice Smith',
      email: 'studygroup@example.com',
      date: 'Minggu lalu',
      teaser:
        "We've uploaded the notes from the last session. Please review them before the next meeting.",
    },
  ],
}
const activeSidebar = ref(data.navMain[0])
const friendMails = ref(data.friendMails)
const groupMails = ref(data.groupMails)

const { setOpen } = useSidebar()
</script>

<template>
  <Sidebar class="overflow-hidden [&>[data-sidebar=sidebar]]:flex-row" v-bind="props">
    <!-- This is the first sidebar -->
    <!-- We disable collapsible and adjust width to icon -->
    <!-- This will make the sidebar appear as icons -->
    <Sidebar collapsible="none" class="!w-[calc(var(--sidebar-width-icon)_+_1px)] border-r">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" as-child class="md:h-8 md:p-0">
              <a href="#">
                <div
                  class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Command class="size-4" />
                </div>
                <div class="grid flex-1 text-left text-sm leading-tight">
                  <span class="truncate font-semibold">ChatApp</span>
                  <span class="truncate text-xs">Enterprise</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent class="px-1.5 md:px-0">
            <SidebarMenu>
              <SidebarMenuItem v-for="item in data.navMain" :key="item.title">
                <SidebarMenuButton
                  :tooltip="h('div', { hidden: false }, item.title)"
                  :is-active="activeSidebar.title === item.title"
                  class="px-2.5 md:px-2"
                  @click="
                    () => {
                      activeSidebar = item
                      setOpen(true)
                    }
                  ">
                  <component :is="item.icon" />
                  <span>{{ item.title }}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <ChatsSidebarUser :user="data.user" />
      </SidebarFooter>
    </Sidebar>
    <!--  This is the second sidebar -->
    <!--  We disable collapsible and let it fill remaining space -->
    <Sidebar collapsible="none" class="hidden flex-1 md:flex">
      <SidebarHeader class="gap-3.5 border-b p-4">
        <div class="flex w-full items-center justify-between">
          <div class="text-base font-medium text-foreground">
            {{ activeSidebar.title }}
          </div>
          <Label class="flex items-center gap-2 text-sm">
            <span>Belum dibaca</span>
            <Switch class="shadow-none" />
          </Label>
        </div>
        <SidebarInput placeholder="Ketik untuk mencari..." />
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup class="px-0">
          <SidebarGroupContent>
            <a
              v-if="activeSidebar.title === 'Teman'"
              v-for="mail in friendMails"
              :key="mail.email"
              href="#"
              class="flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground">
              <div class="flex w-full items-center gap-2">
                <span class="font-medium">{{ mail.name }}</span>
                <span class="ml-auto text-xs">{{ mail.date }}</span>
              </div>
              <span class="line-clamp-2 w-[260px] whitespace-break-spaces text-xs">
                {{ mail.teaser }}
              </span>
            </a>
            <a
              v-if="activeSidebar.title === 'Grup'"
              v-for="mail in groupMails"
              :key="mail.email"
              href="#"
              class="flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground">
              <div class="flex w-full items-center gap-2">
                <span class="font-medium">{{ mail.name }}</span>
                <span class="ml-auto text-xs">{{ mail.date }}</span>
              </div>
              <span class="line-clamp-2 w-[260px] whitespace-break-spaces text-xs">
                <span class="underline font-semibold">{{ mail.userName }}:</span> {{ mail.teaser }}
              </span>
            </a>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  </Sidebar>
</template>
