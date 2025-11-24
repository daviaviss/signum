# 📋 Sistema de Assinaturas - Documentação Técnica

## 🎯 Visão Geral
Sistema MVC para gerenciamento de assinaturas recorrentes com funcionalidade de compartilhamento entre usuários.

---

## 📦 Arquitetura de Classes

### **Assinatura** (Model - `mvc/models/assinaturas_model.py`)
**Herda de:** `Contrato`

**Atributos:**
- `id`, `user_id`, `nome`, `valor`, `data_vencimento`
- `periodicidade`, `tag` (categoria), `forma_pagamento`
- `usuario_compartilhado`, `login`, `senha`
- `favorito`, `status`, `created_at`, `is_readonly`

**Métodos:**
- `__init__(...)`: Inicializa assinatura, valida e converte status para enum
- `tipo` (property): Retorna "assinatura"

---

### **AssinaturasDAO** (Data Access Object - `dao.py`)

**Responsabilidade:** Comunicação com o banco de dados SQLite

**Métodos:**
- `adicionar_assinatura(assinatura) -> int`: Persiste nova assinatura
- `obter_assinaturas_por_usuario(user_id) -> List[Assinatura]`: Busca assinaturas próprias
- `obter_assinaturas_compartilhadas_comigo(user_id) -> List[Assinatura]`: Busca assinaturas compartilhadas
- `atualizar_assinatura(assinatura)`: Atualiza assinatura existente
- `deletar_assinatura(assinatura_id)`: Remove assinatura
- `alternar_favorito(assinatura_id)`: Marca/desmarca favorito
- `compartilhar_assinatura(id, proprietario_id, compartilhado_id) -> bool`: Cria compartilhamento

---

### **AssinaturasController** (Controller - `mvc/controllers/assinaturas_controller.py`)

**Responsabilidade:** Lógica de negócio e coordenação entre View e DAO

**Atributos:**
- `view`: Referência para AssinaturasView
- `user_id`: ID do usuário logado
- `usuario_controller`: Controlador de usuários
- `dao`: Instância de AssinaturasDAO
- `pagamentos_controller`: Controlador de pagamentos

**Métodos de Validação:**
- `obter_dados_formulario() -> dict`: Extrai dados da view
- `validar_dados_formulario(data, assinatura_id=None) -> dict`: Valida campos
- `_validar_data(date_str) -> dict`: Valida formato e valor da data
- `_verificar_nome_duplicado(nome, assinatura_id=None) -> dict`: Verifica unicidade

**Métodos de Negócio:**
- `adicionar(...) -> dict`: Cria nova assinatura
- `editar(...) -> dict`: Atualiza assinatura existente
- `remover(id) -> dict`: Remove assinatura (apenas ENCERRADAS)
- `alternar_favorito(id)`: Marca/desmarca favorito
- `calcular_total_assinaturas() -> float`: Calcula total com regras de compartilhamento
- `processar_compartilhamento(id, email) -> dict`: Valida e cria compartilhamento
- `renovar_vencimento_se_necessario(id) -> bool`: Renova data vencida automaticamente

**Métodos de Mensagens:**
- `mostrar_sucesso(titulo, mensagem)`: Exibe messagebox de sucesso
- `mostrar_erro(titulo, mensagem)`: Exibe messagebox de erro
- `mostrar_aviso(titulo, mensagem)`: Exibe messagebox de aviso
- `confirmar_acao(titulo, mensagem) -> bool`: Exibe diálogo de confirmação

---

### **AssinaturasView** (View - `mvc/views/assinaturas_view.py`)

**Responsabilidade:** Interface gráfica Tkinter

**Atributos:**
- `parent`: Frame pai
- `controller`: Referência para AssinaturasController
- `assinaturas_data`: Lista de assinaturas exibidas
- `tree`: TreeView para lista de assinaturas
- Componentes de formulário: `entry_nome`, `entry_valor`, `combo_periodicidade`, etc.

