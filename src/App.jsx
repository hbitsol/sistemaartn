import { useState } from 'react'
import Navigation from './components/Navigation.jsx'
import Dashboard from './components/Dashboard.jsx'
import PricingCalculator from './components/PricingCalculator.jsx'
import ClientManagement from './components/ClientManagement.jsx'
import ProjectManagement from './components/ProjectManagement.jsx'
import AIAssistant from './components/AIAssistant.jsx'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'pricing':
        return <PricingCalculator />
      case 'clients':
        return <ClientManagement />
      case 'projects':
        return <ProjectManagement />
      case 'ai-assistant':
        return <AIAssistant />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Sistema de Precificação e CRM - Franquia Decoração
          </h1>
          <p className="text-gray-600 mt-1">
            Gerencie clientes, projetos e calcule preços de forma integrada
          </p>
        </div>
      </header>
      
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
          </div>
          
          {/* Main Content */}
          <div className="lg:col-span-3">
            {renderContent()}
          </div>
        </div>
      </div>
      
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-gray-500">
          <p>© 2025 Sistema de Precificação e CRM - Franquia Decoração</p>
        </div>
      </footer>
    </div>
  )
}

export default App
