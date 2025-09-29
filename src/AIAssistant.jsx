import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Loader2, Bot, Lightbulb, TrendingUp, MessageCircle, Sparkles } from 'lucide-react'

const AIAssistant = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  // Project Description Generator
  const [projectMaterials, setProjectMaterials] = useState('')
  const [clientName, setClientName] = useState('')
  const [projectType, setProjectType] = useState('')
  const [generatedDescription, setGeneratedDescription] = useState('')
  
  // Material Suggestions
  const [suggestionProjectType, setSuggestionProjectType] = useState('')
  const [roomType, setRoomType] = useState('')
  const [budgetRange, setBudgetRange] = useState('')
  const [style, setStyle] = useState('')
  const [materialSuggestions, setMaterialSuggestions] = useState([])
  
  // Virtual Assistant
  const [question, setQuestion] = useState('')
  const [assistantResponse, setAssistantResponse] = useState('')
  
  // Pricing Analysis
  const [pricingAnalysis, setPricingAnalysis] = useState(null)

  const franchiseeId = '2dc82321-5f18-46f6-af0f-2b9a0f84e136'

  const generateProjectDescription = async () => {
    if (!projectMaterials.trim()) {
      setError('Informe os materiais do projeto')
      return
    }

    try {
      setLoading(true)
      setError('')
      
      // Parse materials from text input
      const materials = projectMaterials.split('\n').map(line => {
        const parts = line.trim().split(' ')
        return {
          name: parts.slice(0, -2).join(' '),
          quantity: parts[parts.length - 2] || '1',
          unit: parts[parts.length - 1] || 'un'
        }
      }).filter(m => m.name)

      const response = await fetch('/api/ai/generate-project-description', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          materials,
          client_info: { name: clientName },
          project_type: projectType || 'decoração'
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao gerar descrição')
      }

      const data = await response.json()
      setGeneratedDescription(data.description)
    } catch (err) {
      setError('Erro ao gerar descrição: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getSuggestedMaterials = async () => {
    if (!suggestionProjectType.trim()) {
      setError('Informe o tipo de projeto')
      return
    }

    try {
      setLoading(true)
      setError('')

      const response = await fetch('/api/ai/suggest-materials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_type: suggestionProjectType,
          room_type: roomType,
          budget_range: budgetRange,
          style: style
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao obter sugestões')
      }

      const data = await response.json()
      setMaterialSuggestions(data.suggestions || [])
    } catch (err) {
      setError('Erro ao obter sugestões: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const askVirtualAssistant = async () => {
    if (!question.trim()) {
      setError('Digite sua pergunta')
      return
    }

    try {
      setLoading(true)
      setError('')

      const response = await fetch('/api/ai/virtual-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          context: {}
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao consultar assistente')
      }

      const data = await response.json()
      setAssistantResponse(data.response)
    } catch (err) {
      setError('Erro ao consultar assistente: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const analyzePricingTrends = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch('/api/ai/analyze-pricing-trends', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          franchisee_id: franchiseeId
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao analisar tendências')
      }

      const data = await response.json()
      setPricingAnalysis(data)
    } catch (err) {
      setError('Erro ao analisar tendências: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-6 w-6" />
            Assistente Inteligente
          </CardTitle>
          <CardDescription>
            Utilize IA para otimizar seus projetos, obter sugestões e análises inteligentes
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Tabs defaultValue="description" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="description">Descrições</TabsTrigger>
              <TabsTrigger value="suggestions">Sugestões</TabsTrigger>
              <TabsTrigger value="assistant">Assistente</TabsTrigger>
              <TabsTrigger value="analysis">Análises</TabsTrigger>
            </TabsList>

            <TabsContent value="description" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5" />
                    Gerador de Descrições de Projeto
                  </CardTitle>
                  <CardDescription>
                    Crie descrições profissionais automaticamente baseadas nos materiais
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="clientName">Nome do Cliente</Label>
                      <Input
                        id="clientName"
                        value={clientName}
                        onChange={(e) => setClientName(e.target.value)}
                        placeholder="Nome do cliente"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="projectType">Tipo de Projeto</Label>
                      <Input
                        id="projectType"
                        value={projectType}
                        onChange={(e) => setProjectType(e.target.value)}
                        placeholder="Ex: Reforma de sala, Decoração de quarto"
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="materials">Materiais (um por linha)</Label>
                    <Textarea
                      id="materials"
                      value={projectMaterials}
                      onChange={(e) => setProjectMaterials(e.target.value)}
                      placeholder="Ex:&#10;MDF 15mm 10 m²&#10;Tecido Algodão 5 m&#10;Tinta Acrílica 2 L"
                      rows={6}
                    />
                  </div>
                  
                  <Button 
                    onClick={generateProjectDescription} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Gerando...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4 mr-2" />
                        Gerar Descrição
                      </>
                    )}
                  </Button>
                  
                  {generatedDescription && (
                    <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                      <h4 className="font-semibold text-green-800 mb-2">Descrição Gerada:</h4>
                      <p className="text-green-700">{generatedDescription}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="suggestions" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="h-5 w-5" />
                    Sugestões Inteligentes de Materiais
                  </CardTitle>
                  <CardDescription>
                    Obtenha sugestões de materiais baseadas em IA para seu projeto
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="suggestionProjectType">Tipo de Projeto</Label>
                      <Input
                        id="suggestionProjectType"
                        value={suggestionProjectType}
                        onChange={(e) => setSuggestionProjectType(e.target.value)}
                        placeholder="Ex: Reforma de cozinha"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="roomType">Tipo de Ambiente</Label>
                      <Select value={roomType} onValueChange={setRoomType}>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione o ambiente" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="sala">Sala</SelectItem>
                          <SelectItem value="quarto">Quarto</SelectItem>
                          <SelectItem value="cozinha">Cozinha</SelectItem>
                          <SelectItem value="banheiro">Banheiro</SelectItem>
                          <SelectItem value="escritorio">Escritório</SelectItem>
                          <SelectItem value="area-externa">Área Externa</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="budgetRange">Faixa de Orçamento</Label>
                      <Select value={budgetRange} onValueChange={setBudgetRange}>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione a faixa" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="baixo">Baixo (até R$ 5.000)</SelectItem>
                          <SelectItem value="medio">Médio (R$ 5.000 - R$ 15.000)</SelectItem>
                          <SelectItem value="alto">Alto (R$ 15.000 - R$ 30.000)</SelectItem>
                          <SelectItem value="premium">Premium (acima de R$ 30.000)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="style">Estilo Desejado</Label>
                      <Select value={style} onValueChange={setStyle}>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione o estilo" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="moderno">Moderno</SelectItem>
                          <SelectItem value="classico">Clássico</SelectItem>
                          <SelectItem value="minimalista">Minimalista</SelectItem>
                          <SelectItem value="rustico">Rústico</SelectItem>
                          <SelectItem value="industrial">Industrial</SelectItem>
                          <SelectItem value="escandinavo">Escandinavo</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <Button 
                    onClick={getSuggestedMaterials} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Analisando...
                      </>
                    ) : (
                      <>
                        <Lightbulb className="h-4 w-4 mr-2" />
                        Obter Sugestões
                      </>
                    )}
                  </Button>
                  
                  {materialSuggestions.length > 0 && (
                    <div className="mt-4 space-y-3">
                      <h4 className="font-semibold">Materiais Sugeridos:</h4>
                      {materialSuggestions.map((suggestion, index) => (
                        <div key={index} className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex justify-between items-start">
                            <div>
                              <h5 className="font-medium text-blue-800">
                                {suggestion.material_name}
                              </h5>
                              <p className="text-sm text-blue-600">
                                Quantidade sugerida: {suggestion.suggested_quantity} {suggestion.unit}
                              </p>
                            </div>
                          </div>
                          <p className="text-sm text-blue-700 mt-2">
                            {suggestion.justification}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="assistant" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MessageCircle className="h-5 w-5" />
                    Assistente Virtual
                  </CardTitle>
                  <CardDescription>
                    Faça perguntas sobre decoração, materiais e processos
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="question">Sua Pergunta</Label>
                    <Textarea
                      id="question"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="Ex: Qual a melhor tinta para cozinha? Como calcular a quantidade de papel de parede?"
                      rows={3}
                    />
                  </div>
                  
                  <Button 
                    onClick={askVirtualAssistant} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Consultando...
                      </>
                    ) : (
                      <>
                        <MessageCircle className="h-4 w-4 mr-2" />
                        Perguntar ao Assistente
                      </>
                    )}
                  </Button>
                  
                  {assistantResponse && (
                    <div className="mt-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                      <h4 className="font-semibold text-purple-800 mb-2">Resposta do Assistente:</h4>
                      <p className="text-purple-700 whitespace-pre-wrap">{assistantResponse}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="analysis" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    Análise de Tendências de Preços
                  </CardTitle>
                  <CardDescription>
                    Obtenha insights inteligentes sobre seus preços e margens
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button 
                    onClick={analyzePricingTrends} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Analisando...
                      </>
                    ) : (
                      <>
                        <TrendingUp className="h-4 w-4 mr-2" />
                        Analisar Tendências
                      </>
                    )}
                  </Button>
                  
                  {pricingAnalysis && (
                    <div className="mt-4 space-y-4">
                      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <h4 className="font-semibold text-yellow-800 mb-2">Análise:</h4>
                        <p className="text-yellow-700">{pricingAnalysis.analysis}</p>
                      </div>
                      
                      {pricingAnalysis.recommendations && pricingAnalysis.recommendations.length > 0 && (
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                          <h4 className="font-semibold text-green-800 mb-2">Recomendações:</h4>
                          <ul className="list-disc list-inside space-y-1">
                            {pricingAnalysis.recommendations.map((rec, index) => (
                              <li key={index} className="text-green-700">{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {pricingAnalysis.key_metrics && (
                        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <h4 className="font-semibold text-blue-800 mb-2">Métricas Principais:</h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {Object.entries(pricingAnalysis.key_metrics).map(([key, value]) => (
                              <div key={key} className="text-center">
                                <p className="text-sm text-blue-600 capitalize">
                                  {key.replace('_', ' ')}
                                </p>
                                <p className="text-lg font-bold text-blue-800">{value}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

export default AIAssistant

