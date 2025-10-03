// formata números para exibição
function formata_numero(valor, casasDecimais = 1) {
    return parseFloat(valor).toFixed(casasDecimais);
}

// Atualiza o status do LED na interface
function atualiza_led(estado) {
    const modo_led = document.getElementById('status-led');
    if (!modo_led) return;
    if (estado === 1) {
        modo_led.innerHTML = '🟢 LED LIGADO';
    } else {
        modo_led.innerHTML = '🔴 LED DESLIGADO';
    }
}

// atualiza os valores dos sensores
function atualiza_dados() {

    // envia comando para solicitar atualização ao ESP
    fetch('/publish_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: '/aula_flask/atualizar', message: '1' })
    }).then(() => {
        // após mandar solicitar, pega os dados do Flask
        fetch('/get_sensor_data')
            .then(response => response.json())
            .then(data => {
                const valor_temperatura = document.getElementById('valor_temperatura');
                const valor_umidade = document.getElementById('valor_umidade');
                const atualizar = document.getElementById('ultima_atualizacao');

                if (valor_temperatura) valor_temperatura.textContent = formata_numero(data.temperatura);
                if (valor_umidade) valor_umidade.textContent = formata_numero(data.umidade);

                if (atualizar) {
                    const data_atualizacao = new Date(data.last_update * 1000);
                    atualizar.textContent = data_atualizacao.toLocaleTimeString();
                }
            })
            .catch(err => console.log('Erro ao obter dados dos sensores:', err));
    });
}


// publica comando LED
function publicar_led(estado) {
    if (!verifica_conexao()) return;

    const ligar_botao = document.getElementById('ligar_botao');
    const desligar_botao = document.getElementById('desligar_botao');

    // Desabilitar botões durante a requisição
    if (ligar_botao) ligar_botao.disabled = true;
    if (desligar_botao) desligar_botao.disabled = true;

    fetch('/publish_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: '/aula_flask/led', message: estado.toString() })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta da rede');
            }
            return response.json();
        })
        .then(data => {
            atualiza_led(data.led_status);
        })
        .catch(err => {
            logEvento('Erro ao publicar: ' + err.message, 'error');
        })
        .finally(() => {
            // Reabilitar botões
            if (ligar_botao) ligar_botao.disabled = false;
            if (desligar_botao) desligar_botao.disabled = false;
        });
}

// inicialização baseada na página
document.addEventListener('DOMContentLoaded', function () {
    // verificar se estamos na página de controle do LED
    if (document.getElementById('ligar_botao') && document.getElementById('desligar_botao')) {
        logEvento('Página de controle do LED carregada', 'info');
    }

    // verificar se estamos na página de tempo real
    if (document.getElementById('valor_temperatura') && document.getElementById('valor_umidade')) {
        logEvento('Página de tempo real carregada', 'info');
        atualiza_dados();

        // atualizar dados a cada 3 segundos
        setInterval(atualiza_dados, 3000);
    }
});
