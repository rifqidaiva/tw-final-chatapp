<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
</script>

<template>
  <div class="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
    <div class="w-full max-w-sm md:max-w-3xl">
      <div class="flex flex-col gap-6">
        <Card class="overflow-hidden">
          <CardContent class="grid p-0 md:grid-cols-2">
            <form class="p-6 md:p-8">
              <div class="flex flex-col gap-6">
                <div class="flex flex-col items-center text-center">
                  <h1 class="text-2xl font-bold">Selamat Datang</h1>
                  <p class="text-balance text-muted-foreground">Silahkan masuk ke aplikasi</p>
                </div>
                <div class="grid gap-2">
                  <Label for="email">Email</Label>
                  <Input id="email" type="email" placeholder="m@example.com" required />
                </div>
                <div class="grid gap-2">
                  <div class="flex items-center">
                    <Label for="password">Password</Label>
                    <RouterLink to="#" class="ml-auto text-sm underline-offset-2 hover:underline">
                      Forgot your password?
                    </RouterLink>
                  </div>
                  <Input id="password" type="password" required />
                </div>
                <Button type="submit" class="w-full">Masuk</Button>
                <div
                  class="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border">
                  <span class="relative z-10 bg-background px-2 text-muted-foreground">
                    Pilihan lain
                  </span>
                </div>
                <div class="text-center text-sm">
                  Belum punya akun?
                  <RouterLink to="register" class="underline underline-offset-4">Daftar</RouterLink>
                </div>
              </div>
            </form>
            <div class="relative hidden bg-muted bg-slate-500 md:block">
              <img
                src="@/assets/login.svg"
                alt="Image"
                class="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale" />
            </div>
          </CardContent>
        </Card>
        <div
          class="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:text-primary">
          Dengan melanjutkan, Anda setuju dengan <RouterLink to="#">Ketentuan Layanan</RouterLink>to
          <RouterLink to="#">Kebijakan Privasi</RouterLink> kami.
        </div>
      </div>
    </div>
  </div>
</template>
