'use client'

export default function BotConfigPage() {
  return (
    <div className="flex">
      {/* Left Side - Config */}
      <div className="flex-1 border-r border-gray-200 p-6">
        {/* Instructions */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2>Инструкции</h2>
            <button className="text-blue-600 hover:text-blue-700">
              + Сгенерировать
            </button>
          </div>
          <textarea
            placeholder="Напишите здесь свое ключевое слово подсказки, введите '{', чтобы вставить переменную..."
            className="w-full h-40 p-4 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {/* Variables */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <span className="text-blue-600 mr-2">[×]</span>
              <h2>Переменные</h2>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              + Добавить
            </button>
          </div>
          <p className="text-sm text-gray-600">
            Переменные позволяют пользователям вводить промпты или вступительные замечания при заполнении форм.
            Вы можете попробовать ввести  в промптах.
          </p>
        </div>

        {/* Context */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2>Контекст</h2>
            <button className="text-blue-600 hover:text-blue-700">
              + Добавить
            </button>
          </div>
          <p className="text-sm text-gray-600">
            Вы можете импортировать знания в качестве контекста
          </p>
        </div>
      </div>

      {/* Right Side - Testing */}
      <div className="flex-1 p-6">
        <div className="mb-4">
          <h2>Отладка и предварительный просмотр</h2>
        </div>
        <div className="border border-gray-200 rounded-lg h-[calc(100vh-180px)] flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h3>Поговорить с ботом</h3>
          </div>
          <div className="flex-1 p-4 overflow-auto">
            {/* Chat messages will go here */}
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                  <span className="text-blue-600">F</span>
                </div>
                <span>Features Enabled</span>
              </div>
              <div className="flex justify-end">
                <button className="text-blue-600 hover:text-blue-700 text-sm">
                  Manage →
                </button>
              </div>
            </div>
          </div>
          <div className="p-4 border-t border-gray-200">
            <input
              type="text"
              placeholder="Введите сообщение..."
              className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  )
}