**Métodos de UI:**
- `_create_ui()`: Cria interface principal
- `_create_form(parent)`: Cria formulário de entrada
- `_create_treeview(parent)`: Cria lista de assinaturas

**Métodos de Eventos:**
- `_ao_adicionar()`: Handler do botão adicionar
- `_ao_remover()`: Handler do botão remover
- `_on_tree_click(event)`: Handler de clique no TreeView (favorito)
- `_on_double_click(event)`: Handler de duplo clique (detalhes)

**Métodos de Modais:**
- `_mostrar_modal_detalhes(assinatura)`: Exibe popup com detalhes completos
- `_mostrar_modal_edicao(assinatura)`: Exibe popup para edição

**Métodos de Atualização:**
- `atualizar_lista(assinaturas)`: Atualiza TreeView com nova lista
- `_atualizar_treeview()`: Renderiza dados no TreeView
- `_ordenar_coluna(col)`: Ordena lista por coluna clicada

---

## 🔄 Diagrama de Sequência: Adicionar Assinatura

### **Passo 1: Usuário Clica no Botão "Adicionar Assinatura"**

```
Usuário → View.btn_adicionar (click)
```

**O que acontece:**
- Botão configurado com `command=self._ao_adicionar`
- Evento de clique dispara método `_ao_adicionar()`

---

### **Passo 2: View Captura e Valida Dados**

```
View._ao_adicionar()
  │
  ├─► Controller.obter_dados_formulario()
  │     │
  │     └─► Retorna dict com dados dos Entry/Combobox:
  │           {
  │             'nome': string,
  │             'valor': string,
  │             'data_vencimento': string (DD/MM/AAAA),
  │             'periodicidade': string,
  │             'categoria': string,
  │             'forma_pagamento': string,
  │             'usuario_compartilhado': string,
  │             'login': string,
  │             'senha': string
  │           }
  │
  └─► Controller.validar_dados_formulario(data, assinatura_id=None)
```

**O que acontece:**
- View chama método do controller para extrair dados
- Controller lê valores dos widgets (Entry, Combobox)
- Normaliza dados (ex: substitui vírgula por ponto no valor)

---

### **Passo 3: Controller Valida Dados (5 Etapas)**

```
Controller.validar_dados_formulario(data, assinatura_id=None)
  │
  ├─► Etapa 1: Validar Campos Obrigatórios
  │     ├─ Verifica se nome, valor, data, periodicidade, categoria e forma_pagamento não estão vazios
  │     └─ Se falhar → retorna {'success': False, 'error_code': 'REQUIRED_FIELDS', ...}
  │
  ├─► Etapa 2: Validar Formato do Valor
  │     ├─ Tenta converter string para float
  │     ├─ Verifica se é >= 0
  │     └─ Se falhar → retorna {'success': False, 'error_code': 'INVALID_NUMBER', ...}
  │
  ├─► Etapa 3: Validar Formato da Data
  │     ├─ Tenta converter string para datetime (formato DD/MM/AAAA)
  │     └─ Se falhar → retorna {'success': False, 'error_code': 'INVALID_DATE_FORMAT', ...}
  │
  ├─► Etapa 4: Validar Data Não é Passada
  │     ├─ Compara data com datetime.now().date()
  │     └─ Se data < hoje → retorna {'success': False, 'error_code': 'INVALID_DATE_PAST', ...}
  │
  ├─► Etapa 5: Validar Nome Único
  │     ├─ Controller._verificar_nome_duplicado(nome, assinatura_id)
  │     │   ├─► DAO.obter_assinaturas_por_usuario(user_id)
  │     │   ├─► Itera sobre assinaturas existentes
  │     │   └─► Compara nomes (case-insensitive)
  │     └─ Se duplicado → retorna {'success': False, 'error_code': 'DUPLICATE_NAME', ...}
  │
  └─► Se tudo OK → retorna {'success': True, 'data': data_validada, ...}
```

