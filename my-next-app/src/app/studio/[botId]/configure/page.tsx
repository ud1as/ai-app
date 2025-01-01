'use client'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { botApi } from '@/api/endpoints/bots'
import { knowledgeApi, Dataset } from '@/api/endpoints/knowledge'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function ConfigureBotPage() {
  const params = useParams()
  const router = useRouter()
  const botId = params.botId as string

  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [config, setConfig] = useState({
    prompt_template: '',
    dataset_id: ''
  })
  const [chat, setChat] = useState({
    message: '',
    conversation_id: 'default'
  })
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'bot',
    content: string
  }>>([])
  const [isConfiguring, setIsConfiguring] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const fetchedDatasets = await knowledgeApi.getDatasets()
        setDatasets(fetchedDatasets)
      } catch (err) {
        console.error('Error fetching datasets:', err)
        setError('Failed to load datasets')
      }
    }

    fetchDatasets()
  }, [])

  const handleConfigure = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsConfiguring(true)
    setError(null)
    setSuccessMessage(null)

    try {
      const response = await botApi.configure(botId, {
        prompt_template: config.prompt_template,
        dataset_id: config.dataset_id
      })
      
      console.log('Configuration response:', response)
      setSuccessMessage('Сохранено')
    } catch (err) {
      console.error('Configuration error:', err)
      setError(err instanceof Error ? err.message : 'Ошибка')
    } finally {
      setIsConfiguring(false)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!chat.message.trim()) return

    setIsSending(true)
    setMessages(prev => [...prev, { role: 'user', content: chat.message }])
    
    try {
      const response = await botApi.chat(botId, {
        query: chat.message,
        conversation_id: chat.conversation_id
      })
      
      setMessages(prev => [...prev, { role: 'bot', content: response.answer }])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
    } finally {
      setIsSending(false)
      setChat(prev => ({ ...prev, message: '' }))
    }
  }

  return (
    <div className="container max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <Link 
          href="/studio"
          className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Назад
        </Link>
        <h1 className="text-2xl font-bold">Настройки</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="rounded-lg border p-6">
            <h2 className="text-lg font-semibold mb-4">Конфигурация</h2>
            
            <form onSubmit={handleConfigure} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Промпт
                </label>
                <Textarea
                  value={config.prompt_template}
                  onChange={(e) => setConfig(prev => ({
                    ...prev,
                    prompt_template: e.target.value
                  }))}
                  rows={6}
                  placeholder="Ты ассистент помощник и тебя зовут Алиса ...."
                  className="min-h-[150px] resize-none"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">
                  База Знаний
                </label>
                <Select 
                  value={config.dataset_id}
                  onValueChange={(value) => setConfig(prev => ({
                    ...prev,
                    dataset_id: value
                  }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Выберите Базу Знаний" />
                  </SelectTrigger>
                  <SelectContent>
                    {datasets.map((dataset) => (
                      <SelectItem 
                        key={dataset.id} 
                        value={dataset.id}
                      >
                        {dataset.name || 'Unnamed Dataset'}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {error && (
                <div className="text-sm text-red-500 p-3 bg-red-50 rounded-md">
                  {error}
                </div>
              )}

              {successMessage && (
                <div className="text-sm text-green-600 p-3 bg-green-50 rounded-md">
                  {successMessage}
                </div>
              )}

              <Button 
                type="submit" 
                disabled={isConfiguring}
                className="w-full"
              >
                {isConfiguring ? 'Saving Configuration...' : 'Сохранить Настройки'}
              </Button>
            </form>
          </div>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="text-lg font-semibold mb-4">Протестируйте своего Бота</h2>
          
          <div className="h-[500px] overflow-y-auto space-y-4 mb-4 p-4 border rounded-lg bg-gray-50">
            {messages.length === 0 && (
              <div className="text-center text-muted-foreground text-sm py-8">
                Начните диалог
              </div>
            )}
            
            {messages.map((message, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg ${
                  message.role === 'user' 
                    ? 'bg-blue-50 ml-12 border border-blue-100' 
                    : 'bg-white mr-12 border'
                }`}
              >
                <div className="text-xs text-muted-foreground mb-1">
                  {message.role === 'user' ? 'You' : 'Bot'}
                </div>
                {message.content}
              </div>
            ))}
          </div>

          <form onSubmit={handleSendMessage} className="flex gap-2">
            <Input
              value={chat.message}
              onChange={(e) => setChat(prev => ({
                ...prev,
                message: e.target.value
              }))}
              placeholder="Привет"
              disabled={isSending}
            />
            <Button 
              type="submit" 
              disabled={isSending || !chat.message.trim()}
              className="min-w-[80px]"
            >
              {isSending ? '...' : 'Отправить'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}