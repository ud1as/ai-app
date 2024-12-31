'use client'

import React, { useState, useEffect, use } from 'react'
import { botApi } from '@/api/endpoints/bots'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export const ConfigureBotForm: React.FC = () => {
  const [bots, setBots] = useState<{ id: string; name: string }[]>([])
  const [selectedBot, setSelectedBot] = useState('')
  const [promptTemplate, setPromptTemplate] = useState('')
  const [datasetId, setDatasetId] = useState('')

  useEffect(() => {
    const fetchBots = async () => {
      
        const fetchedBots = await botApi.getAll()
        setBots(fetchedBots)
     
    fetchBots()

    }
    }, [])
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedBot) return
      await botApi.configure(selectedBot, { prompt_template: promptTemplate, dataset_id: datasetId })     
    
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="bot">Select Bot</Label>
        <Select onValueChange={setSelectedBot}>
          <SelectTrigger>
            <SelectValue placeholder="Select a bot" />
          </SelectTrigger>
          <SelectContent>
            {bots.map((bot) => (
              <SelectItem key={bot.id} value={bot.id}>{bot.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div>
        <Label htmlFor="promptTemplate">Prompt Template</Label>
        <Textarea
          id="promptTemplate"
          value={promptTemplate}
          onChange={(e) => setPromptTemplate(e.target.value)}
          required
        />
      </div>
      <div>
        <Label htmlFor="datasetId">Dataset ID</Label>
        <Input
          id="datasetId"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          required
        />
      </div>
      <Button type="submit" disabled={!selectedBot}>Configure Bot</Button>
    </form>
  )
}
