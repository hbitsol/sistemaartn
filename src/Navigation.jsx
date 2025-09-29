import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card } from '@/components/ui/card.jsx'
import { BarChart3, Calculator, Users, FolderOpen, Bot } from 'lucide-react'

const Navigation = ({ activeTab, onTabChange }) => {
  const tabs = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: BarChart3,
      description: 'Visão geral dos seus negócios'
    },
    {
      id: 'pricing',
      label: 'Precificação',
      icon: Calculator,
      description: 'Calcule preços de projetos'
    },
    {
      id: 'clients',
      label: 'Clientes',
      icon: Users,
      description: 'Gerencie seus clientes'
    },
    {
      id: 'projects',
      label: 'Projetos',
      icon: FolderOpen,
      description: 'Visualize seus projetos'
    },
    {
      id: 'ai-assistant',
      label: 'IA Assistant',
      icon: Bot,
      description: 'Assistente inteligente'
    }
  ]

  return (
    <Card className="p-4">
      <nav className="space-y-2">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          
          return (
            <Button
              key={tab.id}
              variant={isActive ? 'default' : 'ghost'}
              className={`w-full justify-start h-auto p-3 ${
                isActive ? 'bg-blue-600 text-white' : 'hover:bg-gray-100'
              }`}
              onClick={() => onTabChange(tab.id)}
            >
              <div className="flex items-center gap-3">
                <Icon className="h-5 w-5" />
                <div className="text-left">
                  <div className="font-medium">{tab.label}</div>
                  <div className={`text-xs ${
                    isActive ? 'text-blue-100' : 'text-gray-500'
                  }`}>
                    {tab.description}
                  </div>
                </div>
              </div>
            </Button>
          )
        })}
      </nav>
    </Card>
  )
}

export default Navigation

