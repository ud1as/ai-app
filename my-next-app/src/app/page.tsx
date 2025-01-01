export default function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mt-20">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Добро пожаловать в FLITCHAT
          </h1>
          <p className="text-xl text-gray-600 mb-12">
            Ваша платформа для создания AI-ассистентов
          </p>
          
          <div className="flex gap-4 justify-center mb-20">
            <a
              href="/studio"
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Начать работу со Студией
            </a>
            <a
              href="/knowledge"
              className="px-8 py-3 bg-white text-gray-700 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              Изучить базу знаний
            </a>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
            <div className="p-8 rounded-lg border border-gray-100 bg-white shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Создание чат-ботов
              </h3>
              <p className="text-gray-600">
                Создавайте и настраивайте чат-ботов с AI для ваших нужд
              </p>
            </div>

            <div className="p-8 rounded-lg border border-gray-100 bg-white shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Управление знаниями
              </h3>
              <p className="text-gray-600">
                Организуйте и поддерживайте вашу базу знаний AI эффективно
              </p>
            </div>

            <div className="p-8 rounded-lg border border-gray-100 bg-white shadow-sm">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Автоматизация рабочих процессов
              </h3>
              <p className="text-gray-600">
                Оптимизируйте ваши процессы с помощью интеллектуальной автоматизации
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}