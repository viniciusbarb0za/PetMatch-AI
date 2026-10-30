# 🐾 PetMatch AI

**Aplicação web para reencontrar animais perdidos usando Inteligência Artificial**

PetMatch AI ajuda tutores e ONGs a encontrar animais perdidos comparando fotos através de busca visual com o modelo **CLIP** (Contrastive Language-Image Pre-training).

> 🏆 **Projeto desenvolvido para o Hackathon Estácio em parceria com a AWS**

---

## 📋 Funcionalidades

- ✅ **Cadastro de animais** perdidos ou encontrados com foto
- 🔍 **Busca visual por IA** usando similaridade de imagens
- 📊 **Ranking de correspondências** do mais ao menos semelhante
- 🗺️ **Localização aproximada** com integração ao OpenStreetMap
- 💾 **Modo local** para demonstração (sem necessidade de Supabase)
- 🔒 **Proteção de dados** sem armazenar informações pessoais

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- **Python 3.10 a 3.12** (recomendado: 3.12). Não use Python 3.13 ou superior: o PyTorch ainda pode não ter suporte.
- **pip** (gerenciador de pacotes Python)
- **Conexão com a internet** na instalação e na primeira busca (o modelo CLIP é baixado, ~600 MB)

### Passo 1: Baixe o projeto completo

```bash
git clone https://github.com/seu-usuario/petmatch-ai.git
cd petmatch-ai
```

Se baixar o ZIP do GitHub, extraia e abra o terminal **dentro da pasta que contém o `app.py`**.

Confira se a pasta `src/` existe ao lado do `app.py` (com `config.py`, `database.py`, `image_service.py` e `matching.py`). Sem ela o app não inicia (`No module named 'src'`).

### Passo 2: Crie o ambiente virtual

**Windows (PowerShell):**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Se o PowerShell bloquear a ativação, rode antes:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Quando o ambiente estiver ativo, o prompt começa com `(.venv)`.

> ⚠️ **Todo terminal novo precisa reativar o ambiente** (`.venv\Scripts\activate`) ou usar o Python do `.venv` diretamente, como mostrado no Passo 5.

### Passo 3: Instale as dependências

```bash
python -m pip install -r requirements.txt
```

⚠️ A instalação pode demorar vários minutos devido ao tamanho do PyTorch (~2 GB).

> **Importante:** o projeto usa `transformers` na versão **4.x** (`>=4.46.3,<5`). A versão 5 muda o retorno do CLIP e causa o erro `'BaseModelOutputWithPooling' object has no attribute 'cpu'`. O `requirements.txt` já deve limitar a versão; confira com:
> ```bash
> python -m pip show transformers
> ```
> Se estiver na 5.x, corrija com:
> ```bash
> python -m pip install "transformers>=4.46.3,<5"
> ```

### Passo 4: Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

**Windows:**
```powershell
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

**Para usar o modo demonstração local (padrão, sem Supabase):** abra o `.env` e deixe `SUPABASE_URL` e `SUPABASE_KEY` **vazios**:

```env
SUPABASE_URL=
SUPABASE_KEY=
```

> ⚠️ Se mantiver os valores de exemplo (`https://seu-projeto.supabase.co`), o app tentará conectar em um Supabase que não existe e dará erro.

Para usar o Supabase, preencha com as credenciais do seu projeto (veja "Configuração Avançada").

### Passo 5: (Opcional) Carregue dados de demonstração

```bash
python scripts/seed_demo.py
```

Cria registros e imagens de exemplo para testar a busca logo de cara.

### Passo 6: Execute o projeto

Com o ambiente ativo:

```bash
python -m streamlit run app.py
```

Ou, sem precisar ativar o ambiente (Windows):

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

Ou dê dois cliques em `run.bat` (Windows).

A aplicação abrirá automaticamente em: **http://localhost:8501**

> 💡 Use sempre `python -m streamlit` (e não `py -3.12 -m streamlit`) com o ambiente ativo. O comando `py` chama o Python do sistema, que não tem as dependências instaladas.

---

## 🎯 Como Usar

### 1. **Cadastrar um animal**
   - Acesse a aba **"Cadastrar"**
   - Envie uma foto do animal
   - Preencha as informações (tipo, espécie, cor, data, localização)
   - Clique em **"Cadastrar"**

### 2. **Buscar por foto**
   - Acesse a aba **"Buscar por foto"**
   - Envie uma foto do animal que deseja encontrar
   - Escolha os filtros (perdido/encontrado, espécie)
   - Clique em **"Buscar semelhantes"**
   - Veja os resultados ordenados por similaridade visual

### 3. **Ver todos os registros**
   - Acesse a aba **"Registros"**
   - Filtre por tipo (perdido/encontrado)

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **Python 3.12** | Linguagem principal |
| **Streamlit** | Interface web |
| **PyTorch** | Framework de deep learning |
| **Transformers (Hugging Face) 4.x** | Modelo CLIP pré-treinado |
| **CLIP** | Busca visual por similaridade |
| **Pillow** | Processamento de imagens |
| **Supabase** | Banco de dados (opcional) |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |

---

## 📁 Estrutura do Projeto

