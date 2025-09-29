import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx';
import { Alert, AlertDescription } from '@/components/ui/alert.jsx';
import { Loader2, Calculator, Plus, Trash2 } from 'lucide-react';

const PricingCalculator = () => {
  const [materials, setMaterials] = useState([]);
  const [difficultyFactors, setDifficultyFactors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState(null);
  const [items, setItems] = useState([{
    id: 1,
    materialId: '',
    quantity: '',
    difficultyId: '',
    employeeLevel: 'Ajudante de Envelopador', // Default employee level
    estimatedDays: '', // New field
    numEnvelopers: '', // New field
    result: null
  }]);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      const [materialsRes, difficultyRes] = await Promise.all([
        fetch('/api/materials'),
        fetch('/api/difficulty-factors')
      ]);

      if (!materialsRes.ok || !difficultyRes.ok) {
        throw new Error('Erro ao carregar dados');
      }

      const materialsData = await materialsRes.json();
      const difficultyData = await difficultyRes.json();

      setMaterials(materialsData);
      setDifficultyFactors(difficultyData);
    } catch (err) {
      setError('Erro ao carregar dados: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const addItem = () => {
    const newId = Math.max(...items.map(item => item.id)) + 1;
    setItems([...items, {
      id: newId,
      materialId: '',
      quantity: '',
      difficultyId: '',
      employeeLevel: 'Ajudante de Envelopador', // Default employee level for new items
      estimatedDays: '',
      numEnvelopers: '',
      result: null
    }]);
  };

  const removeItem = (id) => {
    if (items.length > 1) {
      setItems(items.filter(item => item.id !== id));
    }
  };

  const updateItem = (id, field, value) => {
    setItems(items.map(item => 
      item.id === id ? { ...item, [field]: value, result: null } : item
    ));
  };

  const calculatePrice = async (itemId) => {
    const item = items.find(i => i.id === itemId);
    if (!item.materialId || !item.quantity || !item.difficultyId || !item.employeeLevel || !item.estimatedDays || !item.numEnvelopers) {
      setError('Preencha todos os campos do item');
      return;
    }

    try {
      setCalculating(true);
      setError(null);

      const response = await fetch('/api/calculate-price', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          material_id: item.materialId,
          quantity: parseFloat(item.quantity),
          difficulty_id: item.difficultyId,
          employee_level: item.employeeLevel,
          estimated_days: parseFloat(item.estimatedDays),
          num_envelopers: parseFloat(item.numEnvelopers)
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao calcular preço');
      }

      const result = await response.json();
      
      setItems(items.map(i => 
        i.id === itemId ? { ...i, result } : i
      ));
    } catch (err) {
      setError('Erro ao calcular preço: ' + err.message);
    } finally {
      setCalculating(false);
    }
  };

  const getTotalProject = () => {
    const itemsWithResults = items.filter(item => item.result);
    if (itemsWithResults.length === 0) return null;

    const totalMaterialCost = itemsWithResults.reduce((sum, item) => sum + item.result.material_cost, 0);
    const totalLaborCost = itemsWithResults.reduce((sum, item) => sum + item.result.labor_cost, 0);
    const totalCost = itemsWithResults.reduce((sum, item) => sum + item.result.total_cost, 0);
    const totalSelling = itemsWithResults.reduce((sum, item) => sum + item.result.selling_price, 0);

    return {
      totalMaterialCost,
      totalLaborCost,
      totalCost,
      totalSelling,
      itemCount: itemsWithResults.length
    };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Carregando dados...</span>
      </div>
    );
  }

  const projectTotal = getTotalProject();

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calculator className="h-6 w-6" />
            Calculadora de Precificação
          </CardTitle>
          <CardDescription>
            Calcule o preço de projetos de decoração baseado em materiais, grau de dificuldade e nível do funcionário.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {items.map((item, index) => (
            <Card key={item.id} className="border-l-4 border-l-blue-500">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Item {index + 1}</CardTitle>
                  {items.length > 1 && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => removeItem(item.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor={`material-${item.id}`}>Material</Label>
                    <Select
                      value={item.materialId}
                      onValueChange={(value) => updateItem(item.id, 'materialId', value)}
                    >
                      <SelectTrigger id={`material-${item.id}`}>
                        <SelectValue placeholder="Selecione o material" />
                      </SelectTrigger>
                      <SelectContent>
                        {materials.map((material) => (
                          <SelectItem key={material.id} value={material.id}>
                            {material.nome} ({material.unidade_medida}) - R$ {material.custo_unitario_base.toFixed(2)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`quantity-${item.id}`}>Quantidade</Label>
                    <Input
                      id={`quantity-${item.id}`}
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      value={item.quantity}
                      onChange={(e) => updateItem(item.id, 'quantity', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`difficulty-${item.id}`}>Grau de Dificuldade</Label>
                    <Select
                      value={item.difficultyId}
                      onValueChange={(value) => updateItem(item.id, 'difficultyId', value)}
                    >
                      <SelectTrigger id={`difficulty-${item.id}`}>
                        <SelectValue placeholder="Selecione a dificuldade" />
                      </SelectTrigger>
                      <SelectContent>
                        {difficultyFactors.map((factor) => (
                          <SelectItem key={factor.id} value={factor.id}>
                            {factor.nivel}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`employee-level-${item.id}`}>Nível do Funcionário</Label>
                    <Select
                      value={item.employeeLevel}
                      onValueChange={(value) => updateItem(item.id, 'employeeLevel', value)}
                    >
                      <SelectTrigger id={`employee-level-${item.id}`}>
                        <SelectValue placeholder="Selecione o nível" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Ajudante de Envelopador">Ajudante de Envelopador</SelectItem>
                        <SelectItem value="Envelopador Pleno">Envelopador Pleno</SelectItem>
                        <SelectItem value="Envelopador Senior">Envelopador Senior</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`estimated-days-${item.id}`}>Duração Estimada (dias)</Label>
                    <Input
                      id={`estimated-days-${item.id}`}
                      type="number"
                      step="0.5"
                      min="0.5"
                      placeholder="Ex: 1.5"
                      value={item.estimatedDays}
                      onChange={(e) => updateItem(item.id, 'estimatedDays', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`num-envelopers-${item.id}`}>Número de Envelopadores</Label>
                    <Input
                      id={`num-envelopers-${item.id}`}
                      type="number"
                      step="1"
                      min="1"
                      placeholder="Ex: 2"
                      value={item.numEnvelopers}
                      onChange={(e) => updateItem(item.id, 'numEnvelopers', e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex justify-between items-center">
                  <Button
                    onClick={() => calculatePrice(item.id)}
                    disabled={calculating || !item.materialId || !item.quantity || !item.difficultyId || !item.employeeLevel || !item.estimatedDays || !item.numEnvelopers}
                    className="w-auto"
                  >
                    {calculating ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Calculando...
                      </>
                    ) : (
                      'Calcular Preço'
                    )}
                  </Button>
                </div>

                {item.result && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 space-y-2">
                    <h4 className="font-semibold text-green-800">Resultado do Cálculo:</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Custo Material:</span>
                        <p className="font-semibold">R$ {item.result.material_cost.toFixed(2)}</p>
                      </div>
                      <div>
                        <span className="text-gray-600">Custo Mão de Obra:</span>
                        <p className="font-semibold">R$ {item.result.labor_cost.toFixed(2)}</p>
                      </div>
                      <div>
                        <span className="text-gray-600">Custo Total (c/ Imposto):</span>
                        <p className="font-semibold">R$ {item.result.total_cost.toFixed(2)}</p>
                      </div>
                      <div>
                        <span className="text-gray-600">Preço de Venda:</span>
                        <p className="font-semibold text-green-700">R$ {item.result.selling_price.toFixed(2)}</p>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}

          <div className="flex justify-between items-center">
            <Button
              variant="outline"
              onClick={addItem}
              className="flex items-center gap-2"
            >
              <Plus className="h-4 w-4" />
              Adicionar Item
            </Button>
          </div>

          {projectTotal && (
            <Card className="bg-blue-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-blue-800">Resumo do Projeto</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <span className="text-blue-600">Itens Calculados:</span>
                    <p className="text-2xl font-bold text-blue-800">{projectTotal.itemCount}</p>
                  </div>
                  <div>
                    <span className="text-blue-600">Custo Material Total:</span>
                    <p className="text-2xl font-bold text-blue-800">R$ {projectTotal.totalMaterialCost.toFixed(2)}</p>
                  </div>
                  <div>
                    <span className="text-blue-600">Custo Mão de Obra Total:</span>
                    <p className="text-2xl font-bold text-blue-800">R$ {projectTotal.totalLaborCost.toFixed(2)}</p>
                  </div>
                  <div>
                    <span className="text-blue-600">Preço de Venda Total:</span>
                    <p className="text-2xl font-bold text-green-700">R$ {projectTotal.totalSelling.toFixed(2)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PricingCalculator;