**O que acontece:**
- Validações executam em ordem específica
- Primeira falha interrompe validação e retorna erro
- Dados validados incluem valor convertido para float

---

### **Passo 4: View Trata Resultado da Validação**

```
View._ao_adicionar()
  │
  └─► if not validation['success']:
        │
        └─► Controller.exibir_erro_validacao(validation)
              │
              ├─► Analisa error_code
              │     ├─ 'REQUIRED_FIELDS' → mostrar_aviso()
              │     └─ outros → mostrar_erro()
              │
              └─► messagebox exibe mensagem ao usuário
              
      INTERROMPE FLUXO (return)
```

**O que acontece:**
- Se validação falhar, exibe mensagem apropriada
- Fluxo para, usuário corrige dados e tenta novamente

---

### **Passo 5: Controller Cria Objeto Assinatura**

```
View._ao_adicionar() (continuação)
  │
  └─► Controller.adicionar(
        nome=validated_data['nome'],
        data_vencimento=validated_data['data_vencimento'],
        valor=validated_data['valor'],
        periodicidade=validated_data['periodicidade'],
        categoria=validated_data['categoria'],
        forma_pagamento=validated_data['forma_pagamento'],
        usuario_compartilhado=validated_data['usuario_compartilhado'],
        login=validated_data['login'],
        senha=validated_data['senha']
      )
      
Controller.adicionar(...)
  │
  └─► Controller._criar_objeto_assinatura(...)
        │
        └─► INSTANCIA: Assinatura(
              assinatura_id=None,  # Nova assinatura
              user_id=self.user_id,
              nome=nome,
              data_vencimento=data_vencimento,
              valor=valor,
              periodicidade=periodicidade,
              tag=categoria,
              forma_pagamento=forma_pagamento,
              usuario_compartilhado=usuario_compartilhado,
              login=login,
              senha=senha,
              favorito=0,
              status=StatusAssinatura.ATIVO
            )
            │
            └─► Assinatura.__init__() executa:
                  ├─ Chama super().__init__() (Contrato)
                  ├─ Define forma_pagamento, login, senha
                  ├─ Define created_at = datetime.now().isoformat()
                  ├─ Define is_readonly = False
                  └─ Converte status para StatusAssinatura enum
```

**O que acontece:**
- Controller recebe dados validados
- Cria instância do model Assinatura
- Assinatura herda de Contrato e adiciona atributos específicos
- Status inicializado como ATIVO
- Objeto em memória, ainda não persistido

---

### **Passo 6: DAO Persiste no Banco**

```
Controller.adicionar(...) (continuação)
  │
  └─► assinatura_id = DAO.adicionar_assinatura(assinatura)
        │
        ├─► Monta query SQL INSERT
        ├─► Executa INSERT na tabela 'assinaturas'
        ├─► Faz COMMIT
        └─► Retorna cursor.lastrowid (ID da nova assinatura)
```

**O que acontece:**
- DAO recebe objeto Assinatura
- Extrai atributos e insere no banco
- Retorna ID gerado pelo banco (autoincrement)
- Assinatura agora persiste no SQLite

---

### **Passo 7: Processamento de Compartilhamento (Se Informado)**

