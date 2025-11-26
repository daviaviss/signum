from dao import AssinaturasDAO
from mvc.models.assinaturas_model import Assinatura
from mvc.models.periodicidade_enum import Periodicidade
from mvc.models.assinatura_categoria_enum import CategoriaAssinatura
from mvc.models.status_enum import Status
from datetime import datetime
from tkinter import messagebox


class AssinaturasController:
    """Controller para Assinaturas."""
    
    def __init__(self, view, user_id=None, usuario_controller=None):
        self.view = view
        self.user_id = user_id
        self.usuario_controller = usuario_controller
        self.dao = AssinaturasDAO()
        self.view.controller = self
        
        from mvc.controllers.pagamentos_controller import PagamentosController
        self.pagamentos_controller = PagamentosController(user_id=user_id)
        
        self.view.set_combo_values(
            [p.value for p in Periodicidade],
            [c.value for c in CategoriaAssinatura],
            self.pagamentos_controller.obter_nomes_metodos_pagamento()
        )
        
        self._carregar_assinaturas()
    
    # Métodos de mensagens
    
    @staticmethod
    def mostrar_sucesso(titulo: str, mensagem: str):
        """Exibe mensagem de sucesso com ícone verde."""
        messagebox.showinfo(f"✅ {titulo}", mensagem)
    
    @staticmethod
    def mostrar_erro(titulo: str, mensagem: str):
        """Exibe mensagem de erro com ícone vermelho."""
        messagebox.showerror(f"❌ {titulo}", mensagem)
    
    @staticmethod
    def mostrar_aviso(titulo: str, mensagem: str):
        """Exibe mensagem de aviso com ícone amarelo."""
        messagebox.showwarning(f"⚠️ {titulo}", mensagem)
    
    @staticmethod
    def confirmar_acao(titulo: str, mensagem: str) -> bool:
        """
        Exibe diálogo de confirmação.
        
        Returns:
            bool: True se confirmou, False se cancelou
        """
        return messagebox.askyesno(f"❓ {titulo}", mensagem)
    
    def _exibir_erro_campos_obrigatorios(self, mensagem: str):
        """Exibe erro de campos obrigatórios não preenchidos."""
        self.mostrar_aviso("Campos Obrigatórios", mensagem)
    
    def _exibir_erro_valor_invalido(self, mensagem: str):
        """Exibe erro de valor com formato inválido."""
        self.mostrar_erro("Valor Inválido", mensagem)
    
    def _exibir_erro_data_invalida(self, mensagem: str):
        """Exibe erro de data com formato ou valor inválido."""
        self.mostrar_erro("Data Inválida", mensagem)
    
    def _exibir_erro_nome_duplicado(self, mensagem: str):
        """Exibe erro de nome duplicado."""
        self.mostrar_erro("Nome Duplicado", mensagem)
    
    def _exibir_erro_compartilhamento_proprio(self, mensagem: str):
        """Exibe erro de tentativa de compartilhar consigo mesmo."""
        self.mostrar_erro("Compartilhamento Inválido", mensagem)
    
    def _exibir_erro_generico(self, mensagem: str):
        """Exibe erro genérico de validação."""
        self.mostrar_erro("Erro de Validação", mensagem)
    
    def _obter_mapeamento_erros_validacao(self):
        """
        Retorna o mapeamento entre error_code e método de exibição.
        
        Returns:
            dict: Dicionário mapeando error_code para método
        """
        return {
            'REQUIRED_FIELDS': self._exibir_erro_campos_obrigatorios,
            'INVALID_NUMBER': self._exibir_erro_valor_invalido,
            'INVALID_DATE_FORMAT': self._exibir_erro_data_invalida,
            'INVALID_DATE_PAST': self._exibir_erro_data_invalida,
            'DUPLICATE_NAME': self._exibir_erro_nome_duplicado,
            'SELF_SHARE': self._exibir_erro_compartilhamento_proprio
        }
    
    def exibir_erro_validacao(self, validacao):
        """
        Exibe a mensagem de erro apropriada baseado no código de validação.
        Usa mapeamento de error_code para método específico.
        
        Args:
            validacao: Dicionário retornado por validar_dados_formulario
        """
        error_code = validacao.get('error_code', '')
        mensagem = validacao.get('message', 'Erro desconhecido')
        
        mapeamento_erros = self._obter_mapeamento_erros_validacao()
        metodo_exibicao = mapeamento_erros.get(error_code, self._exibir_erro_generico)
        metodo_exibicao(mensagem)
    
    # Métodos de negócio
    
    def _carregar_assinaturas(self):
        """Carrega e exibe as assinaturas do usuário (próprias + compartilhadas)."""
        if self.user_id:
            # Renova assinaturas ativas vencidas
            self.renovar_todas_assinaturas_ativas()
            
            # Busca assinaturas próprias
            assinaturas_proprias = self.dao.obter_assinaturas_por_usuario(self.user_id)
            
            # Busca assinaturas compartilhadas comigo
            assinaturas_compartilhadas = self.dao.obter_assinaturas_compartilhadas_comigo(self.user_id)
            
            # Combina listas
            todas_assinaturas = assinaturas_proprias + assinaturas_compartilhadas
            
            # Ordena favoritos primeiro
            todas_assinaturas.sort(key=lambda a: (a.favorito != 1, a.data_vencimento))
            
            self.view.atualizar_lista(todas_assinaturas)
    
    def calcular_total_assinaturas(self, assinaturas=None):
        """
        Calcula o valor total de assinaturas ativas do usuário.
        
        Regras:
        - Assinatura própria sem compartilhamento: valor integral
        - Assinatura própria compartilhada: metade do valor
        - Assinatura compartilhada comigo: metade do valor
        
        Args:
            assinaturas: Lista de assinaturas (opcional). Se None, busca do usuário atual.
            
        Returns:
            float: Soma total dos valores
        """
        if not self.user_id:
            return 0.0
        
        # Busca assinaturas próprias
        assinaturas_proprias = self.dao.obter_assinaturas_por_usuario(self.user_id)
        
        # Busca compartilhadas comigo
        assinaturas_compartilhadas = self.dao.obter_assinaturas_compartilhadas_comigo(self.user_id)
        
        total = 0.0
        
        # Calcula total próprias
        for assinatura in assinaturas_proprias:
            if assinatura.status == Status.ATIVO:
                # Se compartilhou, paga metade
                if assinatura.usuario_compartilhado and assinatura.usuario_compartilhado.strip():
                    total += assinatura.valor / 2
                else:
                    total += assinatura.valor
        
        # Calcula total compartilhadas
        for assinatura in assinaturas_compartilhadas:
            if assinatura.status == Status.ATIVO:
                # Sempre paga metade
                total += assinatura.valor / 2
        
        return total
    
    def calcular_diferenca_meta(self):
        """
        Calcula a diferença entre a meta de assinaturas e o total de assinaturas ativas.
        
        Returns:
            float: Meta - Total de assinaturas ativas (positivo = dentro da meta, negativo = acima da meta)
        """
        # Obtém meta do usuário
        if not self.usuario_controller:
            return 0.0
        
        meta = float(self.usuario_controller.get_limite_assinaturas())
        total_ativo = self.calcular_total_assinaturas()
        
        return meta - total_ativo
    
    def obter_dados_formulario(self):
        """Extrai e normaliza os dados do formulário da view."""
        return {
            'nome': self.view.entry_nome.get().strip(),
            'valor': self.view.entry_valor.get().strip().replace(',', '.'),
            'data_vencimento': self.view.entry_data.get().strip(),
            'periodicidade': self.view.combo_periodicidade.get(),
            'categoria': self.view.combo_categoria.get(),
            'forma_pagamento': self.view.combo_pagamento.get(),
            'usuario_compartilhado': self.view.entry_usuario_compartilhado.get().strip(),
            'login': self.view.entry_login.get().strip(),
            'senha': self.view.entry_senha.get().strip()
        }
    
    def _validar_data(self, date_str):
        """
        Valida se a data está no formato correto e se é >= data atual.
        
        Returns:
            dict: {'valid': bool, 'message': str, 'date': datetime.date or None}
        """
        try:
            # Tenta converter para datetime
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            # Falha na conversão
            return {
                'valid': False,
                'message': 'Data inválida! Use o formato DD/MM/AAAA.',
                'date': None
            }
        
        # Verifica se é futura
        today = datetime.now().date()
        
        if date_obj < today:
            return {
                'valid': False,
                'message': 'A data de vencimento deve ser hoje ou uma data futura!',
                'date': None
            }
        
        return {
            'valid': True,
            'message': 'Data válida',
            'date': date_obj
        }
    
    def _verificar_nome_duplicado(self, nome, assinatura_id=None):
        """
        Verifica se já existe uma assinatura com o mesmo nome para o usuário.
        
        Args:
            nome: Nome da assinatura
            assinatura_id: ID da assinatura (None para nova, int para edição)
        
        Returns:
            dict: {'duplicate': bool, 'message': str}
        """
        if not self.user_id:
            return {'duplicate': False, 'message': ''}
        
        assinaturas = self.dao.obter_assinaturas_por_usuario(self.user_id)
        
        for assinatura in assinaturas:
            # Ignora própria assinatura ao editar
            if assinatura_id and assinatura.id == assinatura_id:
                continue
            
            if assinatura.nome.lower() == nome.lower():
                return {
                    'duplicate': True,
                    'message': 'Já existe uma assinatura com esse nome! Tente outro.'
                }
        
        return {'duplicate': False, 'message': ''}
    
    def _validar_campos_obrigatorios(self, data):
        """
        Valida se todos os campos obrigatórios foram preenchidos.
        
        Args:
            data: Dict com os dados do formulário
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': None}
        """
        required_fields = {
            'nome': 'Nome',
            'valor': 'Valor',
            'data_vencimento': 'Data de Vencimento',
            'periodicidade': 'Periodicidade',
            'categoria': 'Categoria',
            'forma_pagamento': 'Forma de Pagamento'
        }
        
        missing = []
        for field, label in required_fields.items():
            if not data.get(field):
                missing.append(label)
        
        if missing:
            return {
                'success': False,
                'message': 'Preencha todos os campos obrigatórios!',
                'error_code': 'REQUIRED_FIELDS',
                'data': None
            }
        
        return {'success': True, 'error_code': 'OK', 'data': data}
    
    def _validar_formato_valor(self, data):
        """
        Valida se o valor tem formato numérico válido e é positivo.
        Converte o valor para float se válido.
        
        Args:
            data: Dict com os dados do formulário (será modificado)
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': dict ou None}
        """
        try:
            valor = float(data['valor'])
            
            if valor < 0:
                raise ValueError("Negativo")
            
            data['valor'] = valor
            return {'success': True, 'error_code': 'OK', 'data': data}
            
        except ValueError:
            return {
                'success': False,
                'message': 'Valor inválido! Use apenas números positivos (ex: 99.90 ou 99,90).',
                'error_code': 'INVALID_NUMBER',
                'data': None
            }
    
    def _validar_formato_data(self, data):
        """
        Valida se a data tem formato DD/MM/AAAA válido.
        
        Args:
            data: Dict com os dados do formulário
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': None, 'date_obj': date ou None}
        """
        try:
            date_obj = datetime.strptime(data['data_vencimento'], "%d/%m/%Y").date()
            return {
                'success': True,
                'error_code': 'OK',
                'data': data,
                'date_obj': date_obj
            }
        except ValueError:
            return {
                'success': False,
                'message': 'Data inválida! Use o formato DD/MM/AAAA.',
                'error_code': 'INVALID_DATE_FORMAT',
                'data': None,
                'date_obj': None
            }
    
    def _validar_data_nao_futura(self, date_obj):
        """
        Valida se a data é maior ou igual à data atual.
        
        Args:
            date_obj: datetime.date objeto
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': None}
        """
        today = datetime.now().date()
        if date_obj < today:
            return {
                'success': False,
                'message': 'A data de vencimento deve ser hoje ou uma data futura!',
                'error_code': 'INVALID_DATE_PAST',
                'data': None
            }
        
        return {'success': True, 'error_code': 'OK', 'data': None}
    
    def _validar_nome_unico(self, data, assinatura_id=None):
        """
        Valida se o nome da assinatura é único para o usuário.
        
        Args:
            data: Dict com os dados do formulário
            assinatura_id: ID da assinatura (None para nova, int para edição)
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': None}
        """
        duplicate_check = self._verificar_nome_duplicado(data['nome'], assinatura_id)
        if duplicate_check['duplicate']:
            return {
                'success': False,
                'message': duplicate_check['message'],
                'error_code': 'DUPLICATE_NAME',
                'data': None
            }
        
        return {'success': True, 'error_code': 'OK', 'data': data}
    
    def _validar_compartilhamento_nao_proprio(self, data):
        """
        Valida se o usuário não está tentando compartilhar consigo mesmo.
        
        Args:
            data: Dict com os dados do formulário
            
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': None}
        """
        usuario_compartilhado = data.get('usuario_compartilhado', '').strip().lower()
        
        # Sem email de compartilhamento
        if not usuario_compartilhado:
            return {'success': True, 'error_code': 'OK', 'data': data}
        
        # Busca user_id do email
        from dao import UserDAO
        user_dao = UserDAO()
        user_id_compartilhado = user_dao.get_user_id_by_email(usuario_compartilhado)
        
        # Verifica compartilhamento consigo mesmo
        if user_id_compartilhado == self.user_id:
            return {
                'success': False,
                'message': 'Você não pode compartilhar uma assinatura com você mesmo!',
                'error_code': 'SELF_SHARE',
                'data': None
            }
        
        return {'success': True, 'error_code': 'OK', 'data': data}
    
    def validar_dados_formulario(self, data, assinatura_id=None):
        """
        Valida os dados do formulário na ordem especificada:
        1. Campos obrigatórios
        2. Valor inválido (formato)
        3. Data inválida (formato)
        4. Data < data_atual
        5. Nome duplicado
        6. Compartilhamento consigo mesmo
        
        Args:
            data: Dict com os dados do formulário
            assinatura_id: ID da assinatura (None para nova, int para edição)
        
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': dict}
        """
        # 1. VALIDAR CAMPOS OBRIGATÓRIOS
        validacao = self._validar_campos_obrigatorios(data)
        if not validacao['success']:
            return validacao
        
        # 2. VALIDAR FORMATO DO VALOR
        validacao = self._validar_formato_valor(data)
        if not validacao['success']:
            return validacao
        
        # 3. VALIDAR FORMATO DA DATA
        validacao = self._validar_formato_data(data)
        if not validacao['success']:
            return validacao
        
        date_obj = validacao['date_obj']

        # 4. VALIDAR SE DATA >= DATA ATUAL
        validacao = self._validar_data_nao_futura(date_obj)
        if not validacao['success']:
            return validacao
        
        # 5. VALIDAR SE O NOME É ÚNICO
        validacao = self._validar_nome_unico(data, assinatura_id)
        if not validacao['success']:
            return validacao
        
        # 6. VALIDAR SE NÃO ESTÁ COMPARTILHANDO CONSIGO MESMO
        validacao = self._validar_compartilhamento_nao_proprio(data)
        if not validacao['success']:
            return validacao
        
        return {
            'success': True,
            'message': 'Dados validados com sucesso!',
            'error_code': 'SUCCESS',
            'data': data
        }
    
    def limpar_formulario(self):
        """Limpa todos os campos do formulário."""
        self.view.entry_nome.delete(0, 'end')
        self.view.entry_valor.delete(0, 'end')
        self.view.entry_data.delete(0, 'end')
        self.view.entry_usuario_compartilhado.delete(0, 'end')
        self.view.entry_login.delete(0, 'end')
        self.view.entry_senha.delete(0, 'end')
    
    def _criar_objeto_assinatura(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0,
        status: Status = None,
        assinatura_id: int = None
    ):
        """
        Cria um objeto Assinatura com os dados fornecidos.
        Centraliza a criação para evitar duplicação entre adicionar() e editar().
        
        Returns:
            Assinatura: Objeto assinatura criado
        """
        return Assinatura(
            assinatura_id=assinatura_id,
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            categoria=categoria,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=favorito,
            status=status if status else Status.ATIVO
        )
    
    def _finalizar_operacao(
        self, 
        assinatura_id: int, 
        usuario_compartilhado: str, 
        mensagem_sucesso: str
    ):
        """
        Finaliza operações de adicionar/editar:
        1. Processa compartilhamento se necessário
        2. Recarrega assinaturas
        3. Retorna resultado
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        # Processa compartilhamento se foi informado email
        if usuario_compartilhado and usuario_compartilhado.strip():
            resultado = self.processar_compartilhamento(assinatura_id, usuario_compartilhado)
            if not resultado['success']:
                # Se falhar compartilhamento, retorna erro mas operação já foi feita
                self._carregar_assinaturas()
                resultado_final = {'success': False, 'message': resultado['message']}
                return resultado_final
        
        self._carregar_assinaturas()
        resultado_final = {'success': True, 'message': mensagem_sucesso}
        return resultado_final
    
    def adicionar(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = ""
    ):
        """Adiciona uma nova assinatura."""
        assinatura = self._criar_objeto_assinatura(
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            categoria=categoria,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=0,
            status=Status.ATIVO
        )
        assinatura_id = self.dao.adicionar_assinatura(assinatura)
        
        resultado = self._finalizar_operacao(
            assinatura_id, 
            usuario_compartilhado, 
            'Assinatura adicionada com sucesso!'
        )
        return resultado
    
    def _pode_remover_assinatura(self, assinatura_id: int):
        """
        Verifica se uma assinatura pode ser removida.
        Regras:
        1. Apenas o proprietário pode remover
        2. Apenas assinaturas com status ENCERRADO podem ser removidas
        
        Returns:
            dict: {'can_remove': bool, 'message': str}
        """
        if not self.user_id:
            return {'can_remove': False, 'message': 'Usuário não identificado!'}
        
        # Busca a assinatura APENAS entre as do próprio usuário (não nas compartilhadas)
        assinaturas_proprias = self.dao.obter_assinaturas_por_usuario(self.user_id)
        assinatura = next((a for a in assinaturas_proprias if a.id == assinatura_id), None)
        
        if not assinatura:
            # Assinatura não encontrada entre as do usuário = não é proprietário ou não existe
            return {
                'can_remove': False, 
                'message': 'Você não pode remover esta assinatura!\n\nApenas o proprietário pode remover assinaturas.'
            }
        
        # Verifica se o status é ENCERRADO
        if assinatura.status == Status.ENCERRADO:
            return {'can_remove': True, 'message': ''}
        
        # Não pode remover se ainda está ATIVO
        return {
            'can_remove': False,
            'message': 'Não é possível remover esta assinatura!\n\nPara remover, primeiro altere o status para ENCERRADO.'
        }
    
    def remover(self, assinatura_id: int):
        """Remove uma assinatura (apenas se status for ENCERRADO)."""
        # Valida se pode remover
        validacao = self._pode_remover_assinatura(assinatura_id)
        
        if not validacao['can_remove']:
            return {'success': False, 'message': validacao['message']}
        
        # Remove a assinatura
        self.dao.deletar_assinatura(assinatura_id)
        self._carregar_assinaturas()
        return {'success': True, 'message': 'Assinatura removida com sucesso!'}
    
    def alternar_favorito(self, assinatura_id: int):
        """Alterna o status de favorito de uma assinatura."""
        if self.user_id:
            self.dao.alternar_favorito(assinatura_id)
            self._carregar_assinaturas()
    
    def _ultimo_dia_mes(self, ano: int, mes: int) -> int:
        """Retorna o último dia do mês."""
        import calendar
        return calendar.monthrange(ano, mes)[1]
    
    def _calcular_proxima_data(self, data_atual, periodicidade: str):
        """
        Calcula a próxima data de vencimento baseado na periodicidade.
        Extrai lógica de cálculo para evitar duplicação.
        
        Args:
            data_atual: datetime.date - Data atual a ser incrementada
            periodicidade: str - Periodicidade da assinatura
            
        Returns:
            datetime.date: Próxima data de vencimento
        """
        from mvc.models.periodicidade_enum import Periodicidade
        
        if periodicidade == Periodicidade.MENSAL.value:
            # Adiciona 1 mês
            mes = data_atual.month + 1
            ano = data_atual.year
            if mes > 12:
                mes = 1
                ano += 1
            dia = min(data_atual.day, self._ultimo_dia_mes(ano, mes))
            return data_atual.replace(year=ano, month=mes, day=dia)
            
        elif periodicidade == Periodicidade.TRIMESTRAL.value:
            # Adiciona 3 meses
            mes = data_atual.month + 3
            ano = data_atual.year
            while mes > 12:
                mes -= 12
                ano += 1
            dia = min(data_atual.day, self._ultimo_dia_mes(ano, mes))
            return data_atual.replace(year=ano, month=mes, day=dia)
            
        elif periodicidade == Periodicidade.SEMESTRAL.value:
            # Adiciona 6 meses
            mes = data_atual.month + 6
            ano = data_atual.year
            if mes > 12:
                mes -= 12
                ano += 1
            dia = min(data_atual.day, self._ultimo_dia_mes(ano, mes))
            return data_atual.replace(year=ano, month=mes, day=dia)
            
        elif periodicidade == Periodicidade.ANUAL.value:
            # Adiciona 1 ano
            ano = data_atual.year + 1
            mes = data_atual.month
            dia = min(data_atual.day, self._ultimo_dia_mes(ano, mes))
            return data_atual.replace(year=ano, day=dia)
        
        # Periodicidade desconhecida, retorna a mesma data
        return data_atual
    
    def renovar_vencimento_se_necessario(self, assinatura_id: int):
        """
        Verifica se o vencimento passou e renova automaticamente baseado na periodicidade.
        Apenas para assinaturas ATIVAS.
        
        Args:
            assinatura_id: ID da assinatura a verificar
            
        Returns:
            bool: True se renovou, False caso contrário
        """
        if not self.user_id:
            return False
        
        # Busca a assinatura
        assinaturas = self.dao.obter_assinaturas_por_usuario(self.user_id)
        assinatura = next((a for a in assinaturas if a.id == assinatura_id), None)
        
        if not assinatura or assinatura.status != Status.ATIVO:
            return False
        
        try:
            # Converte a data de vencimento
            data_vencimento = datetime.strptime(assinatura.data_vencimento, "%d/%m/%Y").date()
            hoje = datetime.now().date()
            
            # Se a data de vencimento já passou
            if data_vencimento < hoje:
                # Continua renovando até que a data seja >= hoje
                nova_data = data_vencimento
                while nova_data < hoje:
                    nova_data = self._calcular_proxima_data(nova_data, assinatura.periodicidade)
                    
                    # Segurança contra loop infinito (periodicidade desconhecida)
                    if nova_data == data_vencimento:
                        return False
                
                # Atualiza a assinatura com a nova data
                self.editar(
                    assinatura_id=assinatura.id,
                    nome=assinatura.nome,
                    data_vencimento=nova_data.strftime("%d/%m/%Y"),
                    valor=assinatura.valor,
                    periodicidade=assinatura.periodicidade,
                    categoria=assinatura.categoria,
                    forma_pagamento=assinatura.forma_pagamento,
                    usuario_compartilhado=assinatura.usuario_compartilhado,
                    login=assinatura.login,
                    senha=assinatura.senha,
                    favorito=assinatura.favorito,
                    status=assinatura.status
                )
                return True
            
            return False
            
        except ValueError:
            # Se a data for inválida, não renova
            return False
    
    def renovar_todas_assinaturas_ativas(self):
        """
        Renova todas as assinaturas ativas que estão vencidas.
        Chamado ao carregar a lista de assinaturas.
        """
        if not self.user_id:
            return
        
        assinaturas = self.dao.obter_assinaturas_por_usuario(self.user_id)
        
        for assinatura in assinaturas:
            if assinatura.status == Status.ATIVO:
                self.renovar_vencimento_se_necessario(assinatura.id)
    
    def editar(
        self,
        assinatura_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0,
        status: Status = None
    ):
        """Edita uma assinatura existente."""
        assinatura = self._criar_objeto_assinatura(
            assinatura_id=assinatura_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            categoria=categoria,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=favorito,
            status=status
        )
        self.dao.atualizar_assinatura(assinatura)
        
        return self._finalizar_operacao(
            assinatura_id, 
            usuario_compartilhado, 
            'Assinatura atualizada com sucesso!'
        )
    
    def obter_categorias_disponiveis(self):
        """Retorna lista de categorias disponíveis."""
        return [c.value for c in CategoriaAssinatura]
    
    def obter_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return [p.value for p in Periodicidade]
    
    def obter_formas_pagamento(self):
        """Retorna lista de formas de pagamento cadastradas."""
        return self.pagamentos_controller.obter_nomes_metodos_pagamento()
    
    def _criar_compartilhamento_assinatura(self, assinatura_id: int, user_id_compartilhado: int, email_compartilhado: str):
        """
        Cria o compartilhamento da assinatura no banco de dados.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        self.dao.compartilhar_assinatura(assinatura_id, self.user_id, user_id_compartilhado)
        return {
            'success': True,
            'message': f'Assinatura compartilhada com sucesso com {email_compartilhado}!'
        }
    
    def processar_compartilhamento(self, assinatura_id: int, email_compartilhado: str):
        """
        Processa o compartilhamento de uma assinatura com outro usuário.
        
        Args:
            assinatura_id: ID da assinatura a compartilhar
            email_compartilhado: Email do usuário que receberá acesso readonly
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        from dao import UserDAO
        user_dao = UserDAO()
        
        # Normaliza email e busca user_id
        email_normalizado = email_compartilhado.strip().lower()
        user_id_compartilhado = user_dao.get_user_id_by_email(email_normalizado)
        
        # Cria o compartilhamento
        resultado = self._criar_compartilhamento_assinatura(
            assinatura_id, 
            user_id_compartilhado, 
            email_normalizado
        )
        return resultado
