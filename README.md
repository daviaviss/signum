# signum

Gestor de contratos e assinaturas em python desktop

## Dependências

O projeto utiliza as seguintes bibliotecas principais:

- bcrypt: para criptografia de senhas
- tkcalendar: para seleção de datas na interface gráfica

## Como executar o código?

### 1. Configure o ambiente virtual (opcional, mas recomendado)

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/MacOS
python -m venv venv
source venv/bin/activate
```

### 2. Instale as dependências

Você pode instalar todas as dependências usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

Ou instalar individualmente:

```bash
pip install bcrypt==4.2.0
pip install tkcalendar==1.6.1
```

### 3. Execute o programa

```bash
python main.py
```