```
Controller.adicionar(...) (continuação)
  │
  └─► Controller._finalizar_operacao(
        assinatura_id,
        usuario_compartilhado,
        'Assinatura adicionada com sucesso!'
      )
      
Controller._finalizar_operacao(...)
  │
  └─► if usuario_compartilhado and usuario_compartilhado.strip():
        │
        └─► Controller.processar_compartilhamento(assinatura_id, usuario_compartilhado)
              │
              ├─► Valida email não vazio
              ├─► email = email.strip().lower()
              │
              ├─► INSTANCIA: UserDAO()
              │     │
              │     └─► UserDAO.get_user_id_by_email(email)
              │           ├─► Busca usuário no banco por email
              │           └─► Retorna user_id ou None
              │
              ├─► if not user_id_compartilhado:
              │     └─► Retorna erro: "Usuário não encontrado"
              │
              ├─► if user_id_compartilhado == self.user_id:
              │     └─► Retorna erro: "Não pode compartilhar consigo mesmo"
              │
              └─► DAO.compartilhar_assinatura(
                    assinatura_id,
                    self.user_id,  # proprietário
                    user_id_compartilhado
                  )
                  │
                  ├─► Remove compartilhamento anterior (se existir)
                  ├─► INSERT na tabela 'assinaturas_compartilhadas'
                  ├─► COMMIT
                  └─► Retorna True
```

**O que acontece:**
- Se campo email está preenchido, processa compartilhamento
- Valida que email existe no sistema
- Valida que não está compartilhando consigo mesmo
- Cria registro de compartilhamento na tabela auxiliar
- Se falhar, retorna erro mas assinatura JÁ FOI CRIADA

---

### **Passo 8: Recarregamento da Lista**

```
Controller._finalizar_operacao(...) (continuação)
  │
  └─► Controller._carregar_assinaturas()
        │
        ├─► Controller.renovar_todas_assinaturas_ativas()
        │     │
        │     └─► Para cada assinatura ATIVA vencida:
        │           └─► Controller.renovar_vencimento_se_necessario(id)
        │                 ├─► Calcula nova data baseada em periodicidade
        │                 └─► Chama Controller.editar() com nova data
        │
        ├─► assinaturas_proprias = DAO.obter_assinaturas_por_usuario(user_id)
        │     └─► SELECT assinaturas WHERE user_id = ?
        │
        ├─► assinaturas_compartilhadas = DAO.obter_assinaturas_compartilhadas_comigo(user_id)
        │     └─► SELECT assinaturas JOIN assinaturas_compartilhadas
        │           ├─► Marca is_readonly = True em cada assinatura
        │           └─► Retorna lista
        │
        ├─► todas_assinaturas = assinaturas_proprias + assinaturas_compartilhadas
        │
        └─► View.atualizar_lista(todas_assinaturas)
              │
              ├─► View.assinaturas_data = assinaturas
              │
              └─► View._atualizar_treeview()
                    │
                    ├─► Limpa TreeView (delete all items)
                    │
                    ├─► Para cada assinatura:
                    │     ├─► Formata valores (R$, favorito ★/☆)
                    │     └─► tree.insert() adiciona linha
                    │
                    ├─► Controller.calcular_total_assinaturas()
                    │     │
                    │     ├─► Para assinaturas próprias:
                    │     │     ├─ Se compartilhada → total += valor / 2
                    │     │     └─ Se não → total += valor
                    │     │
                    │     ├─► Para assinaturas compartilhadas comigo:
                    │     │     └─ total += valor / 2
                    │     │
                    │     └─► Retorna total
                    │
                    └─► Atualiza labels de total e diferença
```

**O que acontece:**
- Controller busca todas assinaturas do usuário (próprias + compartilhadas)
- Antes de buscar, renova assinaturas vencidas automaticamente
- Assinaturas compartilhadas marcadas como readonly
- View atualiza TreeView com nova lista completa
- Recalcula e exibe total (considerando regra: compartilhadas = metade)
- Calcula diferença (Meta - Total) e exibe com cor apropriada

---

### **Passo 9: Feedback ao Usuário**

```
View._ao_adicionar() (continuação)
  │
  └─► if resultado['success']:
        │
        ├─► Controller.limpar_formulario()
        │     └─► Limpa todos os Entry/Combobox do formulário
        │
        └─► Controller.mostrar_sucesso("Sucesso", resultado['message'])
              └─► messagebox.showinfo("✅ Sucesso", "Assinatura adicionada com sucesso!")
              
      else:
        │
        └─► Controller.mostrar_erro("Erro no Compartilhamento", resultado['message'])
              └─► messagebox.showerror("❌ Erro no Compartilhamento", mensagem)
```

