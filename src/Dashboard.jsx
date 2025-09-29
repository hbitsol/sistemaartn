import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Loader2, Users, FolderOpen, DollarSign, TrendingUp, CheckCircle, Clock, XCircle, Send } from 'lucide-react'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Mock franchisee ID - in real app this would come from authentication
  const franchiseeId = '2dc82321-5f18-46f6-af0f-2b9a0f84e136'

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/dashboard/stats?franchisee_id=${franchiseeId}`)
      
      if (!response.ok) {
        throw new Error('Erro ao carregar estatísticas')
      }

      const data = await response.json()
      setStats(data)
    } catch (err) {
      setError('Erro ao carregar estatísticas: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Carregando dashboard...</span>
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Rascunho':
        return <Clock className="h-5 w-5" />
      case 'Enviado':
        return <Send className="h-5 w-5" />
      case 'Aprovado':
        return <CheckCircle className="h-5 w-5" />
      case 'Rejeitado':
        return <XCircle className="h-5 w-5" />
      default:
        return <Clock className="h-5 w-5" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'Rascunho':
        return 'text-gray-600'
      case 'Enviado':
        return 'text-blue-600'
      case 'Aprovado':
        return 'text-green-600'
      case 'Rejeitado':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="space-y-6">
      {/* Main Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_clients || 0}</div>
            <p className="text-xs text-muted-foreground">
              Clientes cadastrados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Projetos</CardTitle>
            <FolderOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_projects || 0}</div>
            <p className="text-xs text-muted-foreground">
              Projetos criados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Projetos Aprovados</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.approved_projects_count || 0}</div>
            <p className="text-xs text-muted-foreground">
              Projetos fechados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita Total</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {stats?.total_revenue?.toFixed(2) || '0.00'}
            </div>
            <p className="text-xs text-muted-foreground">
              De projetos aprovados
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Projects by Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Projetos por Status</CardTitle>
            <CardDescription>
              Distribuição dos seus projetos por status atual
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.projects_by_status && Object.entries(stats.projects_by_status).map(([status, count]) => (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={getStatusColor(status)}>
                      {getStatusIcon(status)}
                    </div>
                    <span className="font-medium">{status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold">{count}</span>
                    <span className="text-sm text-muted-foreground">projetos</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Resumo de Performance</CardTitle>
            <CardDescription>
              Indicadores principais do seu negócio
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-medium">Taxa de Aprovação</span>
                <span className="text-2xl font-bold text-green-600">
                  {stats?.total_projects > 0 
                    ? ((stats.approved_projects_count / stats.total_projects) * 100).toFixed(1)
                    : '0'
                  }%
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="font-medium">Ticket Médio</span>
                <span className="text-2xl font-bold text-blue-600">
                  R$ {stats?.approved_projects_count > 0 
                    ? (stats.total_revenue / stats.approved_projects_count).toFixed(2)
                    : '0.00'
                  }
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="font-medium">Projetos por Cliente</span>
                <span className="text-2xl font-bold text-purple-600">
                  {stats?.total_clients > 0 
                    ? (stats.total_projects / stats.total_clients).toFixed(1)
                    : '0'
                  }
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Próximos Passos
          </CardTitle>
          <CardDescription>
            Sugestões para melhorar seus resultados
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stats?.total_clients === 0 && (
              <div className="p-4 border border-blue-200 rounded-lg bg-blue-50">
                <h4 className="font-semibold text-blue-800 mb-2">Cadastre seu primeiro cliente</h4>
                <p className="text-sm text-blue-600">
                  Comece adicionando clientes para criar projetos e orçamentos.
                </p>
              </div>
            )}

            {stats?.projects_by_status?.Rascunho > 0 && (
              <div className="p-4 border border-yellow-200 rounded-lg bg-yellow-50">
                <h4 className="font-semibold text-yellow-800 mb-2">
                  {stats.projects_by_status.Rascunho} projeto(s) em rascunho
                </h4>
                <p className="text-sm text-yellow-600">
                  Finalize e envie seus projetos para os clientes.
                </p>
              </div>
            )}

            {stats?.projects_by_status?.Enviado > 0 && (
              <div className="p-4 border border-blue-200 rounded-lg bg-blue-50">
                <h4 className="font-semibold text-blue-800 mb-2">
                  {stats.projects_by_status.Enviado} projeto(s) aguardando resposta
                </h4>
                <p className="text-sm text-blue-600">
                  Faça o acompanhamento com seus clientes.
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

