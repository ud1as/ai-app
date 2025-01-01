// src/app/studio/page.tsx
'use client'
import { useState, useEffect } from 'react'
import { Plus, Settings2 } from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { botApi } from '@/api/endpoints/bots'
import Link from 'next/link'

interface Bot {
  id: string;
  name: string;
  description: string;
  type?: 'Чат-Бот' | 'АГЕНТ' | 'РАБОЧИЙ ПРОЦЕСС';
}

export default function StudioPage() {
  const [isOpen, setIsOpen] = useState(false)
  const [bots, setBots] = useState<Bot[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    type: 'Чат-Бот' as const
  })
  const [isCreating, setIsCreating] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  useEffect(() => {
    fetchBots()
  }, [])

  const fetchBots = () => {
    setLoading(true)
    botApi.getAll()
      .then(response => {
        setBots(response)
      })
      .catch(err => {
        console.error('Error fetching bots:', err)
        setError('Failed to load bots')
      })
      .finally(() => setLoading(false))
  }

  const handleCreateBot = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsCreating(true)
    setCreateError(null)

    try {
      await botApi.create({
        name: formData.name,
        description: formData.description
      })
      setIsOpen(false)
      fetchBots()
      setFormData({ name: '', description: '', type: 'Чат-Бот' })
    } catch (err) {
      setCreateError(err instanceof Error ? err.message : 'Failed to create bot')
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className="container max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Студия</h1>
          <p className="text-muted-foreground mt-1">Создайте своего AI-бота</p>
        </div>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Создать нового бота
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Создать нового бота</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleCreateBot} className="space-y-4">
              {createError && (
                <div className="text-sm text-red-500 p-3 bg-red-50 rounded-md">
                  {createError}
                </div>
              )}

              <div className="space-y-2">
                <Select
                  value={formData.type}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, type: value as typeof prev.type }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select bot type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Чат-Бот">Chat Bot</SelectItem>
                    <SelectItem value="АГЕНТ">Agent</SelectItem>
                    <SelectItem value="РАБОЧИЙ ПРОЦЕСС">Workflow</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Input
                  id="name"
                  placeholder="Bot name"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Textarea
                  id="description"
                  placeholder="Bot description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  rows={4}
                />
              </div>

              <div className="flex justify-end pt-4">
                <Button type="submit" disabled={isCreating}>
                  {isCreating ? 'Creating...' : 'Create Bot'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Bot Grid */}
      <div className="rounded-lg border bg-card">
        {loading && (
          <div className="p-8 text-center text-muted-foreground">
            Loading bots...
          </div>
        )}

        {error && (
          <div className="p-8 text-center text-red-500">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
            {bots.map((bot) => (
              <Link
                key={bot.id}
                href={`/studio/${bot.id}/configure`}
                className="group block p-4 rounded-lg border hover:border-primary hover:shadow-sm transition-all"
              >
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                    🤖
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium group-hover:text-primary transition-colors">
                        {bot.name}
                      </h3>
                      <Settings2 className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {bot.type || 'Чат-Бот'}
                    </div>
                    {bot.description && (
                      <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                        {bot.description}
                      </p>
                    )}
                  </div>
                </div>
              </Link>
            ))}

            {bots.length === 0 && (
              <div className="col-span-full p-8 text-center text-muted-foreground">
                <div className="max-w-sm mx-auto">
                  <h3 className="font-medium mb-2">Пока ничего.....</h3>
                  <p className="text-sm mb-4">Создайте нового бота</p>
                  <Button onClick={() => setIsOpen(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Создать бота
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}