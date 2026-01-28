/* --- runner_sheet/static/runner_sheet/script.js --- */

// 1. Variáveis Globais
let danoFisicoAtual = 0;
let danoStunAtual = 0;
let personagemId = 0;

// 2. Inicialização
document.addEventListener("DOMContentLoaded", () => {
    const bodyData = document.body.dataset;
    personagemId = bodyData.id;
    danoFisicoAtual = parseInt(bodyData.fisico || 0);
    danoStunAtual = parseInt(bodyData.stun || 0);
    renderizarDano();
});

// --- 3. LÓGICA DE DANO ---

function renderizarDano() {
    document.querySelectorAll('.box-fisico').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoFisicoAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
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
        // CORREÇÃO AQUI: Removido '/runner'
        await fetch(`/api/dano/${personagemId}/${tipo}/${valor}/`);
        console.log(`Dano ${tipo} salvo: ${valor}`);
    } catch (error) {
        console.error("Falha ao salvar dano:", error);
        logNoConsole("ERRO DE CONEXÃO: Dano não salvo!", true);
    }
}

// --- 4. LÓGICA DE DADOS E ARMAS ---

async function rolarDados(periciaId, nomeArma = null) {
    const consoleDiv = document.getElementById('console-log');
    
    let msgInicial = ">> Iniciando sub-rotina de dados...";
    let corMsg = "#666"; 

    if (nomeArma) {
        msgInicial = `>> ENGAJANDO ALVO COM: [${nomeArma}]...`;
        corMsg = "#ff3333"; 
    }
    
    logNoConsole(msgInicial, false, corMsg);

    try {
        // CORREÇÃO AQUI: Removido '/runner'
        const response = await fetch(`/api/rolar/${periciaId}/`);
        
        if (!response.ok) throw new Error("Erro na API (Verifique o servidor)");
        
        const data = await response.json();

        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

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

async function rolarAtributo(attrId, nomeAttr) {
    // Reutiliza a função de log (certifique-se que logNoConsole existe)
    logNoConsole(`>> TESTE DE ATRIBUTO: [${nomeAttr}]...`, false, "#ffff00"); // Amarelo

    try {
        const response = await fetch(`/api/rolar_atributo/${attrId}/`);
        const data = await response.json();
        
        // Logica de sucesso visual
        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

        const html = `
            <div class="log-entry">
                <div>
                    <strong>${data.teste}</strong>: 
                    <span class="${classeResultado}">HITS: ${data.hits} (${data.mensagem})</span>
                </div>
                <div class="dice-results">[Pool: ${data.pool_total}] :: [${data.resultados.join(', ')}]</div>
            </div>
        `;
        const consoleDiv = document.getElementById('console-log');
        consoleDiv.innerHTML += html; // Adiciona direto (cuidado com o header novo, ideal é adicionar num container interno)
        consoleDiv.scrollTop = consoleDiv.scrollHeight;
        
    } catch (e) {
        console.error(e);
    }
}

// --- 5. FUNÇÃO AUXILIAR ---
function logNoConsole(msg, isError, color=null) {
    const consoleDiv = document.getElementById('console-log');
    let style = "";
    if (color) style = `style="color:${color}"`;
    if (isError) style = `style="color:#f00; font-weight:bold"`;
    consoleDiv.innerHTML += `<div ${style}>${msg}</div>`;
    consoleDiv.scrollTop = consoleDiv.scrollHeight;
}

// --- 6. UI: CONSOLE RETRÁTIL
function toggleConsole() {
    const consoleDiv = document.getElementById('console-log');
    const btn = document.getElementById('btn-toggle-console');
    
    // Adiciona ou remove a classe 'collapsed'
    consoleDiv.classList.toggle('collapsed');

    // Muda o ícone do botão
    if (consoleDiv.classList.contains('collapsed')) {
        btn.innerText = '[ MAXIMIZAR ]'; // Quando fechado
    } else {
        btn.innerText = '[ MINIMIZAR ]'; // Quando aberto
    }
}