import { Suspense } from 'react'
import { CreateBotForm } from '@/app/components/create_bot'
import { ConfigureBotForm } from '@/app/components/configure_bot'
import { BotList } from '@/app/components/botlist'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function DashboardPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Bot Dashboard</h1>
      <Tabs defaultValue="create">
        <TabsList>
          <TabsTrigger value="create">Create Bot</TabsTrigger>
          <TabsTrigger value="configure">Configure Bot</TabsTrigger>
          <TabsTrigger value="list">Bot List</TabsTrigger>
        </TabsList>
        <TabsContent value="create">
          <CreateBotForm />
        </TabsContent>
        <TabsContent value="configure">
          <ConfigureBotForm />
        </TabsContent>
        <TabsContent value="list">
          <Suspense fallback={<div>Loading...</div>}>
            <BotList />
          </Suspense>
        </TabsContent>
      </Tabs>
    </div>
  )
}

