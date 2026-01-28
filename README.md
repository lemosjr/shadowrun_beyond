# 🌆 SHADOWRUN BEYOND // Runner Sheet Manager

> **Status:** MVP Funcional (Sana Fest Build)  
> **Versão:** 0.9.3 [BETA]

O **Shadowrun Beyond** é um assistente digital para jogadores de RPG de mesa (focado em Shadowrun 5e/6e). Ele substitui a ficha de papel por um **Deck Digital Interativo**, permitindo rolagens de dados automatizadas, controle de dano em tempo real e gestão de arsenal, tudo com uma interface imersiva Cyberpunk.

---

## ⚡ Funcionalidades Principais

* **🗂️ Seleção de Operativos:** Dashboard visual com cards de todos os personagens cadastrados.
* **🎲 Rolador de Dados Automatizado:**
    * Cálculo automático de Hits (5 ou 6).
    * Detecção de Glitches e Falhas Críticas.
    * Rolagens de Perícias, Atributos Puros e Armas.
* **🔫 Arsenal Linkado:** Ao disparar uma arma, o sistema já puxa a perícia correta e calcula o pool de dados.
* **❤️ Monitores de Vitalidade:** Controle de Dano Físico e Atordoamento (Stun) interativo.
    * *Sync:* O dano é salvo automaticamente no banco de dados via API.
* **📟 Console Terminal:** Log de rolagens estilo "hacker" com histórico de ações, retrátil para não poluir a tela.
* **🖌️ UI/UX Imersiva:** Design responsivo com estética Neon/Dark, efeitos de Glitch e Scanlines.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3 + Django Framework.
* **Banco de Dados:** SQLite3 (Nativo).
* **Frontend:** HTML5, CSS3 (Variáveis CSS e Animações), JavaScript (Vanilla + Fetch API).
* **Assets:** Pillow (Gerenciamento de Imagens/Avatars).

---

## 🚀 Como Rodar o Projeto Localmente

Siga os passos abaixo para iniciar o "Deck" na sua máquina:

### 1. Pré-requisitos
Certifique-se de ter o **Python** instalado.

### 2. Clonar e Entrar na Pasta
```bash
git clone [https://github.com/SEU_USUARIO/shadowrun_beyond.git](https://github.com/SEU_USUARIO/shadowrun_beyond.git)
cd shadowrun_beyond

```

### 3. Configurar o Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

```

### 4. Instalar Dependências

```bash
pip install django pillow

```

### 5. Configurar o Banco de Dados

```bash
python manage.py migrate

```

### 6. Criar um Admin (Para cadastrar armas e perícias base)

```bash
python manage.py createsuperuser
# Siga as instruções para criar login e senha

```

### 7. Iniciar o Servidor

```bash
python manage.py runserver

```

Acesse no navegador: `http://127.0.0.1:8000/`

---

## 📂 Estrutura do Projeto

Para a equipe de **Design e Frontend**, aqui é onde vocês devem focar:

* `runner_sheet/static/runner_sheet/style.css` 🎨 **(Design)**: Todas as cores, fontes e efeitos visuais.
* `runner_sheet/templates/runner_sheet/` 🖥️ **(HTML)**:
* `home.html`: Tela inicial.
* `ficha.html`: A ficha do personagem.


* `runner_sheet/static/runner_sheet/script.js` ⚙️ **(Lógica)**: O motor das rolagens e interatividade.

---

## ⚠️ Troubleshooting (Problemas Comuns)

**Erro: "no such column: runner_sheet_pericia.pontos"**
Se você encontrar erros de banco de dados após atualizar o código:

1. Pare o servidor.
2. Delete o arquivo `db.sqlite3`.
3. Rode `python manage.py migrate`.
4. Crie o superusuário novamente.

**Alterei o CSS/JS mas não mudou na tela:**
O navegador guarda cache. Use **CTRL + F5** na página para forçar o recarregamento, ou atualize a versão no final do arquivo HTML (`script.js?v=X`).

---

## 🔜 Próximos Passos (Roadmap Sana Fest)

* [x] Backend de Regras e Dados
* [x] Interface Básica e Console
* [x] Cadastro de Personagem pelo Usuário
* [ ] Efeitos Sonoros (SFX) para tiros e dados
* [ ] Modo Fullscreen (Apresentação)

---

Developed by **[Lemos junior, Levi mansinho e João pedro]** for Sana Fest.
*See you in the shadows, chummer.*

```

```
