'use client'
import { useState } from 'react'
import { FileText, UploadCloud } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function CreateKnowledgePage() {
  const router = useRouter()

  return (
    <div>
      <div className="flex items-center mb-8">
        <Link href="/knowledge" className="text-gray-600 hover:text-gray-900">
          ← Создать базу знаний
        </Link>
      </div>

      <h1 className="text-2xl font-semibold mb-8">Выберите источник данных</h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="border border-blue-500 bg-blue-50 rounded-lg p-6">
          <FileText className="w-6 h-6 text-blue-600 mb-3" />
          <h3 className="font-medium mb-2">Импортировать из файла</h3>
        </div>

        <div className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50">
          <FileText className="w-6 h-6 text-gray-600 mb-3" />
          <h3 className="font-medium mb-2">Синхронизировать из Notion</h3>
        </div>

        <div className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50">
          <UploadCloud className="w-6 h-6 text-gray-600 mb-3" />
          <h3 className="font-medium mb-2">Синхронизировать с веб-сайта</h3>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-medium mb-4">Загрузить файл</h2>
        <div className="border-2 border-dashed border-gray-200 rounded-lg p-8">
          <div className="text-center">
            <UploadCloud className="w-8 h-8 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-2">
              Перетащите файл или <span className="text-blue-600 cursor-pointer">Обзор</span>
            </p>
            <p className="text-sm text-gray-500">
              Поддерживаются TXT, MARKDOWN, PDF, HTML, XLSX, XLS, DOCX, CSV, MD, HTM. Максимум 15 МБ каждый.
            </p>
          </div>
        </div>
        <div className="mt-4">
          <button
            onClick={() => router.push('/knowledge/create/preprocessing')}
            className="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200"
          >
            Далее
          </button>
        </div>
      </div>

      <div className="mt-8">
        <button className="text-blue-600 hover:text-blue-700 flex items-center">
          <span className="mr-2">+</span>
          Я хочу создать пустую базу знаний
        </button>
      </div>
    </div>
  )
}