```
petmatch-ai/
├── app.py                  # Interface Streamlit
├── src/
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── database.py        # Repositórios (local e Supabase)
│   ├── image_service.py   # Validação e armazenamento de imagens
│   └── matching.py        # Busca visual com CLIP
├── scripts/
│   ├── seed_demo.py       # Gera dados de demonstração
│   └── check_search.py    # Verifica a busca com o CLIP real
├── sql/
│   └── schema.sql         # Tabela e políticas para o Supabase
├── tests/                 # Testes automatizados (pytest)
├── data/
│   ├── images/            # Fotos cadastradas (não versionadas)
│   └── demo_db.json       # Banco local em modo demo
├── requirements.txt       # Dependências Python
├── run.bat                # Atalho para rodar no Windows
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

---

## ⚙️ Configuração Avançada

### Usar o Supabase (Produção)

1. Crie uma conta em [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Execute o conteúdo de `sql/schema.sql` no **SQL Editor** do Supabase, ou o SQL abaixo:

```sql
CREATE TABLE animal_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_type TEXT NOT NULL CHECK (report_type IN ('perdido', 'encontrado')),
  species TEXT NOT NULL,
  color TEXT NOT NULL,
  description TEXT,
  event_date DATE NOT NULL,
  city TEXT NOT NULL,
  latitude NUMERIC,
  longitude NUMERIC,
  image_path TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar Row Level Security (segurança)
ALTER TABLE animal_reports ENABLE ROW LEVEL SECURITY;

-- Permitir leitura pública
CREATE POLICY "Permitir leitura pública" ON animal_reports
  FOR SELECT USING (true);

-- Permitir inserção pública (ajuste conforme necessário)
CREATE POLICY "Permitir inserção pública" ON animal_reports
  FOR INSERT WITH CHECK (true);
```

4. Copie a **URL do projeto** e a **chave anon/public** em **Project Settings → API**
5. Cole as credenciais no arquivo `.env`:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

---

## 🧪 Testes

Com o ambiente ativo:

```bash
python -m pytest
```

Para verificar a busca com o CLIP real (requer internet na primeira vez):

```bash
python scripts/check_search.py
```

---

## ⚠️ Limitações e Avisos

- ⚠️ **O modelo CLIP identifica similaridade visual, não identidade individual**
- ⚠️ **Os resultados são sugestões que devem ser confirmadas pessoalmente**
- ⚠️ **Não inclua dados pessoais** (telefone, endereço completo) nas descrições
- ⚠️ **No modo local**, as imagens ficam armazenadas apenas na sua máquina
- ⚠️ **Primeira busca**: o modelo CLIP (~600 MB) é baixado automaticamente

---

## 🆘 Problemas Comuns

### `No module named streamlit`
O terminal não está usando o ambiente virtual. Confira se o prompt começa com `(.venv)`. Se não, ative com `.venv\Scripts\activate` ou rode direto com `.venv\Scripts\python.exe -m streamlit run app.py`. Evite `py -3.12 -m streamlit`, que chama o Python do sistema.

### `No module named 'src'`
A pasta `src/` não está ao lado do `app.py`. Confira com `dir` (Windows) ou `ls` (Linux/Mac). Execute o projeto a partir da raiz do repositório, não de dentro de outras pastas. Se a pasta realmente não existir, o download veio incompleto: baixe o projeto de novo.

### `'BaseModelOutputWithPooling' object has no attribute 'cpu'`
Versão incompatível do `transformers` (5.x). Instale a 4.x e reinicie o Streamlit (Ctrl+C e rode de novo):
```bash
python -m pip install "transformers>=4.46.3,<5"
```

### Erro de conexão com o Supabase ao abrir o app
O `.env` está com valores de exemplo. Para o modo demonstração, deixe `SUPABASE_URL` e `SUPABASE_KEY` vazios.

### "torch not found" ou erro na instalação do PyTorch
Use Python 3.10 a 3.12. Se o pip não encontrar a versão pedida no `requirements.txt`, relaxe a exigência (por exemplo, `torch>=2.4.0`).

### "Microsoft Visual C++ required"
No Windows, use versões pré-compiladas das bibliotecas:
```bash
python -m pip install --only-binary :all: -r requirements.txt
```

### Aviso sobre `hf_xet` ao baixar o modelo
É apenas informativo. Para downloads mais rápidos: `python -m pip install hf_xet`.

### A busca falha na primeira vez
O modelo CLIP precisa ser baixado. Verifique a conexão com a internet e tente de novo.

### Aplicação não abre
Verifique se o Streamlit foi instalado corretamente:
```bash
python -m streamlit --version
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de código aberto. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 👥 Equipe

**Grupo 15 - Hackathon Estácio x AWS:**
- Felipe Ramos
- Vinicius Barboza
- Davi Marins

---

## 🎓 Sobre o Hackathon

Este projeto foi desenvolvido durante o **Hackathon da Estácio em parceria com a AWS**, com o objetivo de criar soluções tecnológicas inovadoras que impactem positivamente a sociedade. O PetMatch AI utiliza inteligência artificial para resolver um problema real: ajudar a reunir animais perdidos com seus tutores.

---

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/seu-usuario/petmatch-ai/issues) no GitHub.

---

**Feito com ❤️ e 🐶🐱 por estudantes apaixonados por tecnologia e animais**
