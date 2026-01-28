/* --- runner_sheet/static/runner_sheet/script.js --- */

// Variáveis Globais (serão preenchidas ao carregar a página)
let danoFisicoAtual = 0;
let danoStunAtual = 0;
let personagemId = 0;

// Quando o HTML terminar de carregar, leia os dados iniciais
document.addEventListener("DOMContentLoaded", () => {
    const bodyData = document.body.dataset;
    
    // Pega os dados que escondemos na tag <body> do HTML
    personagemId = bodyData.id;
    danoFisicoAtual = parseInt(bodyData.fisico || 0);
    danoStunAtual = parseInt(bodyData.stun || 0);

    // Pinta as caixinhas iniciais
    renderizarDano();
});

// --- LÓGICA DE DANO ---

function renderizarDano() {
    // Físico
    document.querySelectorAll('.box-fisico').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoFisicoAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
    // Stun
    document.querySelectorAll('.box-stun').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoStunAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
}

async function setDano(tipo, valor) {
    if (tipo === 'fisico') danoFisicoAtual = valor;
    if (tipo === 'stun') danoStunAtual = valor;
    renderizarDano();

    try {
        await fetch(`/runner/api/dano/${personagemId}/${tipo}/${valor}/`);
        console.log(`Dano ${tipo} salvo: ${valor}`);
    } catch (error) {
        console.error("Falha ao salvar dano:", error);
        logNoConsole("ERRO DE CONEXÃO: Dano não salvo!", true);
    }
}

// --- LÓGICA DE DADOS ---

// Agora a função aceita um nome de arma opcional
async function rolarDados(periciaId, nomeArma = null) {
    const consoleDiv = document.getElementById('console-log');
    
    // Feedback visual mais rico
    let msgInicial = ">> Iniciando sub-rotina de dados...";
    if (nomeArma) {
        msgInicial = `>> ENGAJANDO ALVO COM: [${nomeArma}]...`;
    }
    logNoConsole(msgInicial, false, nomeArma ? "#ff3333" : "#666");

    try {
        const response = await fetch(`/runner/api/rolar/${periciaId}/`);
        if (!response.ok) throw new Error("Erro na API");
        const data = await response.json();

        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

        // Se tiver arma, mudamos o título do log
        const tituloTeste = nomeArma ? `${nomeArma} (via ${data.teste})` : data.teste;

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