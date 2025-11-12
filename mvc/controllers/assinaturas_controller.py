from dao import AssinaturasDAO
from mvc.models.assinaturas_model import Assinatura
from mvc.models.periodicidade_enum import Periodicidade
from mvc.models.assinatura_categoria_enum import CategoriaAssinatura
from mvc.models.assinatura_status_enum import StatusAssinatura
from datetime import datetime, timedelta


class AssinaturasController:
    """Controller para Assinaturas."""
    
    def __init__(self, view, user_id=None):
        self.view = view
        self.user_id = user_id
        self.dao = AssinaturasDAO()
        self.view.controller = self
        
        from mvc.controllers.pagamentos_controller import PagamentosController
        self.pagamentos_controller = PagamentosController()
        
        self.view.set_combo_values(
            [p.value for p in Periodicidade],
            [c.value for c in CategoriaAssinatura],
            self.pagamentos_controller.obter_nomes_metodos_pagamento()
        )
        
        self._carregar_assinaturas()
    
    def _carregar_assinaturas(self):
        """Carrega e exibe as assinaturas do usuário."""
        if self.user_id:
            assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
            self.view.atualizar_lista(assinaturas)
    
    def get_form_data(self):
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
    
    def _validate_date(self, date_str):
        """
        Valida se a data está no formato correto e se é >= data atual.
        
        Returns:
            dict: {'valid': bool, 'message': str, 'date': datetime.date or None}
        """
        try:
            # Tenta converter DD/MM/AAAA para datetime
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            # Se falhar na conversão, formato inválido
            return {
                'valid': False,
                'message': 'Data inválida! Use o formato DD/MM/AAAA.',
                'date': None
            }
        
        # Se chegou aqui, formato é válido, agora verifica se é futura
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
    
    def _check_duplicate_name(self, nome, assinatura_id=None):
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
        
        assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
        
        for assinatura in assinaturas:
            # Ignora a própria assinatura ao editar
            if assinatura_id and assinatura.id == assinatura_id:
                continue
            
            if assinatura.nome.lower() == nome.lower():
                return {
                    'duplicate': True,
                    'message': 'Já existe uma assinatura com esse nome!'
                }
        
        return {'duplicate': False, 'message': ''}
    
    def validate_form_data(self, data, assinatura_id=None):
        """
        Valida os dados do formulário na ordem especificada:
        1. Campos obrigatórios
        2. Valores numéricos
        3. Data válida e >= data atual
        4. Nome não duplicado
        
        Args:
            data: Dict com os dados do formulário
            assinatura_id: ID da assinatura (None para nova, int para edição)
        
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': dict}
        """
        # 1. VALIDAR CAMPOS OBRIGATÓRIOS
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
        
        # 2. VALIDAR SE VALORES NUMÉRICOS SÃO DE FATO NUMÉRICOS
        try:
            valor = float(data['valor'])
            
            if valor < 0:  # Mudado para permitir 0
                return {
                    'success': False,
                    'message': 'O valor não pode ser negativo!',
                    'error_code': 'INVALID_VALUE',
                    'data': None
                }
            
            data['valor'] = valor
        except ValueError:
            return {
                'success': False,
                'message': 'Valor inválido! Use apenas números (ex: 99.90 ou 99,90).',
                'error_code': 'INVALID_NUMBER',
                'data': None
            }
        
        # 3. VALIDAR SE A DATA É MAIOR OU IGUAL À DATA ATUAL
        date_validation = self._validate_date(data['data_vencimento'])
        if not date_validation['valid']:
            return {
                'success': False,
                'message': date_validation['message'],
                'error_code': 'INVALID_DATE',
                'data': None
            }
        
        # 4. VALIDAR SE O NOME NUNCA FOI CADASTRADO
        duplicate_check = self._check_duplicate_name(data['nome'], assinatura_id)
        if duplicate_check['duplicate']:
            return {
                'success': False,
                'message': duplicate_check['message'],
                'error_code': 'DUPLICATE_NAME',
                'data': None
            }
        
        return {
            'success': True,
            'message': 'Dados validados com sucesso!',
            'error_code': 'SUCCESS',
            'data': data
        }
    
    def clear_form(self):
        """Limpa todos os campos do formulário."""
        self.view.entry_nome.delete(0, 'end')
        self.view.entry_valor.delete(0, 'end')
        self.view.entry_data.delete(0, 'end')
        self.view.entry_usuario_compartilhado.delete(0, 'end')
        self.view.entry_login.delete(0, 'end')
        self.view.entry_senha.delete(0, 'end')
    
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
        assinatura = Assinatura(
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
            user_id=self.user_id,
            status=StatusAssinatura.ATIVO
        )
        self.dao.add_assinatura(assinatura)
        self._carregar_assinaturas()
        return True
    
    def _pode_remover_assinatura(self, assinatura_id: int):
        """
        Verifica se uma assinatura pode ser removida.
        Regras:
        - Assinatura vencida (data < hoje): pode remover sempre
        - Vencimento a mais de 7 dias: pode remover sempre
        - Vencimento a 7 dias ou menos (mas não vencida): só pode remover se valor = 0
        
        Returns:
            dict: {'can_remove': bool, 'message': str}
        """
        if not self.user_id:
            return {'can_remove': False, 'message': 'Usuário não identificado!'}
        
        # Busca a assinatura
        assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
        assinatura = next((a for a in assinaturas if a.id == assinatura_id), None)
        
        if not assinatura:
            return {'can_remove': False, 'message': 'Assinatura não encontrada!'}
        
        try:
            # Converte a data de vencimento
            data_vencimento = datetime.strptime(assinatura.data_vencimento, "%d/%m/%Y").date()
            hoje = datetime.now().date()
            dias_ate_vencimento = (data_vencimento - hoje).days
            
            # Se a assinatura já venceu (data < hoje), pode remover sempre
            if dias_ate_vencimento < 0:
                return {'can_remove': True, 'message': ''}
            
            # Se vencimento está a mais de 7 dias, pode remover
            if dias_ate_vencimento > 7:
                return {'can_remove': True, 'message': ''}
            
            # Se vencimento está a 7 dias ou menos (mas ainda não venceu), só pode remover se valor for zero
            if assinatura.valor == 0 or assinatura.valor == 0.0:
                return {'can_remove': True, 'message': ''}
            
            # Não pode remover
            return {
                'can_remove': False,
                'message': 'Não é possível remover esta assinatura pois faltam 7 dias ou menos para o vencimento!\n\nPara remover, altere o valor para R$ 0,00 antes.'
            }
            
        except ValueError:
            # Se a data for inválida, permite remoção
            return {'can_remove': True, 'message': ''}
    
    def remover(self, assinatura_id: int):
        """Remove uma assinatura (com validação de regras)."""
        # Valida se pode remover
        validacao = self._pode_remover_assinatura(assinatura_id)
        
        if not validacao['can_remove']:
            return {'success': False, 'message': validacao['message']}
        
        # Remove a assinatura
        self.dao.delete_assinatura(assinatura_id)
        self._carregar_assinaturas()
        return {'success': True, 'message': 'Assinatura removida com sucesso!'}
    
    def toggle_favorito(self, assinatura_id: int):
        """Alterna o status de favorito de uma assinatura."""
        if self.user_id:
            self.dao.toggle_favorito(assinatura_id)
            self._carregar_assinaturas()
    
    def verificar_e_atualizar_status(self, assinatura_id: int):
        """
        Verifica se a assinatura venceu e atualiza o status automaticamente.
        
        Args:
            assinatura_id: ID da assinatura a verificar
            
        Returns:
            Assinatura atualizada ou None se não encontrada
        """
        if not self.user_id:
            return None
        
        # Busca a assinatura
        assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
        assinatura = next((a for a in assinaturas if a.id == assinatura_id), None)
        
        if not assinatura:
            return None
        
        try:
            # Converte a data de vencimento
            data_vencimento = datetime.strptime(assinatura.data_vencimento, "%d/%m/%Y").date()
            hoje = datetime.now().date()
            
            # Se a data de vencimento é menor que hoje E status ainda é ATIVO
            if data_vencimento < hoje and assinatura.status == StatusAssinatura.ATIVO:
                # Atualiza para ENCERRADO
                self.editar(
                    assinatura_id=assinatura.id,
                    nome=assinatura.nome,
                    data_vencimento=assinatura.data_vencimento,
                    valor=assinatura.valor,
                    periodicidade=assinatura.periodicidade,
                    categoria=assinatura.tag,
                    forma_pagamento=assinatura.forma_pagamento,
                    usuario_compartilhado=assinatura.usuario_compartilhado,
                    login=assinatura.login,
                    senha=assinatura.senha,
                    favorito=assinatura.favorito,
                    status=StatusAssinatura.ENCERRADO
                )
                
                # Recarrega a assinatura atualizada
                assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
                assinatura = next((a for a in assinaturas if a.id == assinatura_id), None)
            
            return assinatura
            
        except ValueError:
            # Se a data for inválida, retorna a assinatura sem alterações
            return assinatura
    
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
        status: StatusAssinatura = None
    ):
        """Edita uma assinatura existente."""
        if not self.user_id:
            return False
        
        assinatura = Assinatura(
            assinatura_id=assinatura_id,
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
            favorito=favorito,
            status=status if status else StatusAssinatura.ATIVO
        )
        self.dao.update_assinatura(assinatura)
        self._carregar_assinaturas()
        return True
    
    def get_categorias_disponiveis(self):
        """Retorna lista de categorias disponíveis."""
        return [c.value for c in CategoriaAssinatura]
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return [p.value for p in Periodicidade]
    
    def get_formas_pagamento(self):
        """Retorna lista de formas de pagamento cadastradas."""
        return self.pagamentos_controller.obter_nomes_metodos_pagamento()
