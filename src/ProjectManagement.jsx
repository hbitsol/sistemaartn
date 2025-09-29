import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Loader2, FolderOpen, Eye, Trash2, Calendar, DollarSign, User } from 'lucide-react'

const ProjectManagement = () => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedProject, setSelectedProject] = useState(null)
  const [projectItems, setProjectItems] = useState([])

  // Mock franchisee ID - in real app this would come from authentication
  const franchiseeId = '2dc82321-5f18-46f6-af0f-2b9a0f84e136'

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/projects?franchisee_id=${franchiseeId}`)
      
      if (!response.ok) {
        throw new Error('Erro ao carregar projetos')
      }

      const data = await response.json()
      setProjects(data)
    } catch (err) {
      setError('Erro ao carregar projetos: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchProjectItems = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/items`)
      
      if (!response.ok) {
        throw new Error('Erro ao carregar itens do projeto')
      }

      const data = await response.json()
      setProjectItems(data)
    } catch (err) {
      setError('Erro ao carregar itens do projeto: ' + err.message)
    }
  }

  const updateProjectStatus = async (projectId, newStatus) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
      })

      if (!response.ok) {
        throw new Error('Erro ao atualizar status do projeto')
      }

      await fetchProjects()
    } catch (err) {
      setError('Erro ao atualizar status: ' + err.message)
    }
  }

  const deleteProject = async (projectId) => {
    if (!confirm('Tem certeza que deseja excluir este projeto?')) {
      return
    }

    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Erro ao excluir projeto')
      }

      await fetchProjects()
      if (selectedProject && selectedProject.id === projectId) {
        setSelectedProject(null)
        setProjectItems([])
      }
    } catch (err) {
      setError('Erro ao excluir projeto: ' + err.message)
    }
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Rascunho': { variant: 'secondary', color: 'bg-gray-100 text-gray-800' },
      'Enviado': { variant: 'default', color: 'bg-blue-100 text-blue-800' },
      'Aprovado': { variant: 'default', color: 'bg-green-100 text-green-800' },
      'Rejeitado': { variant: 'destructive', color: 'bg-red-100 text-red-800' }
    }

    const config = statusConfig[status] || statusConfig['Rascunho']
    
    return (
      <Badge className={config.color}>
        {status}
      </Badge>
    )
  }

  const handleViewProject = async (project) => {
    setSelectedProject(project)
    await fetchProjectItems(project.id)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Carregando projetos...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FolderOpen className="h-6 w-6" />
            Gestão de Projetos
          </CardTitle>
          <CardDescription>
            Visualize e gerencie todos os seus projetos e orçamentos
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {projects.length === 0 ? (
            <div className="text-center py-8">
              <FolderOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum projeto encontrado</h3>
              <p className="text-gray-500 mb-4">Crie seu primeiro projeto usando a calculadora de precificação</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Projeto</TableHead>
                    <TableHead>Cliente</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Data Criação</TableHead>
                    <TableHead>Valor Total</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {projects.map((project) => (
                    <TableRow key={project.id}>
                      <TableCell className="font-medium">{project.nome_projeto}</TableCell>
                      <TableCell>
                        {project.client && (
                          <div className="flex items-center gap-1">
                            <User className="h-4 w-4 text-gray-400" />
                            {project.client.nome}
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <Select
                          value={project.status}
                          onValueChange={(value) => updateProjectStatus(project.id, value)}
                        >
                          <SelectTrigger className="w-32">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Rascunho">Rascunho</SelectItem>
                            <SelectItem value="Enviado">Enviado</SelectItem>
                            <SelectItem value="Aprovado">Aprovado</SelectItem>
                            <SelectItem value="Rejeitado">Rejeitado</SelectItem>
                          </SelectContent>
                        </Select>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 text-sm text-gray-600">
                          <Calendar className="h-4 w-4" />
                          {new Date(project.data_criacao).toLocaleDateString('pt-BR')}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 font-medium text-green-600">
                          <DollarSign className="h-4 w-4" />
                          R$ {project.preco_venda_sugerido.toFixed(2)}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleViewProject(project)}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => deleteProject(project.id)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {selectedProject && (
        <Card>
          <CardHeader>
            <CardTitle>Detalhes do Projeto: {selectedProject.nome_projeto}</CardTitle>
            <CardDescription>
              Cliente: {selectedProject.client?.nome} | Status: {getStatusBadge(selectedProject.status)}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800">Custo Total</h4>
                <p className="text-2xl font-bold text-blue-900">
                  R$ {selectedProject.custo_total_estimado.toFixed(2)}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold text-green-800">Preço de Venda</h4>
                <p className="text-2xl font-bold text-green-900">
                  R$ {selectedProject.preco_venda_sugerido.toFixed(2)}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800">Margem de Lucro</h4>
                <p className="text-2xl font-bold text-purple-900">
                  {(selectedProject.margem_lucro_aplicada * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            {projectItems.length > 0 && (
              <div>
                <h4 className="font-semibold mb-4">Itens do Projeto</h4>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Material</TableHead>
                        <TableHead>Quantidade</TableHead>
                        <TableHead>Dificuldade</TableHead>
                        <TableHead>Custo</TableHead>
                        <TableHead>Preço Venda</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {projectItems.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell>
                            {item.material?.nome} ({item.material?.unidade_medida})
                          </TableCell>
                          <TableCell>{item.quantidade}</TableCell>
                          <TableCell>
                            {item.difficulty?.nivel} ({item.difficulty?.fator_multiplicador_mao_obra}x)
                          </TableCell>
                          <TableCell>R$ {item.custo_item.toFixed(2)}</TableCell>
                          <TableCell className="font-medium text-green-600">
                            R$ {item.preco_venda_item.toFixed(2)}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default ProjectManagement