**O que acontece:**
- Se sucesso: limpa formulário e exibe mensagem de sucesso
- Se erro no compartilhamento: exibe erro (mas assinatura já foi criada)
- Usuário vê lista atualizada com nova assinatura

---

## 📊 Resumo do Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Usuário preenche formulário e clica "Adicionar Assinatura"  │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. View._ao_adicionar()                                         │
│    └─ Captura dados do formulário via Controller               │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Controller.validar_dados_formulario()                        │
│    ├─ Campos obrigatórios                                       │
│    ├─ Formato do valor                                          │
│    ├─ Formato da data                                           │
│    ├─ Data >= hoje                                              │
│    └─ Nome único                                                │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Controller.adicionar()                                       │
│    └─ INSTANCIA Assinatura(dados validados)                    │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. DAO.adicionar_assinatura()                                   │
│    ├─ INSERT no banco de dados                                  │
│    └─ Retorna ID da nova assinatura                            │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Controller.processar_compartilhamento() [SE INFORMADO EMAIL] │
│    ├─ INSTANCIA UserDAO()                                       │
│    ├─ Busca usuário por email                                   │
│    ├─ Valida compartilhamento                                   │
│    └─ DAO.compartilhar_assinatura()                            │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. Controller._carregar_assinaturas()                           │
│    ├─ Renova assinaturas vencidas                              │
│    ├─ DAO busca assinaturas próprias                           │
│    ├─ DAO busca assinaturas compartilhadas                     │
│    └─ Combina listas                                            │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. View.atualizar_lista()                                       │
│    ├─ _atualizar_treeview() renderiza dados                    │
│    ├─ Controller.calcular_total_assinaturas()                  │
│    └─ Atualiza labels de total e diferença                     │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. Feedback ao Usuário                                          │
│    ├─ Controller.limpar_formulario()                            │
│    └─ Controller.mostrar_sucesso() exibe messagebox            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Regras de Negócio

1. **Validação Rigorosa:**
   - Campos obrigatórios: nome, valor, data, periodicidade, categoria, forma de pagamento
   - Valor deve ser número positivo
   - Data formato DD/MM/AAAA e >= data atual
   - Nome único por usuário (case-insensitive)

2. **Compartilhamento:**
   - Proprietário e usuário compartilhado pagam metade cada
   - Apenas proprietário pode editar/remover
   - Usuário compartilhado tem acesso readonly
   - Email deve existir no sistema

3. **Remoção:**
   - Apenas assinaturas ENCERRADAS podem ser removidas
   - Apenas o proprietário pode remover

4. **Renovação Automática:**
   - Assinaturas ATIVAS com data vencida são renovadas automaticamente
   - Nova data calculada baseada na periodicidade
   - Ocorre sempre ao carregar lista

5. **Cálculo de Total:**
   - Assinatura própria sem compartilhamento: valor integral
   - Assinatura própria compartilhada: metade do valor
   - Assinatura compartilhada comigo: metade do valor

---

## 🗄️ Estrutura do Banco de Dados

**Tabela: assinaturas**
- Armazena dados de cada assinatura
- Relaciona com user_id do proprietário

**Tabela: assinaturas_compartilhadas**
- Relaciona assinatura com usuário compartilhado
- UNIQUE constraint impede duplicatas
- ON DELETE CASCADE remove compartilhamento se assinatura for deletada

---

## 📝 Notas Importantes

- **Instanciações:** Assinatura criada em memória ANTES de persistir
- **UserDAO:** Instanciado apenas quando necessário (compartilhamento)
- **Transações:** DAO gerencia conexões e commits automaticamente
- **Validação em Cascata:** Primeira falha interrompe processo
- **Erro Não-Fatal:** Falha no compartilhamento não impede criação da assinatura

