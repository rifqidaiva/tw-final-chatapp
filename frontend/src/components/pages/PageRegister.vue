<script setup lang="ts">
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
    <div class="w-full max-w-sm md:max-w-3xl">
      <div class="flex flex-col gap-6">
        <Card class="mx-auto max-w-sm">
          <CardHeader>
            <CardTitle class="text-xl">Daftar</CardTitle>
            <CardDescription>Masukkan informasi Anda untuk membuat akun</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="grid gap-4">
              <div class="grid gap-2">
                <Label for="name">Nama Lengkap</Label>
                <Input id="name" placeholder="Robinson" required />
              </div>
              <div class="grid gap-2">
                <Label for="email">Email</Label>
                <Input id="email" type="email" placeholder="m@example.com" required />
              </div>
              <div class="grid gap-2">
                <Label for="password">Kata Sandi</Label>
                <Input id="password" type="password" />
              </div>
              <div class="grid gap-2">
                <Label for="password-confirmation">Konfirmasi Kata Sandi</Label>
                <Input id="password-confirmation" type="password" />
              </div>
              <Button type="submit" class="w-full">Buat Akun</Button>
            </div>
            <div class="mt-4 text-center text-sm">
              Sudah punya akun?
              <a href="login" class="underline">Masuk</a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
