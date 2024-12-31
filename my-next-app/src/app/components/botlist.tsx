import { botApi } from '@/api/endpoints/bots'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export async function BotList() {
  const bots = await botApi.getAll()

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {bots.map((bot) => (
        <Card key={bot.id}>
          <CardHeader>
            <CardTitle>{bot.name}</CardTitle>
            <CardDescription>{bot.type || 'No type specified'}</CardDescription>
          </CardHeader>
          <CardContent>
            <p>{bot.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

