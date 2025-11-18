from dao import ContratosDAO
from mvc.models.contratos_model import Contrato
from mvc.models.periodicidade_enum import Periodicidade
from mvc.models.contrato_categoria_enum import CategoriaContrato
from mvc.models.contrato_status_enum import StatusContrato
from datetime import datetime
from tkinter import messagebox


class ContratosController:
    """Controller para Contratos com funcionalidades avançadas."""
    
    def __init__(self, view, user_id=None, usuario_controller=None):
        self.view = view
        self.user_id = user_id
        self.usuario_controller = usuario_controller
        self.dao = ContratosDAO()
        self.view.controller = self
        
        # Popula os comboboxes (periodicidade e tags) via enums
        self.view.set_combo_values(
            [p.value for p in Periodicidade],
            [c.value for c in CategoriaContrato],
        )
        
        self._carregar_contratos()
    
    # ==================== MÉTODOS DE MENSAGENS ====================
    
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
    
    def exibir_erro_validacao(self, validation):
        """
        Exibe a mensagem de erro apropriada baseado no código de validação.
        
        Args:
            validation: Dicionário retornado por validate_form_data
        """
        error_code = validation.get('error_code', '')
        message = validation.get('message', 'Erro desconhecido')
        
        if error_code == 'REQUIRED_FIELDS':
            self.mostrar_aviso("Campos Obrigatórios", message)
        elif error_code in ['INVALID_NUMBER', 'INVALID_VALUE', 'INVALID_DATE']:
            self.mostrar_erro("Valor Inválido", message)
        elif error_code == 'DUPLICATE_NAME':
            self.mostrar_erro("Nome Duplicado", message)
        else:
            self.mostrar_erro("Erro de Validação", message)
    
    # ==================== MÉTODOS DE NEGÓCIO ====================
    
    def _carregar_contratos(self):
        """Carrega e exibe os contratos do usuário."""
        if self.user_id:
            # Primeiro renova todos os contratos ativos vencidos
            self.renovar_todos_contratos_ativos()
            
            # Busca apenas contratos próprios (removido compartilhamento)
            contratos_proprios = self.dao.get_contratos_by_user(self.user_id)
            
            # Converte para objetos Contrato
            contratos_obj = [
                Contrato(
                    contrato_id=r["id"],
                    user_id=r["user_id"],
                    nome=r["nome"],
                    data_vencimento=r["data_vencimento"],
                    valor=r["valor"],
                    periodicidade=r["periodicidade"],
                    tag=r["tag"],
                    usuario_compartilhado=r.get("usuario_compartilhado") or "",
                    favorito=1 if r.get("favorito") else 0,
                    status=StatusContrato(r.get("status", "Ativo"))
                )
                for r in contratos_proprios
            ]
            
            self.view.atualizar_lista(contratos_obj)
    
    def calcular_total_contratos(self, contratos=None):
        """
        Calcula o valor total de contratos ativos do usuário.
        
        Args:
            contratos: Lista de contratos (opcional). Se None, busca do usuário atual.
            
        Returns:
            float: Soma total dos valores
        """
        if not self.user_id:
            return 0.0
        
        # Busca contratos próprios (removido compartilhamento)
        contratos_proprios = self.dao.get_contratos_by_user(self.user_id)
        
        total = 0.0
        
        # Calcula total dos contratos próprios
        for contrato in contratos_proprios:
            if contrato["status"] == "Ativo":
                total += contrato["valor"]
        
        return total
    
    def calcular_diferenca_meta(self):
        """
        Calcula a diferença entre a meta de contratos e o total de contratos ativos.
        
        Returns:
            float: Meta - Total de contratos ativos (positivo = dentro da meta, negativo = acima da meta)
        """
        # Obter a meta de contratos do usuário
        if not self.usuario_controller:
            return 0.0
        
        meta = float(self.usuario_controller.get_limite_contratos())
        total_ativo = self.calcular_total_contratos()
        
        return meta - total_ativo
    
    def get_form_data(self):
        """Extrai e normaliza os dados do formulário da view."""
        return {
            'nome': self.view.entry_nome.get().strip(),
            'valor': self.view.entry_valor.get().strip().replace(',', '.'),
            'data_vencimento': self.view.entry_data.get().strip(),
            'periodicidade': self.view.combo_periodicidade.get(),
            'tag': self.view.combo_categoria.get(),
            'usuario_compartilhado': ''  # Removido compartilhamento
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
    
    def _check_duplicate_name(self, nome, contrato_id=None):
        """
        Verifica se já existe um contrato com o mesmo nome para o usuário.
        
        Args:
            nome: Nome do contrato
            contrato_id: ID do contrato (None para novo, int para edição)
        
        Returns:
            dict: {'duplicate': bool, 'message': str}
        """
        if not self.user_id:
            return {'duplicate': False, 'message': ''}
        
        contratos = self.dao.get_contratos_by_user(self.user_id)
        
        for contrato in contratos:
            # Ignora o próprio contrato ao editar
            if contrato_id and contrato["id"] == contrato_id:
                continue
            
            if contrato["nome"].lower() == nome.lower():
                return {
                    'duplicate': True,
                    'message': 'Já existe um contrato com esse nome! Tente outro.'
                }
        
        return {'duplicate': False, 'message': ''}
    
    def validate_form_data(self, data, contrato_id=None):
        """
        Valida os dados do formulário na ordem especificada:
        1. Campos obrigatórios
        2. Valores numéricos
        3. Data válida e >= data atual
        4. Nome não duplicado
        
        Args:
            data: Dict com os dados do formulário
            contrato_id: ID do contrato (None para novo, int para edição)
        
        Returns:
            dict: {'success': bool, 'message': str, 'error_code': str, 'data': dict}
        """
        # 1. VALIDAR CAMPOS OBRIGATÓRIOS
        required_fields = {
            'nome': 'Nome',
            'valor': 'Valor',
            'data_vencimento': 'Data de Vencimento',
            'periodicidade': 'Periodicidade',
            'tag': 'Categoria'
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
            
            if valor < 0:
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
        duplicate_check = self._check_duplicate_name(data['nome'], contrato_id)
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
        # Removido compartilhamento - não precisa limpar campo inexistente
    
    def _criar_objeto_contrato(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
        status: StatusContrato = None,
        contrato_id: int = None
    ):
        """
        Cria um objeto Contrato com os dados fornecidos.
        Centraliza a criação para evitar duplicação entre adicionar() e editar().
        
        Returns:
            Contrato: Objeto contrato criado
        """
        return Contrato(
            contrato_id=contrato_id,
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            status=status if status else StatusContrato.ATIVO
        )
    
    def _finalizar_operacao(
        self, 
        contrato_id: int, 
        usuario_compartilhado: str, 
        mensagem_sucesso: str
    ):
        """
        Finaliza operações de adicionar/editar:
        1. Recarrega contratos
        2. Retorna resultado
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        # Removido compartilhamento - apenas recarrega contratos
        self._carregar_contratos()
        return {'success': True, 'message': mensagem_sucesso}
    
    def adicionar(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
    ):
        """Adiciona um novo contrato."""
        contrato = self._criar_objeto_contrato(
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=0,
            status=StatusContrato.ATIVO
        )
        contrato_id = self.dao.add_contrato(contrato)
        
        return self._finalizar_operacao(
            contrato_id, 
            usuario_compartilhado, 
            'Contrato adicionado com sucesso!'
        )
    
    def _pode_remover_contrato(self, contrato_id: int):
        """
        Verifica se um contrato pode ser removido.
        Regras:
        1. Apenas o proprietário pode remover
        2. Apenas contratos com status ENCERRADO podem ser removidos
        
        Returns:
            dict: {'can_remove': bool, 'message': str}
        """
        if not self.user_id:
            return {'can_remove': False, 'message': 'Usuário não identificado!'}
        
        # Busca o contrato APENAS entre os do próprio usuário (não nas compartilhados)
        contratos_proprios = self.dao.get_contratos_by_user(self.user_id)
        contrato = next((c for c in contratos_proprios if c["id"] == contrato_id), None)
        
        if not contrato:
            # Contrato não encontrado entre os do usuário = não é proprietário ou não existe
            return {
                'can_remove': False, 
                'message': 'Você não pode remover este contrato!\n\nApenas o proprietário pode remover contratos.'
            }
        
        # Verifica se o status é ENCERRADO
        if contrato.get("status") == "Encerrado":
            return {'can_remove': True, 'message': ''}
        
        # Não pode remover se ainda está ATIVO
        return {
            'can_remove': False,
            'message': 'Não é possível remover este contrato!\n\nPara remover, primeiro altere o status para ENCERRADO.'
        }
    
    def remover(self, contrato_id: int):
        """Remove um contrato (apenas se status for ENCERRADO)."""
        # Valida se pode remover
        validacao = self._pode_remover_contrato(contrato_id)
        
        if not validacao['can_remove']:
            return {'success': False, 'message': validacao['message']}
        
        # Remove o contrato
        self.dao.delete_contrato(contrato_id)
        self._carregar_contratos()
        return {'success': True, 'message': 'Contrato removido com sucesso!'}
    
    def toggle_favorito(self, contrato_id: int):
        """Alterna o status de favorito de um contrato."""
        if self.user_id:
            self.dao.toggle_favorito(contrato_id)
            self._carregar_contratos()
    
    def renovar_vencimento_se_necessario(self, contrato_id: int):
        """
        Verifica se o vencimento passou e renova automaticamente baseado na periodicidade.
        Apenas para contratos ATIVOS.
        
        Args:
            contrato_id: ID do contrato a verificar
            
        Returns:
            bool: True se renovou, False caso contrário
        """
        if not self.user_id:
            return False
        
        # Busca o contrato
        contratos = self.dao.get_contratos_by_user(self.user_id)
        contrato = next((c for c in contratos if c["id"] == contrato_id), None)
        
        if not contrato or contrato.get("status") != "Ativo":
            return False
        
        try:
            # Converte a data de vencimento
            data_vencimento = datetime.strptime(contrato["data_vencimento"], "%d/%m/%Y").date()
            hoje = datetime.now().date()
            
            # Se a data de vencimento já passou
            if data_vencimento < hoje:
                # Continua renovando até que a data seja >= hoje
                nova_data = data_vencimento
                while nova_data < hoje:
                    nova_data = self._calcular_proxima_data(nova_data, contrato["periodicidade"])
                    
                    # Segurança contra loop infinito (periodicidade desconhecida)
                    if nova_data == data_vencimento:
                        return False
                
                # Atualiza o contrato com a nova data
                self.editar(
                    contrato_id=contrato["id"],
                    nome=contrato["nome"],
                    data_vencimento=nova_data.strftime("%d/%m/%Y"),
                    valor=contrato["valor"],
                    periodicidade=contrato["periodicidade"],
                    tag=contrato["tag"],
                    usuario_compartilhado=contrato.get("usuario_compartilhado") or "",
                    favorito=1 if contrato.get("favorito") else 0,
                    status=StatusContrato(contrato.get("status", "Ativo"))
                )
                return True
            
            return False
            
        except ValueError:
            # Se a data for inválida, não renova
            return False
    
    def _ultimo_dia_mes(self, ano: int, mes: int) -> int:
        """Retorna o último dia do mês."""
        import calendar
        return calendar.monthrange(ano, mes)[1]
    
    def _calcular_proxima_data(self, data_atual, periodicidade: str):
        """
        Calcula a próxima data de vencimento baseado na periodicidade.
        
        Args:
            data_atual: datetime.date - Data atual a ser incrementada
            periodicidade: str - Periodicidade do contrato
            
        Returns:
            datetime.date: Próxima data de vencimento
        """
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
    
    def renovar_todos_contratos_ativos(self):
        """
        Renova todos os contratos ativos que estão vencidos.
        Chamado ao carregar a lista de contratos.
        """
        if not self.user_id:
            return
        
        contratos = self.dao.get_contratos_by_user(self.user_id)
        
        for contrato in contratos:
            if contrato.get("status") == "Ativo":
                self.renovar_vencimento_se_necessario(contrato["id"])
    
    def editar(
        self,
        contrato_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
        status: StatusContrato = None
    ):
        """Edita um contrato existente."""
        if not self.user_id:
            return {'success': False, 'message': 'Usuário não identificado!'}
        
        contrato = self._criar_objeto_contrato(
            contrato_id=contrato_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            status=status
        )
        self.dao.update_contrato(contrato)
        
        return self._finalizar_operacao(
            contrato_id, 
            usuario_compartilhado, 
            'Contrato atualizado com sucesso!'
        )
    
    def get_tags_disponiveis(self):
        """Retorna lista de tags disponíveis."""
        return [c.value for c in CategoriaContrato]
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return [p.value for p in Periodicidade]
    
    def processar_compartilhamento(self, contrato_id: int, email_compartilhado: str):
        """
        Processa o compartilhamento de um contrato com outro usuário.
        
        Args:
            contrato_id: ID do contrato a compartilhar
            email_compartilhado: Email do usuário que receberá acesso readonly
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        if not email_compartilhado or not email_compartilhado.strip():
            # Campo vazio = sem compartilhamento
            return {'success': True, 'message': ''}
        
        email_compartilhado = email_compartilhado.strip().lower()
        
        # Busca o ID do usuário pelo email
        from dao import UserDAO
        user_dao = UserDAO()
        user_id_compartilhado = user_dao.get_user_id_by_email(email_compartilhado)
        
        if not user_id_compartilhado:
            return {
                'success': False,
                'message': f'Usuário com email "{email_compartilhado}" não encontrado no sistema!'
            }
        
        if user_id_compartilhado == self.user_id:
            return {
                'success': False,
                'message': 'Você não pode compartilhar um contrato com você mesmo!'
            }
        
        # Cria o compartilhamento
        sucesso = self.dao.compartilhar_contrato(
            contrato_id=contrato_id,
            user_id_proprietario=self.user_id,
            user_id_compartilhado=user_id_compartilhado
        )
        
        if not sucesso:
            return {
                'success': False,
                'message': 'Este contrato já está compartilhado com este usuário!'
            }
        
        return {
            'success': True,
            'message': f'Contrato compartilhado com sucesso com {email_compartilhado}!'
        }