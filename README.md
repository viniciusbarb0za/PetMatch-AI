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

- **Python 3.10 a 3.12** (recomendado: 3.12)
- **pip** (gerenciador de pacotes Python)

### Passo 1: Clone o repositório

```bash
git clone https://github.com/seu-usuario/petmatch-ai.git
cd petmatch-ai
```

### Passo 2: Configure o ambiente

**Windows:**
```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

⚠️ **Atenção:** A instalação pode demorar alguns minutos devido ao tamanho do PyTorch (~2 GB).

### Passo 4: Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Por padrão, o projeto roda em **modo demonstração local** (sem Supabase). Se quiser usar o Supabase, preencha as credenciais no `.env`:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

### Passo 5: Execute o projeto

**Windows:**
```bash
py -3.12 -m streamlit run app.py
```

**Ou clique duas vezes em `run.bat`**

**Linux/Mac:**
```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em: **http://localhost:8501**

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
| **Transformers (Hugging Face)** | Modelo CLIP pré-treinado |
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
├── data/
│   ├── images/            # Fotos cadastradas (não versionadas)
│   └── demo_db.json       # Banco local em modo demo
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

---

## ⚙️ Configuração Avançada

### Usar o Supabase (Produção)

1. Crie uma conta em [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Execute o SQL abaixo no **SQL Editor** do Supabase:

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
5. Cole as credenciais no arquivo `.env`

---

## 🧪 Testes

Execute os testes (se disponíveis):

```bash
pytest
```

---

## ⚠️ Limitações e Avisos

- ⚠️ **O modelo CLIP identifica similaridade visual, não identidade individual**
- ⚠️ **Os resultados são sugestões que devem ser confirmadas pessoalmente**
- ⚠️ **Não inclua dados pessoais** (telefone, endereço completo) nas descrições
- ⚠️ **No modo local**, as imagens ficam armazenadas apenas na sua máquina
- ⚠️ **Primeira busca**: o modelo CLIP (~340 MB) é baixado automaticamente

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

## 🆘 Problemas Comuns

### "No module named 'src'"
Execute o projeto a partir da raiz do repositório, não de dentro de pastas.

### "torch not found" ou erro na instalação
Use Python 3.10 a 3.12. O Python 3.15+ ainda não tem suporte completo.

### "Microsoft Visual C++ required"
No Windows, use versões pré-compiladas das bibliotecas:
```bash
pip install --only-binary :all: -r requirements.txt
```

### Aplicação não abre
Verifique se o Streamlit foi instalado corretamente:
```bash
streamlit --version
```

---

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/seu-usuario/petmatch-ai/issues) no GitHub.

---

**Feito com ❤️ e 🐶🐱 por estudantes apaixonados por tecnologia e animais**
