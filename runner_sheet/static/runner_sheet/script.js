/* --- runner_sheet/static/runner_sheet/script.js --- */

// 1. Variáveis Globais (serão preenchidas ao carregar a página)
let danoFisicoAtual = 0;
let danoStunAtual = 0;
let personagemId = 0;

// 2. Inicialização: Lê os dados escondidos no HTML quando a página carrega
document.addEventListener("DOMContentLoaded", () => {
    const bodyData = document.body.dataset;
    
    // Pega os dados do body (Ex: <body data-id="1" ...>)
    personagemId = bodyData.id;
    danoFisicoAtual = parseInt(bodyData.fisico || 0);
    danoStunAtual = parseInt(bodyData.stun || 0);

    // Pinta as caixinhas iniciais
    renderizarDano();
});

// --- 3. LÓGICA DE DANO (Vida) ---

function renderizarDano() {
    // Pinta Físico
    document.querySelectorAll('.box-fisico').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoFisicoAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
    // Pinta Stun
    document.querySelectorAll('.box-stun').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoStunAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
}

async function setDano(tipo, valor) {
    // Atualiza visualmente na hora
    if (tipo === 'fisico') danoFisicoAtual = valor;
    if (tipo === 'stun') danoStunAtual = valor;
    renderizarDano();

    // Salva no servidor
    try {
        await fetch(`/runner/api/dano/${personagemId}/${tipo}/${valor}/`);
        console.log(`Dano ${tipo} salvo: ${valor}`);
    } catch (error) {
        console.error("Falha ao salvar dano:", error);
        logNoConsole("ERRO DE CONEXÃO: Dano não salvo!", true);
    }
}

// --- 4. LÓGICA DE DADOS E ARMAS ---

async function rolarDados(periciaId, nomeArma = null) {
    const consoleDiv = document.getElementById('console-log');
    
    // Feedback visual inicial
    let msgInicial = ">> Iniciando sub-rotina de dados...";
    let corMsg = "#666"; // Cinza padrão

    if (nomeArma) {
        msgInicial = `>> ENGAJANDO ALVO COM: [${nomeArma}]...`;
        corMsg = "#ff3333"; // Vermelho alerta
    }
    
    // Chama a função auxiliar (que agora existe lá embaixo!)
    logNoConsole(msgInicial, false, corMsg);

    try {
        // Bate na API do Django
        const response = await fetch(`/runner/api/rolar/${periciaId}/`);
        
        if (!response.ok) throw new Error("Erro na API");
        
        const data = await response.json();

        // Lógica de sucesso/falha/glitch
        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

        // Título do resultado (Arma ou Perícia)
        const tituloTeste = nomeArma ? `${nomeArma} (via ${data.teste})` : data.teste;

        // Monta o HTML do log
        const html = `
            <div class="log-entry">
                <div>
                    <strong>${tituloTeste}</strong>: 
                    <span class="${classeResultado}">HITS: ${data.hits} (${data.mensagem})</span>
                </div>
                <div class="dice-results">[Pool: ${data.pool_total}] :: [${data.resultados.join(', ')}]</div>
            </div>
        `;
        
        consoleDiv.innerHTML += html;
        consoleDiv.scrollTop = consoleDiv.scrollHeight;

    } catch (error) {
        console.error(error);
        logNoConsole(">> FATAL ERROR: Falha na conexão com Matrix.", true);
    }
}

// --- 5. FUNÇÃO AUXILIAR (Que estava faltando) ---
function logNoConsole(msg, isError, color=null) {
    const consoleDiv = document.getElementById('console-log');
    
    let style = "";
    if (color) style = `style="color:${color}"`;
    if (isError) style = `style="color:#f00; font-weight:bold"`;
    
    consoleDiv.innerHTML += `<div ${style}>${msg}</div>`;
    consoleDiv.scrollTop = consoleDiv.scrollHeight;
}